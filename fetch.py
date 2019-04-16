from Bio import SeqIO
import argparse


class Fetch:
    """
    Encapsulates 3 main fetch scripts from our lab by calling the right
    function based on txt file type:
    fetch_fam --> txt file obtained from Orthofinder, containing family number
    followed by proteins on that family. Outputs one fasta file for each family
    fetch_seqs --> txt file containing sequences to find in the fasta file.
    Outputs one fasta file with all the sequences
    fetch_seqs_coords --> txt file containing the sequence, followed by the two
    coordinates from which to get. Outputs a fasta file containing the
    sequences at the required coordinates
    """

    def __init__(self, fasta_file, txt_file, jobs):
        """
        Open and parse the fasta file and txt file required to run any
        of the fetch scripts
        jobs: number of cpu cores to use when running the script
        """

        self.jobs = int(jobs)
        self.outfile_name = txt_file.split(".txt")[0]
        with open(fasta_file) as fasta:
            self.seqs = list(SeqIO.parse(fasta, "fasta"))
        with open(txt_file) as txt:
            self.names = [line.strip().split() for line in txt]

    def call_fetch(self):
        """
        Calls the appropriate fetch script according to file pattern
        """
        if len(self.names[0]) == 1:
            print("txt file matches fetch_seqs pattern")
            Fetch.fetch_seqs(self)
        elif len(self.names[0]) == 3 and self.names[0][1].isdigit()\
                and self.names[0][2].isdigit():
            print("txt file matches fetch_seqs_coords pattern")
            Fetch.fetch_seqs_coords(self)
        else:
            print("txt most likely matches fetch_fam pattern")
            Fetch.fetch_fam(self)

    def fetch_seqs(self):
        """
        docstring
        """

        print("Fetching seqs...")

        flattened_names = [name[0] for name in self.names]
        desired_seqs = [seq for seq in self.seqs if seq.id in flattened_names]

        with open("{}.fasta".format(self.outfile_name), "w") as outfile:
            SeqIO.write(desired_seqs, outfile, "fasta")
            print("Seqs written to {}.fasta".format(self.outfile_name))

    def fetch_fam(self):
        """
        docstring
        """

        print("Fetching fams...")

        fam_names = [fam_name[0] for fam_name in self.names]
        fam_seqs = [fam_seq[1:] for fam_seq in self.names]
        fam_dict = dict(zip(fam_names, fam_seqs))

        for k in fam_dict:
            fam_dict[k] = [seq for seq in self.seqs if seq.id in fam_dict[k]]

            with open("{}.{}.fasta".format(self.outfile_name, k), "w") as outfile:
                SeqIO.write(fam_dict[k], outfile, "fasta")
        print("Seqs written to their respective families' file")

    def fetch_seqs_coords(self):
        """
        docstring
        """

        print("Fetching seqs at designated coordinates...")

        scaff_names = [scaff_name[0] for scaff_name in self.names]
        scaff_coords = [scaff_coord[1:3] for scaff_coord in self.names]
        scaff_dict = dict(zip(scaff_names, scaff_coords))
        desired_seqs = []

        for k, coords in scaff_dict.items():
            for seq in self.seqs:
                if k == seq.id:
                    seq = seq[int(coords[0]):int(coords[1]) + 1]
                    seq.id = seq.id + "_{}_{}".format(coords[0], coords[1])
                    desired_seqs.append(seq)

        with open("{}.fasta".format(self.outfile_name), "w") as outfile:
            SeqIO.write(desired_seqs, outfile, "fasta")
        print("Seqs at designated coordinates written to {}".format(outfile))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Usage: python3 \
                                     fetch.py [txt file] [fasta file]")
    parser.add_argument("fasta_file")
    parser.add_argument("txt_file")
    parser.add_argument("--jobs", default=1)
    args = parser.parse_args()

    task = Fetch(args.fasta_file, args.txt_file, args.jobs)
    task.call_fetch()

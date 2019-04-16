## fetch.py: Utilities to fetch sequences from FASTA files

This script encapsulates what used to be 3 widely used perl scripts in our lab. It automatically detects the correct function to be called and writes the respective output file of this function.

### Description and usage

`python3 fetch.py [TXT FILE] [FASTA FILE] --jobs [optional number of cores, default 1]`

TXT FILE: `.txt` file containing sequences in a pattern respective to one of the 3 functions (`fetch_fam`, `fetch_seqs` or `fetch_seqs_coords`)

FASTA FILE: `FASTA` file to search for sequences

---

#### `Fetch_seqs`
Fetches sequences named in the `.txt` file from the `FASTA` file and adds them to an output `FASTA` named according to family name on txt file.

`.txt` file follows Orthofinder/OrthoMCL pattern for orthogroups, with the family name tab-separated from sequences). Example:
```
OG0001  Seq1  Seq2  Seq3 Seq4
OG0002  Seq5  Seq6 Seq6 Seq7  Seq8
```

#### `Fetch_seqs`
Fetches sequences named in the `.txt` file from the `FASTA` file and adds them to the same output `FASTA`.
Sequence names should be one on each line. Example:
```
Seq1
Seq2
Seq3
Seq4
```
#### `Fetch_seqs_coords`
Fetches sequences named in the `.txt` file at their estabilished coordinates from the `FASTA` file and adds them to the same output `FASTA`
Sequences/scaffolds should be one on each line, followed by tab separated starting and ending coords. Example:
```
Scaffold1 50  200
Scaffold2  10  40
Scaffold3 10000 10500 
```

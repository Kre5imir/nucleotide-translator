# Nucleotide ORF finder

This project contains a simple Python script that reads a DNA sequence file and searches for open reading frames (ORFs) across all six reading frames.

The program:
- prompts for a filename
- reads the file contents
- removes whitespace and normalizes the sequence to uppercase
- generates the three forward reading frames and the three reverse-complement reading frames
- translates each frame into amino acids using a codon table
- identifies open reading frames starting at methionine (`M`) and ending at stop codons (`_`)
- prints the frame number, start/stop codon positions, and each ORF found

This is a six-frame ORF analysis tool, not a single-sequence DNA-to-protein translator with command-line flags.

## How to run

From the project directory:

```bash
py -3 translate.py
```

The script will ask for a filename, for example:

```text
Enter the name of the file: tmp.fa
```

The file should look like this:

```text
>example
ATGAAATAG
```

## Example output

```text
>example

 Frame 1 start and stop positions are [[0], [2]]

ORF 1 : MK amino acid: 2 nucleotides 6
```

The output shows:
- the FASTA header
- the frame number
- start and stop positions in the translated protein
- each ORF sequence found in that frame

## Notes

- The script reads a file, not a raw sequence argument from the command line.
- It ignores whitespace in the sequence file.
- It keeps only the sequence content after the first line, so a FASTA header is printed but not included in the nucleotide search.
- If the file cannot be opened, the script prints an error and exits with status 1.

## Tests

The current test suite checks the real script behavior by running it as a subprocess:

```bash
py -3 -m unittest -q
```

The tests cover:
- reading a FASTA file and reporting ORFs
- handling a missing file cleanly
- processing a file with a header and sequence without crashing

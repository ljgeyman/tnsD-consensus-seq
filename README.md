**README.md >> tnsD-consensus-seq**

**Last Updated 2024.03.28**

All of these scripts are intended to be executed in a Unix command line. 

_**Order of Operations**_

There are a series of python scripts associated with this repository. They are meant to be run in the following order using the output from the previous script as the new input:
1. xparse_xml.py
2. xmuscle_align.py
3. xtrim_seqs.py
4. xgen_bitmap.py


_xparse_xml.py_
usage: xparse_xml.py [-h] -i INPUT -o OUTPUT

This script extracts sequences from a .xml file downloaded from the BLASTn results screen.
options:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Input file - requires .xml from Blast
  -o OUTPUT, --output OUTPUT
                        Output file path (FASTA)


_xmuscle_align.py_
usage: xmuscle_align.py [-h] -i INPUT -o OUTPUT

This script uses the MUSCLE algorithm to align the sequences extracted from the BLASTn XML file. 
options:

  -h, --help            show this help message and exit
  
  -i INPUT, --input INPUT
                        Input file - requires .fasta from xparse_xml.py
                        
  -o OUTPUT, --output OUTPUT
                        Output file path (FASTA)


_xtrim_seqs.py_
usage: xtrim_seqs.py [-h] -i INPUT -o OUTPUT [-bp BASEPAIRS]

Extract desired region for bitmap construction - default is 36 bp from C-term

options:

  -h, --help            show this help message and exit
  
  -i INPUT, --input INPUT
                        Input file - requires .fasta from alignment
                        
  -o OUTPUT, --output OUTPUT
                        Output file path (FASTA)
                        
  -bp BASEPAIRS, --basepairs BASEPAIRS
                        What segment size do you want (bp)? Counted and sliced from index -1.

_xgen_bitmap.py_
usage: xgen_bitmap.py [-h] -i INPUT [-rs] [-ro]

Extract bitmap from alignment

options:

  -h, --help            show this help message and exit
  
  -i INPUT, --input INPUT
                        Input file - requires .fasta from alignment
                        
  -rs, --rev_sense      Changes the sense of the bases inplace
  
  -ro, --rev_order      Reverses the order of the sequence - index -1 becomes index 0


**_Example Use Case_**

This example walks through how the Bit map for the putative TnsD binding site from Geyman et. al. 2024.

First the whole _glmS_ nucleotide sequence was obtained from the GenBank Database for _Vibrio campbellii_ BB120 - CP000789.1 | VIBHAR_00831

Following this, a BLASTn search was performed excluding _Vibrio campbelli_ (taxid:680) but limiting the results to _Vibrionaceae_ (taxid:641). These were excluded to prevent the formation of a Bitmap using primarily glmS sequences within the _harveyi_ clade.
The program selected was discontiguous Megablast with 5,000 max target sequences. All other settings were left as default.

This search produced 848 sequences with percent Identities between 65% and 97% and Query Converages between 85% and 100%. 

The results were downloaded as blastn_results.xml and processed as follows:

> python3 ./xparse_xml.py -i blastn_results.xml -o extracted_seqs.fasta
> 
> python3 ./xmuscle_align.py -i extracted_seqs.fasta -o aligned_seqs.fasta
> 
> python3 ./xtrim_seqs.py -i aligned_seqs.fasta -o trimmed_seqs.fasta
> 
> python3 ./xgen_bitmap.py -i trimmed_seqs.fasta -rs -ro

This produced the following output [Adapted from Geyman et. al. 2024]:

![bitmap](https://github.com/ljgeyman/tnsD-consensus-seq/assets/125898022/1d6f9678-d6f7-444f-a2ec-68745baede07)

Here the numbers on the x-axis indicate the distance from the Tn7 insertion site. The final step also outputs the raw position weight matrix to an excel file:

[pwm_raw.xlsx](https://github.com/ljgeyman/tnsD-consensus-seq/files/14793466/pwm_raw.xlsx)

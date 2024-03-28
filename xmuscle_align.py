#Python script for aligning xparse_xml.py outputs
from Bio.Align.Applications import MuscleCommandline
from Bio import AlignIO
import argparse as arg


def main(input_sequences, output_alignment):
    # Define the MUSCLE command-line call
    muscle_exe = "muscle"  # This assumes MUSCLE is in your system's PATH
    
    muscle_cline = MuscleCommandline(muscle_exe, input=input_sequences, out=output_alignment)
    
    # Execute MUSCLE
    muscle_cline()
    
    # Read and print the alignment
    alignment = AlignIO.read(output_alignment, "fasta")
    print(alignment)

if __name__ == '__main__':
    # Parse command line arguments
    parser = arg.ArgumentParser(description='Extract sequences from xml')
    parser.add_argument('-i', '--input', required=True, help='Input file - requires .fasta from xparse_xml.py')
    parser.add_argument('-o', '--output', required=True, help='Output file path (FASTA)')

    args = parser.parse_args()

    main(args.input, args.output)

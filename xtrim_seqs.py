from Bio import SeqIO
import argparse as arg

def main(input_file, output_file):
    with open(output_file, 'w') as out_f:
        for record in SeqIO.parse(input_file, 'fasta'):
            # Check if the sequence is at least 36 bp long
            if len(record.seq) >= 36:
                # Trim the sequence to the last 36 base pairs
                record.seq = record.seq[-36:]
                # Write the trimmed sequence to the output file
                SeqIO.write(record, out_f, 'fasta')
            else:
                print(f"Sequence {record.id} is shorter than 36 base pairs and was skipped.")

if __name__ == '__main__':
    # Parse command line arguments
    parser = arg.ArgumentParser(description='Extract bitmap from alignment')
    parser.add_argument('-i', '--input', required=True, help='Input file - requires .fasta from alignment')
    parser.add_argument('-o', '--output', required=True, help='Output file path (FASTA)')
    
    args = parser.parse_args()

    main(args.input, args.output)

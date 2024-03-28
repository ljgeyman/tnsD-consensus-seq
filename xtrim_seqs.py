from Bio import SeqIO
import argparse as arg

def main(input_file, output_file, bp):
    with open(output_file, 'w') as out_f:
        for record in SeqIO.parse(input_file, 'fasta'):
            # Check if the sequence is at least 36 bp long
            if len(record.seq) >= bp:
                # Trim the sequence to the last 36 base pairs
                record.seq = record.seq[-bp:]
                # Write the trimmed sequence to the output file
                SeqIO.write(record, out_f, 'fasta')
            else:
                print(f"Sequence {record.id} is shorter than {bp} base pairs and was skipped.")

if __name__ == '__main__':
    # Parse command line arguments
    parser = arg.ArgumentParser(description='Extract desired region for bitmap construction - default is 36 bp from C-term')
    parser.add_argument('-i', '--input', required=True, help='Input file - requires .fasta from alignment')
    parser.add_argument('-o', '--output', required=True, help='Output file path (FASTA)')
    parser.add_argument('-bp', '--basepairs', default=36, help='What segment size do you want (bp)? Counted and sliced from index -1.')
    
    args = parser.parse_args()

    main(args.input, args.output, args.basepairs)

#Python3 script for parsing BLAST XML output for sequence hits

from Bio import SeqIO, Seq
from Bio.Blast import NCBIXML
from Bio.SeqRecord import SeqRecord
import argparse as arg

def main(input_xml, output):
    # List to hold SeqRecord objects
    seq_records = []

    with open(input_xml) as result_handle:
        blast_records = NCBIXML.parse(result_handle)

        for blast_record in blast_records:
            for alignment in blast_record.alignments:
                for hsp in alignment.hsps:
                    # Use the sequence as is for forward orientation
                    seq_record = SeqRecord(Seq.Seq(hsp.sbjct),
                                           id=alignment.hit_id,
                                           description=alignment.hit_def)
                # Add the SeqRecord to our list
                seq_records.append(seq_record)

    # Write the SeqRecord objects to a FASTA file
    SeqIO.write(seq_records, output, "fasta")


if __name__ == '__main__':
    # Parse command line arguments
    parser = arg.ArgumentParser(description='Extract sequences from xml')
    parser.add_argument('-i', '--input', required=True, help='Input file - requires .xml from Blast')
    parser.add_argument('-o', '--output', required=True, help='Output file path (FASTA)')

    args = parser.parse_args()

    main(args.input, args.output)

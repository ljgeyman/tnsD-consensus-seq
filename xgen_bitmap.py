from Bio import SeqIO
import pandas as pd
import logomaker
import matplotlib.pyplot as plt
import argparse as arg
import numpy as np


# Initialize primary code function

def main(input, reverse_sense, reverse_order):
    # Path to MUSCLE aligned FASTA file
    fasta = input

    # Read the sequences from FASTA
    sequences = [str(record.seq) for record in SeqIO.parse(fasta, 'fasta')]

    # Assume all seqs are the same length, set seq_length
    seq_length = len(sequences[0])

    # Create an position count DataFrame
    pcm = pd.DataFrame(index=range(1, seq_length + 1),
                       columns=['A', 'G', 'C', 'T', '-', 'R', 'Y', 'M', 'W', 'K', 'S'])

    # Fill pcm with 0s
    pcm = pcm.fillna(0)

    # Count occurrences of each nucleotide at each position
    for seq in sequences:
        for i, nt in enumerate(seq):
            pcm.at[i + 1, nt] += 1

    # Initialize position frequency matrix
    pfm = pcm.drop(columns=['R', 'Y', 'M', 'W', 'K', 'S'])
    row_sums = pfm.sum(axis=1)
    pfm = pfm.div(row_sums, axis=0)

    # Flip sequence sense if that argument is recieved
    if reverse_sense:
        flipped = {'A': pfm['T'],
                   'C': pfm['G'],
                   'G': pfm['C'],
                   'T': pfm['A'],
                   ' ': pfm['-']}
        pfm = pd.DataFrame(flipped)
    else:
        pfm[' '] = pfm['-']
        pfm = pfm.drop(columns=['-'])

    if reverse_order:
        pfm = pfm.iloc[::-1].reset_index(drop=True)

    # Add pseudocount to avoid log(0)
    pfm = pfm.drop(columns=[' '])
    pseudo = 0.01
    pfm += pseudo

    # Recalculate the probabilities with the pseudocounts considered
    pfm_sums = pfm.sum(axis=1)
    pfm = pfm.div(pfm_sums, axis=0)
    pfm = pd.DataFrame(pfm)

    # Set Background probabilities for each nucleotide
    background = {'A': 0.2725,
                  'T': 0.2725,
                  'G': 0.2275,
                  'C': 0.2275}

    # Add pseudocount to background and normalize
    background = {k: v + pseudo for k, v in background.items()}
    total = sum(background.values())
    background = {k: v / total for k, v in background.items()}

    # Calculate the pwm
    pwm = pd.DataFrame()
    for nt in pfm.columns:
        pwm[nt] = np.log2(pfm[nt] / background[nt])

    print(pwm)

    # If a pwm is less than 0 set it to 0
    #for col in pwm.columns:
    	#pwm[col] = [0 if pwm[col][i] < 0 else pwm[col][i] for i in range(len(pwm))]

    # Set index to match numbering desired on x-axis of bitmap
    pwm.index = range(28, 28 + len(pwm))

    # Define custom color scheme for bitmap
    colors = {'A': 'green',  # Adenine
              'C': 'blue',  # Cytosine
              'G': 'orange',  # Guanine
              'T': 'red',  # Thymine
              ' ': 'white'}

    # init bitmap logo
    logo = logomaker.Logo(pwm, color_scheme=colors, fade_below=0.5)
    
    # Set axis options
    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)

    # Add x-axis and y-axis title
    ax.set_xlabel('Position Relative to Stop Codon', fontsize=12, fontweight='bold')
    ax.set_ylabel('Bits', fontsize=12, fontweight='bold')
    plt.ylim(0, 2.1)

    # Save bitmap
    plt.savefig('bitmap.png')
    
    # Save pwm as an excel file
    pwm.to_excel('pwm_raw.xlsx', index = False)
    
if __name__ == '__main__':
    # Parse command line arguments
    parser = arg.ArgumentParser(description='Extract bitmap from alignment')
    parser.add_argument('-i', '--input', required=True, help='Input file - requires .fasta from alignment')
    parser.add_argument('-rs', '--rev_sense', action='store_true', help='Changes the sense of the bases inplace')
    parser.add_argument('-ro', '--rev_order', action='store_true', help='Reverses the order of the sequence - index -1 becomes index 0')
    
    args = parser.parse_args()
    
    main(args.input, args.rev_sense, args.rev_order)


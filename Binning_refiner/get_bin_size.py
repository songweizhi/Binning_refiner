from Bio import SeqIO

def get_bin_size(bin_file):
    bin_content = SeqIO.parse(bin_file, 'fasta')
    total_length = 0
    for each in bin_content:
        contig_length = len(each.seq)
        total_length += contig_length
    return total_length
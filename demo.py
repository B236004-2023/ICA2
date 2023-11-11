import argparse
import os
parser = argparse.ArgumentParser(
                    prog='Conservation finder',
                    description='The software is designed to identify a family of protein acoss a tree The user should should offer the name of protein family, and species name list.',
                    epilog='Version:1.0.0 Author:dongyao@connect.hku.hk')

parser.add_argument('-p', '--proteinname', type=str)
parser.add_argument('-l', '--species_list', type=str)
parser.add_argument('-w', '--windowsize', type=int, help="required insert_seq or backbone")
parser.add_argument('-1', '--primerLeft', type=str)
parser.add_argument('-2', '--primerRight', type=str)
parser.add_argument('-vl','--vector_left_primer_start', type=int)
parser.add_argument('-vr', '--vector_right_primer_start', type=int)
parser.add_argument('-dl', '--vector_deletion_left', type=int, help="use the last-base index of forword primer")
parser.add_argument('-dr', '--vector_deletion_right', type=int, help="use the first-base index of reversed primer")
args = parser.parse_args()

cmd1 = 'esearch -db protein -query "glucose-6-phosphatase proteins" | efetch -format fasta'
os.system(cmd1)

print(args.proteinname)
print(args.species_list)
print(args.windowsize)

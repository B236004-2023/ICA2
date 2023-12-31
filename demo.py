import argparse
import os
parser = argparse.ArgumentParser(
                    prog='Conservation finder',
                    description='The software is designed to identify a family of protein acoss a tree The user should should offer the name of protein family, and species name list.',
                    epilog='Version:1.0.0 Author:dongyao@connect.hku.hk')

parser.add_argument('-p', '--proteinname', type=str)
parser.add_argument('-l', '--species_list', type=str)
parser.add_argument('-n', '--filename', type=str)
parser.add_argument('-t', '--test', type=str)
parser.add_argument('-w', '--windowsize', type=int)
parser.add_argument('-f', '--graph_format', type=str)
parser.add_argument('-1', '--primerLeft', type=str)
parser.add_argument('-2', '--primerRight', type=str)
parser.add_argument('-vl','--vector_left_primer_start', type=int)
parser.add_argument('-vr', '--vector_right_primer_start', type=int)
parser.add_argument('-dl', '--vector_deletion_left', type=int, help="use the last-base index of forword primer")
parser.add_argument('-dr', '--vector_deletion_right', type=int, help="use the first-base index of reversed primer")
args = parser.parse_args()

default_protein_name = "glucose-6-phosphatase proteins"

cmd1 = f'esearch -db protein -query "{args.proteinname} AND {args.species_list}[organism]" | efetch -format fasta >{args.filename}'
print(cmd1)
os.system(cmd1)

if args.test=="no":
    cmd2 = f"emma -sequence {args.filename} -outseq {args.filename}.alignment -dendoutfile {args.filename}.dnd"
    os.system(cmd2)
else:
    cmd3 = f"head -50 {args.filename} >demo.fasta"
    cmd4 = f"emma -sequence demo.fasta -outseq {args.filename}.alignment -dendoutfile {args.filename}.dnd"
    os.system(cmd3)
    os.system(cmd4)

cmd5 = f"plotcon -sequences {args.filename}.alignment -graph {args.graph_format} -winsize {args.windowsize}"


print(args.proteinname)
print(args.species_list)
print(args.windowsize)

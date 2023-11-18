import argparse
import subprocess
import os
parser = argparse.ArgumentParser(
                    prog='Conservation finder',
                    description='The software is designed to do conservation analysis within a group of user-defined species.',
                    epilog='Version:0.0.1 Author:dongyao')

parser.add_argument('-p', '--proteinname', type=str, help="You need give description here")
parser.add_argument('-sl', '--species_list', type=str, help="You need give description here")
parser.add_argument('-on', '--organism_name', type=str, help="You need give description here")
parser.add_argument('-n', '--prefix', type=str)
parser.add_argument('-w', '--windowsize', type=int)
parser.add_argument('-f', '--graph_format', type=str)
args = parser.parse_args()







def conservation_analysis(fasta_file, out_file_prefix, graph_format, windowsize):
	multi_sequence_aln = f"emma -sequence fasta_file -outseq {out_file_prefix}.aln -dendoutfile {out_file_prefix}.dnd"
	align_info = "infoalign {out_file_prefix}.aln {out_file_prefix}.info"
	#We filter the alignment base on the align info column 7. similarity percent. you can open this to user in further time.
	## current cut off is 0.5
	filter_the_alignment = "grep -v "#" {out_file_prefix}.info | awk '{print $2, $7, $7/$3}' | awk '$3 >= 0.5 {print $1}'> species_candidate.txt"
	## we need to extract our alignment by useing pull seq
	alignment_extraction = "/localdisk/data/BPSM/ICA2/pullseq -i {out_file_prefix}.aln -n species_candidate.txt >{out_file_prefix}.filter.aln"
	
	## conservation analysis
	plotcon = f"plotcon -sequences {out_file_prefix}.filter.aln -graph {graph_format} -winsize {windowsize}"
os.system(cmd5)

	motif_search= f"patmatmotifs -sequence {fasta_file} -outfile {out_file_prefix}.motifs"
os.system(cmd6)
	




if args.species_list == "":
	Organism_Information = subprocess.check_output("esearch -db taxonomy -query {args.organism_name}  | esummary | xtract -pattern DocumentSummary -element Rank Id", shell=True) 
	Toxn_level = Organism_Information.split()[0]
	txid = Organism_Information.split()[1]

	if Toxn_level not in ["species", "subspecies"]:
		### we write three new file to the working folder
		### raw_toxin_list store
		raw_toxn_list = os.system(f"esearch -db taxonomy -query {args.organism_name} | esummary | xtract -pattern DocumentSummary -element Rank Id > raw_toxn_list)
		species_list = ("grep "species" raw_toxn_list > species_list)
		genus_above_list = ("grep -V "species" raw_toxn_list > genus_above_list")
		species_number = subprocess.check_output(f"esearch -db taxonomy -query {args.organism_name} | esummary | xtract -pattern DocumentSummary -element Rank Id | grep "species" | wc -l ", shell=True)	
		print(f"You organism name is a {Toxn_level} name and {args.organism_name} contains {species_number} species/subspecies\n")
		print("Do you want to continue the analysis?")
		user_text = input("yes/no")
		if user_text = "no"
			os._exit(0)
		else:
			query_protein_fasta = f'esearch -db protein -query "{args.protein_name}[protein] AND {args.organism_name}[organism]" | efetch -format fasta >{args.prefix}.protein.fa'
			conservation_analysis(fasta_file = query_protein_fasta, 
					out_file_prefix = args.prefix,
					graph_format = graph_format, 
					windowsize = args.windowsize)		
	else:
		# we didn't offer conservaton analysis within single species
		print("We can't offer conservation analysis in single species")
		os._exit(0)

else:
	##query species protein line by line
	fasta_file_out = open(f"{args.prefix}.protein.fa", "a")
	speceis_id_file = open(args.species_list, "r")
	for line in speceis_id_file.readlines():
		query_protein = subprocess.check_output(f"esearch -db protein -query "{args.protein_name}[protein] AND txid{line}[organism]" | efetch -format fasta", shell=T) 
		fasta_file_out.write(query_protein)
	fasta_file_out.close()
	conservation_analysis(fasta_file = fasta_file_out,
                                        out_file_prefix = args.prefix,
                                        graph_format = graph_format,
                                        windowsize = args.windowsize)
	















## Real analysis start from now on
## query the CDS sequence from nucleotide database
cmd1 = f'esearch -db nucleotide -query "{args.proteinname}[protein] AND {args.organism_name}[organism]" | efetch -format fasta_cds_na >{args.filename}'
print(cmd1)
os.system(cmd1)

cmd5 = f"plotcon -sequences {args.filename}.alignment -graph {args.graph_format} -winsize {args.windowsize}"
os.system(cmd5)

cmd6 = f"patmatmotifs -sequence {args.filename} -outfile {args.filename}.motifs"
os.system(cmd6)

print(args.proteinname)
print(args.species_list)
print(args.windowsize)

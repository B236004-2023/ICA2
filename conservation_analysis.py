#Import necessary modules
import argparse #Used for parsing command-line arguments
import subprocess #Used for executing system commands
import os #Used for executing system commands and file operations
parser = argparse.ArgumentParser(
                    prog='Conservation analysis',
                    description='The programme is designed to create a versatile and user-friendly bioinformatics tool that allows users to analyze protein sequences, assess their conservation, identify motifs, and optionally perform additional analyses for relevant biological information.',
                    epilog='Author: B236004-2023')

parser.add_argument('-p', '--protein_name', type=str, help="Specify the protein name.")
parser.add_argument('-sl', '--species_list', type=str, help="Specify the path to the species list file.")
parser.add_argument('-on', '--organism_name', type=str, help="Specify the organism name for taxonomy search.")
parser.add_argument('-n', '--prefix', type=str, help="Specify the name of output file prefix.")
parser.add_argument('-w', '--windowsize', type=int, help="Specify the window size for conservation analysis.")
parser.add_argument('-f', '--graph_format', type=str, help="Specify the graph format for conservation analysis.")
parser.add_argument('-m', '--minlen',type=int, help="Specify the minimum length for antigenic analysis.")
args = parser.parse_args()






#Define the conservation analysis function
def conservation_analysis(fasta_file, out_file_prefix, graph_format, windowsize, minlen):
	#Multiple sequence alignment
        multi_sequence_aln = f"emma -sequence {fasta_file} -outseq {out_file_prefix}.aln -dendoutfile {out_file_prefix}.dnd"
	#Save the alignment information
        align_info = f"infoalign {out_file_prefix}.aln {out_file_prefix}.info"
	#Print alignment information on the screen
        cdm_print = f"cat {out_file_prefix}.info"
        #Filter the alignment based on the align info column 7 similarity per cent.
	#select lines where the value in the 3rd column is greater than or equal to 0.5 then print the value in the 1st column.
        filter_the_alignment = f"grep -v \"#\" {out_file_prefix}.info | awk '{{print $2, $7, $7/$3}}' | awk '$3 >= 0.5 {{print $1}}' > species_candidate.txt"
        #Extract the alignment by useing pullseq
        alignment_extraction = f"/localdisk/data/BPSM/ICA2/pullseq -i {out_file_prefix}.aln -n species_candidate.txt > {out_file_prefix}.filter.aln"
	#plot the graph of conservation analysis
        plotcon = f"plotcon -sequences {out_file_prefix}.filter.aln -graph {graph_format} -winsize {windowsize}"
        #Scan a protein sequence with motifs from the PROSITE database
        motif_search = f"patmatmotifs -sequence {fasta_file} -outfile {out_file_prefix}.motifs"
        #Additional analysis to find antigenic sites in proteins
        antigenic = f"antigenic -sequence {fasta_file} -minlen {minlen} -outfile {out_file_prefix}.antigenic"

        #Execute system commands one by one
        os.system(multi_sequence_aln)
        os.system(align_info)
        os.system(cdm_print)
        os.system(filter_the_alignment)
        os.system(alignment_extraction)
        os.system(plotcon)
        os.system(motif_search)
        os.system(antigenic)


#The main process of performing protein and species conservation analysis by using if loops
#If no species list file is provided
if args.species_list == "":
        #Get organism information
	Organism_Information = subprocess.check_output(f'esearch -db taxonomy -query "{args.organism_name}" | esummary | xtract -pattern DocumentSummary -element Rank Id', shell=True) 
	Toxn_level = Organism_Information.split()[0]
	txid = Organism_Information.split()[1]

	if Toxn_level not in ["species", "subspecies"]:
		#Write three new file to the working folder
		#raw_toxin_list storage
		raw_toxn_list = os.system(f'esearch -db taxonomy -query "{args.organism_name}" | esummary | xtract -pattern DocumentSummary -element Rank Id > raw_toxn_list')
		species_list = os.system('grep "species" raw_toxn_list > species_list')
		genus_above_list = os.system('grep -v "species" raw_toxn_list > genus_above_list')
		species_number = subprocess.check_output(f'esearch -db taxonomy -query "{args.organism_name}" | esummary | xtract -pattern DocumentSummary -element Rank Id | grep "species" | wc -l', shell=True)	
		print(f"Your organism name is a {Toxn_level} name and {args.organism_name} contains {species_number} species/subspecies\n")
		
                #After print the name and number of species, ask users whether the analysis
		print("Do you want to continue the analysis?")
		user_text = input("yes/no")

		if user_text == "no":
			os._exit(0)
		else:
                        #Get protein sequence and perform conservation analysis
                        query_protein_fasta = os.system(f'esearch -db protein -query "{args.protein_name}[protein] AND {args.organism_name}[organism]" | efetch -format fasta > {args.prefix}.protein.fa')
                        conservation_analysis(fasta_file = f"{args.prefix}.protein.fa", 
					out_file_prefix = args.prefix,
					graph_format = args.graph_format, 
					windowsize = args.windowsize, 
					minlen = args.minlen)		
	else:
		#Conservation analysis within single species is not offered
		print("Error: We can't offer conservation analysis in single species.")
		os._exit(0)

#If a species list file is provided
else:
	#Query species protein line by line
	fasta_file_out = open(f"{args.prefix}.protein.fa", "a")
	speceis_id_file = open(args.species_list, "r")
	protein_sequence_number = 0
	for line in speceis_id_file.readlines():
		query_protein = subprocess.check_output(f'esearch -db protein -query "{args.protein_name}[protein] AND txid{line}[organism]" | efetch -format fasta', shell=True).decode() 
		#If the species provided by user does not contain the searched proteins
		if query_protein == "":
			print(f"Speceis {line} not have the protein.")
		else:
			protein_sequence_number = protein_sequence_number + 1
		fasta_file_out.write(query_protein)
	fasta_file_out.close()
	#If the protein provided by user is not a single sequence, perform conservation analysis
	if protein_sequence_number >= 2:
		conservation_analysis(fasta_file = f"{args.prefix}.protein.fa",
                                        out_file_prefix = args.prefix,
                                        graph_format = args.graph_format,
                                        windowsize = args.windowsize,
                                        minlen = args.minlen)
	else:
		print("Error: We can't offer conservation analysis in single species.")

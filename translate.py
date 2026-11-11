#!/usr/bin/env python3
#This program translates given nucleotide sequence in to possible open reading frame(protein)
#run the program and input the name of the file 
#output should give you 6 reading frames, open reading frames for each frame and start stop index of aa
#output can be compared on ncbi website (https://www.ncbi.nlm.nih.gov/orffinder/)
import sys
def main():

    # input the name of the file
    filename = input("Enter the name of the file: ")
    genom = ''
    firstline = ''
    #open the file in reading text mode using error checking
    try:
        f = open( filename , 'r' )
        firstline = f.readline()
        for line in f:
            genom += ''.join(line.split())
        genom = genom.upper()

    except IOError:
        print("error unable to read file or file does not exist!!!")
        print("Exiting the program")
        stop = input("press enter to exit....")
        sys.exit(1) 

    def generate_RF(seq):
        ''' generate 3 reading frame from nucleotide sequence'''
        reading_frame = ''
        list_of_RF = []
        
        for x in range(0,3):#0,1,2 positions to start reading
            reading_frame = seq[x:len(seq)] #from start 
            list_of_RF.append(reading_frame)#3 reading frames
        
        return list_of_RF

    def reverseComplement(s):
        '''function will complement A:T,G:C,T:A,C:G in place '''
        s = ''.join(s.split()).upper()
        complement = {'A' : 'T', 'G':'C', 'T':'A','C':'G'}
        t = ''
        for x in s:
            t = complement[x] + t # reverse order of return with placing t + in front
        return t

    def translate(seq): 
        '''this function will translate nucleotide sequence into aminoacid by its first letter'''
        seq = ''.join(seq.split()).upper()
        table = { 
            'ATA':'I', 'ATC':'I', 'ATT':'I', 'ATG':'M', 
            'ACA':'T', 'ACC':'T', 'ACG':'T', 'ACT':'T', 
            'AAC':'N', 'AAT':'N', 'AAA':'K', 'AAG':'K', 
            'AGC':'S', 'AGT':'S', 'AGA':'R', 'AGG':'R',                  
            'CTA':'L', 'CTC':'L', 'CTG':'L', 'CTT':'L', 
            'CCA':'P', 'CCC':'P', 'CCG':'P', 'CCT':'P', 
            'CAC':'H', 'CAT':'H', 'CAA':'Q', 'CAG':'Q', 
            'CGA':'R', 'CGC':'R', 'CGG':'R', 'CGT':'R', 
            'GTA':'V', 'GTC':'V', 'GTG':'V', 'GTT':'V', 
            'GCA':'A', 'GCC':'A', 'GCG':'A', 'GCT':'A', 
            'GAC':'D', 'GAT':'D', 'GAA':'E', 'GAG':'E', 
            'GGA':'G', 'GGC':'G', 'GGG':'G', 'GGT':'G', 
            'TCA':'S', 'TCC':'S', 'TCG':'S', 'TCT':'S', 
            'TTC':'F', 'TTT':'F', 'TTA':'L', 'TTG':'L', 
            'TAC':'Y', 'TAT':'Y', 'TAA':'_', 'TAG':'_', 
            'TGC':'C', 'TGT':'C', 'TGA':'_', 'TGG':'W', 
        } 
        aa ="" #string to collect value from dictionarie key if match is true 
        for n in range(0,len(seq),3):
            codon = seq[n:n+3] #from zero split sequence by 3
            if(len(codon) == 3):#discard nucleotides that are not divisible by 3 
                aa+= table[codon] # append dict value to aa string from key that matches the codon
        return aa
        #i = 0
        #return [table[seq[x:x+3]]for x in range(i,len(seq) - 2, 3)] 
    
    def get_proteins(amino_seq):
        '''this function will collect amino acid from start to stop codon and save it to a list'''
        current_protein = []#this is a list of amino acid being accumulated
        protein = []#list of list of proteins
        for aa in amino_seq:
            '''when this loop hits stop sign, current_protein list if not empty, it will be saved into protein list'''
            if aa == '_':# this is a stop sign
                if current_protein:
                    for p in current_protein:
                        protein.append(p)#append all aminoacid from seq from current_protein list to protein list 
                current_protein = [] #clear the current_protein list(set back to empty)
            else:
                if aa == 'M':
                    '''if we hit M we append empty string so count of elements is > 0
                    and loop will start accumulating each time we hit M '''
                    current_protein.append("")
                for i in range(len(current_protein)):
                    current_protein[i] += aa
                '''this loop will check if there is any value in current_protein
                if ther is, its gonna keep adding aminoacid'''
                    
        return protein

    def startStop(aa):
        '''function will check for M in given amino acid sequence and append index of position to start list
        same goes for stop codon _ index position will be appended in stop list, it will return everything in one list '''
        index = 0 #set index from start of list
        startlist = []
        stoplist = []
        
        while index < len(aa):
            if aa[index] == 'M': 
                startlist.append(index)#if M found, append integer index of position 
                index += 1 
            else:
                index += 1
        index = 0# set index to zero
        while index < len(aa):
            if aa[index] == '_':# if stop found append index of position
                stoplist.append(index)
                index += 1
            else:
                index += 1
        startstoplist = []
        startstoplist.append(startlist)
        startstoplist.append(stoplist)
        return startstoplist

    def get_proteins_from_all_RF(seq):
        '''this function will return two lists, and it will call rest of the functions to generate list of proteins 
        and their start and stop positions '''
        list_of_RF = generate_RF(seq) #from given sequence generate 3 reading frames 
        
        revComp = reverseComplement(seq)# reverse coplemntary given sequence 
        
        list_of_reversed_RF = generate_RF(revComp)#generate three reading frames from complementary sequence
        
        six_reading_frames = list(list_of_RF + list_of_reversed_RF)# 6 reading frames
        
        aminoacids = [] #empty list to accumulate aminoacid
        protein_list = []#empty list to accumulate protein
        startStopList = []#empty list to accumulate start stop index
       
        for nucleotide in six_reading_frames:
            aa = translate(nucleotide)# first we translate 6 reading frames
            aminoacids.append(aa)# we append each aminoacid to aminoacids list
            start_stop = startStop(aa)#call startStop function to save all start and stop positions in aminoacids
            startStopList.append(start_stop)#we append the start stop index of each aminoacid
        
        for codon in aminoacids:
            proteins = get_proteins(codon)#check for all possible open reading frames
            protein_list.append(proteins)#append proteins
        return protein_list ,startStopList

    prot, startStopList = get_proteins_from_all_RF(genom[:500])#here you can reduce size of file as genom[:50]
    print(firstline)
    print()
    for frame, protein_list in enumerate(prot):
        print('\n','Frame', frame + 1,'start and stop positions are',startStopList[frame] ,'\n')
        for orf, aminoacid in enumerate(protein_list):
            print('ORF',orf + 1,':', aminoacid,'amino acid:',len(aminoacid),'nucleotides',len(aminoacid)*3)
    
    f.close()

    stop = input("enter return to exit")


if __name__ == "__main__":
    main()


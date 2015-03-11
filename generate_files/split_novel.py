__author__ = 'lacheephyo'

"""
Python script to break up a novel downloaded from
Project Gutenberg [http://www.gutenberg.org/ebooks/5200]
into ~100 different files named sequentially as
"1.txt", "2.txt", etc. Each of these files contain about
21 sentences from the original novel.
"""

# open the full novel
fin = open('metamorphosis.txt')

# read in all lines in the novel into a list
next = fin.readlines()

# print len(next) # about ~2300 sentences

# strip new lines from each sentence and ignore lines with just '\n'
sentences = []
for s in next:
    if s != '\n':
        sentences.append(s.strip())

# print "total selected sentences" + str(len(sentences)) # ~2100

# close the file
fin.close()

# try to split into ~100 files
divisor = 100
sentences_in_each_file = len(sentences)//divisor

#print "Sentences in each file: " + str(sentences_in_each_file) # 21

file_counter = 1
for i in range(0,len(sentences), sentences_in_each_file):

    fout_name = str(file_counter) + ".txt"
    fout = open(fout_name, 'w')

    # write 21 sentences into each file
    fout.write(''.join(sentences[i:(i+sentences_in_each_file)]))

    # dump remaining < 21 sentences into the last file
    if ((len(sentences) - i) < sentences_in_each_file):
        fout.write(''.join(sentences[i:]))

    file_counter += 1
    fout.close()
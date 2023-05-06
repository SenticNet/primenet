from gensim.models import KeyedVectors
from gensim.test.utils import datapath
#load word
#py37!
#https://radimrehurek.com/gensim/models/keyedvectors.html
import os
from os import listdir
import csv
rewrite_analogy_dataset=False
if rewrite_analogy_dataset:
    mypath = "analogy"
    ana_files= [os.path.join(mypath,f) for f in listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]
    for filename in ana_files:
        with open(filename, 'r') as file:
            csvreader = csv.reader(file)
            all_rows = []
            for row in csvreader:
                all_rows.append(row)
            analogy_dir = {}
            for row in all_rows[1:]:
                [anatype,word1,word2,word3,word4]=row[1:]
                if anatype in analogy_dir:
                    analogy_dir[anatype].append([word1,word2,word3,word4])
                else:
                    analogy_dir[anatype]=[[word1,word2,word3,word4]]
            fw = open(filename.split(".csv")[0]+"-gensim.csv",'w')
            for anatype,fourtuples in analogy_dir.items():
                fw.write(": {}\n".format(anatype))
                for info in fourtuples:
                    fw.write("\t".join(info)+"\n")

    #
'''Path to file, where lines are 4-tuples of words, split into sections by ": SECTION NAME" lines.
See `gensim/test/test_data/questions-words.txt` as example.
'''
import sys
mypath = sys.argv[1]
wordembed_files= [os.path.join(mypath,f) for f in listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]
for word_embed_file in wordembed_files:
    wv_from_text = KeyedVectors.load_word2vec_format(word_embed_file, binary=False,no_header=True)  # C text format
    output_scores = [word_embed_file]
    for analogy_file in ["analogy/google-analogies-gensim.csv",
                        "analogy/msr-gensim.csv"]:
        # "analogy/jair-gensim.csv",
        # "analogy/sat-gensim.csv",
        # "analogy/semeval-gensim.csv"
        analogy_scores = wv_from_text.evaluate_word_analogies(analogy_file)#)(datapath('questions-words.txt'))#'analogy/google-analogies.csv')
        output_scores.append(str(analogy_scores[0]))
    print("\t".join(output_scores))
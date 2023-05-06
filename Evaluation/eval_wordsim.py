from gensim.models import KeyedVectors
from gensim.test.utils import datapath
#load word
#py37!
#https://radimrehurek.com/gensim/models/keyedvectors.html
import os
from os import listdir
import csv
import math
import numpy
from operator import itemgetter
from numpy.linalg import norm

EPSILON = 1e-6

def euclidean(vec1, vec2):
  diff = vec1 - vec2
  return math.sqrt(diff.dot(diff))

def cosine_sim(vec1, vec2):
  vec1 += EPSILON * numpy.ones(len(vec1))
  vec2 += EPSILON * numpy.ones(len(vec1))
  return vec1.dot(vec2)/(norm(vec1)*norm(vec2))

def assign_ranks(item_dict):
  ranked_dict = {}
  sorted_list = [(key, val) for (key, val) in sorted(item_dict.items(),
                                                     key=itemgetter(1),
                                                     reverse=True)]
  for i, (key, val) in enumerate(sorted_list):
    same_val_indices = []
    for j, (key2, val2) in enumerate(sorted_list):
      if val2 == val:
        same_val_indices.append(j+1)
    if len(same_val_indices) == 1:
      ranked_dict[key] = i+1
    else:
      ranked_dict[key] = 1.*sum(same_val_indices)/len(same_val_indices)
  return ranked_dict

def correlation(dict1, dict2):
  avg1 = 1.*sum([val for key, val in dict1.iteritems()])/len(dict1)
  avg2 = 1.*sum([val for key, val in dict2.iteritems()])/len(dict2)
  numr, den1, den2 = (0., 0., 0.)
  for val1, val2 in zip(dict1.itervalues(), dict2.itervalues()):
    numr += (val1 - avg1) * (val2 - avg2)
    den1 += (val1 - avg1) ** 2
    den2 += (val2 - avg2) ** 2
  return numr / math.sqrt(den1 * den2)

def spearmans_rho(ranked_dict1, ranked_dict2):
  assert len(ranked_dict1) == len(ranked_dict2)
  if len(ranked_dict1) == 0 or len(ranked_dict2) == 0:
    return 0.
  x_avg = 1.*sum([val for val in ranked_dict1.values()])/len(ranked_dict1)
  y_avg = 1.*sum([val for val in ranked_dict2.values()])/len(ranked_dict2)
  num, d_x, d_y = (0., 0., 0.)
  for key in ranked_dict1.keys():
    xi = ranked_dict1[key]
    yi = ranked_dict2[key]
    num += (xi-x_avg)*(yi-y_avg)
    d_x += (xi-x_avg)**2
    d_y += (yi-y_avg)**2
  return num/(math.sqrt(d_x*d_y))


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


import sys
mypath = sys.argv[1]
if os.path.isfile(mypath):
    wordembed_files = [mypath]
else:
    wordembed_files= [os.path.join(mypath,f) for f in listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]

wordsim_files = ['word-sim/EN-YP-130.txt',
                 'word-sim/EN-MEN-TR-3k.txt', 
                 'word-sim/EN-RG-65.txt', 
                 'word-sim/EN-MTurk-771.txt', 
                 'word-sim/EN-SIMLEX-999.txt',
                 'word-sim/EN-SimVerb-3500.txt', 
                 'word-sim/EN-VERB-143.txt', 
                 'word-sim/EN-WS-353-ALL.txt']
for word_embed_file in wordembed_files:
    wv_from_text = KeyedVectors.load_word2vec_format(word_embed_file, binary=False,no_header=True)  # C text format
    output_scores = [word_embed_file]
    
    for analogy_file in ana_files:
        analogy_scores = wv_from_text.evaluate_word_analogies(analogy_file)#)(datapath('questions-words.txt'))#'analogy/google-analogies.csv')
        output_scores.append(str(analogy_scores[0]))
    for filename in wordsim_files:
        manual_dict, auto_dict = ({}, {})
        not_found, total_size = (0, 0)
        for line in open(filename,'r'):
            line = line.strip().lower()
            word1, word2, val = line.split()
            if word1 in wv_from_text and word2 in wv_from_text:
                manual_dict[(word1, word2)] = float(val)
                auto_dict[(word1, word2)] = wv_from_text.similarity(word1, word2)
            else:
                not_found += 1
                total_size += 1    
        mywordsim = spearmans_rho(assign_ranks(manual_dict), assign_ranks(auto_dict))
        output_scores.append(str(mywordsim))
    print("\t".join(output_scores))



## PrimeNet: A Framework for Commonsense Knowledge Representation and Reasoning Based on Conceptual Primitives
PrimeNet is a scalable, generalizable knowledge base which enables effective commonsense and real-world knowledge representation and facilitates commonsense reasoning including inferences.
## Overview

Inspired by the theory of conceptual primitives, PrimeNet is constructed by comprising a small core of primitive commonsense concepts and relations, linked to a much more extensive base of factual knowledge instances.

<p float="center">
  <img src="/fig/overall.png" width="700" />
</p>

## Use Cases
Primitives are organized in a multi-level hierarchy that allows to iteratively generalize words and multiword expressions into increasingly general primitives. Top-level primitives (aka superprimitives) are then defined by means of first-order logic.
<p float="left">
  <img src="/fig/primitive.png" width="500" />
</p>

More cases on primitive generalization:
<p float="left">
  <img src="/fig/case1.png" width="250" />
  <img src="/fig/case2.png" width="250" /> 
  <img src="/fig/case3.png" width="250" />
</p>
<p float="left">
  <img src="/fig/case4.png" width="250" />
  <img src="/fig/case5.png" width="250" /> 
  <img src="/fig/case6.png" width="250" />
</p>





## Evaluation
1. The evaluation of Human Assessment (detailed in Section 4.1) can be reproduced using the facts from PrimeNet V3. Download all facts in PrimeNet V3 from this [link](https://drive.google.com/file/d/1e16lmGdaQ3PP-S4w12S6eAg4h-u_hBeS/view?usp=share_link).

2. The evaluation of Distributional Representations (detailed in Section 4.2) can be reproduced using the released files in the Evaluation folder.  
	
	The code of refining word embeddings is available in this [link](https://github.com/mfaruqui/retrofitting).

	We released the refined representations using different knowledge bases (i.e., WordNet, FrameNet, ConceptNet, and PrimeNet). All files can be downloaded using this [link](https://drive.google.com/file/d/1_R6AS5r-WNLbzl5Vpa_RKffi6F6PIXx8/view?usp=share_link).  

	> glove.6B.50d.primenet.txt
	glove.6B.50d.conceptnet.txt
	glove.6B.50d.wordnet.txt
	glove.6B.50d.framenet.txt
	glove.6B.300d.primenet.txt
	glove.6B.300d.conceptnet.txt
	glove.6B.300d.wordnet.txt
	glove.6B.300d.framenet.txt
	word2vec.cbow.300d.primenet.txt
	word2vec.cbow.300d.conceptnet.txt
	word2vec.cbow.300d.wordnet.txt 
	word2vec.cbow.300d.framenet.txt
	
	Example of evaluating on word similarity task:
		
	> 	python eval_wordsim.py refined_vectors/glove.6B.50d.conceptnet.txt
	
	The output is:
	> 	0.4427091438043214      0.6743373528926029      0.7073685164959393      0.5974265070145617      0.3761684502800549      0.2355190563306831       0.27269399402968747     0.48538634242377177




## Functions (PrimeNet SDK)
In primenet_graph.py, we define over 20 functions to explore PrimeNet.
The input, output, and description of each function is explained on Table 3 in the paper.

We show the examples of using these functions:

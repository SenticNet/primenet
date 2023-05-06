

## PrimeNet: A Framework for Commonsense Knowledge Representation and Reasoning Based on Conceptual Primitives
PrimeNet is a scalable, generalizable knowledge base which enables effective commonsense and real-world knowledge representation and facilitates commonsense reasoning including inferences.
## Overview

Inspired by the theory of conceptual primitives, PrimeNet is constructed by comprising a small core of primitive commonsense concepts and relations, linked to a much more extensive base of factual knowledge instances.

<p float="center">
  <img src="/fig/overall.png" width="700" />
</p>

## Case Study
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
```
primenet = read_json_file("primenet_fact_v3.json")
graph = Graph(primenet)

# generate all nodes and edges in PrimeNet:
graph.nodes()
graph.edges()

graph.get_number_of_nodes()
# output: 1409185
graph.get_number_of_edges()
# output: 3056776
graph.density()
# output: 3.0786328229340862e-06

graph.what_is("hammer")
# output: hammer --isA--> hand_tool
graph.get_node_degree("hammer")
# output: 24
graph.explain(node="hammer",relation="isA")
# output: hammer --isA--> hand_tool --isA--> tool
graph.what_can_be("hammer")
# output: [['isA', 'hand_tool'], ['isA', 'industrial_equipment'], ['isA', 'power_tool'], ['isA', 'tool'], ['mannerOf', 'beat'], ['usedFor', 'hit'], ['madeOf', 'forged_metal'], ['partOf', 'gunlock'], ['partOf', 'piano_action'], ['IntentionOf', 'build'], ['IntentionOf', 'demo'], ['Afford', 'breaking_glass'], ['Afford', 'break_glass'], ['Afford', 'nail_board'], ['Afford', 'break_wall'], ['Afford', 'break_window'], ['Afford', 'strike_nail'], ['Afford', 'force_nail_into_board'], ['Afford', 'break_fragile_objects'], ['Afford', 'nail_nails'], ['Afford', 'strike_with_great_force'], ['Afford', 'nail_nail'], ['Afford', 'hit_nail'], ['Afford', 'drive_in_nails']]
graph.generalize("hammer")
# output: [('Afford', 'BREAKING_GLASS'), ('mannerOf', 'STRIKE'), ('usedFor', 'HIT'), ('IntentionOf', 'BUILD'), ('isA', 'TOOL'), ('partOf', 'ARSENAL'), ('madeOf', 'FORGED_METAL')]

graph.relation_exist(node="hammer",relation="Afford")
# output: True
graph.relation_types("hammer")
# output: ['madeOf', 'Afford', 'IntentionOf', 'usedFor', 'partOf', 'mannerOf', 'isA']

graph.get_node_with_relation(node="hammer",relation="isA")
# output: 'hand_tool'
graph.get_node_with_relation(node="hammer",relation="usedFor")
# output: 'hit'
graph.find_last_nodes("hit_nail")
# output: ['hammer-->Afford-->hit_nail']
graph.get_all_node_with_relation(node="hammer",relation="Afford")
# output: ['breaking_glass', 'break_glass', 'nail_board', 'break_wall', 'break_window', 'strike_nail', 'force_nail_into_board', 'break_fragile_objects', 'nail_nails', 'strike_with_great_force', 'nail_nail', 'hit_nail', 'drive_in_nails']

graph.find_path(start_node="hammer",end_node="tool")
# output: [('START', 'hammer'), ('isA', 'hand_tool'), ('isA', 'tool')]
graph.find_all_paths(start_vertex="hammer",end_vertex="tool")
# output: [[('START', 'hammer'), ('isA', 'hand_tool'), ('isA', 'tool')], [('START', 'hammer'), ('isA', 'power_tool'), ('isA', 'tool')], 002: [('START', 'hammer'), ('isA', 'tool')], [('START', 'hammer'), ('mannerOf', 'beat'), ('isA', 'band'), ('isA', 'record'), ('isA', 'tool')]...]
graph.get_path(start_node="hammer",end_node="tool")
# output:'hammer --isA--> hand_tool --isA--> tool'

graph.get_similarity(node1="hammer",node2="pen",relation="Afford")
# output: 0.11111
graph.get_similarity(node1="hammer",node2="brick",relation="Afford")
# output: 0.66667

graph.add_node("a_new_node")
graph.add_edge(("a_new_node", "isA","testing_example"))
```


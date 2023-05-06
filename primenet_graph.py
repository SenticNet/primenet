# -*- coding: utf-8 -*-
from difflib import SequenceMatcher 
from primenet_polarity import *
from primenet_phonetics import *
import os
import json
def get_file_contents(filename, encoding='utf-8'):
    filename = filename.encode('utf-8')
    with open(filename, encoding=encoding) as f:
        content = f.read()
    return content
def read_json_file(filename, encoding='utf-8'):
    contents = get_file_contents(filename, encoding=encoding)
    return json.loads(contents)
def write_json_to_file(json_object, json_file, mode='w', encoding='utf-8'):
    with open(json_file, mode, encoding=encoding) as outfile:
        json.dump(json_object, outfile, indent=4, sort_keys=True, ensure_ascii=False)
try:
    import cPickle as pickle
except ImportError:
    import pickle
import difflib

class Graph(object):

    def __init__(self, graph_dict=None):
        """ initializes a graph object 
            If no dictionary or None is given, 
            an empty dictionary will be used
        """
        if graph_dict == None:
            graph_dict = {}
        self.__graph_dict = graph_dict

    def nodes(self):
        """ returns the nodes of a graph """
        return list(self.__graph_dict.keys())

    def edges(self):
        """ returns the edges of a graph """
        return self.__generate_edges()

    def add_node(self, node):
        """ If the node "node" is not in 
            self.__graph_dict, a key "node" with an empty
            list as a value is added to the dictionary. 
            Otherwise nothing has to be done. 
        """
        if node not in self.__graph_dict:
            self.__graph_dict[node] = []

    def add_edge(self, edge):
        """ assumes that edge is of type set, tuple or list; 
            between two nodes can be multiple edges! 
        """
        # edge = set(edge)
        (node1, relation, node2) = tuple(edge)
        if node1 in self.__graph_dict:
            self.__graph_dict[node1].append((relation, node2))
        else:
            self.__graph_dict[node1] = [(relation, node2)]
    
    def normalize(self, node):
        node = node.lower().replace(" ", "_")
        if node in primenet_phonetics: 
            node = node.replace(node, primenet_phonetics[node])
        return node
        
    def what_is(self, node):
        node = self.normalize(node)
        if node in self.__graph_dict:
            inode = self.__graph_dict[node][0]
            relation = inode[0]
            neighbour = inode[1]
            return node + " --"+relation+"--> " + neighbour
        else:
            sim_nodes = difflib.get_close_matches(node, self.__graph_dict.keys(), n=5)
            return "Sorry! There is no information for {}..\nSimilar concepts: {}".format(node,",".join(sim_nodes))


    #### return all relation types that the node involved.
    def relation_types(self, node):
        relations = []
        for neighbour in self.__graph_dict[node]:
            relations.append(neighbour[0])
        return list(set(relations))

    ### Check to see if a relationship type exists in the node
    def relation_exist(self, node, relation):
        relations = self.relation_types(node)
        if relation not in relations:
            return False
        else:
            return True

    def get_node_with_relation(self, node, relation):
        node_next = None
        if self.relation_exist(node, relation):
            node_neibors = self.__graph_dict[node]
            
            for pair in node_neibors:
                if pair[0]==relation:
                    node_next = pair[1]
                    # return node_next  
                    break 
            return node_next
        else:
            return None

    def get_all_node_with_relation(self, node, relation):
        node_next = []
        if self.relation_exist(node, relation):
            node_neibors = self.__graph_dict[node]

            for pair in node_neibors:
                if pair[0] == relation:
                    node_next.append(pair[1])
            return node_next
        else:
            return None

    def explain(self, node, relation):
        node = self.normalize(node) 
        node_exist = []

        if not self.relation_exist(node, relation):
            return None
        else:
            output = node
            node_next = self.get_node_with_relation(node, relation)
            if node_next not in node_exist:
                node_exist.append(node_next)

                while (node_next in self.__graph_dict):
                    output+=" --"+relation+"--> "+node_next
                    node_next = self.get_node_with_relation(node_next, relation)
                    ### Have to check the chain's length is no more than 3, and there is no loop in the chain.
                    if node_next is None or node_next in node_exist or len(node_exist)>=3:
                        break
                    if node_next not in node_exist:
                        node_exist.append(node_next)
            # output += " --"+relation+"--> " + node_next.upper()
            return output
 
    def export_pickle(self, graph_name):
        fname = graph_name+'.pkl'
        if os.path.exists(fname):
            os.remove(fname)
        else:
            fw = open(fname, 'wb')
            pickle.dump(self.__graph_dict, fw, protocol=2)
            print("The graph is dumped to %s"%(fname))


    def import_pickle(self, graph_name):
        fname = graph_name + '.pkl'
        if os.path.exists(fname):
            with open(fname,"rb") as f:
                graph = pickle.load(f)
                self.__graph_dict = graph
                return graph
        else:
            print("The file does not exist!") 
            return None


    def is_loop(self, node):
        node = self.normalize(node)
        inode = self.__graph_dict[node][0]
        relation = inode[0]
        isa_node = inode[1]
        output = node
        node_exist = [node]
        Flag = True
        if isa_node in node_exist:
            Flag = False
            print('Error in '+ node + " --"+relation+"--> " + isa_node)
            # assert Flag, ('Error in '+ node + " --IsA-->" + isa_node)
     
        while(isa_node in self.__graph_dict):
            output += " --"+relation+"--> "+ isa_node 
            inode = self.__graph_dict[isa_node][0]
            isa_node = inode[1]
            relation = inode[0]
            if isa_node in node_exist:
                Flag = False 
                print("There is a loop in", output)
                break
                # assert Flag, ("There is a loop in", output)
            else:
                node_exist.append(isa_node)
                
        return Flag
            

    def generalize(self, node):
        node = self.normalize(node)
        relations = self.relation_types(node)
        # print(relations)
        outputs = []
        
        for relation in relations:
            node_next = self.get_node_with_relation(node, relation)
            # print(node_next)
            node_exist = [node]
      
            if node_next not in self.__graph_dict:
                
                outputs.append((relation, node_next.upper()))
            else:
                while (node_next in self.__graph_dict):
                    # print(node_exist, node_next)
                    if node_next not in node_exist:
                        node_exist.append(node_next)
                        output = node_next
                        node_next = self.get_node_with_relation(node_next, relation)
                        
                        if node_next is None: 

                            outputs.append((relation, output.upper()))
                            break 
                    elif len(node_exist)>2:
                        ## Using the third layer as the target
                        # print(node_exist)
                        outputs.append((relation, node_exist[2].upper()))
                        break

                    else:
                        ## Using the third layer as the target
                  
                        outputs.append((relation, node_exist[-1].upper()))
                        break
        return outputs
    
    def get_similarity(self, node1, node2, relation):
        path1 = self.explain(node1, relation)
        # print(path1)
        path2 = self.explain(node2, relation)
        # print(path2)
        return round(SequenceMatcher(None, path1, path2).ratio(),5)
    
    def get_polarity(self, node):
        primitive = self.generalize(node)
        # return primenet_polarity[primitive.lower()]
        return primenet_polarity[node]
    
    def what_can_be(self, node):
        # node = self.normalize(node)
        return self.__graph_dict[node]

    def get_number_of_nodes(self):
        return len(graph.nodes())
        
    def get_number_of_edges(self):
        return len(graph.edges())

    def __generate_edges(self):
        """ A static method generating the edges of the 
            graph "graph". Edges are represented as sets 
            with one (a loop back to the node) or two 
            nodes 
        """
        edges = []
        for node in self.__graph_dict:
            for neighbour in self.__graph_dict[node]:
                # if {neighbour, node} not in edges:
                edges.append(node+"#"+neighbour[0]+"#"+neighbour[1])
        edges = list(set(edges))
        return edges
    def find_last_nodes(self, end_node):
    	outputs = []
    	for node in self.__graph_dict:
    		end_nodes = self.__graph_dict[node]
    		end_nodes_ = [n[0] for n in end_nodes if n[1]==end_node]
    		if len(end_nodes_)>0:
    			o = [(str(node)+"-->" +str(n)+"-->" +str(end_node)) for n in end_nodes_]
    			outputs.extend(o)
    	return outputs

    def find_path(self, start_node, end_node, path=None, relation='START'):
        """ find a path from start_node to end_node 
            in graph """
        if path == None:
            path = [] 
        graph = self.__graph_dict
        path_nodes = [n[1] for n in path]

        if start_node in path_nodes:
            return None
        else:

            path = path + [(relation, start_node)]

        if len(path)>5:
            return None

        if start_node == end_node:
            return path
        if start_node not in graph:
            return None
        for node in graph[start_node]:
            relation, node = node
            if node not in path:
                extended_path = self.find_path(node, 
                                               end_node, 
                                               path,
                                               relation)
                # print(path)
                if extended_path: 
                    return extended_path
        return None

 
    
    def get_path(self, start_node, end_node):

        path = self.find_path(start_node, end_node)
        pathstring = ''
        for node in path:
            relation, node = node
            if relation!="START":
                pathstring = pathstring + " --"+ relation+"--> "+node
            else:
                pathstring += node
        return pathstring


    
    def find_all_paths(self, start_vertex, end_vertex, path=[], relation = "START"):
        """ find all paths from start_vertex to 
            end_vertex in graph """
        
        graph = self.__graph_dict 
        path = path + [(relation, start_vertex)]
        if len(path)>5:
            return []
        if start_vertex == end_vertex:
            return [path]
        if start_vertex not in graph:
            return []
        paths = []
        for vertex_pair in graph[start_vertex]:
            vertex = vertex_pair[1]
            relation = vertex_pair[0]
            path_nodes = [p[1] for p in path]
            if vertex not in path_nodes:
                extended_paths = self.find_all_paths(vertex, 
                                                     end_vertex, 
                                                     path,
                                                     relation)
 
                for p in extended_paths:  
                    paths.append(p)
        return paths
       
    def get_node_degree(self, vertex):
        """ The degree of a vertex is the number of edges connecting
            it, i.e. the number of adjacent vertices. Loops are counted 
            double, i.e. every occurence of vertex in the list 
            of adjacent vertices. """ 
        adj_vertices =  self.__graph_dict[vertex]
        degree = len(adj_vertices) + adj_vertices.count(vertex)
        return degree
    def disambiguation(self, node, pos='n'):
        generalize_pairs = self.generalize(node)## [('isA', 'ACT'), ('mannerOf', 'CONNECT')]
        # print(pos, generalize_pairs)
        for pair in generalize_pairs:
            if pair[0] == 'isA' and pos == 'n':
                out  = node.upper()+" --> "+"NOUN"+ " --> "+pair[1].upper()
                break
                
            elif pair[0] != 'isA' and pos == 'v':
                out  = node.upper()+" --> "+"VERB"+ " --> "+pair[1].upper()
                break
                
            else:
                out = "Sorry! There is no such sense.."
        return out

    def disambiguate_sense(self, word1, word2):

        links = self.find_path(word1, word2)
        if links is not None:
            v = [1 for t in links if t[0]=="usedFor" or t[0]=="mannerOf"]
            n = [1 for t in links if t[0]=="isA"]

        v_num = sum(v)
        n_num = sum(n) 
        if v_num > n_num:
            out = 'VERB'
        elif v_num < n_num:
            out = 'NOUN'
        else:
            out = 'CANNOT Tell'

     
        return out    
    def density(self):
        """ method to calculate the density of a graph """
        g = self.__graph_dict
        V = len(g.keys())
        E = len(self.edges())
        return 2.0 * E / (V *(V - 1))

    def __str__(self):
        res = "nodes: "
        for k in self.__graph_dict:
            res += str(k) + " "
        # res += "\nedges: "
        for edge in self.__generate_edges():
            res += str(edge[0]) + " " + str(edge[1])
        return res
    def get_phonetic(self, sentence):
        return Translate(sentence)

def add_primenet_new(orig_graph,add_graph,relation):
    for concept in add_graph:
        if concept in orig_graph:
            pri_with_relation = orig_graph[concept]
        else:
            pri_with_relation = []
        for pri in add_graph[concept]:
            pri = pri.replace("'","_")
            pri_with_relation.append((relation, pri))
        orig_graph[concept] = pri_with_relation
    return orig_graph

#-------------------Use Cases-------------------------------------------
primenet = read_json_file("primenet_v3_db16.json")
graph = Graph(primenet)

print(graph.get_number_of_nodes())
print(graph.get_number_of_edges())

print(graph.what_is("hammer"))
print(graph.get_similarity(node1="hammer",node2="screwdriver",relation="usedFor"))
exit()


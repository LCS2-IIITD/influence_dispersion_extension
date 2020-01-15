import xml.etree.ElementTree as ET
import pickle
import networkx as nx
import numpy as np
import random

def get_pickle_dump(filepath,filename):
	"""
	@Params:
	filename: filename inside the ./dumps folder
	@Returns:
	Variable: Returns the pickled variable
	"""

	with open(filepath +'/'+filename+'.pickle','rb') as handle:
		Variable = pickle.load(handle)
	return Variable


def dump_file(filepath,filename, Variable):
	"""
	@Params:
	filename: filename inside the ./dumps folder for dumping
	Variable: Variable to dump inside the file
	@Returns:
	None
	"""
	with open(filepath +'/'+filename+'.pickle','wb') as handle:
		pickle.dump(Variable,handle,protocol=pickle.HIGHEST_PROTOCOL)


def parse_year(filename, year_dict):
    #year_dict = {}
    #print(type(year_dict))
    tree=ET.parse(filename)
    root=tree.getroot()

    c=0
    for child in root:
        flag=0
        #doi stand for digital obeject identifier - Paper identifier
        doi_dict = child.attrib
        doi = doi_dict['doi']
        for gchild in child:
           
            if(gchild.tag == 'issue' and flag==0):
                date_dict=gchild.attrib
                date_string=date_dict['printdate']
                #if(doi=='10.1103/PhysRevSTAB.4.101302'):
                #    print(date_string)
                #    print(date_string!="")
                if(date_string!=""):
                    year=int(date_string.split('-')[0])
                    year_dict[doi]=year
                    flag=1
                if(flag==1):
                    break
            #year not yet found
            if(gchild.tag=='history' and flag==0):
                for ggchild in gchild:
                    if(ggchild.tag == 'published'):
                        date_dict = ggchild.attrib
                        date_string = date_dict['date']
                        if(date_string != ""):
                            year = int(date_string.split('-')[0])
                            year_dict[doi] = year
                            flag=1
                if(flag==1):
                    break
    return year_dict

def create_graph(file_name, year_dict):
	G=nx.DiGraph()
	count_forward = 0
	count_key_error=0

	# start=time.time()

	# year_dict=get_pickle_dump('year_dict')
	print(file_name)
	with open(file_name,"r") as f:
		line = f.readline()
		line = f.readline()
		#line = (line.encode('ascii', 'ignore')).decode("utf-8")
		while line:
			line=line.rstrip('\r\n')
			line_array=line.split(',')
			citing_paper=line_array[0]
			cited_paper=line_array[1]
			try:
				if(year_dict[citing_paper]>=year_dict[cited_paper]):
					G.add_edge(citing_paper,cited_paper)
				else:
					#print(citing_paper,year_dict[citing_paper],cited_paper,year_dict[cited_paper])
					count_forward+=1	
			except:
				#print(citing_paper,cited_paper)
				count_key_error+=1

			line = f.readline()
	return G


def remove_cycles(G):
    total_edges_removed = 0
    for n in G.edges().copy(): #returns a list of tuple of edges
        if n[0] == n[1]:   #same node indicating self loop
            G.remove_edge(*n)
            total_edges_removed+=1

    for paper in G.nodes().copy():
        #print("Current Paper : {}".format(paper))
        induced_graph = set()
        induced_graph_list = G.in_edges(nbunch = paper) # report edges incident to that paper

        for e in induced_graph_list: 
            induced_graph.add(e[0])
        induced_graph.add(paper)

        H = G.subgraph(induced_graph)
        cycle_lists = (nx.simple_cycles(H))
        for cycle_list in list(cycle_lists):
            length_of_cycle = len(cycle_list)
            if length_of_cycle <= 2:
                try:
                    G.remove_edge(cycle_list[0] , cycle_list[1])
                except nx.exception.NetworkXError:
                    pass
                continue
            r = random.randint(2,length_of_cycle - 1)
            try:
                G.remove_edge(cycle_list[r- 1] , cycle_list[r])
            except nx.exception.NetworkXError:
                pass
            #print("{} {} Removed from {}".format(cycle_list[r-1] , cycle_list[r] , cycle_list))
            total_edges_removed += 1
    return G

EMPTY = ""

def all_edges_in_visited(IDG,p, visited):
    """
    @Params: 
    IDG: IDG of the paper 
    p: paper whose neighbours we need to check
    visited: set of nodes which are visited
    @Returns:
    True if all the neighbours are visited else False
    """
    edge_list = list(IDG.out_edges(nbunch = [p]))
    for e in edge_list:
        if e[1] not in visited:
            return False
    return True

def remove_edges_except(paper, ancestor_paper , IDG):
    """
    @Params: 
    IDG: IDG of the paper 
    paper: paper whose neighbours we need to check
    ancestor_paper: The ancestor with whom we need to preserve the edges
    @Returns:
    The IDG with all but the given ancestor's edge removed
    """
    edge_list = list(IDG.out_edges(nbunch = paper))
    for e in edge_list:
        if e[1] != ancestor_paper:
            IDG.remove_edge(*e) 
    return IDG

def get_parent_with_most_depth(depth_dict , IDG, p):
    """
    @Params: 
    IDG: IDG of the paper 
    p: paper whose neighbours we need to check
    depth_dict: Dict with all the depth of the papers in the IDG
    @Returns:
    The neighbour which has the most depth and has been visited.
    """
    edge_list = list(IDG.out_edges(nbunch = [p]))
    max_depth = -1
    ancestor_paper = EMPTY
    for e in edge_list:
        if depth_dict[e[1]] > max_depth:
            max_depth = depth_dict[e[1]]
            ancestor_paper = e[1]
    return ancestor_paper

def IDT_init(global_citation_graph):
    removed = 0 
    paper_IDT_dict = {}
    IDT_root_to_leaf_paths = {} 
    nodes_with_cycle = 0
    for paper in global_citation_graph.nodes().copy():
        depth_dict = {}
        induced_graph = set()
        induced_graph_list = list(global_citation_graph.in_edges(nbunch = [paper]))

        for e in induced_graph_list:
            induced_graph.add(e[0])
        induced_graph.add(paper)

        
        IDG = global_citation_graph.subgraph(induced_graph)

        #for e in IDG.nodes():
         #   e_list = list(IDG.out_edges(nbunch = [e]))
          #  if len(e_list) > 1:
           #     IDG.remove_edge(e , paper)

        visited = set()
        not_visited = set(IDG.nodes())
        not_visited.discard(paper)
        visited.add(paper)
        depth_dict[paper] = 0
        cur_depth = 1
        while(len(not_visited) > 0):
            cur_visit_set = set()
            for p in not_visited:
                if all_edges_in_visited(IDG,p,visited):
                    ancestor_paper = get_parent_with_most_depth(depth_dict , IDG , p)
                    IDG = remove_edges_except(p , ancestor_paper , IDG)
                    cur_visit_set.add(p)
                    depth_dict[p] = cur_depth
            visited = visited.union(cur_visit_set)
            for p in cur_visit_set:
                not_visited.discard(p)
            cur_depth += 1 

        if len(IDG.nodes()) >= 2:
            paper_IDT_dict[paper] = IDG        
        else:
           # print(paper, len(IDG.nodes()))
            removed+=1

    return paper_IDT_dict

def get_max_from_dict(d):
	a = [d[w] for w in d.keys()]
	a.sort(reverse = True)
	return a[0]

def global_depth_breadth(tree_dict):
	global_depth_breadth = {}
	for paper in tree_dict.keys():
		H=tree_dict[paper]
		book_keep={}
		done = set()
		not_done = set(H.nodes())
		not_done.discard(paper)
		done.add(paper)

		book_keep[paper] = 0
		counter = 1
		breadth_dict = {0 : 0}
		while(len(not_done) > 0):
			cur_visit_set = set()
			for n in not_done:
				if all_edges_in_visited(H,n,done):
					cur_visit_set.add(n)
					book_keep[n] = counter
					try:
						breadth_dict[counter] += 1
					except KeyError:
						breadth_dict[counter] = 1

			done = done.union(cur_visit_set)
			for element in cur_visit_set:
				not_done.discard(element)
			counter += 1
		citations=len(list(set(H.nodes())))-1
		global_depth_breadth[paper] = [get_max_from_dict(breadth_dict) , get_max_from_dict(book_keep) , citations] # breadth, depth , total_citations
	return global_depth_breadth


def get_ideal_tniceness(n):
        return n

def get_worst_tniceness(n):
        return (n - int((n - 1)/2))*(float(1 + int((n - 1)/2)))

def get_NID(ID, n):
        if n > 3:
                d = abs(get_ideal_tniceness(n) - ID)/float(abs(get_ideal_tniceness(n) - get_worst_tniceness(n)))
                return d
        return 0.0

def get_tree_NID(tree,paper):
        if (len(tree.edges()) == 0):
                return 0
        nodes = list(tree.nodes())
        leaf_nodes = []
        for v in nodes:
                        in_edges = tree.in_edges(nbunch = [v])
                        if len(in_edges) == 0:
                                        leaf_nodes.append(v)

        ID=0
        for v in leaf_nodes:
                        ID+= nx.shortest_path_length(tree , source = v , target = paper)

        citations=len(list(set(tree.nodes())))-1

        NID=get_NID(ID,citations)

        return NID

def get_tree_IDI(tree,paper):
    if (len(tree.edges()) == 0):
                return 0
    nodes = list(tree.nodes())
    leaf_nodes = []
    for v in nodes:
                        in_edges = tree.in_edges(nbunch = [v])
                        if len(in_edges) == 0:
                                        leaf_nodes.append(v)

    IDI=0
    for v in leaf_nodes:
        IDI+= nx.shortest_path_length(tree , source = v , target = paper)

    return IDI

def get_NID_IDI(tree_dict):
    NID_dict = {}
    IDI_dict = {}

    count = 0
    total = len(tree_dict)

    for paper in tree_dict.keys():
            tree = tree_dict[paper]

            nid = get_tree_NID(tree,paper)

            NID_dict[paper] = nid

            idi = get_tree_IDI(tree,paper)

            IDI_dict[paper] = idi

            #count+=1
            #if(count>1000):
                   # total = total-count
                   # print(total)
                   # count = 0
    return NID_dict, IDI_dict

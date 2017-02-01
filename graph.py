import os

import networkx as nx




class AnalyzeGraph():

	def __init__(self, template_list,file_list, path, path1):
		self.template_list = template_list
		self.file_list = file_list
		self.path = path
		self.path1 = path1
	
	
	def SubGraphIsomorphism(self, Graph, Subgraph):
		# Takes a Graph and a "Sub-"Graph (template) and returns the mapping
		GM = nx.isomorphism.GraphMatcher(Graph, Subgraph)
		return [GM.subgraph_is_isomorphic(), GM.mapping]



	def analyze(self):

		results = []

		for atemplate in self.template_list:

			try:
				the_template = nx.DiGraph(nx.read_dot(os.path.join( self.path1, atemplate )))
				
			except:
				print "Error Reading Template in /template/%s" %(str(atemplate))
				print Exception
				continue
							
			for afile in self.file_list:

				try:
					the_graph_to_test = nx.DiGraph(nx.read_dot(os.path.join( self.path, afile )))
					
				except:
					print "Error Reading Graph in /tmp/%ss" %(str(afile))
					print Exception
					continue			

				if the_graph_to_test != None or the_template != None:
				
					# Get a Mapping
					Mapping = self.SubGraphIsomorphism( the_graph_to_test, the_template )
					
					# Append to Results
					if Mapping[0] == True :

						results.append([atemplate, afile, Mapping, nx.number_of_nodes(the_graph_to_test) - nx.number_of_nodes(the_template)])

		return results


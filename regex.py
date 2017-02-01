import re
import os
import importlib

import networkx as nx
from itertools import izip




class AnalyzeAssembly():

	def __init__(self, Graph, Template_Graph, Graph_Node, Template_Node, path ,path1, arch ):
		self.graph = Graph
		self.templategraph = Template_Graph
		self.graphnode = Graph_Node
		self.templatenode = Template_Node
		self.path = path
		self.path1 = path1
		self.arch = arch

			
	def get_BB_Content(self, Graph, Node_Number, arch):
		# Converts the Content of a Basic Block
		Assembly = []
		
		node_number = Node_Number
		# Get Content of the Basic Block
		BasicBlock = Graph.node[str(node_number)]['label']
		
		LinesofBB = BasicBlock.split(r'\n')
		LinesofBB = filter(None, LinesofBB)
		
		# dissect the Assembly Lines into several Strings
		for line in LinesofBB:
			opcode = ''
			operand1 = ''
			operand2 = ''
			rest = ''
			
			line = re.sub('\n', '', line)
			line = line.strip()
			
			assembly = line.split('\t')

			opcode =  assembly[0]           #this is the opcode
			opcode.strip()

			if len(assembly) > 1:
												
				test1 = re.split(',\s*(?![^\[\]\{\}]*(\}|\]|\)))',assembly[1])
				test1 = filter(None, test1)

				operand1 = test1[0]         #this is first operand
				operand1.lstrip(' ')

				if len(test1) > 1:

					operand2 = test1[1]     #this is the second operand
					operand2 = operand2.lstrip(' ')

					if len(test1) > 2:
						rest = test1[2]     #this is the Rest of the Assembly Line
						rest = rest.lstrip(' ')

			Assembly.append([opcode, operand1, operand2, rest])        

		return Assembly

	#get the Regex strings from the template

	def analyze(self):
		regexlist = []
		res = []
		
		#import the correct helper file
		arch = importlib.import_module(self.arch)

		try:
			Graph = nx.DiGraph(nx.read_dot(os.path.join( self.path , self.graph )))
			
		except:
			print "Error Reading Graph in /tmp/%s" %( self.graph )
			print Exception

					
		try:
			TemplateGraph = nx.DiGraph(nx.read_dot(os.path.join( self.path1 , self.templategraph )))
							
		except:
			print "Error Reading Template in /templates/%s" %( self.templategraph )
			print Exception
			

		if 'label' in TemplateGraph.node[self.templatenode]:
		
			for i in  range(len(TemplateGraph.node[str(self.templatenode)]['label'].split(r'\n'))):
				regexline = []
		
				regex = TemplateGraph.node[str(self.templatenode)]['label'].split(r'\n')[i]
									
				reverse = None
									
				for item in filter(None, regex.split(',')):

					if item in arch.arch:
						
						if type(arch.arch[item]) is str:
							#If the string in the template is a keyword, we replace it with the Regex
							regexline.append(re.compile(arch.arch[item], re.UNICODE | re.IGNORECASE))

						if type(arch.arch[item]) is tuple:
							arch.arch[item][0]
							regexline.append(re.compile(arch.arch[item][0], re.UNICODE | re.IGNORECASE))
							reverse = arch.arch[item][1]
							
					else:
						#else we simply use the string as Regex
						regexline.append(re.compile(item, re.UNICODE | re.IGNORECASE))
											

				if reverse is 'SD':
					#print 'Do reverse source and dest'
					regexline[2], regexline[1] = regexline[1], regexline[2]


				regexlist.append(regexline)
			
			#Get Content of Basic Block
			BasicBlock = self.get_BB_Content(Graph, str(self.graphnode), arch)
			

			
			thatmany = 0
			res.append(self.graph)
			res.append(self.templategraph)
			res = [Graph.name.strip('x')]
			
			for regexline in regexlist:
				for line in BasicBlock:
					#matched regex count
					count = 0
					
					# Match the Regex to its corresponding Assembly part
					for i in izip(line,regexline):	
						m = re.match(i[1], i[0])		
					
						if m : 
							count += 1

						else :
							count = 0

					thatmany += count 
					

			matched_regex = 0
			for regexline in regexlist:
				
				matched_regex += len(regexline)

			res.append(abs(matched_regex - thatmany))

		return res

	

























	
		'''
	# This is not needed anymore
	def beautify(self, Graph):
		print Graph
		for node_number in range(0, nx.number_of_nodes(Graph)):
			Node_content = [node_number , Graph.node[str(node_number)]['label']]
			#Node_content_pretty = re.sub('\\l', '', Node_content[1])
			Node_content_pretty = re.sub(r'\\n', '\n', Node_content[1])
			Node_content_pretty = re.sub(r'\\', '', Node_content_pretty)
			Node_content_pretty = re.sub(r'\t ', '\t', Node_content_pretty)
			Node_content_pretty = re.sub(r', ', ',', Node_content_pretty)   

			Graph.node[str(node_number)]['label'] =  Node_content_pretty
			
		return Graph
	

	
	def get_BB_Count(self, Graph):
			return nx.number_of_nodes(Graph)
	'''	
		
		

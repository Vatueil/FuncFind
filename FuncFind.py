# this script is for finding functions e.g. memcpy etc

import idautils 
import idaapi 
import idc 

import networkx as nx

from operator import itemgetter

from idautils import *

from graph import AnalyzeGraph
from regex import AnalyzeAssembly

import config


Funclist = []

def read_files(path_to_tmp):
	files = []
	for file in os.listdir(path_to_tmp):
		if file.endswith(".gv"):
			files.append(file)
	return files
	
def ReadFilesasDot():
	pass

	
def CountXrefsTo(ea):
	return len(list(CodeRefsTo(ea, 1)))
	
def GetXrefs(self, funcea):
		for ref in CodeRefsTo(funcea, 1):
			Xrefs.append(GetFunctionName(ref), ref)

		return Xrefs

class ExportFromIDA():

	def GetFunctionNames(self):
		#
		# Loop from start to end in the current segment
		#
		ea = ScreenEA()
		for funcea in Functions(SegStart(ea), SegEnd(ea)):
			Funclist.append([funcea, GetFunctionName(funcea)])	

		return Funclist
		
		
	def UnkownFuncs(self, funclist):
		#
		# Retrieves a List of unknown Functions (aka all those with name: sub_*)
		#
		unkown_func_list = []
		p = re.compile('\Asub_.')

		for fun in funclist:
			
			if p.match(fun[1]):
				unkown_func_list.append(fun)
				
		return unkown_func_list
		
		
	def CountBasicBlocks(self, ea):
		#
		#Returns the count of Basics Blocks for a given Function
		#
		count = 0
		f = idaapi.FlowChart(idaapi.get_func(ea))
		for block in f:
			count = count + 1

		return count

		
	def GetInstructions(self, start_ea, end_ea):
		#
		#Returns a List of all instructions in the Range start_ea, end_ea
		#
		ins = []
		for head in idautils.Heads(start_ea, end_ea):
			if idaapi.isCode(idaapi.getFlags(head)):
				ins.append(GetDisasm(head))
		return ins
	
		
	def CFG2Dot(self, ea):
		#
		# Converts a Function identified by an ea of the Function to a .dot format
		#
		cfg_graph = ""
		
		f = idaapi.FlowChart(idaapi.get_func(ea))
		# Clear up Function Name
		Func_Name = str(GetFunctionName(ea)) + str(ea)
		#Cleared_Name = re.sub(r'[/\;,.><&*:%=+@!#^()|?^]', '', Func_Name)
		# cfg_graph += "digraph %s { \n" % (Cleared_Name + '+%x' %ea)
		
		# Write beginning of dot file
		cfg_graph += "digraph %s { \n" % ('x%x' %ea)
		cfg_graph += "\t{\n"
		
		# Write all Instructions into corresponding Basic Blocks
		for block in f:
			# Beginning of a Basic Block
			cfg_graph += "\t %s [shape=box label=" % (str(block.id))
			InstructionsHelper = "\""
			#Fill Basic Block with its Assembly
			for Ins in self.GetInstructions(block.startEA, block.endEA):
				head, sep, tail = Ins.partition(";")
				helper = head.split()
				helper[0] = helper[0] + '\t'
				head = ''.join(helper)
				InstructionsHelper += head
				InstructionsHelper += "\\n"
			InstructionsHelper += "\"]\n"
			# Add Basic Block to dot File
			cfg_graph += InstructionsHelper
		# Close Nodes in dot Graph
		cfg_graph += "\n\t}\n"
		
		#Write the Edges
		for block in f:
			for succ_block in block.succs():
				cfg_graph += "%d -> %d\n" % (block.id, succ_block.id)
			
			for pred_block in block.preds():
				cfg_graph += "%d -> %d\n" % (block.id, pred_block.id)
		#Close dot Graph
		cfg_graph += "}"
		
		return cfg_graph

		
	def WriteTmpFiles(self, FuncName , Graph):
		#
		# This writes a File to the given Location on the HD
		#
		filename = config.path
		
		try:
			filename = os.path.join( config.path, 'tmp_' + FuncName + '.gv')

		except Exception:
			print 'File Name Error'
		
		try:
			text_file = open(filename, "w")
			text_file.write(Graph)
			text_file.close
		except Exception:
			print 'File Writing Error'
			
		
def main():
	#
	# Main
	#
	
	# Initialize Result for output
	result = []

	print 'Welcome to FuncFind'

	# All the Functions will be exported to dot
	Export_From_IDA = ExportFromIDA()
	FuncList = Export_From_IDA.GetFunctionNames()
	
	#Clean up File Names
	for func in FuncList:
		func[1] = re.sub(r'[/\;,.><&*:%=+@!#^()$|?^]', '', func[1])


	for Func in FuncList:
		CountofBasicBlocks = Export_From_IDA.CountBasicBlocks(Func[0])
		# Export only files smaller than 60 Basic Blocks
		# This is done due to speed issues and most of the time we do not need more
		# Use e.g. bindiff tools for bigger Functions
		if CountofBasicBlocks <= config.max_BB_Count :
			#Get Graph of this Function
			Graph = Export_From_IDA.CFG2Dot(Func[0])
			#Write it to a File
			Export_From_IDA.WriteTmpFiles(Func[1] , Graph)
			
	print 'Wrote all tmp Files'	
	
	## Now we do the Analyze Stuff	
	## First Call graph analysis

	# Read all the exported Files 
	file_list = read_files(config.path)
	# Read all the templates
	template_list = read_files(config.path1)

	analyzeGraphs = AnalyzeGraph(template_list, file_list, config.path, config.path1)
	
	# We want a mapping of template and Function for comparison
	found_mappings = analyzeGraphs.analyze()

	# We sort these mapping by difference of count of Basic Blocks
	# A Graph Edit distance which would also give us a (maxium) mapping would be nicer
	found_mappings.sort(key= lambda x: int(x[3]))
	
	## Second comes the matching of the Regex in the templates 
	
	print 'Graphs have been analyzed'
	
	if found_mappings != None:
	
		for mapping in found_mappings:
			
			# Match all Regex to all Functions when they have a mapping
			for key,val in mapping[2][1].items():			
			
				Graph = mapping[1]
				Template_Graph = mapping[0]
				Graph_Node = key
				Template_Node = val
				
				# Call matching Routine
				analyzeAssembly = AnalyzeAssembly(Graph, Template_Graph, Graph_Node, Template_Node, config.path , config.path1, config.arch)
				analyzed = analyzeAssembly.analyze()

				# Append Result 
				if len(analyzed) > 0:
					result.append([mapping, analyzed])

					

	# This sorts the result by Function Name, Diffcount of BasicBlocks and Count of Matched Regex
	result.sort(key= lambda x: (x[0][0], x[0][3], x[1][1]))

	print 'Assembly Information has been analyzed'
	
	# Do nice formatted output
	temp = ''
	print 'The smaller the difference the better, usually.'
	for res in result:
		
		if res[0][3] <= config.max_BB_output and res[1][1] <= config.max_REGEX_Count:
			if temp != res[0][0]:
				print "For %s following Functions are candidates:" % (res[0][0])
				print '\t FunctionName         \t Location \t (Diff BB / Regex) \t  #XrefsTO'
			temp = res[0][0]
			
			print "\t %-30s at 0x%-8s  \t (%2s/%2s) \t\t %s" %(GetFunctionName(long(res[1][0],16)) ,res[1][0],  res[0][3] , res[1][1], CountXrefsTo(long(res[1][0],16)))
	print	
	print 'all Done'


if __name__ == "__main__":
    main()

	

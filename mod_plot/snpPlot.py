from parser import _23andmeObject, stream2BEDfile, stream2SSfile, CHROMOSOME_LIST, printMsg
import numpy as np
from matplotlib import pyplot as plt

RSID = 'RSID'
# Value... (fieldnames)
DESCRIPTION = 'DESCRIPTION'
CHROMOSOME = 'CHROMOSOME'
POSITION = 'POSITION'
GENOTYPE = 'GENOTYPE'
DATE = 'DATE'

"""
******* TO BE MOVED TO mod_snp in mySNPit ********
along with parser.py and BioinformaticsFile.py

Needs:
(1) One list of SNP positions for every chromosome (1-22, X, Y, MT)
(2) One list containing tuples of SNP position and asssociated 
chromosome for all chromosomes combined
(3) An X_axis and Y_axis list splitting the tuples in half
(4) Stdout of composition 
"""

class Chromosome:
	"""
	chrom => '1', '2', ..., or 'X', 'Y', 'MT'

	Chromosome object containing all information for 
	analysis and interpretation of the chromosomes. 

	"""
	def __init__(self, chrom=""):
		if chrom == "":
			printMsg("Enter chromosome (1, 2, ..., or 23 (X), 24 (Y), 25 (MT))")
			chrom = raw_input('---> ')

		self.num = int(chrom)
		self.chrLengths = [248956422, 242193529, 198295559, 190214555, 181538259, \
		170805979, 159345973, 145138636, 138394717, 133797422, 135086622, \
		133275309, 114364328, 107043718, 101991189, 90338345, 83257441, \
		80373285, 58617616, 64444167, 46709983, 50818468, 156040895, 57227415, 16569]

		self.positions = []
		self.minSNP = 0
		self.maxSNP = 0

	def size(self):
		return self.chrLengths[self.num-1]

	def totalSNPs(self):
		return len(self.positions)



ChromosomeDict = _23andmeObject("../../BIO_DATA/raw23andme_SNPs_teyden.txt", 'CHROMOSOME')
ChromosomePositions = {}
Chromosomes = {}	# Dictionary of Chromosome objects

### (1) One list of SNP positions for every chromosome (1-22, X, Y, MT)
"""
ChromosomePositions['1'] = a list of positions for chromosome 1
... etc.
"""

# Make dict of all SNP positions. Keys = Chromosome #, Values = lst of positions
for chrom in ChromosomeDict:
	ChromosomePositions[chrom] = ChromosomeDict[chrom].keys()
	ChromosomePositions[chrom].sort()  # Could go without
	Chromosomes[chrom] = Chromosome(chrom=chrom)
	Chromosomes[chrom].positions = ChromosomePositions[chrom]
	ChromosomePositions[chrom] = np.array(ChromosomePositions[chrom],dtype=np.float64)

# Output min and max values
for chrom in ChromosomePositions:
	Chromosomes[chrom].minSNP = ChromosomePositions[chrom].min()
	Chromosomes[chrom].maxSNP = ChromosomePositions[chrom].max()
	printMsg("Chr%s: lowest chromosome position, highest chromosome position = (%s, %s)" % (chrom, Chromosomes[chrom].minSNP, Chromosomes[chrom].maxSNP))
	
ChromosomeSizes = []
for chrom in Chromosomes:
	ChromosomeSizes.append(Chromosomes[chrom].size())
	print Chromosomes[chrom].size()

ChromosomeSizes.sort()
ChromosomeSizes.reverse()
ChromosomeSizes = np.array(ChromosomeSizes)
largest_size = ChromosomeSizes.max()
smallest_size = ChromosomeSizes.min()
largest_chrom = ""
smallest_chrom = ""
printMsg("Chromosomes By Size")
index = 1
for size in ChromosomeSizes:
	for chrom in Chromosomes:
		if size == Chromosomes[chrom].size():
			print "%d | Chr%s  %s bp | %s #SNPs" % (index, chrom, Chromosomes[chrom].size(), Chromosomes[chrom].totalSNPs())
			index += 1
		if largest_size == Chromosomes[chrom].size():
			largest_chrom = chrom
		if smallest_size == Chromosomes[chrom].size():
			smallest_chrom = chrom

print "LARGEST: Chromosome %s, %sbp" % (largest_chrom, largest_size)
print "SMALLEST: Chromosome %s, %sbp" % (smallest_chrom, smallest_size)

### (2) One list containing tuples of every SNP position and asssociated chromsome
AllChromosomes = []
for chrom in ChromosomePositions:
	for i in ChromosomePositions[chrom]:
		AllChromosomes.append((i, int(chrom)))

AllChromosomes = np.array(AllChromosomes)
Y_axis, X_axis = np.split(AllChromosomes,2,1)

# plt.scatter(X_axis, Y_axis)
# plt.show()
# plt.savefig('plot_results/chromosomes.png')
printMsg("Mitochondrial # SNPs = %s, size = %s" % (Chromosomes['25'].totalSNPs(), Chromosomes['25'].size()))

#### Plot composition statistics ####
from plotter import make_scatter_trace, make_bar_trace, plot_with_plotly
import plotly.plotly as py
from plotly.graph_objs import *
red = 'rgb(42, 106, 255)'
blue = 'rgb(234, 153, 153)'

# chr_strings = ['chr%s' % i for i in range(1, 23) + ['M', 'X', 'Y']]
# trace = make_scatter_trace(X=X_axis, Y=Y_axis)
# ticktext = {'x': ['%s' % x for x in range(1, 23) + ['X', 'Y', 'MT']]}
# plot_with_plotly(X=X_axis, Y=Y_axis, Titles=[x_title, y_title, plot_title], trace=[trace], ticktext=ticktext)

# STREAM_ID="rtmpmhxqrz"
# y_title = "SNP location (bp)"
# x_title = "Chromosome"
# plot_title = "23andMe SNP Chromosome Density"
# x_ticks = ['%s' % x for x in range(1, 23) + ['X', 'Y', 'MT']]

# figure = Figure(
# 	data=Data([
# 		Scatter( 
# 			x=X_axis, 
# 			y=Y_axis,
# 			line=Line(color='rgb(234, 153, 153)', width=0.2)
# 		)]),
# 	layout=Layout(
# 		title=plot_title,
# 		xaxis=XAxis(
# 			title=x_title,
# 			ticktext=x_ticks,
# 			tickvals=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25]
# 			),
# 		yaxis=YAxis(
# 			title=y_title
# 			),
# 		font = dict(
# 			size=14
# 			),
# 		titlefont = dict(
# 			size=24
# 			)
# 		)
# 	)

# py.plot(figure, filename='SNP Chromosome Density', stream=Stream(token=STREAM_ID, maxpoints=1000))
# printMsg("Plot (%s) has been plotted with plotly." % plot_title)

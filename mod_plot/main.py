import json

from plotter import make_scatter_trace, make_bar_trace
import plotly.plotly as py
from plotly.graph_objs import *

import numpy as np  # (*) numpy for math functions and arrays
from random import randint

## Constants
# chrLengths[chr number + 1] will give you the length for the respective chr.
chrLengths = [248956422, 242193529, 198295559, 190214555, 181538259, \
170805979, 159345973, 145138636, 138394717, 135086622, 133275309, \
114364328, 107043718, 101991189, 90338345, 83257441, 80373285, \
58617616, 64444167, 46709983, 50818468, 156040895, 57227415]

def printHeader(string):
	length = len(string)
	dashes = ""
	for i in range(0,length+2):
		dashes += "-"
	final = "\n" + dashes + "\n " + string + " \n" + dashes 
	print final 


chrLst = ['chr%s' % x for x in range(1, 23) + ['X', 'Y', 'MT']]

chr_data = {}
for chr in chrLst:
	if chr == "chrX":
		chr_data['chrX'] = {'total_snps': 0, 'total_chromosome_length': chrLengths[-3], 'snp_ratio': 0}
	elif chr == "chrY":
		chr_data['chrY'] = {'total_snps': 0, 'total_chromosome_length': chrLengths[-2], 'snp_ratio': 0}
	elif chr == "chrMT":
		chr_data['chrMT'] = {'total_snps': 0, 'total_chromosome_length': chrLengths[-1], 'snp_ratio': 0}
	else:
		chr_data[chr] = {'total_snps': 0, 'total_chromosome_length': chrLengths[int(chr[-1])], 'snp_ratio': 0}

count = 0
for chrNum in chrLst:
	snp_json_file = open('results/teyden_%s_snps.json' % chrNum, 'r')
	snp_json = json.load(snp_json_file)
	# print snp_json['chr'+chrNum]

	chr_data[chrNum]['positions_rsids'] = snp_json[chrNum]
	chr_data[chrNum]['total_snps'] = len(snp_json[chrNum])
	chr_data[chrNum]['snp_ratio'] = float(chr_data[chrNum]['total_snps'])/ \
	float(chr_data[chrNum]['total_chromosome_length'])

	#### Print out statistics ####
	printHeader("Chromosome %s" % chrNum)
	print "Number of SNPs: %d" % chr_data[chrNum]['total_snps']
	print "Chromosome length: %d" % chr_data[chrNum]['total_chromosome_length']
	print "SNP Ratio (# SNPs / Chromosome Length): %s" % str(chr_data[chrNum]['snp_ratio'])
	
	lstOfdictRSIDs = chr_data[chrNum]['positions_rsids'].values()
	with open('results/%s_snps.txt' % chrNum, 'w') as f:
		for item in lstOfdictRSIDs:
			f.write(item['RSID']+'\n')
	f.close()

	count += 1
	if count > 1:
		break

"""
Notes:
- Number of SNPs == Number of positions 

"""
red = 'rgb(42, 106, 255)'
blue = 'rgb(234, 153, 153)'


chromosome_list = ['chr%s' % i for i in range(1, 23) + ['M', 'X', 'Y']]
#### Plot composition statistics ####

positions1 = chr_data['chr1']['positions_rsids'].keys()
positions1.sort()
y_axis1 = tuple(positions1)
x_axis1 = ('1',)*len(positions1)
trace1 = make_bar_trace(X=x_axis1, Y=y_axis1, color=red)


positions2 = chr_data['chr2']['positions_rsids'].keys()
positions2.sort()
y_axis2 = tuple(positions2)
x_axis2 = ('2',)*len(positions2)
trace2 = make_bar_trace(X=x_axis2, Y=y_axis2, color=blue)


# positions3 = chr_data['chr3']['positions_rsids'].keys()
# positions3.sort()
# y_axis3 = tuple(positions3)
# x_axis3 = ('3',)*len(positions2)
# trace3 = scatter_builder_plotly(x_axis2, y_axis2, mode='text', line=Line(dash='dots', color=red, width=0.2))

y_title = "SNP density (bp)"
x_title = "Chromosome"
X = [x_axis1, x_axis2]
Y = [y_axis1, y_axis2]
# plot_with_plotly(X=[x_title]+x_axis1, Y=[y_title]+y_axis1, plotTitle="23andMe SNP Chromosomal Abundance", trace=[trace1])
rsidList = [randint(1000,2000) for p in range(26)]
rsids = ['rs%d' % x for x in rsidList]
colors = ['#42A5B3']*5 + ['#D15A86']*5 + ['#5C8100']*7 + ['#E58429']*9

# data = Data([
#     make_trace([mtl_P[i], van_P[i]], rsids[i], colors[i])
#     for i in range(12)
# ])
data = Data([make_bar_trace(x_axis1[i], y_axis1[i], rsids[i], colors[i]) for i in range(26)])

title = "SNP Density per Chromosome \
<i>hover with cursor to see each chromosome's SNPs</i>"  # plot's title 

# (2) Make Layout object
layout = Layout(
    barmode='stack',  # (!) bars are stacked on this plot
    bargap=0.6,       # (!) spacing (norm. w.r.t axis) between bars
    title=title,        # set plot title
    showlegend=False,   # remove legend
    yaxis= YAxis(
        title=y_title, # x-axis title 
        gridcolor='white',  # white grid lines
        gridwidth=2,        # bigger grid lines
        zeroline=False,     # remove thick zero line
        ticks='outside',    # draw ticks outside axes
        autotick=False,     # (!) overwrite default tick options
        dtick=100,          # (!) set distance between ticks  
        ticklen=8,          # (!) set tick length
        tickwidth=1.5       #     and width
    ),
    plot_bgcolor='rgb(233,233,233)',  # set plot color to grey
)

# (3) Make Figure object, 
fig = Figure(data=data, layout=layout)

# Send to Plotly and show in notebook
py.plot(fig, filename='snp_density')


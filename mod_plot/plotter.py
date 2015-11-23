import plotly.plotly as py
from plotly.graph_objs import *
import csv


def make_scatter_trace(X=[], Y=[], mode="markers", name="", line=""):
	if line == "":
		trace = Scatter( 
				x=X, 
				y=Y,
				name=name,
				mode=mode,
				line=Line(shape='spline', color='rgb(234, 153, 153)', width=0.3)
			)
	elif line == 'default_dots':
		trace = Scatter( 
				x=X, 
				y=Y,
				mode=mode,
				name=name,
				line=Line(
					shape='dots', 
					color='rgb(234, 153, 153)', 
					width=0.3)
			)
	else:
		trace = Scatter( 
				x=X, 
				y=Y,
				mode=mode,
				name=name,
				line=line
			)
	return trace

def make_bar_trace(X=[], Y=[], name="", color='rgb(234, 153, 153)'):
    return Bar(
        y=Y,   # cities name on the y-axis
        x=X,        # monthly total on x-axis
        name=name,  # label for hover 
        orientation='h',   # (!) for horizontal bars, default is 'v'
        marker= Marker(
            color=color,        # set bar colors
            line= Line(
                color='white',  # set bar border color
                width=1         # set bar border width
            )
        )
    )

def plot_with_plotly(X=[], Y=[], Titles=[], trace=[]):
	"""
	Plotter for the plotly module. Loads the web interface 
	for plotly upon successful call to the function, prints
	out success statement, and returns True. 

	X and Y must be non-empty lists of equal lengths. 
	title is an empty string by default. 
	If trace is not specified, then the default trace will be
	used.  
	"""
	if X == [] and Y == []:
		print "Input non-empty lists for x."
	# if type(X[0]) != type("") or type(Y[0]) != type(""): 
	# 	raise TypeError, "Enter titles in the first element of X and Y"
	# if len(Y) != len(X):
	# 	raise ValueError, "X and Y must be lists of the same length"
	
	# If trace == [], then there is a maximum of one Y axis list.
	if trace == []:  
		# Builds the default trace using the X and Y axis lists
		trace = scatter_builder_plotly(X=X[1:], Y=Y[1:])

	# if trace != type([]):
	# 	trace = [trace]

	data = Data(trace)
	layout = Layout(
		title=Titles[2],
		xaxis=XAxis(
			title=Titles[0],
			showgrid=True,
			zeroline=True,
			gridwidth=0.8
			),
		yaxis=YAxis(
			title=Titles[1],
			showgrid=True,
			zeroline=True,
			gridwidth=0.8
			),
		font=dict(
			size=16
			),
		titlefont=dict(
			size=24
			)
	)
	figure = Figure(data=data, layout=layout)
	plot = py.plot(figure, filename=Titles[2], validate=False)
	print "Plot '%s' has been plotted with plotly." % Titles[2]


def save_toCSV(storage, path):
		''' 
		Inserts every element in storage to a CSV file given by
		the path string.

		storage is a dictionary with two elements with keys as axis titles
		and values as a list of values with the first element as the title
		for the axis 
			storage['x'] = ['title for x axis', x values...]
			storage['y'] = ['title for y axis', y values...]

		'''
		with open(path, 'w') as csvfile:
			fieldnames = [storage['x'][0], storage['y'][0]]
			writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

			# Sets CSV headers with fieldnames
			writer.writeheader()
			# Sets CSV headers with fieldnames
			for key in storage:

				for i in range(1,len(storage[key])):
					writer.writerow({
						storage[key][0]: storage[key][i]
						})
				print "save_toCSV() Status ||| %s added to CSV." % key
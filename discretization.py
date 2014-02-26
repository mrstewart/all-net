"""
This code taken from the matplotlib examples

This example shows how to use a path patch to draw a bunch of
rectangles.  The technique of using lots of Rectangle instances, or
the faster method of using PolyCollections, were implemented before we
had proper paths with moveto/lineto, closepoly etc in mpl.  Now that
we have them, we can draw collections of regularly shaped objects with
homogeous properties more efficiently with a PathCollection.  This
example makes a histogram -- its more work to set up the vertex arrays
at the outset, but it should be much faster for large numbers of
objects
"""
import os
import pickle
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.path as path


def discretize(data, bins):
	return np.histogram(data, bins)

def testDiscretization(n, bins):	
	fig, ax = plt.subplots()

	# get the corners of the rectangles for the histogram
	left = np.array(bins[:-1])
	right = np.array(bins[1:])
	bottom = np.zeros(len(left))
	top = bottom + n


	# we need a (numrects x numsides x 2) numpy array for the path helper
	# function to build a compound path
	XY = np.array([[left,left,right,right], [bottom,top,top,bottom]]).T

	# get the Path object
	barpath = path.Path.make_compound_path_from_polys(XY)

	# make a patch out of it
	patch = patches.PathPatch(barpath, facecolor='blue', edgecolor='gray', alpha=0.8)
	ax.add_patch(patch)

	# update the view limits
	ax.set_xlim(left[0], right[-1])
	ax.set_ylim(bottom.min(), top.max())

	plt.show()

RPI_BINS = 30
WP_BINS = 30
PYTH_BINS = 30
TESTING_BINS = True

if os.path.exists("teams.p"):
	teams = pickle.load( open( "teams.p", "rb" ) )
	rpi_data = []
	for team in teams.keys():
		rpi_data.append(teams[team].ratingPercentageIndex)

	wp_data = []
	for team in teams.keys():
		wp_data.append(teams[team].winningPercentage)

	pyth_data = []
	for team in teams.keys():
		pyth_data.append(teams[team].pythagoreanExpectation)

	# histogram our data with numpy
	rpi_frequency, rpi_bins = discretize(rpi_data, RPI_BINS)
	if TESTING_BINS: testDiscretization(rpi_frequency, rpi_bins)

	# histogram our data with numpy
	wp_frequency, wp_bins = discretize(wp_data, WP_BINS)
	#if TESTING_BINS: testDiscretization(wp_frequency, wp_bins)
	
	# histogram our data with numpy
	pyth_frequency, pyth_bins = discretize(pyth_data, PYTH_BINS)
	#if TESTING_BINS: testDiscretization(pyth_frequency, pyth_bins)

	# Convert rating percentage index for each team to an ordinal value
	for team in teams.keys():
		for i in range(len(rpi_bins) - 1):
			if teams[team].ratingPercentageIndex >= rpi_bins[i] and teams[team].ratingPercentageIndex < rpi_bins[i + 1]:
				teams[team].ratingPercentageIndex = i


	# Convert winning percentage for each team to an ordinal value
	for team in teams.keys():
		for i in range(len(wp_bins) - 1):
			
			if teams[team].winningPercentage >= wp_bins[i] and teams[team].winningPercentage < wp_bins[i + 1]:
				teams[team].winningPercentage = i
				break

	

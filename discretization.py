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
import sys
import os
import pickle
import inspect
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.path as path
from constants import *


def binValue(bins, value):
	for i in range(len(bins) - 1):
		if i < len(bins) - 2:
			if value >= bins[i] and value < bins[i + 1]:
				return i
		else:
			return i


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
CG_BINS = 30
TPF_BINS = 30
TPA_BINS = 30
NV_BINS = 30
NL_BINS = 30
AVGMV_BINS = 30
TESTING_BINS = True

EXPORT_WITH_HEADINGS = True
EXPORT_ID = True
EXPORT_NAME = False
EXPORT_RPI = True
EXPORT_WP = True
EXPORT_PYTH = True
EXPORT_CWG = True
EXPORT_TPF = True
EXPORT_TPA = True
EXPORT_NV = True
EXPORT_NL = True
EXPORT_AVGMV = True

TEAMS_DATA_PATH = "teams.p"

if os.path.exists(TEAMS_DATA_PATH):
	teams = pickle.load( open( TEAMS_DATA_PATH, "rb" ) )

	nl_data = []
	avgMV_data = []
	nv_data = []
	rpi_data = []
	pyth_data = []
	tpa_data = []
	wp_data = []
	tpf_data = []
	cg_data = []

	for team in teams.keys():
		rpi_data.append(teams[team].ratingPercentageIndex)
		wp_data.append(teams[team].winningPercentage)
		pyth_data.append(teams[team].pythagoreanExpectation)
		cg_data.append(teams[team].closeWonGames)
		tpf_data.append(teams[team].totalPointsFor)
		tpa_data.append(teams[team].totalPointsAgainst)
		nv_data.append(teams[team].numVictories)
		nl_data.append(teams[team].numberOfLosses)
		avgMV_data.append(teams[team].averageMarginOfVictory)
	

	# histogram our data with numpy
	rpi_frequency, rpi_bins = discretize(rpi_data, RPI_BINS)
	#if TESTING_BINS: testDiscretization(rpi_frequency, rpi_bins)

	# histogram our data with numpy
	wp_frequency, wp_bins = discretize(wp_data, WP_BINS)
	#if TESTING_BINS: testDiscretization(wp_frequency, wp_bins)
	
	# histogram our data with numpy
	pyth_frequency, pyth_bins = discretize(pyth_data, PYTH_BINS)
	#if TESTING_BINS: testDiscretization(pyth_frequency, pyth_bins)

	# histogram our data with numpy
	cg_frequency, cg_bins = discretize(cg_data, CG_BINS)
	#if TESTING_BINS: testDiscretization(cg_frequency, cg_bins)

	# histogram our data with numpy
	tpf_frequency, tpf_bins = discretize(tpf_data, TPF_BINS)
	#if TESTING_BINS: testDiscretization(tpf_frequency, tpf_bins)

	# histogram our data with numpy
	tpa_frequency, tpa_bins = discretize(tpa_data, TPA_BINS)
	#if TESTING_BINS: testDiscretization(tpa_frequency, tpa_bins)

	# histogram our data with numpy
	nv_frequency, nv_bins = discretize(nv_data, NV_BINS)
	#if TESTING_BINS: testDiscretization(nv_frequency, nv_bins)	

	# histogram our data with numpy
	nl_frequency, nl_bins = discretize(nl_data, NL_BINS)
	#if TESTING_BINS: testDiscretization(nl_frequency, nl_bins)

	# histogram our data with numpy
	avgMV_frequency, avgMV_bins = discretize(avgMV_data, AVGMV_BINS)
	#if TESTING_BINS: testDiscretization(avgMV_frequency, avgMV_bins)

	# Convert winning percentage for each team to an ordinal value
	# write team vector to file
	for team in teams.keys():
		if team in IGNORE_TEAMS: continue
		
		# Go through each bin and figure out what this team's value for this attribute
		# falls in - use the bin's 0-indexed number as the discretized number
		if EXPORT_RPI:
			teams[team].ratingPercentageIndex = binValue(rpi_bins, teams[team].ratingPercentageIndex)

		# Go through each bin and figure out what this team's value for this attribute
		# falls in - use the bin's 0-indexed number as the discretized number
		if EXPORT_WP:
			teams[team].winningPercentage = binValue(wp_bins, teams[team].winningPercentage)
				
		# Go through each bin and figure out what this team's value for this attribute
		# falls in - use the bin's 0-indexed number as the discretized number
		if EXPORT_PYTH:	
			teams[team].pythagoreanExpectation = binValue(pyth_bins, teams[team].pythagoreanExpectation)
				
	
		# Go through each bin and figure out what this team's value for this attribute
		# falls in - use the bin's 0-indexed number as the discretized number
		if EXPORT_CWG:	
			teams[team].closeWonGames = binValue(cg_bins, teams[team].closeWonGames)
				

		# Go through each bin and figure out what this team's value for this attribute
		# falls in - use the bin's 0-indexed number as the discretized number
		if EXPORT_TPF:		
			teams[team].totalPointsFor = binValue(tpf_bins, teams[team].totalPointsFor)
				

		# Go through each bin and figure out what this team's value for this attribute
		# falls in - use the bin's 0-indexed number as the discretized number
		if EXPORT_TPA:		
			teams[team].totalPointsAgainst = binValue(tpa_bins, teams[team].totalPointsAgainst)
				

		# Go through each bin and figure out what this team's value for this attribute
		# falls in - use the bin's 0-indexed number as the discretized number
		if EXPORT_NV:	
			teams[team].numVictories = binValue(nv_bins, teams[team].numVictories)

		
		# Go through each bin and figure out what this team's value for this attribute
		# falls in - use the bin's 0-indexed number as the discretized number
		if EXPORT_NL:
			teams[team].numberOfLosses = binValue(nl_bins, teams[team].numberOfLosses)

		# Go through each bin and figure out what this team's value for this attribute
		# falls in - use the bin's 0-indexed number as the discretized number
		if EXPORT_AVGMV:
			teams[team].averageMarginOfVictory = binValue(avgMV_bins, teams[team].averageMarginOfVictory)
				

# Delete original file
os.remove("teams.p")

# Write teams to that file
pickle.dump(teams, open( "teams.p", "wb" ) )

	

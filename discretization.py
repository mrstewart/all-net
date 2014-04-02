#
#			Discretization.py
#	
# Uses numpy for discretization, bins values into
# specified number of bins for each attribute
# exports the result to the teams pickle file (overwriting it)

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

	

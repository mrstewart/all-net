# This class joins data from a season and the teams file to fill out each team object
# with appropriate data

import pickle
import os
import math
from team import *
from classes import *
from constants import *

teams = pickle.load( open( TEAMS_DATA_PATH, "rb" ) )

# Calculate statistics based on selected seasons
for season in SEASONS_TO_PICK_FROM:
	season_filename = "chopped_data/" + season + "_" + REGULAR_SEASON_FILENAME + ".p"
	regular_season_results = pickle.load( open( season_filename, "rb" ))
	
	for regularGame in regular_season_results:
		# References to make things easier to read
		winningTeamId = regularGame.winningTeam
		losingTeamId = regularGame.losingTeam

		marginOfVictory = regularGame.winningScore - regularGame.losingScore

		# Add opposing team to each respective team (winning team or losing team)
		teams[winningTeamId].opponentList.append(winningTeamId)
		teams[losingTeamId].opponentList.append(winningTeamId)

		# Increment total points for
		teams[winningTeamId].totalPointsFor += regularGame.winningScore
		
		# Increment total points against
		teams[losingTeamId].totalPointsAgainst += regularGame.losingScore

		# Increment number of victories
		teams[winningTeamId].numVictories += 1

		# Increment number of losses
		teams[losingTeamId].numberOfLosses += 1

		# Add term to average margin of victory
		teams[winningTeamId].averageMarginOfVictory += marginOfVictory
		teams[losingTeamId].averageMarginOfVictory -= marginOfVictory

		# Increment number of close won games
		if marginOfVictory <= MAX_CLOSE_GAME_MV:
			teams[winningTeamId].closeWonGames += 1.0


# Calculate averages across seasons
for team in teams:
	#if team in IGNORE_TEAMS: continue
	# Games Played
	gamesPlayed = teams[team].numVictories + teams[team].numberOfLosses 
	
	if gamesPlayed == 0: continue

	# Average margin of victory
	teams[team].averageMarginOfVictory /= gamesPlayed
	
	# Calculate winning percentage
	teams[team].winningPercentage = teams[team].numVictories / gamesPlayed

	# Average total points for
	teams[team].totalPointsFor /= len(SEASONS_TO_PICK_FROM)

	# Average total points against 
	teams[team].totalPointsAgainst /= len(SEASONS_TO_PICK_FROM)

	# Average close won Games
	teams[team].closeWonGames /= len(SEASONS_TO_PICK_FROM)


# Calculate Rating Percentage Index and Pythagorean Expectation, which depend 
# on the above calculations
for team in teams:
	#if team in IGNORE_TEAMS: continue
	# Pythagorean Expectation
	peNumerator = pow(teams[team].totalPointsFor, 13.91)
	peDenominator = pow(teams[team].totalPointsFor, 13.91) + pow(teams[team].totalPointsAgainst, 13.91)
	
	if peDenominator == 0: continue

	teams[team].pythagoreanExpectation =  peNumerator / peDenominator

	# Rating Percentage Index
	OWP = 0.0
	OOWP = 0.0
	OLen = len(teams[team].opponentList)
	OOLen = 0
	
	# Start summation for OWP and OOWP
	for opponent in teams[team].opponentList:
		OWP += teams[opponent].winningPercentage
		OOLen += len(teams[opponent].opponentList)
		for opponentOpponent in teams[opponent].opponentList:
			OOWP += teams[opponentOpponent].winningPercentage

	# Return something only if the team had opponents
	if OLen != 0:
		teams[team].ratingPercentageIndex += 0.5 * (OWP / OLen)
		teams[team].ratingPercentageIndex += 0.25 * (OOWP / OOLen)
		teams[team].ratingPercentageIndex += 0.25 * teams[team].winningPercentage
	
	# Else return "NA"		
	else:			
		teams[team].ratingPercentageIndex = "NA" 

# Delete original file
os.remove(TEAMS_DATA_PATH)

# Write teams to that file
pickle.dump(teams, open( TEAMS_DATA_PATH, "wb" ) )


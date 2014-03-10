##########################################
#
#	Statistics Functions
#
##########################################

MAX_CLOSE_GAME_MV = 7 	# The maximum margin of victory for a close game. 
		 	# Equivalent to: 
			# 	2 3-point shots and a foul shot
			#	3 2-point shots and a foul shot
			#	2 2-point shots and a 3-point shot

# Calculate simple statistics for all teams
def calculateTeamStatistics(teams, season):
	
	for entry in season:
		winningTeamId = entry[2]
		losingTeamId = entry[4]
		gameMarginOfVictory = float(entry[3] - entry[5])	

		winningTeam = teams[winningTeamId]
		losingTeam = teams[losingTeamId]		
		
		# Aggregate stats for the winning team
		if gameMarginOfVictory <= MAX_CLOSE_GAME_MV:
			winningTeam.closeWonGames += 1.0
		
		winningTeam.totalPointsFor 		+= entry[3]
		winningTeam.totalPointsAgainst 		+= entry[5]
		winningTeam.numVictories 		+= 1.0
		winningTeam.averageMarginOfVictory 	+= gameMarginOfVictory
		
		# Aggregate stats for the losing team
		if gameMarginOfVictory <= MAX_CLOSE_GAME_MV:
			winningTeam.closeWonGames += 1.0
		
		losingTeam.totalPointsFor 		+= entry[5]
		losingTeam.totalPointsAgainst 		+= entry[3]
		losingTeam.numberOfLosses 		+= 1.0
		losingTeam.averageMarginOfVictory 	+= -1.0 * gameMarginOfVictory

# This function calculates all statistics except RPI
def calculateSimpleDerivativeStatistics(teams):

	for team in teams.keys():
		# Calculate total number of games played
		gamesPlayed = teams[team].numVictories + teams[team].numberOfLosses

		if gamesPlayed == 0: continue 

		# Calculate winning percentage
		teams[team].winningPercentage = teams[team].numVictories / gamesPlayed

		# Finish calculating average Margin Of victory
		teams[team].averageMarginOfVictory /= gamesPlayed

		# Pythagorean Expectation
		peNumerator = pow(teams[team].totalPointsFor, 13.91)
		peDenominator = pow(teams[team].totalPointsFor, 13.91) + pow(teams[team].totalPointsAgainst, 13.91)

		teams[team].pythagoreanExpectation =  peNumerator / peDenominator


# Calculate RPI for each team
def calculateRPI(teams):
	for team in teams.keys():
		# Calculate OWP
		OWP = 0.0
		OOWP = 0.0
		OLen = len(teams[team].opponentList)
		OOLen = 0
		
		# Start summation for OWP and OOWP
		for opponent in teams[team].opponentList:
			OWP += teams[opponent].winningPercentage
			OOLen += len(teams[opponent].opponentList)
			for opponentOpponent in teams[opponent].opponentList:
				OOWP += teams[opponent].winningPercentage
	
		# Return something only if the team had opponents
		if OLen != 0:
			teams[team].ratingPercentageIndex += 0.5 * (OWP / OLen)
			teams[team].ratingPercentageIndex += 0.25 * (OOWP / OOLen)
			teams[team].ratingPercentageIndex += 0.25 * teams[team].winningPercentage
		
		# Else return "NA"		
		else:			
			teams[team].ratingPercentageIndex = "NA" 

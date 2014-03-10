import pickle 
import os
import matplotlib.pyplot as plt
import math
from team import *
from stats import *

IGNORE_TEAMS = [501,609,656,856]


# Parse out the regular season csv file, cast attributes appropriately so that later
# when we are creating indices, these don't have to get cast for every calculation
def parse_season_csv(filename):
	lines = [];
	csvFile = open(filename, "rt");
	header = True
	while True:
		line = csvFile.readline();
		if not line:
			break;
		if not header: 
			record = line.split(',')
			record[2] = int(record[2])
			record[3] = int(record[3])
			record[4] = int(record[4])
			record[5] = int(record[5])		
			lines.append(record);
		else: header = False
	csvFile.close();
	return lines;

# Parse out the team file
def parse_team_csv(filename):
	lines = [];
	csvFile = open(filename, "rt");
	header = True
	while True:
		line = csvFile.readline();
		if not line:
			break;
		if not header:
			record = line.split(',')	
			record[1] = record[1].replace("\r\n","")	
			lines.append(record);
		else: header = False
	csvFile.close();
	return lines;

# Print out a list representing a csvFile line by line
def print_csv(csvFile):
	for line in range(len(csvFile)):
		print csvFile[line];


def generateOpponentList(season, teams):
	for entry in season:
		winningTeamId = entry[2]
		losingTeamId = entry[4]

		teams[winningTeamId].opponentList.append(losingTeamId)
		teams[losingTeamId].opponentList.append(winningTeamId)


# Create the teams dictionary, iniitally has the winning percentage
def populateTeams(teams_file, seasons):
	teams = {}
	for team in teams_file:
		teamId = int(team[0])
		teamName = team[1]
		teams[teamId] = Team(teamName, teamId)
	return teams

def main():
	if os.path.exists("data/teams.p"):
		teams = pickle.load( open( "data/teams.p", "rb" ) )
		print "Total number of teams : ",len(teams)

		if not os.path.exists("data/team_aggregate.csv"):
			f = open('data/team_aggregate.csv', 'w')
		
			for team in teams.keys(): 
				if team in IGNORE_TEAMS: continue
				teamEntry = ""
				teamEntry += str(teams[team].idNum) + ','
				teamEntry += teams[team].name + ','
				teamEntry += str(teams[team].ratingPercentageIndex) + ','
				teamEntry += str(teams[team].winningPercentage) + ','
				teamEntry += str(teams[team].pythagoreanExpectation) + ','
				teamEntry += str(teams[team].closeWonGames) + ','
				teamEntry += str(teams[team].totalPointsFor) + ','
				teamEntry += str(teams[team].totalPointsAgainst) + ','
				teamEntry += str(teams[team].numVictories) + ','
				teamEntry += str(teams[team].numberOfLosses) + ','
				teamEntry += str(teams[team].averageMarginOfVictory) + '\r\n'
				f.write(teamEntry)

			f.close()
	else:
		print "Pre-baked stats not found, baking... "
		# Should we calculate per season \ team or just per team?
		# The former would give us ~2600 virtual teams
		regular_season_results = parse_season_csv("data/regular_season_results.csv");
		teams_file = parse_team_csv("data/teams.csv")

		seasonsCount = {}
		for season in regular_season_results:
			if season[0] in seasonsCount:
				seasonsCount[season[0]] += 1.0
			else: seasonsCount[season[0]] = 0.0
		for season in seasonsCount.keys():
			print season + " games : ",seasonsCount[season]

		teams = populateTeams(teams_file, regular_season_results)

		generateOpponentList(regular_season_results, teams)

		calculateTeamStatistics(teams, regular_season_results)

		calculateSimpleDerivativeStatistics(teams)

		calculateRPI(teams)
		
		# Get rid of any team with "NA" for rating percentage index
		for team in teams.keys():
			if teams[team].ratingPercentageIndex == "NA":
				print "Deleting team ",team, " which has 'NA' for its RPI."
				del teams[team]

	


		print "Storing as teams.p... "

		pickle.dump(teams, open( "data/teams.p", "wb" ) )
main()

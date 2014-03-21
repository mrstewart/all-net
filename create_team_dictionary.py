from classes import *
import pickle

TEAMS_FILE = "contest_data/teams.csv"

# Parse out the team file
teams = {}
csvFile = open(TEAMS_FILE, "rt")
header = True
while True:
	line = csvFile.readline();
	if not line:
		break
	if not header:
		record = line.split(',')	
		teamName = record[1].replace("\r\n","")	
		teamId = int(record[0])
		team = Team(teamName, teamId)
		teams[teamId] = team 
	else: header = False
csvFile.close()

pickle.dump(teams, open( "teams.p", "wb" ) )





# create_team_dictionary.py
#
# This file reads through the teams csv file and construct
# a pickle file with Team objects. These team objects will be
# fleshed out further, later.
from classes import *
from constants import *
import pickle


teams = {}

teams_csv_file = open(TEAMS_FILE, "rt")

header = True
while True:
	line = teams_csv_file.readline()
	if not line:
		break
	if not header:
		record = line.split(',')	
		teamName = record[1].replace("\r\n","")	
		teamId = int(record[0])
		teams[teamId] = Team(teamName, teamId)
	else: header = False
teams_csv_file.close()

pickle.dump(teams, open( TEAMS_DATA_PATH, "wb" ) )





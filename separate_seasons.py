# season	daynum	wteam	wscore	lteam	lscore	numot
# season	daynum	wteam	wscore	lteam	lscore
import pickle
from classes import *

tournaments = {}

lines = []
csvFile = open('contest_data/tourney_results.csv', "rt")
header = True
while True:
	line = csvFile.readline()
	if not line:
		break
	if not header:
		record = line.split(',')

		season = record[0]
		if season in tournaments:
			record[2] = int(record[2])
			record[4] = int(record[4])
			game = TourneyGame(record[2], record[4])

			tournaments[season].append(game)
		else:
			tournaments[season] = []

			record[2] = int(record[2])
			record[4] = int(record[4])
			game = TourneyGame(record[2], record[4])

			tournaments[season].append(game)
			
		lines.append(record);
	else: header = False
csvFile.close()

for season in tournaments.keys():
	pickle.dump(tournaments[season], open( "chopped_data/" + season + "_tourney_results.p", "wb" ) )

regular_season = {}
lines = []
csvFile = open('contest_data/regular_season_results.csv', "rt")
header = True
while True:
	line = csvFile.readline()
	if not line:
		break
	if not header:
		record = line.split(',')

		season = record[0]

		if season in regular_season:
			winningTeam = int(record[2])
			winningScore = int(record[3])
			losingTeam = int(record[4])
			losingScore = int(record[5])
			game = RegularGame(winningTeam, losingTeam, winningScore, losingScore)
			
			regular_season[season].append(game)
		else:
			regular_season[season] = []

			winningTeam = int(record[2])
			winningScore = int(record[3])
			losingTeam = int(record[4])
			losingScore = int(record[5])
			game = RegularGame(winningTeam, losingTeam, winningScore, losingScore)

			regular_season[season].append(game)
			
		lines.append(record);
	else: header = False
csvFile.close()

for season in regular_season.keys():
	pickle.dump(regular_season[season], open( "chopped_data/" + season + "_regular_season_results.p", "wb" ) )


# season	seed	team
tourney_seeds = {}
lines = []
csvFile = open('contest_data/tourney_seeds.csv', "rt")
header = True
while True:
	line = csvFile.readline()
	if not line:
		break
	if not header:
		record = line.split(',')

		season = record[0]

		if season in tourney_seeds:
			seed = record[1]
			team = int(record[2])
			tourney_seeds[season][team] = seed
		else:
			tourney_seeds[season] = {}
			seed = record[1]
			team = int(record[2])
			tourney_seeds[season][team] = seed
			
		lines.append(record)
	else: header = False
csvFile.close()
	
for season in regular_season.keys():
	pickle.dump(tourney_seeds[season], open( "chopped_data/" + season + "_tourney_seeds.p", "wb" ) )

# season	slot	strongseed	weakseed
tourney_slots = {}
lines = []
csvFile = open('contest_data/tourney_slots.csv', "rt")
header = True
while True:
	line = csvFile.readline()
	if not line:
		break
	if not header:
		record = line.split(',')

		season = record[0]

		if season in tourney_slots:
			slot = record[1]
			strongseed = record[2]
			weakseed = record[3]
			tourneySlot = TourneySlot(slot, strongseed, weakseed)
			tourney_slots[season].append(tourneySlot)
		else:
			tourney_slots[season] = []
			slot = record[1]
			strongseed = record[2]
			weakseed = record[3]
			tourneySlot = TourneySlot(slot, strongseed, weakseed)
			tourney_slots[season].append(tourneySlot)
			
		lines.append(record)
	else: header = False
csvFile.close()
	
for season in regular_season.keys():
	pickle.dump(tourney_seeds[season], open( "chopped_data/" + season + "_tourney_slots.p", "wb" ) )

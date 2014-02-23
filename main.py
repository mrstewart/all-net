class Team:
	idNum = 0 	# Id of the team
	name = ""	# name of the team
	RPI = 0.0	# Rating percentage index of team
	MV = 0.0	# Margin of victory of the team
	WP = 0.0	# Winning percentage of the team

	def __init__(self, name, WP, idNum):
		self.name = name
		self.idNum = idNum
		self.WP = WP

def calculateWinningPercentage(idNum, season):
	# Get winning percentage for id by going through entire season
	# and adding up wins and losses
	WP = 0.0
	numberOfWins = 0.0
	numberOfLosses = 0.0
	for entry in season:
		winningTeamId = entry[2]
		losingTeamId = entry[4]

		if idNum == winningTeamId: numberOfWins += 1.0
		if idNum == losingTeamId: numberOfLosses += 1.0
	
	if (numberOfWins + numberOfLosses) != 0: WP = numberOfWins / (numberOfWins + numberOfLosses)
	else: WP = 0
	return WP

def calculateRPI(team, season, teams):

		# Get list of all opponents in the season, counting duplicates
		opponentIds = []
		for entry in season:
			winningTeamId = entry[2]
			losingTeamId = entry[3]

			if team.idNum != winningTeamId and idNum == losingTeamId:
				opponentIds.append(winningTeamId)

			if team.idNum != losingTeamId and idNum == winningTeamId:
				opponentIds.append(losingTeamId)
		
		# For each opoonent get opponents
		opponentOpponentIds = []
		for opponent in opponentIds:
			for entry in season:
			# Get a list of all of their opponents, counting duplicates
				winningTeamId = entry[2]
				losingTeamId = entry[3]
				
				if opponent != winningTeamId and opponent == losingTeamId:
					opponentOpponentIds.append(winningTeamId)
				
				if opponent != losingTeamId and opponent == winningTeamId:
					opponentOpponentIds.append(losingteamId)
				
		# Get winning percentages for all opponents and oo's
		OWP = 0.0
		for opponent in opponentIds:
			OWP += teams.get(opponent).WP

		OWP /= len(opponentIds)


		OOWP = 0.0
		for opponentOpponent in opponentOpponentIds:
			OOWP += teams.get(opponentOpponent).WP

		OOWP /= len(opponentOpponentIds)

		# Calculate RPI
		RPI = 0.25 * WP + 0.5 * OWP + 0.25 * OOWP

		return RPI
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
			record[4] = int(record[4])		
			lines.append(record);
		else: header = False
	csvFile.close();
	return lines;

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
			lines.append(record);
		else: header = False
	csvFile.close();
	return lines;

def print_csv(csvFile):
	for line in range(len(csvFile)):
		print csvFile[line];

def main():
	teamDictionary = {}
	regular_season_results = parse_season_csv("data/regular_season_results.csv");
	teams_file = parse_team_csv("data/teams.csv")
	teams = {}
	for team in teams_file:
		teamId = int(team[0])
		WP = calculateWinningPercentage(teamId, regular_season_results)
		newTeam = Team(team[1], WP, teamId)
		teams[teamId] = newTeam

	print teams[506].WP

main()

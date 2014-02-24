class Team:
	idNum = 0 	# Id of the team
	name = ""	# name of the team
	RPI = 0.0	# Rating percentage index of team
	MV = 0.0	# Margin of victory of the team
	WP = 0.0	# Winning percentage of the team
	opponentList = [] # List of this team's opponents
	gamesInTheRegularSeason = 0
	def __init__(self, name, WP, MV, idNum):
		self.name = name
		self.idNum = idNum
		self.WP = WP
		self.MV = MV
		self.opponentList = []

# Calculate the winning percentage for a team
def calculateWinningPercentage(idNum, season):

	# Get winning percentage for id by going through entire season
	# and adding up wins and losses
	WP = 0.0
	numberOfWins = 0.0
	numberOfLosses = 0.0
	marginOfVictory = 0.0
	numVictories = 0
	for entry in season:
		winningTeamId = entry[2]
		losingTeamId = entry[4]

		if idNum == winningTeamId: 
			numberOfWins += 1.0
			numVictories += 1
			marginOfVictory = entry[3] - entry[5]
			numberOfWins += 1.0
		if idNum == losingTeamId: numberOfLosses += 1.0
	
	if (numberOfWins + numberOfLosses) != 0: WP = numberOfWins / (numberOfWins + numberOfLosses)
	else: WP = 0
	return [WP, marginOfVictory]

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
			OWP += teams[opponent].WP
			OOLen += len(teams[opponent].opponentList)
			for opponentOpponent in teams[opponent].opponentList:
				OOWP += teams[opponent].WP
	
		# Return something only if the team had opponents
		if OLen != 0:
			teams[team].RPI += 0.5 * (OWP / OLen)
			teams[team].RPI += 0.25 * (OOWP / OOLen)
			teams[team].RPI += 0.25 * teams[team].WP
		
		# Else return "NA"		
		else:			
			teams[team].RPI = "NA" 

# Create the teams dictionary, iniitally has the winning percentage
def populateTeams(teams_file, seasons):
	teams = {}
	for team in teams_file:
		teamId = int(team[0])
		WPMV = calculateWinningPercentage(teamId, seasons)
		newTeam = Team(team[1], WPMV[0], WPMV[1], teamId)
		teams[teamId] = newTeam
	return teams

def main():
	regular_season_results = parse_season_csv("data/regular_season_results.csv");
	teams_file = parse_team_csv("data/teams.csv")

	teams = populateTeams(teams_file, regular_season_results)

	generateOpponentList(regular_season_results, teams)

	calculateRPI(teams)

main()

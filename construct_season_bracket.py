from classes import *
from constants import *
import pickle

def determineWinner(slot, tourneyResults):
	for tourneyGame in tourneyResults:
		if (tourneyGame.winningTeam == slot._highId or tourneyGame.losingTeam == slot._highId) and (tourneyGame.winningTeam == slot._lowId or tourneyGame.losingTeam == slot._lowId):
			if tourneyGame.winningTeam == slot._highId:
				return slot._highId
			else:
				return slot._lowId

def getLeafBrackets(rootBracket):
	if rootBracket == None:
		return None
	elif rootBracket._lChild == None and rootBracket._rChild == None:
		return rootBracket
	else:
		childBrackets = []
		leftLeafBrackets = getLeafBrackets(rootBracket._lChild)
		rightLeafBrackets = getLeafBrackets(rootBracket._rChild)	
		
		if leftLeafBrackets != None:
			if type(leftLeafBrackets) == list:
				childBrackets.extend(leftLeafBrackets)
			else: childBrackets.append(leftLeafBrackets)
		
		if rightLeafBrackets != None:
			if type(rightLeafBrackets) == list:
				childBrackets.extend(rightLeafBrackets)
			else: 
				childBrackets.append(rightLeafBrackets)
		
		# We want brackets that include one play in game as child brackets
		if leftLeafBrackets == None or rightLeafBrackets == None:
			childBrackets.append(rootBracket)

		return childBrackets

def connectBrackets(season):
	for childSlot in season:
		for parentSlot in season:
			parentHighSeed = parentSlot._highSeed
			parentLowSeed = parentSlot._lowSeed
			childName = childSlot._name
			if childName == parentHighSeed or childName == parentLowSeed:
				childSlot._nextBracket = parentSlot
				if childName == parentHighSeed: 
					parentSlot._lChild = childSlot
				else:
					parentSlot._rChild = childSlot

def fillOutBracket(rootNode, season_results):
	if rootNode == None: return None
	elif rootNode._lChild == None and rootNode._rChild == None:
		rootNode._winnerId = determineWinner(rootNode, season_results)
		return rootNode._winnerId
	else:
		if rootNode._highId == 0:
			rootNode._highId = fillOutBracket(rootNode._lChild, season_results)
		
		if rootNode._lowId == 0:
			rootNode._lowId = fillOutBracket(rootNode._rChild, season_results)
		
		rootNode._winnerId = determineWinner(rootNode, season_results)
		return rootNode._winnerId
	

def generateRecord(rootNode, teams):
	record = []
	queue = []
	queue.append(rootNode)
	
	while True:
		curNode = queue.pop(0)
		record.append(curNode)
		
		if curNode._lChild != None: queue.append(curNode._lChild)
		if curNode._rChild != None: queue.append(curNode._rChild)
		
		if len(record) == 63: break

	return record
teams = pickle.load( open( "teams.p", "rb" ) )
tourney_slots = open('contest_data/tourney_slots.csv', "rt")
header = True
seasons = {}
season_championship_nodes = {}
while True:
	line = tourney_slots.readline()
	if not line:
		break
	if not header:
		record = line.split(',')

		season = record[0]
		if season not in seasons:
			seasons[season] = []
		name = record[1]

		strongseed = record[2]
		weakseed = record[3].replace("\r\n","")


		slot = Slot(name,strongseed,weakseed)
		
		if name == "R6CH": season_championship_nodes[season] = slot

		seasons[season].append(slot)

	else: header = False
tourney_slots.close()

season_leafBrackets = {}
for season in seasons.keys():
	connectBrackets(seasons[season])
	season_leafBrackets[season] = getLeafBrackets(season_championship_nodes[season])
# Get victors of play in game and substitute winners for the seeds

#season	seed	team
tourney_seeds = open('contest_data/tourney_seeds.csv', "rt")
header = True

seeds = {}

while True:
	line = tourney_seeds.readline()
	if not line:
		break
	if not header:
		record = line.split(',')

		season = record[0]
		if season not in seeds:
			seeds[season] = {}
		seed = record[1]
		team = int(record[2])
		
		seeds[season][seed] = team 
	else: header = False
tourney_seeds.close()

tourney_results = {}
for season in seasons.keys():
	tourney_results[season]=pickle.load(open("chopped_data/"+season+"_tourney_results.p", "rb"))

# Fill out leaf brackets
for season in season_leafBrackets.keys():
	for leafbracket in season_leafBrackets[season]:
		highSeed = leafbracket._highSeed
		lowSeed = leafbracket._lowSeed
		if highSeed in seeds[season]:
			leafbracket._highId = seeds[season][highSeed]
		if lowSeed in seeds[season]:
			leafbracket._lowId = seeds[season][lowSeed]
		
for season in tourney_results.keys():
	season_results = tourney_results[season]
	for slot in season_leafBrackets[season]:
		slot._winnerId = determineWinner(slot,tourney_results[season])

for season in season_championship_nodes.keys():
	team = teams[fillOutBracket(season_championship_nodes[season], tourney_results[season])].name

training_data = open('training_data.csv', 'w')

bracketRecord = generateRecord(season_championship_nodes["A"],teams)

# Create header
headerStr = ""
for bracket in range(len(bracketRecord) - 1):
	headerStr += bracketRecord[bracket]._name + "_RPI,"
	headerStr += bracketRecord[bracket]._name + "_PYTH,"
	headerStr += bracketRecord[bracket]._name + "_CWG,"
	headerStr += bracketRecord[bracket]._name + "_AVG,"
	

headerStr += bracketRecord[len(bracketRecord) - 1]._name + "_RPI,"
headerStr += bracketRecord[len(bracketRecord) - 1]._name + "_PYTH,"
headerStr += bracketRecord[len(bracketRecord) - 1]._name + "_CWG,"
headerStr += bracketRecord[len(bracketRecord) - 1]._name + "_AVG\n"

training_data.write(headerStr)

for season in SEASONS_TO_PICK_FROM:
	bracketRecord = generateRecord(season_championship_nodes[season],teams)
	bracketRecordRaw = ""

	for bracket in range(len(bracketRecord) - 1):
		team = teams[bracketRecord[bracket]._winnerId]

		rpi = str(team.ratingPercentageIndex)
		pyth = str(team.pythagoreanExpectation)
		cwg = str(team.closeWonGames)
		avg = str(team.averageMarginOfVictory)

		bracketRecordRaw += rpi + "," + pyth + "," + cwg + "," + avg + ","
	
	
	team = teams[bracketRecord[len(bracketRecord) - 1]._winnerId]

	rpi = str(team.ratingPercentageIndex)
	pyth = str(team.pythagoreanExpectation)
	cwg = str(team.closeWonGames)
	avg = str(team.averageMarginOfVictory)

	bracketRecordRaw += rpi + "," + pyth + "," + cwg + "," + avg + "\n"
	training_data.write(bracketRecordRaw)

training_data.close()

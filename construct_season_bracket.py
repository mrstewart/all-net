from classes import *
from constants import *
import pickle

STANDARD_NUMBER_OF_GAMES = 63	# These should be different only if debugging
NUMBER_OF_GAMES_TO_EXPORT = STANDARD_NUMBER_OF_GAMES	#

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
		
		if len(record) == NUMBER_OF_GAMES_TO_EXPORT: break

	return record

def createArffValueEnumeration(numberOfValues):
	values = "{"
	for i in range(numberOfValues - 1):
		values += str(i) + ","
	values += str(numberOfValues - 1) + "}"

	return values
def writeHeader(training_data):
	training_data.write("@relation training_data\n")
	
	rpiBinValues = createArffValueEnumeration(RPI_BINS)
	pythBinValues = createArffValueEnumeration(PYTH_BINS)
	cwgBinValues = createArffValueEnumeration(CG_BINS)
	avgBinValues = createArffValueEnumeration(AVGMV_BINS)

	training_data.write("@attribute RPI0 " + rpiBinValues +"\n")
	training_data.write("@attribute PYTH0 " + pythBinValues + "\n")
	training_data.write("@attribute CWG0 " + cwgBinValues + "\n")
	training_data.write("@attribute AVG0 " + avgBinValues + "\n")
	training_data.write("@attribute RPI1 " + rpiBinValues +"\n")
	training_data.write("@attribute PYTH1 " + pythBinValues + "\n")
	training_data.write("@attribute CWG1 " + cwgBinValues + "\n")
	training_data.write("@attribute AVG1 " + avgBinValues + "\n")
	training_data.write("@attribute W {HIGH_SEED, LOW_SEED}\n")

def writeOutData(training_data, season_championship_nodes, teams):
	training_data.write("@data\n")
	for season in SEASONS_TO_PICK_FROM:
		bracketRecord = generateRecord(season_championship_nodes[season],teams)

		# In WEKA, for the K2 algorithm, nodes to be in such an order that all a nodes
		# parents are to its 'left'. The raw bracket record comes out such that the
		# championship round is at the leftmost spot, but we want it at the rightmost spot
		bracketRecord.reverse()



		for bracket in range(len(bracketRecord)):
			bracketRecordRaw = ""
			winnerId = bracketRecord[bracket]._winnerId
			low = teams[bracketRecord[bracket]._lowId]
			high = teams[bracketRecord[bracket]._highId]

			winBit = "HIGH_SEED" if bracketRecord[bracket]._highId == winnerId else "LOW_SEED"

			rpi0 = str(high.ratingPercentageIndex)
			pyth0 = str(high.pythagoreanExpectation)
			cwg0 = str(high.closeWonGames)
			avg0 = str(high.averageMarginOfVictory)

			rpi1 = str(low.ratingPercentageIndex)
			pyth1 = str(low.pythagoreanExpectation)
			cwg1 = str(low.closeWonGames)
			avg1 = str(low.averageMarginOfVictory)

			training_data.write(rpi0 + "," + pyth0 + "," + cwg0 + "," + avg0 + ",")
			training_data.write(rpi1 + "," + pyth1 + "," + cwg1 + "," + avg1 + ",")
			training_data.write(winBit + "\n")

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

training_data = open('training_data.arff', 'w')

writeHeader(training_data)
writeOutData(training_data, season_championship_nodes, teams)

training_data.close()


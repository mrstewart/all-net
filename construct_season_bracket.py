from classes import *
from constants import *
import pickle
import subprocess
import sys

# Uses tourney results to figure out a past winner for a particular slot, returns the team id of
# the winner
def determineWinnerWithResults(slot, tourneyResults):
	for tourneyGame in tourneyResults:
		if (tourneyGame.winningTeam == slot._highId or tourneyGame.losingTeam == slot._highId) and (tourneyGame.winningTeam == slot._lowId or tourneyGame.losingTeam == slot._lowId):
			if tourneyGame.winningTeam == slot._highId:
				return slot._highId
			else:
				return slot._lowId

# Uses WEKA to figure out a past winner for a particular slot, returns the team id of
# the winner
def determineWinnerWithWEKA(slot, teams):
	if slot._highId == 0 or slot._lowId == 0: return 0
		
	# Get the team of the high id
	high = teams[slot._highId]
	# Get the team of the low id
	low = teams[slot._lowId]

	# Save matchup to arff file
	matchup_data = open('matchup_data.arff', 'w')

	writeHeader(matchup_data)

	matchup_data.write("@data\n")
	rpi0 = str(high.ratingPercentageIndex)
	pyth0 = str(high.pythagoreanExpectation)
	cwg0 = str(high.closeWonGames)
	avg0 = str(high.averageMarginOfVictory)

	rpi1 = str(low.ratingPercentageIndex)
	pyth1 = str(low.pythagoreanExpectation)
	cwg1 = str(low.closeWonGames)
	avg1 = str(low.averageMarginOfVictory)

	matchup_data.write(rpi0 + "," + pyth0 + "," + cwg0 + "," + avg0 + ",")
	matchup_data.write(rpi1 + "," + pyth1 + "," + cwg1 + "," + avg1 + ",")
	matchup_data.write("HIGH_SEED" + "\n")

	matchup_data.close()

	# Ask WEKA to classify arff file
	results = subprocess.check_output(["java","-Xmx1024m","weka.classifiers.bayes.BayesNet","-T","matchup_data.arff","-l","round_model.model","-p","0"])
	
	# Find winner from results
	if results[103] == "H": return slot._highId
	else: return slot._lowId


# Get leaf brackets in bracket tree
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

# Connect the brackets in a particular season, results in a binary tree being constructed
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

# Fills out the bracket by looking at the season results
def fillOutBracket(rootNode, teams, tourney_results, useResults):
	# Base case, this node doesn't exist return
	if rootNode == None: return None
	
	# This node does not have children, it is a 'leaf' bracket, determine its winner
	elif rootNode._lChild == None and rootNode._rChild == None:
		if useResults:
			rootNode._winnerId = determineWinnerWithResults(rootNode, tourney_results)
		else: 
			rootNode._winnerId = determineWinnerWithWEKA(rootNode, teams)
		return rootNode._winnerId

	# Determine the winner for this bracket
	else:
		# If there is no winner assigned, fill out the bracket by traversing child brackets
		if rootNode._highId == 0:
			if useResults: 
				rootNode._highId = fillOutBracket(rootNode._lChild, teams, tourney_results, useResults)
			else:
				rootNode._highId = fillOutBracket(rootNode._lChild, teams, None, useResults)
		# See above
		if rootNode._lowId == 0:
			if useResults:
				rootNode._lowId = fillOutBracket(rootNode._rChild, teams, tourney_results, useResults)
			else:
				rootNode._lowId = fillOutBracket(rootNode._rChild, teams, None, useResults)
		# Determine winner after finding high and low seeds
		if useResults: 
			rootNode._winnerId = determineWinnerWithResults(rootNode, tourney_results)
		else: 
			rootNode._winnerId = determineWinnerWithWEKA(rootNode, teams)
		return rootNode._winnerId
	
# Generate a record for an entire bracket
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

# Create an enumeration formatted to fit the ARFF value enumeration format
# {<value0>, <value1>,..., <valueN>}
def createArffValueEnumeration(numberOfValues):
	values = "{"
	for i in range(numberOfValues - 1):
		values += str(i) + ","
	values += str(numberOfValues - 1) + "}"

	return values

# Write the header of the arff file
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

# Write the data of the arff file
def writeOutARFFData(training_data, season_championship_nodes, teams):
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

# Write out training data
def writeOutData(season_championship_nodes, teams, creatingTestData, creatingTrainingData):
	dataFileName = ""	
	if creatingTrainingData: dataFileName = 'training_data.arff'
	else: dataFileName = 'test_data.arff'

	data = open(dataFileName, 'w')

	writeHeader(data)
	writeOutARFFData(data, season_championship_nodes, teams)

	data.close()



creatingTrainingData = True if sys.argv[1] == 'training' else False
creatingTestData = True if sys.argv[1] == 'test' else False
classifyingData = True if sys.argv[1] == 'classify' else False


teams = pickle.load( open( TEAMS_DATA_PATH, "rb" ) )


# Read in tourney slots data
tourney_slots = open(TOURNEY_SLOTS_FILE, "rt")
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

# Construct bracket structure from tourney slots data
season_leafBrackets = {}
for season in seasons.keys():
	connectBrackets(seasons[season])
	season_leafBrackets[season] = getLeafBrackets(season_championship_nodes[season])


# Get the tourney seeds
tourney_seeds = open(TOURNEY_SEEDS_FILE, "rt")
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
if creatingTrainingData or creatingTestData:
	for season in SEASONS_TO_PICK_FROM:
		tourney_results[season]=pickle.load(open("chopped_data/"+season+"_tourney_results.p", "rb"))

# Fill out leaf brackets
for season in SEASONS_TO_PICK_FROM:
	for leafbracket in season_leafBrackets[season]:
		highSeed = leafbracket._highSeed
		lowSeed = leafbracket._lowSeed
		if highSeed in seeds[season]:
			leafbracket._highId = seeds[season][highSeed]
		if lowSeed in seeds[season]:
			leafbracket._lowId = seeds[season][lowSeed]
		
for season in SEASONS_TO_PICK_FROM:
	for slot in season_leafBrackets[season]:
		if creatingTrainingData or creatingTestData:
			slot._winnerId = determineWinnerWithResults(slot, tourney_results[season])
		else:
			slot._winnerId = determineWinnerWithWEKA(slot,teams)

for season in SEASONS_TO_PICK_FROM:
	if creatingTrainingData or creatingTestData:
		team = teams[fillOutBracket(season_championship_nodes[season], teams, tourney_results[season], True)].name
	else:
		team = teams[fillOutBracket(season_championship_nodes[season], teams, None, False)].name
	print season + " " + team

if not classifyingData:
	writeOutData(season_championship_nodes, teams, creatingTestData, creatingTrainingData)


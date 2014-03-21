class Season:
	_slots = []

	def __init__(self):
		self._slots = slots

class Slot:
	_name = ""
	_highSeed = ""
	_lowSeed = ""
	_highId = 0
	_lowId = 0
	_winnerId = 0
	_nextBrack = None
	_lChild = None
	_rChild = None

	def __init__(self,name,highSeed,lowSeed):
		self._name = name
		self._highSeed = highSeed
		self._lowSeed = lowSeed

class Bracket:
	_slot = ""
	_highseed = ""
	_highseedTeamId = 0
	_lowseed = ""
	_lowseedTeamId = 0
	_nextBracket = None

	def __init__(self,bracketSlot,bracketHighSeed,bracketLowSeed,nextBracket):
		self._slot = bracketSlot
		self._highseed = bracketHighSeed
		self._lowseed = bracketLowSeed
		self._nextBracket = nextBracket


class TourneyGame:
	winningTeam = 0
	losingTeam = 0
	def __init__(self, winningTeam, losingTeam):
		self.winningTeam = winningTeam
		self.losingTeam = losingTeam

	def __str__(self):
		return str(self.winningTeam) + " " + str(self.losingTeam)

class RegularGame:
	winningTeam = 0
	losingTeam = 0
	winningScore = 0
	losingScore = 0
	def __init__(self, winningTeam, losingTeam, winningScore, losingScore):
		self.winningTeam = winningTeam
		self.losingTeam = losingTeam
		self.winningScore = winningScore
		self.losingScore = losingScore

	def __str__(self):
		return str(self.winningTeam) + " " + str(self.losingTeam) + " " + str(self.winningScore) + " " + str(self.losingScore)

class TourneySlot:
	slot = ""
	strongseed = ""
	weakseed = ""
	def __init__(self, slot, strongseed, weakseed):
		self.slot = slot
		self.strongseed = strongseed
		self.weakseed = weakseed

	def __str__(self):
		return str(self.slot) + " " + str(self.strongseed) + " " + str(self.weakseed)


class Team:
	# Id of the team
	idNum = 0 		
	
	# Name of the team	
	name = ""		

	# Ids of opponent teams
	opponentList = []	

	# Rating percentage index of team
	ratingPercentageIndex = 0.0	
	
	# Winning percentage of the team
	winningPercentage = 0.0		

	# Pythagoran expectation
	pythagoreanExpectation = 0.0	

	# Calculate Win % Close games
	closeWonGames = 0.0

	# Calculate total points for a season 
	# (Points Per Game, Pythagorean Expectation)
	totalPointsFor = 0.0

	# Calculate total points against in a season
	# (Pythogorean Expectation)
	totalPointsAgainst = 0.0

	# Calculate total wins in a season
	# (Rating Percentage Index, Margin of Victory, Points Per Game, Winning Percentage)
	numVictories = 0.0

	# Calculate total losses in a season
	# (Rating Percentage Index, Margin of Victory, Points Per Game, Winning Percentage)
	numberOfLosses = 0.0

	# Average of all margins of victory
	averageMarginOfVictory = 0.0



	def __init__(self, name, idNum):
		self.name = name
		self.idNum = idNum
		self.opponentList = []

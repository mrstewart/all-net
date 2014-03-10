class Team:
	idNum = 0 			# Id of the team
	name = ""			# name of the team
	ratingPercentageIndex = 0.0	# Rating percentage index of team
	winningPercentage = 0.0		# Winning percentage of the team
	pythagoreanExpectation = 0.0	# Pythagoran expectation

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

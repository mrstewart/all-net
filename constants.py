TEAMS_FILE = "contest_data/teams.csv"
TOURNEY_SLOTS_FILE = 'contest_data/tourney_slots.csv'
TOURNEY_SEEDS_FILE = 'contest_data/tourney_seeds.csv'
REGULAR_SEASON_FILENAME = "regular_season_results"
TEAMS_DATA_PATH = "teams.p"

#IGNORE_TEAMS = [501,609,656,856,691,697] # 691 and 697 do not appear in the selected seasons

#SEASONS_TO_PICK_FROM = ["A","B","C","D","G","H","I","J","M","N","O"]
SEASONS_TO_PICK_FROM = ["E","F","K","L","P","Q","R"]

MAX_CLOSE_GAME_MV = 7 	# The maximum margin of victory for a close game. 
		 	# Equivalent to: 
			# 	2 3-point shots and a foul shot
			#	3 2-point shots and a foul shot
			#	2 2-point shots and a 3-point shot

STANDARD_NUMBER_OF_GAMES = 63	# These should be different only if debugging
NUMBER_OF_GAMES_TO_EXPORT = STANDARD_NUMBER_OF_GAMES	#

RPI_BINS = 30
WP_BINS = 30
PYTH_BINS = 30
CG_BINS = 30
TPF_BINS = 30
TPA_BINS = 30
NV_BINS = 30
NL_BINS = 30
AVGMV_BINS = 30

TESTING_BINS = True
EXPORT_WITH_HEADINGS = True
EXPORT_ID = True
EXPORT_NAME = False
EXPORT_RPI = True
EXPORT_WP = True
EXPORT_PYTH = True
EXPORT_CWG = True
EXPORT_TPF = True
EXPORT_TPA = True
EXPORT_NV = True
EXPORT_NL = True
EXPORT_AVGMV = True

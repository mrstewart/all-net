

def parse_csv(filename):
	lines = [];
	csvFile = open(filename, "rt");
	while True:
		line = csvFile.readline();
		if not line:
			break;
		lines.append(line);
	csvFile.close();
	return lines;

def print_csv(csvFile):
	for line in range(len(csvFile)):
		print csvFile[line];

def main():
	csvFile = parse_csv("regular_season_results.csv");
	print_csv(csvFile);

main()

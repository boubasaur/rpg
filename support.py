from csv import reader

def import_csv_layout(path):
	floorblocks = []
	with open(path) as level_map:
		layout = reader(level_map,delimiter = ',')
		for row in layout:
			floorblocks.append(list(row))
		return floorblocks



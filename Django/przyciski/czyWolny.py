def checkLinesAvaliability(trainNumber, start, destination, trainList):

	route = [[1,1,1,1], [1,1,1,1], [1,1,1,1], [1,1,1,1]]  # na poczatku wszystkie tory wolne

	for t in trainList:
		route[t[0]][t[1]] = 0  # zmiana na 0 jesli na jakims miejsu jest pociag z listy

	lines = []  # lista interesujacego nas toru

	end = start[0]  #zaczynamy od sektoru startu
	while (end < destination[0]):  # i idziemy do sektora stopu
		end = end + 1
		lines.append(route[end][start[1]]) # dodajac do listy dostenosc danych sektorow

	return (lines) # zwrocona lista
def checkLinesAvaliability(trainNumber, start, destination, train1, train2):
	self.part_left, self.part_up, self.part_down, self.part_right = 1; #wolne

	if(start == "Wrzeszcz"):
	    if(destination == "Strzyza"):
		if(trainNumber == 5):
		    self.part_left, self.part_up, self.part_down, self.part_right = 1;  # wolne
		elif(trainNumber == 1):
		    train2place = self.map.train2.actualTrack.getActualTrack()
		    if(train2place[0] == "PART_LEFT"):
		        self.part_left = 0 # zajete
		        self.part_up, self.part_down, self.part_right = 1;  # wolne
		    elif(train2place[0] == "PART_RIGHT"):
		        self.part_right = 0  # zajete
		        self.part_up, self.part_down, self.part_left = 1;  # wolne
		    elif(train2place[0] == "PART_UP"):
		        self.part_up = 0  # zajete
		        self.part_right, self.part_down, self.part_left = 1;  # wolne
		    else:
		        self.part_down= 0  # zajete
		        self.part_right, self.part_up, self.part_left = 1;  # wolne

		else:
		    train1place = self.map.train1.actualTrack.getActualTrack()
		    if (train1place[0] == "PART_LEFT"):
		        self.part_left = 0  # zajete
		        self.part_up, self.part_down, self.part_right = 1;  # wolne
		    elif (train1place[0] == "PART_RIGHT"):
		        self.part_right = 0  # zajete
		        self.part_up, self.part_down, self.part_left = 1;  # wolne
		    elif (train1place[0] == "PART_UP"):
		        self.part_up = 0  # zajete
		        self.part_right, self.part_down, self.part_left = 1;  # wolne
		    else:
		        self.part_down = 0  # zajete
		        self.part_right, self.part_up, self.part_left = 1;  # wolne


	if (start == "Wrzeszcz"):
	    if (destination == "Kielpinek"):
		if (trainNumber == 5):
		    self.part_left, self.part_up, self.part_down, self.part_right = 1;  # wolne
		elif (trainNumber == 1):
		    train2place = self.map.train2.actualTrack.getActualTrack()
		    if (train2place[0] == "PART_LEFT"):
		        self.part_left = 0  # zajete
		        self.part_up, self.part_down, self.part_right = 1;  # wolne
		    elif (train2place[0] == "PART_RIGHT"):
		        self.part_right = 0  # zajete
		        self.part_up, self.part_down, self.part_left = 1;  # wolne
		    elif (train2place[0] == "PART_UP"):
		        self.part_up = 0  # zajete
		        self.part_right, self.part_down, self.part_left = 1;  # wolne
		    else:
		        self.part_down = 0  # zajete
		        self.part_right, self.part_up, self.part_left = 1;  # wolne
		else:
		    train1place = self.map.train1.actualTrack.getActualTrack()
		    if (train1place[0] == "PART_LEFT"):
		        self.part_left = 0  # zajete
		        self.part_up, self.part_down, self.part_right = 1;  # wolne
		    elif (train1place[0] == "PART_RIGHT"):
		        self.part_right = 0  # zajete
		        self.part_up, self.part_down, self.part_left = 1;  # wolne
		    elif (train1place[0] == "PART_UP"):
		        self.part_up = 0  # zajete
		        self.part_right, self.part_down, self.part_left = 1;  # wolne
		    else:
		        self.part_down = 0  # zajete
		        self.part_right, self.part_up, self.part_left = 1;  # wolne
	if (start == "Strzyza"):
	    if (destination == "Kielpinek"):
		if (trainNumber == 5):
		    self.part_left, self.part_up, self.part_down, self.part_right = 1;  # wolne
		elif (trainNumber == 1):
		    train2place = self.map.train2.actualTrack.getActualTrack()
		    if (train2place[0] == "PART_LEFT"):
		        self.part_left = 0  # zajete
		        self.part_up, self.part_down, self.part_right = 1;  # wolne
		    elif (train2place[0] == "PART_RIGHT"):
		        self.part_right = 0  # zajete
		        self.part_up, self.part_down, self.part_left = 1;  # wolne
		    elif (train2place[0] == "PART_UP"):
		        self.part_up = 0  # zajete
		        self.part_right, self.part_down, self.part_left = 1;  # wolne
		    else:
		        self.part_down = 0  # zajete
		        self.part_right, self.part_up, self.part_left = 1;  # wolne
		else:
		    train1place = self.map.train1.actualTrack.getActualTrack()
		    if (train1place[0] == "PART_LEFT"):
		        self.part_left = 0  # zajete
		        self.part_up, self.part_down, self.part_right = 1;  # wolne
		    elif (train1place[0] == "PART_RIGHT"):
		        self.part_right = 0  # zajete
		        self.part_up, self.part_down, self.part_left = 1;  # wolne
		    elif (train1place[0] == "PART_UP"):
		        self.part_up = 0  # zajete
		        self.part_right, self.part_down, self.part_left = 1;  # wolne
		    else:
		        self.part_down = 0  # zajete
		        self.part_right, self.part_up, self.part_left = 1;  # wolne
	if (start == "Kielpinek"):
	    if (destination == "Strzyza"):
		if (trainNumber == 5):
		    self.part_left, self.part_up, self.part_down, self.part_right = 1;  # wolne
		elif (trainNumber == 1):
		    train2place = self.map.train2.actualTrack.getActualTrack()
		    if (train2place[0] == "PART_LEFT"):
		        self.part_left = 0  # zajete
		        self.part_up, self.part_down, self.part_right = 1;  # wolne
		    elif (train2place[0] == "PART_RIGHT"):
		        self.part_right = 0  # zajete
		        self.part_up, self.part_down, self.part_left = 1;  # wolne
		    elif (train2place[0] == "PART_UP"):
		        self.part_up = 0  # zajete
		        self.part_right, self.part_down, self.part_left = 1;  # wolne
		    else:
		        self.part_down = 0  # zajete
		        self.part_right, self.part_up, self.part_left = 1;  # wolne
		else:
		    train1place = self.map.train1.actualTrack.getActualTrack()
		    if (train1place[0] == "PART_LEFT"):
		        self.part_left = 0  # zajete
		        self.part_up, self.part_down, self.part_right = 1;  # wolne
		    elif (train1place[0] == "PART_RIGHT"):
		        self.part_right = 0  # zajete
		        self.part_up, self.part_down, self.part_left = 1;  # wolne
		    elif (train1place[0] == "PART_UP"):
		        self.part_up = 0  # zajete
		        self.part_right, self.part_down, self.part_left = 1;  # wolne
		    else:
		        self.part_down = 0  # zajete
		        self.part_right, self.part_up, self.part_left = 1;  # wolne
	if (start == "Kielpinek"):
	    if (destination == "Wrzeszcz"):
		if (trainNumber == 5):
		    self.part_left, self.part_up, self.part_down, self.part_right = 1;  # wolne
		elif (trainNumber == 1):
		    train2place = self.map.train2.actualTrack.getActualTrack()
		    if (train2place[0] == "PART_LEFT"):
		        self.part_left = 0  # zajete
		        self.part_up, self.part_down, self.part_right = 1;  # wolne
		    elif (train2place[0] == "PART_RIGHT"):
		        self.part_right = 0  # zajete
		        self.part_up, self.part_down, self.part_left = 1;  # wolne
		    elif (train2place[0] == "PART_UP"):
		        self.part_up = 0  # zajete
		        self.part_right, self.part_down, self.part_left = 1;  # wolne
		    else:
		        self.part_down = 0  # zajete
		        self.part_right, self.part_up, self.part_left = 1;  # wolne
		else:
		    train1place = self.map.train1.actualTrack.getActualTrack()
		    if (train1place[0] == "PART_LEFT"):
		        self.part_left = 0  # zajete
		        self.part_up, self.part_down, self.part_right = 1;  # wolne
		    elif (train1place[0] == "PART_RIGHT"):
		        self.part_right = 0  # zajete
		        self.part_up, self.part_down, self.part_left = 1;  # wolne
		    elif (train1place[0] == "PART_UP"):
		        self.part_up = 0  # zajete
		        self.part_right, self.part_down, self.part_left = 1;  # wolne
		    else:
		        self.part_down = 0  # zajete
		        self.part_right, self.part_up, self.part_left = 1;  # wolne
	if (start == "Strzyza"):
	    if (destination == "Wrzeszcz"):
		if (trainNumber == 5):
		    self.part_left, self.part_up, self.part_down, self.part_right = 1;  # wolne
		elif (trainNumber == 1):
		    train2place = self.map.train2.actualTrack.getActualTrack()
		    if (train2place[0] == "PART_LEFT"):
		        self.part_left = 0  # zajete
		        self.part_up, self.part_down, self.part_right = 1;  # wolne
		    elif (train2place[0] == "PART_RIGHT"):
		        self.part_right = 0  # zajete
		        self.part_up, self.part_down, self.part_left = 1;  # wolne
		    elif (train2place[0] == "PART_UP"):
		        self.part_up = 0  # zajete
		        self.part_right, self.part_down, self.part_left = 1;  # wolne
		    else:
		        self.part_down = 0  # zajete
		        self.part_right, self.part_up, self.part_left = 1;  # wolne
		else:
		    train1place = self.map.train1.actualTrack.getActualTrack()
		    if (train1place[0] == "PART_LEFT"):
		        self.part_left = 0  # zajete
		        self.part_up, self.part_down, self.part_right = 1;  # wolne
		    elif (train1place[0] == "PART_RIGHT"):
		        self.part_right = 0  # zajete
		        self.part_up, self.part_down, self.part_left = 1;  # wolne
		    elif (train1place[0] == "PART_UP"):
		        self.part_up = 0  # zajete
		        self.part_right, self.part_down, self.part_left = 1;  # wolne
		    else:
		        self.part_down = 0  # zajete
		        self.part_right, self.part_up, self.part_left = 1;  # wolne

	if (start == "Wrzeszcz"):
	    if (destination == "Osowa"):
		    self.part_right, self.part_up, self.part_left, self.part_down = 1;  # wolne
	if (start == "Osowa"):
	    if (destination == "Wrzeszcz"):
		    self.part_right, self.part_up, self.part_left, self.part_down = 1;  # wolne

	return self.part_right, self.part_up, self.part_left, self.part_down


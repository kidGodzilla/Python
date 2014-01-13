###################################################################
# mine.py
# James Futhey <james@jamesfuthey.com>
# 10/30/2013
####################################################################
from graphics import *
from random import random

while(1): #Loop for multiple games
	numMines=int(input("How many mines shall we lay? "))
	w=GraphWin("Minefield!",501,501)

	r,t,b,running=[],[],[],1
#list of rectangles, list of textfields, list of bombs, are we still playing or have we won/lost?

	def clearFrom(m): #Recursive loop to clear current and adjacent tiles of mines
		bomb=0 #We have not yet encountered a bomb on this tile
		bombCount=0 #Number of bombs
		for i in range(numMines): #loop through each bomb
			if(b[i] == m): #if there is a bomb in this tile
				bomb=1 #Set the variable to true

		if((m+1) % 10 != 0 and m<99): #Check tile to the right for bombs
			if(t[m+1].getText()=="  "):
				bombCount+=1
		if(m % 10 != 0 and t[m-1].getText()=="  "): #Check the tile to the left for bombs
			bombCount+=1
		if(m < 89):
			if(t[m+10].getText()=="  "): #check the tile to the bottom for bombs
				bombCount+=1
		if(m > 9 and t[m-10].getText()=="  "): #check the tile above for bombs
				bombCount+=1
		if(m % 10 != 0 and m > 9 and t[m-11].getText()=="  "): #Check upper-left tile for bombs
			bombCount+=1
		if(m>9 and (m+1) % 10 != 0 and t[m-9].getText()=="  "): #Check upper-right tile for bombs
			bombCount+=1
		if(m!=0 and m % 10 != 0 and m < 90): #Check lower-left tile for bombs
			if(t[m+9].getText()=="  "):
				bombCount+=1
		if((m+1) % 10 != 0 and m < 88):
			if(t[m+11].getText()=="  "): #Check lower-right tile for bombs
				bombCount+=1
		if(bomb==0): #If we found a bomb in THIS TILE
			r[m].setFill("grey") #clear it
			if(bombCount > 0):
				t[m].setText(bombCount) #Set the cleared tile to the number of adj bombs
			else:
				t[m].setText(" ") #Set to a single space if cleared w/o adj bombs
			if((m+1) % 10 != 0 and t[m+1].getText()==""):
				clearFrom(m+1) #Clear to the left
			if(m !=0 and m % 10 != 0 and t[m-1].getText()==""):
				clearFrom(m-1) #Clear to the right
			if(-1<m-10<100  and t[m-10].getText()==""):
				clearFrom(m-10) #Clear to the top
			if(-1<m+10<100 and t[m+10].getText()==""):
				clearFrom(m+10) #Clear to the bottom

	for i in range(numMines): #Generate random mines
		b.append([]) #Note that there can be more than one mine per tile
		b[i]=int(random()*100) #We're not checking very carefully

	for rY in range(10): #Generate map with 10 rows
		for rX in range(10): #and 10 columns
			n=rY*10+rX #a 10x10 grid was chosen for simplicity. 0x0->0, 10x4->14, etc.
			r.append([n]) #Create a new space to hold a new rectangle
			t.append([n]) #Create a new space to hold a new text object
			r[n]=Rectangle(Point(rX*50+1,rY*50+1),Point((rX*50)+51,(rY*50)+51))
			r[n].setFill('green3')
			r[n].draw(w) #draw a 50px green square 
			t[n]=Text(Point(rX*50+26,rY*50+26),"")
			t[n].draw(w) #draw a blank text label

	for i in range(numMines): #Set mines to be two spaces instead of blank. The user will not
		t[b[i]].setText("  ") #see a difference, but we can easily handle deduping mines

	while(running==1): #Loop for each click of the mouse
		ins=w.getMouse() #Get mouseclick
		cX=int((ins.getX()-1)/50) #Calculate which square was clicked
		cY=int((ins.getY()-1)/50)
		cn=cY*10+cX #cn is the same format as n above 
		for i in range(numMines): #Check mines
			if(b[i] == cn): #If the user clicked a mine
				for i in range(100): #Reveal all squares
					r[i].setFill("grey")
				for i in range(numMines): #Reveal all mines
					t[b[i]].setText(":(")
					r[b[i]].setFill("red")
				w.getMouse() #Wait for a click
				w.close()
				running=0 #End the loop so we can draw a new game window
		clearFrom(cn) #If we haven't lost, clear the tile and adjacent tiles
		remain=0 #Placeholder to count remaining bombs
		for i in range(100): #Check each tile individually
			if(t[i].getText()==""): #If it's a bomb
				remain+=1 #Increment
		if(remain==0): #If there are no more bombs
			for i in range(numMines): #Reveal all bombs
				t[b[i]].setText(":)") #Be happy
				r[b[i]].setFill("blue2") #Blue is happier than red
			if(running==1): #If we won and haven't lost
				w.getMouse() #Wait for a click before starting a new game
			w.close()
			running=0 #End loop so we can start a new game

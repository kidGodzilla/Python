##########################################################
# Snake.py
# James Futhey <james@jamesfuthey.com>
# 10/24/2013
#
# Requires modified graphics.py, which adds checkKey().
#
# Fixme:
# Food is occasionally drawn on top of our snake.
##########################################################

from graphics import *
from time import sleep
from random import random

while(1): #Infinite loop
	speed=0.1 #Sleep Time. Default 0.1. Increase this value if the game runs too quickly.
	cX, cY, l, s, dX, dY, a, fX, fY, grow, q = 20,20,5,[],1,0,[],3,18,0,1
#current X, Current Y, Length of snake, List containing snake part locations, X direction, Y direction, List containing snake rectangle objects, Current food X, Current food Y, 1 if snake will grow, 0 when player loses

	w=GraphWin('Snake!', 500, 500)
	for i in range(l): #Draw the initial snake pieces and put their coordinates in the `s` list
		s.append([cX-i,cY]) #keep track of where the pieces are supposed to be
		a.append([]) #add a blank spot to `a`
		a[i]=Rectangle(Point((cX-i)*10,cY*10),Point((cX-i)*10+10,cY*10+10)) 
		a[i].setFill('green1')
		a[i].draw(w) #draw the piece
	score=Text(Point(250,10),"Score: "+str((l-5)*10)) #Draw the scorebox
	score.draw(w)
	snakeFood=Rectangle(Point(fX*10,fY*10),Point(fX*10+10,fY*10+10)) #draw the snakefood
	snakeFood.setFill('red')
	snakeFood.draw(w)
	while(q==1): #Continue the loop until we `lose` for any reason
		sleep(speed) #Sleep 
		curKey=w.checkKey() #Get input from keyboard
		if(curKey == "Up"): 
			dX=0 #Do not move on the X axis
			if(dY==1): #If we were previously going down, we eat ourselves & lose!
				q=0 #We lose!
			dY=-1 #Otherwise, move -1 on the Y axis each time we loop
		if(curKey == "Down"):
			dX=0
			if(dY==-1):
				q=0
			dY=1
		if(curKey == "Right"):
			if(dX==-1):
				q=0
			dX=1
			dY=0
		if(curKey == "Left"):
			if(dX==1):
				q=0
			dX=-1
			dY=0
		cX+=dX #Move the `head` of the snake
		cY+=dY #
		if(cX>49 or cY>49 or cX<0 or cY<=0): #If we've left the screen, we LOSE!
			q=0
		#Calculate new positions for each piece of the snake
		for i in range(l-1,-1,-1): #Loop through the snake pieces from tail to head
			s[i]=s[i-1] #Shifts the previous piece to current pointer
			if(s[i] == [cX,cY]): #If the head and a body piece intersect, we LOSE!
				q=0
			a[i].undraw() #Undraw the piece after it's location is shifted
		if(cX == fX and cY == fY): #If we've eaten a piece of snake food
			snakeFood.undraw() #Destroy the snakefood
			grow=1 #Remember to grow later
			fX=int(random()*50) #Pick a new random position for the snakefood
			fY=int(random()*50)
			snakeFood=Rectangle(Point(fX*10,fY*10),Point(fX*10+10,fY*10+10)) 
			snakeFood.setFill('red')
			snakeFood.draw(w) #Draw the new snakefood
		s[0]=[cX,cY] #This is the new position of the `head` of the snake
		a[4].undraw() #Undraw the piece of the last piece of the tail
		for i in range(l): #We still need to draw the snake body, so lets do that.
			a[i]=Rectangle(Point((s[i][0])*10,s[i][1]*10),Point((s[i][0])*10+10,s[i][1]*10+10))
			a[i].setFill('green1')
			a[i].draw(w) #Draw a segment of the snake's body based on our `s` list
		if(grow==1): #If we have to grow, do that.
			l+=1 #Increase the snake length by one
			score.setText("Score: "+str((l-5)*10)) #Increase the score by 10
			speed*=0.95 #Increase the speed by 5% (Should be fine with any initial speed value)
			s.append([]) #Create new spaces for the new snake piece
			a.append([]) #
			a[l-1]=Point(0,0) #Because we will try to destroy all objects inside of the `a` list,
			a[l-1].draw(w) #We need a dummy object to avoid an error in python.
			grow=0 #We already grew, ensure we don't grow again until we need to
	w.close() #Close the screen if the player `loses`, so we can play again

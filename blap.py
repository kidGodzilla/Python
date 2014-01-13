###################################################################
# blap.py
# James Futhey <james@jamesfuthey.com>
# 10/18/2013
#
# Requires modified graphics.py, which adds checkKey().
#
# Name based on `blap`, written in C by Sam Steele and James Futhey
#
# To do: Increase speed as game progresses
###################################################################

from graphics import *
from random import random
from time import sleep

speed=0.003 #Increase this if the game runs too fast on your machine.

def beep(): #Trick to get a simple beep in shell. Some machines have an annoying beep.
	#print("\a") #Comment out this line to disable sound.
        return 0
	
def main():
	w=GraphWin('Blap!',900,500)
	w.setBackground('black')
	b=Circle(Point(100,250),14) #Ball
	b.setFill('white')
	b.draw(w)
	r=Rectangle(Point(850,200),Point(875,300)) #Computer Player
	r.setFill('white')
	r.draw(w)
	p=Rectangle(Point(25,200),Point(50,300)) #Human Player
	p.setFill('white')
	p.draw(w)
	l=Line(Point(450,0),Point(450,500)) #Center Line
	l.setFill('white')
	l.draw(w)
	s1,s2=0,0 #Scores
	t1=Text(Point(225,50),"Score: 0") #Player 1 score
	t2=Text(Point(675,50),"Score: 0") #Player 2 score
	t1.setTextColor('white')
	t2.setTextColor('white')
	t1.draw(w)
	t2.draw(w)
	xd,yd,ys=1,1,1 #X Direction, Y Direction, Y Speed (Randomizes Direction)
	while(1): #Infinite Loop because 1 always evaluates to true
		if(b.getCenter().getX() < 836): #Is inside court
			b.move(xd,0) #Handle x movement
			if(b.getCenter().getX() == 64): #Does P1 return?
				if(b.getCenter().getY() - 64 < p.getCenter().getY() < b.getCenter().getY() + 64): #If P1 intersects with ball, P1 returns
					xd=-xd #Change x direction 
					b.move(xd,0) #move 1px
					s1+=1 #P1 Score +1
					t1.setText("Score: "+str(s1))
					beep()
		else: #Computer player cannot lose. Always returns serve.
			xd=-xd #Change ball direction
			b.move(xd,0) #move ball
			beep()
		if(b.getCenter().getX() < -50): #P1 did not return ball
			b.undraw() #Destroy ball
			b=Circle(Point(450,250),14) #Create a new ball
			b.setFill('white')
			b.draw(w)
			r.undraw() #Destroy P2
			r=Rectangle(Point(850,200),Point(875,300)) #New P2
			r.setFill('white')
			r.draw(w)
			s2+=5 #P2 scores 5 points
			t2.setText("Score: "+str(s2))
		if(14 < b.getCenter().getY() < 485): #If ball is inside court
			b.move(0,yd) #Handle ball movement on y axis
			r.move(0,yd) #P2 mirrors ball movement
		else: #If the ball is about to leave the court:
			ys=-ys #Change direction
			yd=(ys * (random()/2+.75)) #Randomize bounce angle
			b.move(0,yd) #Move ball
			beep()
		curKey=w.checkKey() #Get current keypress
		if(curKey == "Up"): #If up
			p.move(0,-15) #Move P1 up
		if(curKey == "Down"): #If down
			p.move(0,15) #Move P1 down
		sleep(speed)

main()

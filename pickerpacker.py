try:
    import simplegui
except:
    print 'simplegui could not be imported. graphics will not work.'

import random

#CONFIGURATION OPTIONS
##Play variables
conveyorSpeed = 10
diversionSpeed = 1
inZoneProbability = 50
toteCapacity = (1,10)
playerSpeed = 5

##Spacial variables
conveyorY = 10
diversionY = 40 

#holders to keep track of totes that are on the conveyor an/or diversion line
conveyor = set([])
diversion = set([])


def generateTote():
    #Creates a new tote, adds to global totes
    tote()


def randomEvent(p):
    #Pass in probability on scale from 0 to 100.
    #Decides whether the event occurs, and returns boolean.
    assert type(p) == int and p >= 0 and p <= 100,\
            'Probabilities must be ints from 0 to 100'
    return p > random.randrange(0,100)


class tote():
    def __init__(self):
        conveyor.add(self)
        self.shelved = False
        self.x, self.y = 400, conveyorY
        self.inZone = randomEvent(inZoneProbability)
        self.quantity = random.randint(toteCapacity[0],toteCapacity[1])

        
generateTote()
generateTote()
generateTote()
generateTote()

for tote in conveyor:
    print tote.inZone

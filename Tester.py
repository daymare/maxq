#!/usr/bin/python2.7

# library imports
import gym
import sys
import pdb

# user imports
import Params

import environments.MRTaxiDecoder as decoder


class Getch:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)

        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

        return ch


class Tester:
    def __init__(self):
        # environment setup
        self.env = gym.make('MultiRoomTaxi-v0')
        self.getch = Getch()

    def runEpisodes(self, episodes=500):
        for i in range(episodes):
            self.runEpisode()

    def initEpisode(self):
        self.stuff = self.env.reset()
        self.terminate = False

    def runEpisode(self, maxTimesteps=2000):
        self.initEpisode()

        print(chr(27) + "[2J]")
        self.env.render()
        
        self.displayTerminalFeedback(self.stuff)

        for i in range(maxTimesteps):
            # get user action
            character = self.getch()

            # perform user action
            self.performAction(character)

            if self.terminate == True:
                break

            # output debug information and environment state
            print(chr(27) + "[2J]")
            print 'got character: {}'.format(character)
            
            # output decoder information
            self.displayTerminalFeedback(self.stuff[0])

            self.env.render()

    def displayTerminalFeedback(self, state):
        terminal, pseudoReward = decoder.navigate_put_r3_isTerminal(state)
        print 'terminal: {}'.format(terminal)
        print 'pseudo reward: {}'.format(pseudoReward)
        


    def performAction(self, character):
        if character == 'q':
            sys.exit()
        elif character == 'r':
            self.terminate = True
        elif character == 'w':
            self.stuff = self.env.step(1) # go up
        elif character == 'a':
            self.stuff = self.env.step(3) # go left
        elif character == 's':
            self.stuff = self.env.step(0) # go down
        elif character == 'd':
            self.stuff = self.env.step(2) # go right
        elif character == 'p':
            self.stuff = self.env.step(4) # pickup
        elif character == 'f':
            self.stuff = self.env.step(5) # dropoff




def myMain():
    tester = Tester()
    tester.runEpisodes()

if __name__ == '__main__':
    myMain()
    


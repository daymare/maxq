#!/usr/bin/python2.7

import gym
import sys

import tty, sys, termios


# parameters (because I'm too lazy to make another module)


class HandControl:
    def __init__(self):
        self.env = gym.make('Taxi-v2')

    def runEpisode(self):
        terminal = False
        state = self.env.reset()
        action = 0
        resultingState = state

        while terminal == False:
            state = resultingState

            # display the environment
            print chr(27) + "[2J]"
            print "state: {}\n".format(state)
            self.env.render()

            # have user choose an action
            action = self.getUserAction()

            # update the environment
            resultingState, reward, terminal, _ = self.env.step(action)

            # display the resulting environment
            print "action: {}\n".format(action)
            print "resulting state: {}\n".format(resultingState)
            self.env.render()


    def getUserAction(self):
        actionNum = int(self.getChar())
        
        while actionNum < 0 or actionNum > self.env.action_space.n:
            actionNum = int(self.getChar())

        return actionNum


    def getChar(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


if __name__ == '__main__':
    handControl = HandControl()

    while True:
        handControl.runEpisode()





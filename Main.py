#!/usr/bin/python2.7

# library imports
import gym
import sys
import matplotlib.pyplot as plt
import pdb

# user imports
import Params
from Maxq import MaxQ
from MaxGraph import MaxGraph
from environments.TaxiGraph import TaxiGraph

class LearningManager:
    def __init__(self):
        # environment setup
        self.env = gym.make('Taxi-v2')

        # setup parameters
        Params.params = Params.Params(self.env)

        # setup the graph
        self.maxGraph = TaxiGraph()

        # maxq setup
        self.maxq = MaxQ(self.env, self.maxGraph)

    def test(self):
        legend = []
        averagedRewards = []

        plt.title("MaxQ Learning")
        plt.xlabel("Time Step")
        plt.ylabel("Reward")

        for i in range(Params.params.maxEpisodes - Params.params.numEpisodes):
            reward = 0

            # train the model
            if Params.params.viewToggle == True:
                if i % Params.params.viewDelay == 0:
                    raw_input("press enter to continue...")
                    reward = self.maxq.runEpisode(True)
                else:
                    reward = self.maxq.runEpisode(False)
            else:
                reward = self.maxq.runEpisode(False)

            Params.params.rewards.append(reward)

            # print feedback to the user
            if i % Params.params.printDelay == 0:
                print "episode: {} timesteps: {} reward: ".format(Params.params.numEpisodes, Params.params.numTimesteps, reward)

            # save the model
            if i % Params.params.saveDelay == 0 and i != 0:
                self.maxQ.save()
                Params.saveParameters()


        # create averaged rewards
        averages = range(Params.params.numEpisodes-100)

        summation = 0
        for i in range(Params.params.total_episodes):
            if i // 100 == 0:
                summation += Params.params.rewards[i]
            else:
                summation += Params.params.rewards[i]
                summation -= Params.params.rewards[i-100]
                averagedRewards.append(summation/100)

        plt.plot(averages, averagedRewards)
        legend = []
        plt.show()


def myMain():
    manager = LearningManager()
    manager.test()

if __name__ == '__main__':
    myMain()



#!/usr/bin/python2.7

# library imports
import gym
import sys
import matplotlib.pyplot as plt

# user imports
import params
from maxq import MaxQ
from maxGraph import MaxGraph

class LearningManager:
    def __init__(self):
        # environment setup
        self.env = gym.make('Taxi-v2')

        # setup parameters
        params.params = params.Params(self.env)

        # setup the graph
        self.maxGraph = MaxGraph()
        self.maxGraph.constructTaxiGraph()

        # maxq setup
        self.maxq = MaxQ(self.env, self.maxGraph)

    def test(self):
        legend = []
        averagedRewards = []

        plt.title("MaxQ Learning")
        plt.xlabel("Time Step")
        plt.ylabel("Reward")

        for i in range(params.params.maxEpisodes - params.params.numEpisodes):
            reward = 0

            # train the model
            if params.params.viewToggle == True:
                if i % params.params.viewDelay == 0:
                    raw_input("press enter to continue...")
                    reward = self.maxq.runEpisode(True)
                else:
                    reward = self.maxq.runEpisode(False)
            else:
                reward = self.maxq.runEpisode(False)

            params.params.rewards.append(reward)

            # print feedback to the user
            if i % params.params.printDelay == 0:
                print "episode: {} timesteps: {} reward: ".format(params.params.numEpisodes, params.params.numTimesteps, reward)

            # save the model
            if i % params.params.saveDelay == 0 and i != 0:
                self.maxQ.save()
                params.saveParameters()


        # create averaged rewards
        averages = range(params.params.numEpisodes-100)

        summation = 0
        for i in range(params.total_episodes):
            if i // 100 == 0:
                summation += params.rewards[i]
            else:
                summation += params.rewards[i]
                summation -= params.rewards[i-100]
                averagedRewards.append(summation/100)

        plt.plot(averages, averagedRewards)
        legend = []
        plt.show()


def myMain():
    manager = LearningManager()
    manager.test()

if __name__ == '__main__':
    myMain()



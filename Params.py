


# TODO save and load

class Params:
    def __init__(self, env):
        # training parameters
        self.alpha = 0.9
        self.gamma = 0.99 # discount on future reward
        self.epsilon = 0.1 # probability of taking a random action

        # defaults
        self.defaultVValue = 1
        self.defaultCValue = 1

        # episode parameters
        self.maxEpisodes = 100000
        self.maxEpisodeLength = 200

        # view parameters
        self.viewToggle = False
        self.viewDelay = 1
        self.printDelay = 1
        
        # save/load parameters
        loadModel = False
        loadParameters = False
        saveDelay = 500
        savePath = "./save"
        parameterSavePath = "./save/parameters"

        # environment paramaters (extracted from environment)
        self.numStates = env.observation_space.n
        self.numActions = env.action_space.n

        # count values
        self.numEpisodes = 0
        self.numTimesteps = 0

        # data
        self.rewards = []





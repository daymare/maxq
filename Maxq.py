
# library imports
import random

# user imports
from Params import Params
from Display import Display

class MaxQ:
    def __init__(self, env, maxGraph):
        self.graph = maxGraph
        self.env = env

        self.ancestorStack = []
        self.display = False

        self.displayManager = Display(env)

    # run a single episode of the environment
    # returns the toal reward gained over the episode
    def runEpisode(self, display=False):
        self.initEpisode()
        self.display = display

        # run episode
        initState = self.env.reset()
        self._MaxQQ(self.graph.getRoot(), initState)

        return self.episodeReward

    def initEpisode(self):
        self.ancestorStack = []
        self.episodeReward = 0

    # run the MaxQ-Q algorithm
    def _MaxQQ(self, maxNode, state):
        seq = []

        # manage stack on input
        self.ancestorStack.append(maxNode)
        resultState = state

        # if i is primitive
        if maxNode.isPrimitive():
            # execute and receive feedback
            resultState, reward, terminal, _ = self.env.step(maxNode.primitiveAction)
            self.episodeReward += reward

            # if it is terminal ancestor terminate the whole stack. root terminal is the same as env terminal.
            if terminal == True:
                self.ancestorTerminate(maxGraph.getRoot())

            # check for ancestor termination on the whole stack
            self.handleAncestorTermination(resultState)

            # update projected value function V
            maxNode.updateVValue(state, reward)

            # push s onto the beginning of seq
            seq.insert(0, state)
        else:
            count = 0

            while maxNode.isTerminal(state) == False
                # choose action according to exploration policy
                action = self.getAction(maxNode, state) 
                actionMaxNode = maxNode.getMaxChild(action)
                childSequence, resultState = self._MaxQQ(actionMaxNode, state)

                # display the environment and program state to the user
                self.displayManager.displayStep(self.ancestorStack, state, action, maxNode)

                # check for ancestor termination 
                # check the stack to see if we are the node that should be running right now. and if not, terminate
                if self.ancestorStack[len(self.ancestorStack)-1] != maxNode:
                    return childSequence, resultState

                # find a-prime, best action
                aPrime = maxNode.getMaxAction(state)
               
                # update completion functions 
                n = 1
                for s in childSequence:
                    self.updateCompletionFunctions(maxNode, s, action, resultState, aPrime)
                    n += 1

                # append child sequence onto the front of seq
                seq.insert(0, childSequence)

                state = resultState

        # manage stack on return
        self.ancestorStack.pop()
        
        return seq, resultState

    # check if any nodes up the call stack have terminated and then ancestor terminate them
    def handleAncestorTermination(self, nextState):
        for maxNode in self.ancestorStack:
            terminate, _ = maxNode.terminationFunction(nextState)
            if terminate == True:
                self.ancestorTerminate(maxNode)
                return

    def ancestorTerminate(self, maxNode):
        print "ancestor terminating {}!".format(maxNode.name)

        # remove up to the terminating node from the stack
        while self.ancestorStack[len(self.ancestorStack)-1] != maxNode:
            self.ancestorStack.pop()

        # remove the terminating node from the stack
        self.ancestorStack.pop()

    def updateCompletionFunctions(self, maxNode, state, action, resultState, resultAction):
        # Q nodes
        actionQNode = maxNode.getChild(action)
        resultQNode = maxNode.getChild(resultAction)
        
        # get C values
        oldICValue = actionQNode.getInteriorCValue(state)
        oldCValue = actionQNode.getExteriorCValue(state)

        # get resulting C values
        resultICValue = resultQNode.getInteriorCValue(resultState)
        resultCValue = resultQNode.getExteriorCValue(resultState)

        # get V result
        maxChild = maxNode.getMaxChild(resultAction)
        resultV = maxChild.getVValue(resultState)

        # get pseudo reward
        pseudoReward = maxNode.getPseudoReward(resultState)

        # update completion functions
        actionQNode.updateInteriorCValue(state, oldICValue, pseudoReward, resultICValue, resultV)
        actionQNode.updateExteriorCValue(state, oldCValue, resultCValue, resultV)


    def getAction(self, maxNode, state):
        rand = random.random()
        action = 0
    
        if rand < 0.1:
            action = maxNode.getRandomAction(state)
        else:
            action = maxNode.getMaxAction(state)

        return action



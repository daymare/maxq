
# library imports
import random

# user imports
from params import Params

class MaxQ:
    def __init__(self, env, maxGraph):
        self.graph = maxGraph
        self.env = env

        self.ancestorStack = []

    # run a single episode of the environment
    # returns the toal reward gained over the episode
    def runEpisode(self, display=False):
        self.initEpisode()

        # run episode
        initState = self.env.reset()
        self._MaxQQ(self.graph.getRoot(), initState)

    def initEpisode(self):
        self.ancestorStack = []

    # run the MaxQ-Q algorithm
    def _MaxQQ(self, maxNode, state, parameter=0):
        seq = []

        # manage stack on input
        self.ancestorStack.append(maxNode)
        resultState = state

        # if i is primitive
        if maxNode.isPrimitive():
            # execute and receive feedback
            resultState, reward, terminal, _ = self.env.step(maxNode.primitiveAction)

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

            while maxNode.isTerminal(state, parameter) == False and maxNode.isActive(state, parameter) == True:
                # choose action according to exploration policy
                action = self.getAction(maxNode, state, parameter) # note that action is also a MaxNode
                actionMaxNode = maxNode.getMaxChild(action)
                childSequence, resultState = self._MaxQQ(actionMaxNode, parameter)

                # check for ancestor termination 
                # check the stack to see if we are the node that should be running right now. and if not, terminate
                if self.ancestorStack[len(self.ancestorStack)-1] != maxNode:
                    return childSequence, resultState

                # find a-prime, best action
                aPrime = maxNode.getMaxAction(state, parameter)
               
                # update completion functions 
                n = 1
                for s in childSequence:
                    self.updateCompletionFunctions(maxNode, s, action, resultState, aPrime, parameter)
                    n += 1

                # append child sequence onto the front of seq
                seq.insert(0, childSequence)

        # manage stack on return
        self.ancestorStack.pop()
        
        return seq, resultState

    # check if any nodes up the call stack have terminated and then ancestor terminate them
    def handleAncestorTermination(self, nextState):
        for maxNode in self.ancestorStack:
            terminate, _ = maxNode.terminationFunction(nextState, parameter)
            if terminate == True:
                self.ancestorTerminate(maxNode)
                return

    def ancestorTerminate(self, maxNode):
        # remove up to the terminating node from the stack
        while self.ancestorStack[len(self.ancestorStack)-1] != maxNode:
            self.ancestorStack.pop()

        # remove the terminating node from the stack
        self.ancestorStack.pop()

    def updateCompletionFunctions(self, maxNode, state, action, resultState, resultAction, parameter):
        # Q nodes
        actionQNode = maxNode.getChild(action)
        resultQNode = maxNode.getChild(resultAction)
        
        # get C values
        oldICValue = actionQNode.getInteriorCValue(state, parameter)
        oldCValue = actionQNode.getExteriorCValue(state, parameter)

        # get resulting C values
        resultICValue = resultQNode.getInteriorCValue(resultState, parameter)
        resultCValue = resultQNode.getExteriorCValue(resultState, parameter)

        # get V result
        maxChild = maxNode.getMaxChild(resultAction)
        resultV = maxChild.getVValue(resultState, parameter)

        # get pseudo reward
        pseudoReward = maxNode.getPseudoReward(resultState)

        # update completion functions
        actionQNode.updateInteriorCValue(state, parameter, oldICValue, pseudoReward, resultICValue, resultV)
        actionQNode.updateExteriorCValue(state, parameter, oldCValue, resultCValue, resultV)


    def getAction(self, maxNode, state, parameter=0):
        rand = random.random()
        action = 0
    
        if rand < 0.1:
            action = maxNode.getRandomAction(state, parameter)
        else:
            action = maxNode.getMaxAction(state, parameter)

        return action



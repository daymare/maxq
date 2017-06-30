
# python imports
import copy
import random
import pdb

# user imports
import Params
from environments import TaxiDecoder


# class containing all max and q nodes. 
# Effectively contains the policy for the whole algorithm.
class MaxGraph:
    def __init__(self):
        self.maxRoot = MaxNode()
        self.maxRoot.addTerminationFunction(TaxiDecoder.root_isTerminal)

        self.constructGraph()

    def constructGraph(self):
        pass

    def getRoot(self):
        return self.maxRoot

def getStateId(state):
    return state


def createMaxNode(name, qChildren, terminationFunction):
    maxNode = MaxNode(name, False)

    maxNode.addTerminationFunction(terminationFunction)

    for child in qChildren:
        maxNode.addChild(child)

    return maxNode

def createQNode(name, maxChild):
    qNode = QNode(name)
    qNode.setChild(maxChild)

    return qNode

# creates a primitive Qnode maxnode pair and returns the Q node parent
def createPrimitiveNode(name, primitiveAction):
    maxPrimitive = MaxNode(name, True, primitiveAction)
    qPrimitive = createQNode("q"+name, maxPrimitive)
    return qPrimitive

# creates a composite Qnode maxnode pair and returns the Q node parent
def createCompositeNode(name, qChildren, terminationFunction):
    maxNode = createMaxNode(name, qChildren, terminationFunction)
    qNode = createQNode("q"+name, maxNode)
    return qNode


# max node calculating the projected value function V(pi, s)
class MaxNode:
    def __init__(self, name="root", isPrimitive=False, primitiveAction=0):
        self.name = name
        self.childNodes = [] # list of q nodes
        self._isPrimitive = isPrimitive
        self.primitiveAction = primitiveAction
        self.vFunction = {}
        self.terminationFunction = TaxiDecoder.primitive_isTerminal

    def addChild(self, qChild):
        newChild = copy.deepcopy(qChild)
        self.childNodes.append(newChild)

    def getChild(self, childIndex):
        return self.childNodes[childIndex]

    def addTerminationFunction(self, terminationFunction):
        self.terminationFunction = terminationFunction

    def isPrimitive(self):
        return self._isPrimitive

    def isTerminal(self, state):
        actuallyIsTerminal, _ = self.terminationFunction(state)
        return actuallyIsTerminal

    def getPseudoReward(self, state):
        _, pseudoReward = self.terminationFunction(state)
        return pseudoReward

    # returns the index of the highest q child
    def getMaxAction(self, state):
        _, index = self.getMaxQValue(state)
        return index

    def getRandomAction(self, state):
        return random.randint(0, len(self.childNodes)-1)

    def getMaxChild(self, index):
        qChild = self.childNodes[index]
        maxChild = qChild.getChild()
        return maxChild

    def getInteriorValue(self, state, actionIndex):
        qChild = self.childNodes[actionIndex]
        value = qChild.getInteriorQValue(state)
        return value

    def getExteriorValue(self, state, actionIndex):
        qChild = self.childNodes[actionIndex]
        value = qChild.getExteriorQValue(state)
        return value

    # returns the value of the highest q child and the index of the highest q child
    def getMaxQValue(self, state):
        maxIndex = 0
        maxIValue = None
        maxValue = None

        print("\nget max Q value: {}".format(self.name))
        
        for i in range(0, len(self.childNodes)):
            child = self.childNodes[i]
            value = child.getInteriorQValue(state)

            # check if child is valid for this state
            maxChild = self.getMaxChild(i)
            if maxChild.isTerminal(state) == True and maxChild.isPrimitive() == False:
                continue

            print ("child: {} qValue: {}".format(child.name, value))
            
            if maxIValue == None or value > maxIValue:
                maxIValue = value
                maxValue = child.getExteriorQValue(state)
                maxIndex = i

        print("chosen child: {} internalValue: {} externalValue: {}\n".format(self.childNodes[maxIndex].name, maxIValue, maxValue))

        return maxValue, maxIndex


    def getVValue(self, state):
        if self.isPrimitive: # node is primitive
            stateId = getStateId(state)
            return self.vFunction.get(stateId, Params.params.defaultVValue)
        else: # node is non primitive
            # get max Q value from q children
            vValue, _= self.getMaxQValue(state)
            return vValue

    def updateVValue(self, state, reward):
        assert self._isPrimitive == True

        stateId = getStateId(state)
        prevValue = self.vFunction.get(stateId, Params.params.defaultVValue)

        newVValue = (1 - Params.params.alpha) * prevValue + Params.params.alpha * reward
        self.vFunction[stateId] = newVValue


# Q node calculating the Qfunction Q(pi, s, a)
# Contains completion function C(pi, s, a)
# asks child max node for projected value function V(a, s)
class QNode:
    def __init__(self, name="qNode"):
        self.name = name
        self.child = None # max node child
        self.exteriorCFunction = {}
        self.interiorCFunction = {}

    def setChild(self, maxChild):
        newChild = copy.deepcopy(maxChild)
        self.child = newChild

    def getChild(self):
        return self.child

    def getInteriorQValue(self, state=0):
        numStates = Params.params.numStates

        vValue = self.child.getVValue(state)
        stateId = getStateId(state)
        cValue = self.interiorCFunction.get(stateId, Params.params.defaultCValue)

        return vValue + cValue

    def getExteriorQValue(self, state):
        numStates = Params.params.numStates

        vValue = self.child.getVValue(state)
        stateId = getStateId(state)
        cValue = self.exteriorCFunction.get(stateId, Params.params.defaultCValue)

        return vValue + cValue

    def getInteriorCValue(self, state):
        stateId = getStateId(state)
        return self.interiorCFunction.get(stateId, Params.params.defaultCValue)

    def getExteriorCValue(self, state):
        stateId = getStateId(state)
        return self.exteriorCFunction.get(stateId, Params.params.defaultCValue)

    def updateInteriorCValue(self, state, oldICValue, pseudoReward, resultICValue, resultV):
        alpha = Params.params.alpha
        gamma = Params.params.gamma

        # calculate new interior value
        newICValue = (1-alpha) * oldICValue + alpha * gamma * (pseudoReward + resultICValue + resultV)

        print("\nupdate interior c value for: {}".format(self.name))
        print("oldICValue: {}".format(oldICValue))
        print("newPart: {}".format(pseudoReward + resultICValue + resultV))
        print("newICValue: {}".format(newICValue))
        print("pseudoReward: {}".format(pseudoReward))
        print("resultICValue: {}".format(resultICValue))
        print("resultV: {}".format(resultV))
        print("gamma: {}\n".format(gamma))

        # udpate the interior value table
        stateId = getStateId(state)
        print("before: {}".format(self.interiorCFunction.get(stateId, Params.params.defaultCValue)))
        self.interiorCFunction[stateId] = newICValue
        print("after: {}\n".format(self.interiorCFunction[stateId]))

    def updateExteriorCValue(self, state, oldCValue, resultCValue, resultV):
        alpha = Params.params.alpha
        gamma = Params.params.gamma

        # calculate new interior value
        newICValue = (1-alpha) * oldCValue + alpha * gamma * (resultCValue + resultV)

        # udpate the exterior value table
        stateId = getStateId(state)
        self.exteriorCFunction[stateId] = newICValue





        


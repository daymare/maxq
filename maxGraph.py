
# python imports
import copy
import random

# user imports
import params
import taxiDecoder


# class containing all max and q nodes. 
# Effectively contains the policy for the whole algorithm.
class MaxGraph:
    def __init__(self):
        self.maxRoot = MaxNode()
        self.maxRoot.addTerminationFunction(taxiDecoder.root_isTerminal)
        self.maxRoot.addActiveFunction(taxiDecoder.root_isActive)

    def constructTaxiGraph(self):
        ## create nodes
        # get
        qGet = QNode("qGet")
        maxGet = MaxNode("maxGet", False)
        maxGet.addTerminationFunction(taxiDecoder.get_isTerminal)
        maxGet.addActiveFunction(taxiDecoder.get_isActive)

        # pickup
        qPickup = QNode("qPickup")
        pickup = MaxNode("pickup", True, 4)

        # put
        qPut = QNode("qPut")
        maxPut = MaxNode("maxPut", False)
        maxPut.addTerminationFunction(taxiDecoder.put_isTerminal)
        maxPut.addActiveFunction(taxiDecoder.put_isActive)

        # putdown
        qPutdown = QNode("qPutdown")
        putdown = MaxNode("putdown", True, 5)

        # navigate
        qNavigate_Get = QNode("qNavigate_Get")
        qNavigate_Put = QNode("qNavigate_Put")
        maxNavigate = MaxNode("maxNavigate", False)
        maxNavigate.addTerminationFunction(taxiDecoder.navigate_isTerminal)
        maxNavigate.addActiveFunction(taxiDecoder.navigate_isActive)

        # movement
        qNorth = QNode("qNorth")
        qEast = QNode("qEast")
        qSouth = QNode("qSouth")
        qWest = QNode("qWest")

        North = MaxNode("North", True, 1)
        East = MaxNode("East", True, 2)
        South = MaxNode("South", True, 0)
        West = MaxNode("West", True, 3)

        ## string nodes together from the bottom up
        # movement nodes
        qNorth.setChild(North)
        qEast.setChild(East)
        qSouth.setChild(South)
        qWest.setChild(West)

        # navigate nodes
        maxNavigate.addChild(qNorth)
        maxNavigate.addChild(qEast)
        maxNavigate.addChild(qSouth)
        maxNavigate.addChild(qWest)

        qNavigate_Get.setChild(maxNavigate, 0)
        qNavigate_Put.setChild(maxNavigate, 1)

        # get
        qPickup.setChild(pickup)
        maxGet.addChild(qPickup)
        maxGet.addChild(qNavigate_Get)
        qGet.setChild(maxGet)

        # put
        qPutdown.setChild(putdown)
        maxPut.addChild(qPutdown)
        maxPut.addChild(qNavigate_Put)
        qPut.setChild(maxPut)

        # root
        root = self.maxRoot
        root.addChild(qGet)
        root.addChild(qPut)

    def getRoot(self):
        return self.maxRoot

def getStateId(self, state, parameter=0):
    numStates = params.params.numStates
    return numStates * (parameter + 1) + state

# max node calculating the projected value function V(pi, s)
class MaxNode:
    def __init__(self, name="root", isPrimitive=False, primitiveAction=0):
        self.name = name
        self.childNodes = [] # list of q nodes
        self._isPrimitive = isPrimitive
        self.primitiveAction = primitiveAction
        self.vFunction = {}
        self.terminationFunction = taxiDecoder.primitive_isTerminal
        self.activeFunction = taxiDecoder.primitive_isActive

    def addChild(self, qChild):
        newChild = copy.deepcopy(qChild)
        self.childNodes.append(newChild)

    def getChild(self, childIndex):
        return self.childNodes[childIndex]

    def addActiveFunction(self, activeFunction):
        self.activeFunction = activeFunction

    def addTerminationFunction(self, terminationFunction):
        self.terminationFunction = terminationFunction

    def isPrimitive(self):
        return self._isPrimitive

    def isTerminal(self, state, parameter=0):
        actuallyIsTerminal, _ = self.terminationFunction(state, parameter)
        return actuallyIsTerminal

    def isActive(self, state, parameter=0):
        return self.activeFunction(state, parameter)

    def getPseudoReward(self, state):
        _, pseudoReward = self.terminationFunction(state, paramater=0)
        return pseudoReward

    # returns the index of the highest q child
    def getMaxAction(self, state, parameter=0):
        _, index = self.getMaxQValue(state, parameter)
        return index

    def getRandomAction(self, state, parameter=0):
        return random.randint(0, len(self.childNodes)-1)

    def getMaxChild(self, index):
        qChild = self.childNodes[index]
        maxChild = qChild.getChild()
        return maxChild

    # returns the value of the highest q child and the index of the highest q child
    def getMaxQValue(self, state, parameter=0):
        maxIndex = 0
        maxIValue = self.childNodes[0].getInteriorQValue(state, parameter)
        maxValue = self.childNodes[0].getExteriorQValue(state, parameter)
        
        for i in range(1, len(self.childNodes)):
            child = self.childNodes[i]
            value = child.getInteriorQValue(state, parameter)
            
            if value > maxValue:
                maxIValue = value
                maxValue = child.getExteriorQValue(state, parameter)
                maxIndex = i

        return maxValue, maxIndex


    def getVValue(self, state, parameter=0):
        if self.isPrimitive: # node is primitive
            stateId = getStateId(state, parameter)
            return self.vFunction.get(stateId, params.params.defaultVValue)
        else: # node is non primitive
            # get max Q value from q children
            vValue, _= self.getMaxQValue(state, parameter)
            return vValue

    def updateVValue(self, state, reward, parameter=0):
        assert self._isPrimitive == True

        stateId = getStateId(state, parameter)
        prevValue = self.vFunction.get(stateId, params.params.defaultVValue)

        newVValue = (1 - params.params.alpha) * prevValue + params.params.alpha * reward
        self.vFunction[stateId] = newVValue


# Q node calculating the Qfunction Q(pi, s, a)
# Contains completion function C(pi, s, a)
# asks child max node for projected value function V(a, s)
class QNode:
    def __init__(self, name="qNode"):
        self.name = name
        self.child = None # max node child
        self.parameter = 0 # parameter for the node to send to it's child
        self.exteriorCFunction = {}
        self.interiorCFunction = {}

    def setChild(self, maxChild, childParameter=0):
        newChild = copy.deepcopy(maxChild)
        self.child = newChild
        self.parameter = childParameter

    def getChild(self):
        return self.child

    def getInteriorQValue(self, state, parameter=0):
        numStates = params.params.numStates

        vValue = self.child.getVValue(state, self.parameter)
        stateId = getStateId(state, parameter)
        cValue = self.interiorCFunction.get(stateId, params.params.defaultCValue)

        return vValue + cValue

    def getExteriorQValue(self, state, parameter=0):
        numStates = params.params.numStates

        vValue = self.child.getVValue(state, self.parameter)
        stateId = getStateId(state, parameter)
        cValue = self.exteriorCFunction.get(stateId, params.params.defaultCValue)

        return vValue + cValue

    def getInteriorCValue(self, state, parameter=0):
        stateId = getStateId(state, parameter)
        return self.interiorCFunction.get(stateId, params.params.defaultCValue)

    def getExteriorCValue(self, state, parameter=0):
        stateId = getStateId(state, parameter)
        return self.exteriorCFunction.get(stateId, params.params.defaultCValue)

    def updateInteriorCValue(self, state, parameter, oldICValue, pseudoReward, resultICValue, resultV):
        alpha = params.params.alpha
        gamma = params.params.gamma

        # calculate new interior value
        newICValue = (1-alpha) * oldICValue + alpha * gamma * (pseudoReward + resultICValue + resultV)

        # udpate the interior value table
        stateId = getStateId(state, parameter)
        self.interiorCFunction[stateId] = newICValue

    def updateExteriorCValue(self, state, parameter, oldCValue, resultCValue, resultV):
        alpha = params.params.alpha
        gamma = params.params.gamma

        # calculate new interior value
        newICValue = (1-alpha) * oldCValue + alpha * gamma * (resultCValue + resultV)

        # udpate the interior value table
        stateId = getStateId(state, parameter)
        self.interiorCFunction[stateId] = newICValue





        


import time


# user imports
import Params

class Display:
    def __init__(self, env):
        self.env = env
    
    def displayStep(self, nodeStack, state, action, maxNode):
        print(chr(27) + "[2J]")

        self.printParameters()
        self.printStack(nodeStack)
        self.printActionValue(state, action, maxNode)
        self.env.render()
        time.sleep(Params.params.viewSleepTime)
        #raw_input("")

    def printStack(self, nodeStack):
        print("")

        for node in nodeStack:
            print("{}".format(node.name))

        print("")
        

    def printParameters(self):
        print("episodes: " + str(Params.params.numEpisodes))
        print("timesteps: " + str(Params.params.numTimesteps))
        print("epsilon: " + str(Params.params.epsilon))

    def printActionValue(self, state, action, maxNode):
        # get node children
        childrenNames = []
        for child in maxNode.childNodes:
            childrenNames.append(child.name)

        # get node qValues
        interiorValues = []
        exteriorValues = []
        for i in range(len(maxNode.childNodes)):
            interiorValues.append(maxNode.getInteriorValue(state, i))
            exteriorValues.append(maxNode.getExteriorValue(state, i))

        print("node: {}".format(maxNode.name))
        print("node children: {}".format(childrenNames))
        print("interior Q Values: {}".format(interiorValues))
        print("exterior Q Values: {}".format(exteriorValues))

        # gather data
        actionMaxNode = maxNode.getMaxChild(action)
        interiorValue = maxNode.getInteriorValue(state, action)
        exteriorValue = maxNode.getExteriorValue(state, action)

        # display
        print("chosen action: {}".format(actionMaxNode.name))
        print("chosen action interior value: {}".format(interiorValue))
        print("chosen action exterior value: {}".format(exteriorValue))



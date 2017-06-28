
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

    def printStack(self, nodeStack):
        print("\n")

        for node in nodeStack:
            print("{}\n".format(node.name))

        print("\n")
        

    def printParameters(self):
        print("episodes: " + str(Params.params.numEpisodes) + "\n")
        print("timesteps: " + str(Params.params.numTimesteps) + "\n")
        print("epsilon: " + str(Params.params.epsilon) + "\n")

    def printActionValue(self, state, action, maxNode):
        # gather data
        actionMaxNode = maxNode.getMaxChild(action)
        interiorValue = maxNode.getInteriorValue(state, action)
        exteriorValue = maxNode.getExteriorValue(state, action)

        # display
        print("chosen action: {}".format(actionMaxNode.name))
        print("chosen action interior value: {}".format(interiorValue))
        print("chosen action exterior value: {}".format(exteriorValue))



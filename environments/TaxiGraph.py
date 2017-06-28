

# system imports
import pdb

# user imports
import MaxGraph
import TaxiDecoder

class TaxiGraph(MaxGraph.MaxGraph):
    def constructGraph(self):
        # movement
        qNorth = MaxGraph.createPrimitiveNode("North", 1)
        qEast = MaxGraph.createPrimitiveNode("East", 2)
        qSouth = MaxGraph.createPrimitiveNode("South", 0)
        qWest = MaxGraph.createPrimitiveNode("West", 3)

        # navigate
        qNavigate_Get = MaxGraph.createCompositeNode("Navigate_Get", [qNorth, qEast, qSouth, qWest], TaxiDecoder.navigate_get_isTerminal, TaxiDecoder.navigate_get_isActive)
        qNavigate_Put = MaxGraph.createCompositeNode("Navigate_Put", [qNorth, qEast, qSouth, qWest], TaxiDecoder.navigate_put_isTerminal, TaxiDecoder.navigate_put_isActive)

        # get
        qPickup = MaxGraph.createPrimitiveNode("Pickup", 4)
        qGet = MaxGraph.createCompositeNode("Get", [qPickup, qNavigate_Get], TaxiDecoder.get_isTerminal, TaxiDecoder.get_isActive)

        # put
        qDropoff = MaxGraph.createPrimitiveNode("Dropoff", 5)
        qPut = MaxGraph.createCompositeNode("Put", [qDropoff, qNavigate_Put], TaxiDecoder.put_isTerminal, TaxiDecoder.put_isActive)

        # root
        root = self.getRoot()
        root.addChild(qGet)
        root.addChild(qPut)




# system imports
import pdb

# user imports
import MaxGraph
import MRTaxiDecoder_flatter as TaxiDecoder

class MRTaxiGraph_flatter(MaxGraph.MaxGraph):
    def constructGraph(self):
        # movement
        qNorth = MaxGraph.createPrimitiveNode("North", 1)
        qEast = MaxGraph.createPrimitiveNode("East", 2)
        qSouth = MaxGraph.createPrimitiveNode("South", 0)
        qWest = MaxGraph.createPrimitiveNode("West", 3)

        # navigate
        qNavigate_Get = MaxGraph.createCompositeNode("Navigate_Get", [qNorth, qEast, qSouth, qWest], TaxiDecoder.navigate_get_isTerminal)
        qNavigate_Put = MaxGraph.createCompositeNode("Navigate_Put", [qNorth, qEast, qSouth, qWest], TaxiDecoder.navigate_put_isTerminal)

        # get
        qPickup = MaxGraph.createPrimitiveNode("Pickup", 4)
        qGet = MaxGraph.createCompositeNode("Get", [qPickup, qNavigate_Get], TaxiDecoder.get_isTerminal)

        # put
        qDropoff = MaxGraph.createPrimitiveNode("Dropoff", 5)
        qPut = MaxGraph.createCompositeNode("Put", [qDropoff, qNavigate_Put], TaxiDecoder.put_isTerminal)

        # root
        root = self.getRoot()
        root.addChild(qGet)
        root.addChild(qPut)


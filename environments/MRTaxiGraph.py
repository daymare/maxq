

# system imports
import pdb

# user imports
import MaxGraph
import TaxiDecoder

class MRTaxiGraph(MaxGraph.MaxGraph):
    def constructGraph(self):
        # movement
        qNorth = MaxGraph.createPrimitiveNode("North", 1)
        qEast = MaxGraph.createPrimitiveNode("East", 2)
        qSouth = MaxGraph.createPrimitiveNode("South", 0)
        qWest = MaxGraph.createPrimitiveNode("West", 3)

        ## navigation
        # room naviation
        qNav_get_r1 = MaxGraph.createCompositeNode("Nav_get_r1", [qNorth, qEast, qSouth, qWest], TaxiDecoder.navigate_get_r1_isTerminal)
        qNav_get_r2 = MaxGraph.createCompositeNode("Nav_get_r2", [qNorth, qEast, qSouth, qWest], TaxiDecoder.navigate_get_r2_isTerminal)
        qNav_get_r3 = MaxGraph.createCompositeNode("Nav_get_r3", [qNorth, qEast, qSouth, qWest], TaxiDecoder.navigate_get_r3_isTerminal)

        qNav_put_r1 = MaxGraph.createCompositeNode("Nav_put_r1", [qNorth, qEast, qSouth, qWest], TaxiDecoder.navigate_put_r1_isTerminal)
        qNav_put_r2 = MaxGraph.createCompositeNode("Nav_put_r2", [qNorth, qEast, qSouth, qWest], TaxiDecoder.navigate_put_r2_isTerminal)
        qNav_put_r3 = MaxGraph.createCompositeNode("Nav_put_r3", [qNorth, qEast, qSouth, qWest], TaxiDecoder.navigate_put_r3_isTerminal)


        # overall navigation
        qNavigate_Get = MaxGraph.createCompositeNode("Navigate_Get", [qNav_get_r1, qNav_get_r2, qNav_get_r3], TaxiDecoder.navigate_get_isTerminal)
        qNavigate_Put = MaxGraph.createCompositeNode("Navigate_Put", [qNav_put_r1, qNav_put_r2, qNav_put_r3], TaxiDecoder.navigate_put_isTerminal)

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


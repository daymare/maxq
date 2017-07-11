import pdb

locations = [(0,0), (4,0), (4,5), (3,9)]


# decode a taxi state
# return list of state features:
# taxirow, taxicolumn, passenger location, destinationid
def decodeTaxiState(taxiState):
    print 
    i = taxiState
    out = []
    out.append(i % 4)
    i = i // 4
    out.append(i % 5)
    i = i // 5
    out.append(i % 10)
    i = i // 10
    out.append(i)
    assert 0 <= i < 5

    out.reverse()
    return out


### termination functions
# all return two values: whether the current state is a terminal state and the value of this terminal state
# thus termination functions specify both the termination function and the pseudo reward function

# primitive
def primitive_isTerminal(state):
    return True, 0

# level 0
def root_isTerminal(state):
    return False, -1

# level 1
def get_isTerminal(state):
    features = decodeTaxiState(state)
    if features[2] == 4:
        return True, 0
    else:
        return False, -1

def put_isTerminal(state):
    features = decodeTaxiState(state)
    if features[2] != 4:
        return True, 0
    else:
        return False, -1

# level 2
def navigate_get_isTerminal(state):
    features = decodeTaxiState(state)
    taxiloc = (features[0], features[1])

    if features[2] == 4:
        return True, -1

    if taxiloc == locations[features[2]]:
        return True, 0
    else:
        return False, -1

def navigate_put_isTerminal(state):
    features = decodeTaxiState(state)
    taxiloc = (features[0], features[1])

    if features[2] != 4:
        return True, -1

    if taxiloc == locations[features[3]]:
        return True, 0
    else:
        return False, -1

# level 3

# walls are defined to the left of where they actually exist
# IE wall is between wall and wall+1
leftWall = 2
rightWall = 6


def isInRoom2(state):
    features = decodeTaxiState(state)
    taxiloc = (features[0], features[1])
    return taxiloc[1] <= rightWall and taxiloc[1] > leftWall

def isInRoom1(state):
    features = decodeTaxiState(state)
    taxiloc = (features[0], features[1])
    return taxiloc[1] <= leftWall

def isInRoom3(state):
    features = decodeTaxiState(state)
    taxiloc = (features[0], features[1])
    return taxiloc[1] > rightWall

def onPassenger(state):
    features = decodeTaxiState(state)
    taxiloc = (features[0], features[1])
    passengerLoc = features[2]
    return taxiloc == locations[passengerLoc]

def onDestination(state):
    features = decodeTaxiState(state)
    taxiloc = (features[0], features[1])
    destinationLoc = features[3]
    return taxiloc == locations[destinationLoc]


def navigate_get_r1_isTerminal(state):
    features = decodeTaxiState(state)
    taxiloc = (features[0], features[1])

    passengerLoc = features[2]

    # check if the passenger is in the taxi
    if passengerLoc == 4:
        return True, -1

    # check if we have achieved the desired location
    if passengerLoc == 0 or passengerLoc == 1:
        # passenger is in this room
        if isInRoom1(state) == False:
            # this must be called in room 1
            return True, -1

        # are we on top of the passenger?
        if onPassenger(state) == True:
            return True, 0
    else:
        # passenger is not in this room
        if inInRoom3(state) == True:
            return True, -1 # cannot call this subtask from room 3

        if isInRoom2(state) == True:
            return True, 0 # successfully went to the next room

    return False, -1


def navigate_get_r2_isTerminal(state):
    features = decodeTaxiState(state)
    taxiloc = (features[0], features[1])

    passengerLoc = features[2]

    # check if the passenger is in the taxi
    if passengerLoc == 4:
        return True, -1

    # check if we have achieved the desired location
    if passengerLoc == 2:
        # passenger is in this room
        if isInRoom2(state) == True:
            if onPassenger(state) == True:
                return True, 0
        else:
            return True, -1

    elif passengerLoc == 0 or passengerLoc == 1:
        # passenger is in the left room
        if isInRoom3(state) == True:
            return True, -1

        if isInRoom1(state) == True:
            return True, 0

    elif passengerLoc == 3:
        # passenger is in the right room
        if isInRoom1(state) == True:
            return True, -1

        if isInRoom3(state) == True:
            return True, 0

    return False, -1

def navigate_get_r3_isTerminal(state):
    features = decodeTaxiState(state)
    taxiloc = (features[0], features[1])

    passengerLoc = features[2]

    # check if the passenger is in the taxi
    if passengerLoc == 4:
        return True, -1

    # check if we have achieved the desired location
    if passengerLoc == 3:
        # passenger is in this room
        if isInRoom3(state) == False:
            return True, -1

        if isInRoom3(state) == True and onPassenger(state) == True:
            return True, 0

    else:
        # passenger is to the left of this room
        if isInRoom1(state) == True:
            return True, -1 # cannot call this from room 1

        if isInRoom2(state) == True:
            return True, 0

    return False, -1

def navigate_put_r1_isTerminal(state):
    features = decodeTaxiState(state)
    taxiloc = (features[0], features[1])

    passengerLoc = features[2]
    destinationLoc = features[3]

    # check if the passenger is in the taxi
    if passengerLoc != 4:
        return True, -1

    # check if we have achieved the desired location
    if destinationLoc == 0 or destinationLoc == 1:
        # destination is in this room
        if isInRoom1(state) == False:
            # this must be called in room 1
            return True, -1

        # are we on top of the passenger?
        if onDestination(state) == True:
            return True, 0
    else:
        # destination is not in this room
        if isInRoom3(state) == True:
            return True, -1 # cannot call this subtask from room 3

        if isInRoom2(state) == True:
            return True, 0 # successfully went to the next room

    return False, -1

def navigate_put_r2_isTerminal(state):
    features = decodeTaxiState(state)
    taxiloc = (features[0], features[1])

    passengerLoc = features[2]
    destinationLoc = features[3]

    # check if the passenger is in the taxi
    if passengerLoc != 4:
        return True, -1

    # check if we have achieved the desired location
    if destinationLoc == 2:
        # destination is in this room
        if isInRoom2(state) == True:
            if onDestination(state) == True:
                return True, 0
        else:
            return True, -1

    elif destinationLoc == 0 or destinationLoc == 1: 
        # destination is in the left room
        if isInRoom3(state) == True:
            return True, -1 # invalid call

        if isInRoom1(state) == True:
            return True, 0 # success

    elif destinationLoc == 3:
        # passenger is in the right room
        if isInRoom1(state) == True:
            return True, -1 # invalid call

        if isInRoom3(state) == True:
            return True, 0 # success

    return False, -1

def navigate_put_r3_isTerminal(state):
    features = decodeTaxiState(state)
    taxiloc = (features[0], features[1])

    passengerLoc = features[2]
    destinationLoc = features[3]

    # check if the passenger is in the taxi
    if passengerLoc != 4:
        return True, -1

    # check if we have achieved the desired location
    if destinationLoc == 3:
        # destination is in this room
        if isInRoom3(state) == False:
            return True, -1 # invalid call

        if isInRoom3(state) == True and onDestination(state) == True:
            return True, 0 # success

    else:
        # destination is to the left of this room
        if isInRoom1(state) == True:
            return True, -1 # cannot call this from room 1

        if isInRoom2(state) == True:
            return True, 0 # success

    return False, -1



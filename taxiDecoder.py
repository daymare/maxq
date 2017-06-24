

locations = [(0,0), (0,4), (4,0), (4,3)]


# decode a taxi state
# return list of state features:
# taxirow, taxicolumn, passenger location, destinationid
def decodeTaxiState(taxiState):
    out = []
    out.append(taxiState % 4)
    taxiState = taxiState // 4
    out.append(taxiState % 5)
    taxiState = taxiState // 5
    out.append(taxiState % 5)
    taxiState = taxiState // 5
    out.append(taxiState)
    assert 0 <= taxiState < 5
    return list(reversed(out))


### termination functions
# all return two values: whether the current state is a terminal state and the value of this terminal state
# thus termination functions specify both the termination function and the pseudo reward function
def primitive_isTerminal(state, parameter=0):
    return True, 0

def root_isTerminal(state, parameter):
    return False, -1

def get_isTerminal(state, parameter=0):
    features = decodeTaxiState(state)
    if features[2] == 5:
        return True, 0
    else:
        return False, -1

def put_isTerminal(state, parameter=0):
    features = decodeTaxiState(state, terminal=0)
    if features[2] != 5:
        return True, 0
    else:
        return False, -1

def navigate_isTerminal(state, parameter):
    features = decodeTaxiState(state)
    taxiloc = (features[0], features[1])

    assert parameter == 0 or parameter == 1

    if parameter == 0:
        # get 
        if taxiloc == locs[features[2]]:
            return True, 0

    elif parameter == 1:
        # put
        if taxiloc == locs[features[3]]:
            return True, 0

    return False, -1
    
    

### Active State functions
# all return whether the current state is valid for the given subproblem
def primitive_isActive(state, parameter):
    return True

def root_isActive(state, parameter):
    return True

def get_isActive(state, parameter):
    features = decodeTaxiState(state)
    return features[2] != 5

def put_isActive(state, parameter):
    features = decodeTaxiState(state)
    return features[2] == 5

def navigate_isActive(state, parameter):
    return True


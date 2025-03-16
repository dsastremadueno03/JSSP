from individual import Individual

# INDIVIDUAL COMPARISON TESTS

ind1 = Individual([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
ind1.fitness = [5, 850]
ind2 = Individual([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
ind2.fitness = [4, 850]

def test_Individual_Min_Tardiness():
    ind2.fitness = [4, 850]
    assert ind1.isBetter(ind2, 0, 0) == False # False because individual 2 tardiness is smaller
    ind2.fitness = [5, 1000]
    assert ind1.isBetter(ind2, 0, 0) == True # True because individual 2 energy cost is bigger
    ind2.fitness = [6, 850]
    assert ind1.isBetter(ind2, 0, 0) == True # True because individual 2 tardiness is bigger
    ind2.fitness = [6, 600]
    assert ind1.isBetter(ind2, 0, 0) == True # True because individual 2 tardiness is bigger
    ind2.fitness = [5, 850] 
    assert ind1.isBetter(ind2, 0, 0) == False # False because both individuals are equal
    assert ind1 == ind2 # True because both individuals are equal
    

def test_Individual_Min_Energy():
    ind2.fitness = [4, 850]
    assert ind1.isBetter(ind2, 0, 1) == False # False because individual 2 tardiness is smaller
    ind2.fitness = [5, 1000]
    assert ind1.isBetter(ind2, 0, 1) == True # True because individual 2 energy cost is bigger
    ind2.fitness = [6, 850]
    assert ind1.isBetter(ind2, 0, 1) == True # True because individual 2 tardiness is bigger
    ind2.fitness = [6, 600]
    assert ind1.isBetter(ind2, 0, 1) == False # False because individual 2 energy cost is smaller
    ind2.fitness = [5, 850] 
    assert ind1.isBetter(ind2, 0, 1) == False # False because both individuals are equal

def test_Individual_Max_Tardiness():
    ind2.fitness = [4, 850]
    assert ind1.isBetter(ind2, 1, 0) == True # True because individual 2 tardiness is smaller
    ind2.fitness = [5, 1000]
    assert ind1.isBetter(ind2, 1, 0) == False # False because individual 2 energy cost is bigger
    ind2.fitness = [6, 850]
    assert ind1.isBetter(ind2, 1, 0) == False # False because individual 2 tardiness is bigger
    ind2.fitness = [6, 600]
    assert ind1.isBetter(ind2, 1, 0) == False # False because individual 2 tardiness is bigger
    ind2.fitness = [5, 850] 
    assert ind1.isBetter(ind2, 1, 0) == False # False because both individuals are equal
    
def test_Individual_Max_Energy():
    ind2.fitness = [4, 850]
    assert ind1.isBetter(ind2, 1, 1) == True # True because individual 2 tardiness is smaller
    ind2.fitness = [5, 1000]
    assert ind1.isBetter(ind2, 1, 1) == False # False because individual 2 energy cost is bigger
    ind2.fitness = [6, 850]
    assert ind1.isBetter(ind2, 1, 1) == False # False because individual 2 tardiness is bigger
    ind2.fitness = [6, 600]
    assert ind1.isBetter(ind2, 1, 1) == True # True because individual 2 energy cost is smaller
    ind2.fitness = [5, 850] 
    assert ind1.isBetter(ind2, 1, 1) == False # False because both individuals are equal
    

test_Individual_Min_Tardiness()
test_Individual_Min_Energy()
test_Individual_Max_Tardiness()
test_Individual_Max_Energy()
print("All tests passed")
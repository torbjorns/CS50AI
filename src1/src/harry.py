from logic import *

rain = Symbol("rain")
hagrid = Symbol("hagrid")
dumbledore = Symbol("dumbledore")

knowledge = And( # These are all the things we know
    Implication(Not(rain), hagrid), # If it's not raining, then Harry visited Hagrid
    Or(hagrid, dumbledore), # Harry visited Hagrid or Dumbledore
    Not(And(hagrid, dumbledore)), # Harry didn't visit both Hagrid and Dumbledore
    dumbledore # Harry visited Dumbledore
)

print("Is it raining?")
print(model_check(knowledge, rain)) # Is it raining?

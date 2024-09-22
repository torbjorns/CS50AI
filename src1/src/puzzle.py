from logic import *

people = ["Gilderoy", "Pomona", "Minerva", "Horace"]
houses = ["Gryffindor", "Hufflepuff", "Ravenclaw", "Slytherin"]

symbols = []

knowledge = And()

for person in people:
    for house in houses:
        symbols.append(Symbol(f"{person}{house}"))

# Each person belongs to a house.
for person in people:
    knowledge.add(Or(
        Symbol(f"{person}Gryffindor"),
        Symbol(f"{person}Hufflepuff"),
        Symbol(f"{person}Ravenclaw"),
        Symbol(f"{person}Slytherin")
    ))

# Only one house per person.
for person in people:
    for h1 in houses:
        for h2 in houses:
            if h1 != h2:
                knowledge.add(
                    Implication(Symbol(f"{person}{h1}"), Not(Symbol(f"{person}{h2}"))) # If person is in house 1, then person is not in house 2
                )

# print("Knowledge after 1: ", knowledge.formula())

# Only one person per house.
for house in houses:
    for p1 in people:
        for p2 in people:
            if p1 != p2:
                knowledge.add(
                    Implication(Symbol(f"{p1}{house}"), Not(Symbol(f"{p2}{house}"))) # If person 1 is in house, then person 2 is not in house
                )

# print("Knowledge after 2: ", knowledge.formula())

knowledge.add(
    Or(Symbol("GilderoyGryffindor"), Symbol("GilderoyRavenclaw")) # Gilderoy is in Gryffindor or Ravenclaw
)

knowledge.add(
    Not(Symbol("PomonaSlytherin")) # Pomona is not in Slytherin
)

knowledge.add(
    Symbol("MinervaGryffindor") # Minerva is in Gryffindor
)

for symbol in symbols:
    if model_check(knowledge, symbol):
        print(symbol)

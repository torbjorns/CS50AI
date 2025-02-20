from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

knowledgeBase = And(
    Or(AKnight, AKnave),  # A is either a knight or a knave
    Not(And(AKnight, AKnave)),  # A is not both a knight and a knave
    Or(BKnight, BKnave),  # B is either a knight or a knave
    Not(And(BKnight, BKnave)),  # B is not both a knight and a knave
    Or(CKnight, CKnave),  # B is either a knight or a knave
    Not(And(CKnight, CKnave)),  # B is not both a knight and a knave
)

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    knowledgeBase,
    Implication(And(AKnight, AKnave), AKnight),  # A is a knight if and only if the statement is true 
    Implication(Not(And(AKnight, AKnave)), AKnave)  # A is a knave if and only if the statement is false
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    knowledgeBase,
    Implication(And(AKnave, BKnave), AKnight),  # A is a knight if both are knaves
    Implication(Not(And(AKnave, BKnave)), AKnave),  # A is a knave if both are not knaves
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    knowledgeBase,
    Implication(Or(And(AKnave, BKnave),And(AKnight, BKnight)), And(AKnight, BKnave)),  # A is a knight and B is a knave if they are the same kind
    Implication(Not(Or(And(AKnave, BKnave),And(AKnight, BKnight))), And(AKnave, BKnight)),  # A is a knave and B is a knight if they are not the same kind
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    knowledgeBase,
    Implication(AKnight,Or(AKnight, AKnave)),  # A is a knight if A is a knight or A is a knave
    Implication(AKnave,Not(Or(AKnight, AKnave))),  # A is a knave if A is not a knight or A is not a knave
    Implication(CKnave, BKnight),  # B is a knight if C is a knave
    Implication(CKnight, BKnave),  # B is a knave if C is a knight
    Implication(AKnight, CKnight),  # C is a knight if A is a knight
    Implication(AKnave, CKnave),  # C is a knave if A is a knave
    Or(Implication(BKnight, Or(Implication(AKnight, AKnave), Implication(AKnave, Not(AKnave)))), Implication(BKnave, Not(Or(Implication(AKnight, AKnave), Implication(AKnave, Not(AKnave)))))) # B is a knight if this statement is true, B is a knave if this statement is false
)

def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()

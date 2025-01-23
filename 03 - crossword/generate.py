import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword

        # Create a dictionary to store the domains of each variable
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        # Fill in letters from variables
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0) 
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        # Fill each cell with white and add a letter
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                # If the cell is blocked, fill it with black
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        # Center the letter in the cell
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        # Remove words that do not have the correct length
        for var in self.crossword.variables:
            for word in self.crossword.words:
                if len(word) != var.length: 
                    self.domains[var].remove(word)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        # Initialize revised as False
        revised = False
        # Get the overlap between x and y
        overlap = self.crossword.overlaps[x, y]

        # Check if there is an overlap between x and y
        if overlap is not None:
            i, j = overlap
            for word_x in self.domains[x].copy():
                if not any(word_x[i] == word_y[j] for word_y in self.domains[y]):
                    self.domains[x].remove(word_x)
                    revised = True
        return revised

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        # Initialize arcs
        if arcs is None:
            arcs = [(x, y) for x in self.crossword.variables for y in self.crossword.neighbors(x)]

        # Check all arcs
        while arcs:
            x, y = arcs.pop(0)
            if self.revise(x, y):
                if not self.domains[x]:
                    return False
                # Add all neighbors of x except y
                for z in self.crossword.neighbors(x) - {y}: 
                    arcs.append((z, x))
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        # Check if all variables are assigned
        return all(var in assignment for var in self.crossword.variables)

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # Check if all words are distinct and do not conflict
        words = set()
        # Check all variables
        for var, word in assignment.items():

            # Check if the word is already assigned to another variable
            if var.length != len(word) or word in words: 
                return False
            words.add(word)
            for neighbor in self.crossword.neighbors(var):

                # Check if the neighbor is already assigned
                if neighbor in assignment: 
                    i, j = self.crossword.overlaps[var, neighbor] 
                    if word[i] != assignment[neighbor][j]: 
                        return False
        return True

    def order_domain_values(self, var, assignment):
        vals_ruleout = {val: 0 for val in self.domains[var]}

        for neighbor in self.crossword.neighbors(var):
            if neighbor not in assignment:
                i, j = self.crossword.overlaps[var, neighbor]
                for val in self.domains[var]:
                    # Count how many neighbor values the current value rules out
                    ruled_out = sum(
                        1 for neighbor_val in self.domains[neighbor] 
                        if val[i] == neighbor_val[j]
                    )
                    vals_ruleout[val] += ruled_out

        return [val for val, _ in sorted(vals_ruleout.items(), key=lambda x: x[1], reverse=True)]
    
    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        # Get all unassigned variables
        unassigned = self.crossword.variables - set(assignment)
        # Return the variable with the minimum number of remaining values
        return min(unassigned, key=lambda var: (len(self.domains[var]), -len(self.crossword.neighbors(var))))

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # Check if the assignment is complete
        if self.assignment_complete(assignment):
            return assignment
        # Select an unassigned variable
        var = self.select_unassigned_variable(assignment)

        # Try all possible values for the variable
        for value in self.order_domain_values(var, assignment):
            assignment[var] = value
            if self.consistent(assignment):
                result = self.backtrack(assignment)
                if result is not None:
                    return result
            del assignment[var]
        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()

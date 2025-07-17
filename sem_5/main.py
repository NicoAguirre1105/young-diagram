import random
import time
import matplotlib.pyplot as plt

class Diagram:
    def __init__(self):
        self.cells = set()

        #Initial state
        self.cells.add((0, 0))
        
    def get_possible_moves(self):
        
        #Find all possible movements. 
        #A cell can be added if there would be a cell already to his left and down (or that it is close to the x or y axis).

        possible_moves = set()
        for x, y in self.cells:
            
            #All neighbors
            neighbors = [(x + 1, y), (x, y + 1)]
            for x, y in neighbors:
                # If the space has been taken already
                if (x, y) not in self.cells:
                    # Check if it has a cell at the left and down.
                    # if (((x - 1, y) in self.cells)) or (((x, y - 1) in self.cells)):
                    if (((x - 1, y) in self.cells) or (x - 1 == -1)) and (((x, y - 1) in self.cells) or (y - 1 == -1)):
                        possible_moves.add((x, y))
        return possible_moves
    
    def get_S(self, c, alpha=1):
    
        #Compute S(c) = (perimeter of rectangle defined by (0,0) and c) raised to the power alpha.
        
        x, y = c
        perimeter = (x + y + 2)*2
        return perimeter ** alpha
    
    def add_cell(self, c):
        # Add a selected cell into diagram
        self.cells.add(c)
        
    def simulate(self, n_steps=1000, alpha=1):
        #Simulates n_steps times the diagram selection 
        for step in range(n_steps):
            # Get all addable cells
            possible_moves = self.get_possible_moves()
            S_values = []
            cells_list = list(possible_moves)
            # Compute S(c) for each possible cell
            for c in cells_list:
                S_values.append(self.get_S(c, alpha))
            # Compute probabilities for each cell
            total_S = sum(S_values)
            probabilities = [S / total_S for S in S_values]
            # Randomly select a cell to add based on probabilities
            c = random.choices(cells_list, weights=probabilities, k=1)[0]
            self.add_cell(c)
                
    def visualize(self, tic, filename=None):

        # Diagram using matplot

        x_coords = [x for x, y in self.cells]
        y_coords = [y for x, y in self.cells]
        plt.scatter(x_coords, y_coords, marker='s', s=1)
        plt.gca().set_aspect('equal', adjustable='box')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('Diagram after {} steps'.format(len(self.cells) - 1))
        if filename:
            plt.savefig(filename)
        toc = time.perf_counter()
        print("TIME:", toc-tic)
        plt.show()
        
    def save_cells(self, filename):
        """
        Save the list of cells to a file.
        """
        with open(filename, 'w') as f:
            for x, y in sorted(self.cells):
                f.write(f'{x},{y}\n')

def main():
    tic = time.perf_counter()
    alpha = 0.8       
    n_steps = 10000
    diagram = Diagram()
    diagram.simulate(n_steps=n_steps, alpha=alpha)
    diagram.visualize(tic, filename='diagram.png')
    diagram.save_cells('diagram_cells.txt')

if __name__ == '__main__':
    main()
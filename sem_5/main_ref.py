import random
import time
import matplotlib.pyplot as plt

class Diagram:
    def __init__(self):
        self.cells = list()

        #Initial state
        self.cells.append(1)
    
    def get_S(self, c, alpha=1):
    
        #Compute S(c) = (perimeter of rectangle defined by (0,0) and c) raised to the power alpha.
        
        x, y = c
        perimeter = (x + y)*2
        return perimeter ** alpha
        
    def simulate(self, n_steps=1000, alpha=1):
        #Simulates n_steps times the diagram selection 
        for step in range(n_steps):
            # Get all addable cells
            S_values = []
            possible_moves = list()
            # Compute S(c) for each possible cell
            for x in range (0, len(self.cells)):
                y = self.cells[x]
                if(x == 0 or (self.cells[x - 1] > y)):
                    possible_moves.append(x)
                    S_values.append(self.get_S((x, y + 1), alpha))
            possible_moves.append(len(self.cells))
            S_values.append(self.get_S((len(self.cells), 1), alpha))
            # Compute probabilities for each cell
            total_S = sum(S_values)
            probabilities = [S / total_S for S in S_values]
            # Randomly select a cell to add based on probabilities
            c = random.choices(possible_moves, weights=probabilities, k=1)[0]
            if(c == len(self.cells)):
                self.cells.append(1)
            else:
                self.cells[c] += 1
                
    def visualize(self, tic, n_steps, filename=None):

        # Diagram using matplot

        x_coords = []
        y_coords = []
        for x in range(0, len(self.cells)):
            for y in range(0, self.cells[x]):
                x_coords.append(x)
                y_coords.append(y)
        plt.scatter(x_coords, y_coords)
        plt.gca().set_aspect('equal', adjustable='box')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('Diagram after {} steps'.format(n_steps))
        if filename:
            plt.savefig(filename)
        toc = time.perf_counter()
        print("TIME:", toc - tic)
        plt.show()
        
    def save_cells(self, filename):
        """
        Save the list of cells to a file.
        """
        with open(filename, 'w') as f:
            for x in range(0, len(self.cells)):
                for y in range(0, self.cells[x]):
                    f.write(f'{x},{y}\n')

def main():
    tic = time.perf_counter()
    alpha = 1        
    n_steps = 1000  
    diagram = Diagram()
    diagram.simulate(n_steps=n_steps, alpha=alpha)
    diagram.visualize(tic, filename='diagram.png', n_steps=n_steps)
    diagram.save_cells('diagram_cells.txt')

if __name__ == '__main__':
    main()
import random
import time
import matplotlib.pyplot as plt
import os

class Frequency_Diagram:
    def __init__(self):
        self.diagrams = list()
        self.cells = set()
        self.colors_options = ["#00ff00","#d1ff00","#ecff00","#ffff00","#ffdc00","#ffa600","#ff7800","#ff4200","#ff0000","#d60808"]
        self.colors = list()

    def create_diagrams(self, n_diagrams, n_steps, alpha=1):
        
        for i in range(0, n_diagrams):   
            diagram = Diagram()
            diagram.simulate(n_steps=n_steps, alpha=alpha)
            self.diagrams.append(diagram)
            diagram.save_cells("diagram_cells" + str(i + 1) + ".txt")
            # if(i <= (n_diagrams - 1)/2):
            #     self.colors_options.append('#%02x%02x%02x' % (int((i/((n_diagrams-1)/2))*255), 255, 0))
            # else:
            #     self.colors_options.append('#%02x%02x%02x' % (255, int(1 - (((n_diagrams-1) - i)/((n_diagrams-1)/2))*255), 0))

    
    def count_reps(self):
        all_cells = []
        for diagram in self.diagrams:
            all_cells += list(diagram.all_cells)
        
        for cell in all_cells:
            self.cells.add((cell, all_cells.count(cell)))

    def generate_colors(self):
        for cell, count in self.cells:
            self.colors.append(self.colors_options[count - 1])

    def visualize(self, filename=None):
        self.count_reps()
        self.generate_colors()
        x_coords = [x for (x, y), count in self.cells]
        y_coords = [y for (x, y), count in self.cells]
        plt.figure(figsize=(10, 10))
        plt.scatter(x_coords, y_coords, c=self.colors, marker='s', s=1)
        plt.gca().set_aspect('equal', adjustable='box')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('Frequency diagram')
        if filename:
            plt.savefig(filename)
        plt.show()



class Diagram:
    def __init__(self):
        self.cells = list()
        self.all_cells = set()
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
        
    def save_cells(self, filename):
        """
        Save the list of cells to a file.
        """
        with open(filename, 'w') as f:
            for x in range(0, len(self.cells)):
                for y in range(0, self.cells[x]):
                    self.all_cells.add((x, y))
                    f.write(f'{x},{y}\n')

def main():
    tic = time.perf_counter()
    alpha = 1.2       
    n_steps = 1000
    n_diagrams = 10
    freq_diagram = Frequency_Diagram()
    freq_diagram.create_diagrams(n_diagrams, n_steps, alpha=alpha)
    freq_diagram.visualize('rep_diagram.png')

if __name__ == '__main__':
    main()
import random
import matplotlib.pyplot as plt
import time
import math

def get_S(x, y, alpha):
    perimeter = (x + y + 2) * 2 # +2 is because we have index x starting from 0 and we are searching one y + 1 (the cell above the one we already have)
    return perimeter ** alpha

def select_move(possible_moves, weights):
    total = sum(weights)
    r = random.uniform(0, total)
    upto = 0
    for item, weight in zip(possible_moves, weights):
        upto += weight
        if upto >= r:
            return item
        
def update_diff(left_value, diagram_value, max_diff):
    if left_value < diagram_value and diagram_value - left_value > max_diff: #other case dont change values max_diff nor left_value
        max_diff = diagram_value - left_value
        return left_value, max_diff
    elif left_value > diagram_value:
        max_diff = max_diff + left_value - diagram_value
        left_value = diagram_value
        return left_value, max_diff
    return left_value, max_diff

    
# if left_value == 0:
#     left_value = diagram_value
# else:
#     if left_value < diagram_value:
#         if diagram_value - left_value > max_diff:
#             max_diff = diagram_value - left_value
#     else:
#         max_diff = max_diff + left_value - diagram_value
#         left_value = diagram_value


def visualize_data(steps, columns, diff, values):
    ## Uncomment the following lines to visualize the data for m > 1

    # plt.figure(figsize=(12, 6))

    # plt.subplot(1, 2, 1)
    # plt.plot(steps, diff, marker='o', linestyle='-', color='b')
    # plt.title('Maximum Difference Between Diagrams')
    # plt.xlabel('Number of Cells')
    # plt.ylabel('Maximum Difference')

    # plt.subplot(1, 2, 2)
    # plt.plot(steps, values, marker='o', linestyle='-', color='r')
    # plt.title('Average Length of the Diagram')
    # plt.xlabel('Number of Cells')
    # plt.ylabel('Average Length')



    ## Uncomment the following lines to visualize the data for m=1

    plt.figure(figsize=(8, 8))
    plt.plot(steps, values, marker='o', linestyle='-', color='r')
    plt.title('Coefficient c_(alpha) calculated for every step')
    plt.xlabel('Number of Cells')
    plt.ylabel('Coefficient c_(alpha)')

    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(8, 8))
    plt.plot(steps, columns, marker='o', linestyle='-', color='g')
    plt.title('Average Length of the Diagram vs Number of Cells')
    plt.xlabel('Number of Cells')
    plt.ylabel('Coefficient c_(alpha)')

    plt.tight_layout()
    plt.show()


class Diagram:
    def __init__(self, max_len):
        self.columns = [1]
        self.len = 1
        self.max_len = max_len
        self.poss_moves_column = []
        self.poss_moves_weight = []

    def get_new_cell(self,alpha):
        for x in range(self.len):
            if x == 0 or self.columns[x-1] > self.columns[x]: # first column
                s_value = get_S(x, self.columns[x], alpha)
                self.poss_moves_column.append(x)
                self.poss_moves_weight.append(s_value)
        
        x = self.len # add a new column
        s_value = get_S(x, 0, alpha)
        self.poss_moves_column.append(x)
        self.poss_moves_weight.append(s_value)

        return select_move(self.poss_moves_column, self.poss_moves_weight)

    ## Uncomment the following lines to visualize the diagram after each simulation

    def visualize(self):
        x_coords = []
        y_coords = []
        for x in range(len(self.columns)):
            for y in range(self.columns[x]):
                x_coords.append(x)
                y_coords.append(y)
          
        plt.scatter(x_coords, y_coords, marker='s', s=1)
        plt.gca().set_aspect('equal', adjustable='box')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.show()


    def simulate_young_diagram(self, n, columns, step, steps, values, alpha=1):
        idx = 0
        for i in range(n):
            x = self.get_new_cell(alpha)
            if x == self.len:
                self.len += 1
                self.columns.append(0)
            self.columns[x] += 1
            if (i + 1) == step*(idx + 1):
                values.append(self.len / math.sqrt(i + 1))
                steps.append(i + 1)
                columns.append(self.len)
                idx += 1
            self.poss_moves_column.clear()
            self.poss_moves_weight.clear()
 
def main():
    m = int(input("Enter the number of repetitions (m): ")) #How many times to repeat the simulation for each number of cells
    n = int(input("Enter the maximum number of cells (n): ")) #Maximum number of cells in the diagram
    step = int(input("Enter the step value: ")) #Step value for difference of number of cells between diagrams
    alpha = int(input("Enter alpha value: ")) #Alpha value for the S function

    steps = [] #Save steps for visualization
    values = [] #Save avg_value for each step
    diff = [] #Save avg_value's maximum difference given between m repetitions
    columns = [] #Save value for l_n

    start = time.time()

    for i in range(m):
        diagram = Diagram(int(5 * math.sqrt(n)))  # Maximum length of the diagram with approximate value of 5*sqrt(n)
        diagram.simulate_young_diagram(n, columns, step, steps, values, alpha)
        
        print("Time taken: ", time.time() - start)
        diagram.visualize()

    visualize_data(steps, columns, diff, values)

if __name__ == "__main__":
    main()
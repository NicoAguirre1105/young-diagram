import random 
import matplotlib.pyplot as plt
import time
import math
from mpmath import mp 

## More clear and readable but slower and tends to change experiment's duration a lot         
# def select_move(possible_moves, weights):
#     return random.choices(possible_moves, weights=weights, k=1)[0]
        
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


def visualize_data(steps, columns, diff, values, results, n, m, alpha, step):
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
    plt.savefig(f'c_alpha({n},{m},{alpha},{step}).pdf', format='pdf', bbox_inches='tight')
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(8, 8))
    plt.plot(steps, columns, marker='o', linestyle='-', color='g')
    plt.title('Average Length of the Diagram vs Number of Cells')
    plt.xlabel('Number of Cells')
    plt.ylabel('Coefficient c_(alpha)')
    plt.savefig(f'col_value({n},{m},{alpha},{step}).pdf', format='pdf', bbox_inches='tight')
    plt.tight_layout()
    plt.show()

    print(results)


class Diagram:
    def __init__(self):
        self.columns = [1]
        self.len = 1
        self.poss_moves_column = [0]
        self.poss_moves_weight = [1]
        self.last_idx = 0

    def get_S(self, x, y, alpha):
        perimeter = (x + y + 2) * 2 # +2 is because we have index x starting from 0 and we are searching one y + 1 (the cell above the one we already have)
        if perimeter ** alpha == 0.0:
            return mp.mpf(perimeter) ** alpha
        return perimeter ** alpha
    
    def select_move(self):
        total = sum(self.poss_moves_weight)
        r = random.uniform(0, total)
        upto = 0
        count = 0
        for item, weight in zip(self.poss_moves_column, self.poss_moves_weight):
            upto += weight
            if upto >= r:
                self.last_idx = count
                return item
            count += 1
    
    def get_poss_moves(self, alpha):
        check_done = False
        x = self.poss_moves_column[self.last_idx]
        next_x = self.poss_moves_column[self.last_idx + 1] if self.last_idx + 1 < len(self.poss_moves_column) else None
        if x == 0 or self.columns[x-1] > self.columns[x]:
            s_value = self.get_S(x, self.columns[x], alpha)
            self.poss_moves_weight[self.last_idx] = s_value
            self.last_idx += 1
        else:
            self.poss_moves_column.pop(self.last_idx)
            self.poss_moves_weight.pop(self.last_idx)
        while not check_done:  
            if next_x is not None and x + 1 == next_x: #En caso que ya se haya agregado el siguiente
                check_done = True
                continue
            
            if x + 1 == self.len: #En caso que se agrego el ultimo la vex pasada
                s_value = self.get_S(x + 1, 0, alpha)
                self.poss_moves_column.append(x + 1)
                self.poss_moves_weight.append(s_value)
                check_done = True 
                continue


            x += 1
            if self.columns[x-1] > self.columns[x]: 
                s_value = self.get_S(x, self.columns[x], alpha)
                self.poss_moves_column.insert(self.last_idx, x)
                self.poss_moves_weight.insert(self.last_idx, s_value)
                self.last_idx += 1

    def get_new_cell(self, alpha):
        self.get_poss_moves(alpha)
        return self.select_move()


    # def get_new_cell(self,alpha):
    #     for x in range(self.len):
    #         if x == 0 or self.columns[x-1] > self.columns[x]: # first column
    #             s_value = get_S(x, self.columns[x], alpha)
    #             poss_moves_column.append(x)
    #             poss_moves_weight.append(s_value)
        
    #     x = self.len # add a new column
    #     s_value = get_S(x, 0, alpha)
    #     poss_moves_column.append(x)
    #     poss_moves_weight.append(s_value)

    #     return select_move(poss_moves_column, poss_moves_weight)

    ## Uncomment the following lines to visualize the diagram after each simulation

    def visualize(self, n, m, alpha, step):
        x_coords = []
        y_coords = []
        for x in range(len(self.columns)):
            for y in range(self.columns[x]):
                x_coords.append(x)
                y_coords.append(y)
          
        plt.figure(figsize=(8, 8))
        plt.scatter(x_coords, y_coords, marker='s', s=1)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('Young Diagram Visualization')
        plt.tight_layout()
        plt.savefig(f'diagram({n},{m},{alpha},{step}).pdf', format='pdf', bbox_inches='tight')
        plt.show()


    def simulate_young_diagram(self, n, columns, step, steps, values, alpha, sqrt_cache):
        idx = 0

        for i in range(n):
            x = self.get_new_cell(alpha)
            if x == self.len:
                self.len += 1
                self.columns.append(0)
            self.columns[x] += 1
            if (i + 1) == step*(idx + 1):
                values.append(self.len / sqrt_cache[idx]) #Average length of the diagram
                if len(steps) < n//step:
                    steps.append(i + 1)
                columns.append(self.len)
                idx += 1
 
def main():
    mp.dps = 700  # Set the precision for mpmath
    m = int(input("Enter the number of repetitions (m): ")) #How many times to repeat the simulation for each number of cells
    n = int(input("Enter the maximum number of cells (n): ")) #Maximum number of cells in the diagram
    step = int(input("Enter the step value: ")) #Step value for difference of number of cells between diagrams
    alpha = float(input("Enter alpha value: ")) #Alpha value for the S function

    diff = [] #Save avg_value's maximum difference given between m repetitions
    steps = [] #Save steps for visualization
    results = [0] * m #Save results for m repetitions
    sqrt_cache = [math.sqrt(i) for i in range(step, n + 1, step)] #This is for m>1, to speed up the calculation of sqrt(i + 1)
    start = time.time()

    for i in range(m):
        values = [] #Save avg_value for each step
        columns = [] #Save value for l_n

        diagram = Diagram()  # Maximum length of the diagram with approximate value of 5*sqrt(n)
        diagram.simulate_young_diagram(n, columns, step, steps, values, alpha, sqrt_cache)
        results[i] = values[-1]

    print("Time taken: ", time.time() - start)
    diagram.visualize(n, m, alpha, step)

    visualize_data(steps, columns, diff, values, results, n, m, alpha, step)

if __name__ == "__main__":
    main()
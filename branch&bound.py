# a class as a data structure to store info of each node
class Node:
    def __init__(self, level, profit, weight, bound, includes):
        self.level = level           # level of node (its height in tree) 
        self.profit = profit         # sum of value choices in includes
        self.weight = weight         # sum of weights of choices in includes
        self.bound = bound           # imaginary possible profit in this choice
        self.includes = includes     # all choices to get here (0 & 1 representing from first item  0 shows not included , and 1 shows included)

# main hosting function 
def knapsack(weights, values, W):
    # find items count
    n = len(weights) 
       
    # variables for comparing each node & storing choices
    max_profit = 0      
    best_solution = []
    
    # node to start (root)
    initial_node = Node(-1, 0, 0, 0, [])
    
    # func 1
    def calculation(node):
        if node.weight >= W:
            return 0
        
        bound = node.profit
        nodelevel = node.level + 1
        total_weight = node.weight
 
        # add values to bound , unless it goes over the limit or the items choice exeed the item count
        while nodelevel < n and total_weight + weights[nodelevel] <= W:
            total_weight += weights[nodelevel]
            bound += values[nodelevel]
            nodelevel += 1

        # if there is still 1 item slot left (less the item count added) , we can atleast dd a fraction of that one item left
        if nodelevel < n:
            bound += (W - total_weight) * (values[nodelevel] / weights[nodelevel])

        return bound
    
    # fun 2
    def recursive(parent):
        # use of none local to link this 2 varibales to the same name used in the hosting func to update them each time we take a step
        nonlocal max_profit, best_solution  
        
        # create left and right child (on with the item included and one without same item included)
        # we do choose a rule that always going to right means not including an item , and left means adding that item to includes(chosen items list)
        if parent.bound > max_profit:      
            left_child = Node(parent.level + 1, parent.profit + values[parent.level + 1], parent.weight + weights[parent.level + 1], 0, parent.includes + [1])
            right_child = Node(parent.level + 1, parent.profit, parent.weight, 0, parent.includes + [0])
            
            #calculate bound for each new node
            left_child.bound = calculation(left_child)
            right_child.bound = calculation(right_child)
            
            # beacuse going right does not add any value , we just compare left child with parent, if it adds value and dont exeed the max weight possible it replaces as answer
            if left_child.weight <= W and left_child.profit > max_profit:
                max_profit = left_child.profit
                best_solution = left_child.includes
            
            # peymayesh arzi
            if left_child.bound > max_profit:
                recursive(left_child)

            if right_child.bound > max_profit:
                recursive(right_child)
                
    # start calculation and comparing from the root created witch has 0 items and has the most estimated value 
    initial_node.bound = calculation(initial_node)
    recursive(initial_node)
    
    return best_solution, max_profit

# Example entry:
weights = [2,5,10,5,4]
values = [40,30,50,10,4]
W = 16

# first call of the main function 
result, total_value = knapsack(weights, values, W)

# incase the answer list length is less thean number of items append zero untill ,so we reach have 0/1 for each item

while(len(result)!= len(weights)):
    result.append(0)

# printing values 
print(f"\n* Max weight : {W}\n* Values : {values} \n* Weights : {weights}")
print("\n* Choosed items :", result)
print("* Total value :", total_value)
print()
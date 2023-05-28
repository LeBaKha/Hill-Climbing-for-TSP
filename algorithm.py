import random
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# Tạo ma trận khoảng cách ngẫu nhiên dựa trên số lượng thành phố
def create_distance_matrix(num_cities):
    distance_matrix = []
    for i in range(num_cities):
        row = []
        for j in range(num_cities):
            if i == j:
                row.append(0)
            elif j > i:
                row.append(random.randint(1, 300))
            else:
                row.append(distance_matrix[j][i])
        distance_matrix.append(row)
    return distance_matrix

# Tạo ra một giải pháp ngẫu nhiên ban đầu để thực hiện
def randomSolution(num_cities):
    cities = list(range(num_cities))
    solution = []
    for i in range(num_cities):
        randomCity = random.choice(cities)
        solution.append(randomCity)
        cities.remove(randomCity)
    return solution
   
# Tính độ dài quãng đường
def routeLength (tsp, solution): 
    routeLength = 0 
    for i in range(len(solution)):
        routeLength += tsp[solution[i - 1]][solution[i]] 
    return routeLength 

# Tạo ra các giải pháp hàng xóm
def getNeighbours(solution):
    neighbours = []
    for i in range(len(solution)):
        for j in range(i + 1, len(solution)):
            neighbour = solution.copy()
            neighbour[i] = solution[j]
            neighbour[j] = solution[i]
            neighbours.append(neighbour)
    return neighbours

# Tạo ra giải pháp tốt nhất và đường đi tốt nhất
def getBestNeighbour (tsp, neighbours): 
    bestRouteLength = routeLength(tsp, neighbours[0]) 
    bestNeighbour = neighbours[0]  
    for neighbour in neighbours:  
        currentRouteLength = routeLength(tsp, neighbour) 
        if currentRouteLength < bestRouteLength: 
            bestRouteLength = currentRouteLength  
            bestNeighbour = neighbour 
    return bestNeighbour, bestRouteLength 


#Áp dụng thuật toán và in kết quả
def hillClimbing(num_cities):
    tsp = create_distance_matrix(num_cities)
    print("Ma trận khoảng cách:")
    for row in tsp:
        print(row)
    return ""

class HillClimbing():
    def __init__(self, num_cities):
        self.matrix = None
        self.result = None
        self.isRunning = True
        self.num_cities = num_cities
    def create_plot(self):
        print((self.matrix))
        distance = np.array(self.matrix)
        G = nx.from_numpy_array(distance)
        print(G)
        pos = nx.spring_layout(G)
        # Vẽ các đỉnh và cạnh của đồ thị bằng Matplotlib
        nx.draw_networkx_nodes(G, pos, node_color='r')
        nx.draw_networkx_edges(G, pos)
        nx.draw_networkx_labels(G, pos)
        
        # Hiển thị đồ thị
        plt.show()
       
    def solve(self):
        self.matrix = create_distance_matrix(self.num_cities)
        currentSolution = randomSolution(self.num_cities)
        self.result = "Giải pháp ngẫu nhiên đầu tiên là: " + str([city for city in currentSolution]) + "\n"
        currentRouteLength = routeLength(self.matrix, currentSolution)
        self.result += "Độ dài quãng đường ngẫu nhiên đầu tiên là: " + str(currentRouteLength) + "\n"
        neighbours = getNeighbours(currentSolution)
        self.result += "Các giải pháp hàng xóm được tạo ra:\n"
        for neighbour in neighbours:
            neighbour_route_length = routeLength(self.matrix, neighbour)
            self.result += "   " + str([city for city in neighbour]) + " - Độ dài quãng đường hàng xóm này: " + str(neighbour_route_length) + "\n"
        bestNeighbour, bestNeighbourRouteLength = getBestNeighbour(self.matrix, neighbours)
        while bestNeighbourRouteLength < currentRouteLength:
            currentSolution = bestNeighbour
            currentRouteLength = bestNeighbourRouteLength
            neighbours = getNeighbours(currentSolution)
            bestNeighbour, bestNeighbourRouteLength = getBestNeighbour(self.matrix, neighbours)
        self.result += "Giải pháp tốt nhất: " + str([city for city in currentSolution]) + "\n"
        self.result += "Quãng đường ngắn nhất: " + str(currentRouteLength) + "\n"
        return currentSolution

def main(): 
    # Nhập vào số lượng thành phố
    num_cities = int(input("Số lượng thành phố cần đi qua: ")) 

    if num_cities >= 2 :
        print(hillClimbing(num_cities))
        hill = HillClimbing(num_cities)
        hill.solve() 
        print(hill.result)
        hill.create_plot()
    else :
        print("Hãy nhập số lượng thành phố >= 2 !!!")

if __name__ == "__main__":
    main()
      



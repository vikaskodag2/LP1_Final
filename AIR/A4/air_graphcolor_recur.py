
class graph :
    def __init__(self) :
        self.n = int(input())
        self.edges = int(input())
        self.max_color = int(input())
        self.adj = [[] for i in range (self.n)]
        self.color = [-1 for _ in range (self.n)]

    def input_graph(self) :
        for _ in range (self.edges) :
            x, y = map(int, input().split(" "))
            x -= 1
            y -= 1
            self.adj[x].append(y)
            self.adj[y].append(x)

    def clear_graph(self) :
        for i in range (self.n) :
            self.color[i] = -1

    def is_valid(self, cur, col) :
        for i in self.adj[cur] :
            if self.color[i] == col :
                return False
        return True
    
    def color_graph(self, cur) :
        if cur == self.n :
            return True
        for i in range (self.max_color) :
            if self.is_valid(cur, i) :
                self.color[cur] = i
                if self.color_graph(cur + 1) :
                    return True
                self.color[cur] = -1
        return False

    def print_sol(self) :
        for i in self.color :
            print(i + 1, end = " ")
        print()

    def min_m(self) :
        for i in range (1, self.n + 1) :
            self.clear_graph()
            self.max_color = i
            if self.color_graph(0) :
                return i

b = graph()
b.input_graph()
if b.color_graph(0) :
    b.print_sol()
else :
    print("No solution")    
    print("min color req : " + str(b.min_m()))
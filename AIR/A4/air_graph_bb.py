import queue, copy

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

    def is_valid(self, cur, col, color) :
        for i in self.adj[cur] :
            if color[i] == col :
                return False
        return True

    def is_end(self, col) :
        if -1 not in col :
            return True
        return False

    def colors_used(self, col) :
        return max(col) + 1

    def possible_colors(self, col) :
        p = []
        for i in col :
            if i != -1 :
                p.append(i)
        return p

    def color_graph(self) :
        cur_best = self.n
        q = queue.Queue()
        color = [-1 for _ in range (self.n)]
        color[0] = 0
        q.put(color)
        itr = 0
        while q.qsize() > 0 :
            itr += 1
            cur = q.get()
            if self.is_end(cur) :
                if cur_best >= self.colors_used(cur) :
                    cur_best = self.colors_used(cur)
                    self.color = copy.deepcopy(cur)
                    continue
            
            possible_colors = self.possible_colors(cur)
            for i in range (self.n) :
                if cur[i] == -1 :
                    for j in possible_colors :
                        duplicate = copy.deepcopy(cur)
                        if self.is_valid(i, j, duplicate) :
                            duplicate[i] = j
                            if self.colors_used(duplicate) <= cur_best :
                                q.put(duplicate)
                    duplicate = copy.deepcopy(cur)
                    duplicate[i] = self.colors_used(duplicate)
                    if self.colors_used(duplicate) <= cur_best :
                        q.put(duplicate)

    def print_sol(self) :
        for i in self.color :
            print(i + 1, end = " ")

g = graph()
g.input_graph()
g.color_graph()
if g.colors_used(g.color) <= g.max_color :
    g.print_sol()
else :
    print("colors req  : " + str(g.colors_used(g.color)))
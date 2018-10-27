import queue as q
import math, time, copy

class game :
    def __init__(self) :
        self.n = 0
        self.initial_state = []
        self.final_state = []
        self.visited = set()
        self.pq = q.PriorityQueue()
        self.num_pos = {}
        self.trace_game = {}
        self.solvable = True

        self.n = int(input())
        for _ in range (self.n) :
            l = list(map(int, input().split(" ") ))
            self.initial_state.append(l)
        for _ in range (self.n) :
            l = list(map(int, input().split(" ") ))
            self.final_state.append(l)

        for i in range (self.n) :
            for j in range (self.n) :
                self.num_pos[self.final_state[i][j]] = (i, j)

    def is_valid(self, i, j) :
        if i < 0 or i >= self.n or j < 0 or j >= self.n :
            return False
        return True

    def gen_move(self, board) :
        moves = []
        for i in range (self.n) :
            for j in range (self.n) :
                if board[i][j] == 0 :
                    if self.is_valid(i - 1, j) :
                        moves.append( (i - 1, j) )
                    if self.is_valid(i + 1, j) :
                        moves.append( (i + 1, j) )
                    if self.is_valid(i, j - 1) :
                        moves.append( (i, j - 1) )
                    if self.is_valid(i, j + 1) :
                        moves.append( (i, j + 1) )
        return moves 

    def heuristic(self, state) :
        cost = 0
        for i in range (self.n) :
            for j in range (self.n) :
                pos = self.num_pos[state[i][j]]
                cost += abs(i - pos[0]) + abs(j - pos[1])
        return cost

    def zero_pos(self, board):
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j]==0:
                    return (i,j)

    def tuple_for_list(self, board) :
        tup = tuple(tuple(_) for _ in board)
        return tup

    def list_for_tuple(self, board) :
        l = [list(_) for _ in board]
        return l

    def play(self) :
        itr = 0
        self.pq.put( ( (0, 0), self.tuple_for_list(self.initial_state) ) )
        self.trace_game[self.tuple_for_list(self.initial_state)] = self.tuple_for_list(self.initial_state)
        while self.pq.qsize() > 0 :
            cur_node = self.pq.get()
            board = self.list_for_tuple(cur_node[1])
            if self.tuple_for_list(board) in self.visited :
                continue
            self.visited.add(self.tuple_for_list(board))
            if board == self.final_state :
                print("Moves req : " + str(cur_node[0][1]))
                return
            
            pos_zero = self.zero_pos(board)

            moves = self.gen_move(board)
            for i in moves :
                duplicate = copy.deepcopy(board)
                duplicate[pos_zero[0]][pos_zero[1]] = duplicate[i[0]][i[1]]
                duplicate[i[0]][i[1]] = 0
                if self.tuple_for_list(duplicate) in self.visited :
                    continue
                ht = cur_node[0][1]
                self.trace_game[self.tuple_for_list(duplicate)] = self.tuple_for_list(board)
                self.pq.put( ( (ht + 1 + self.heuristic(duplicate), ht + 1), self.tuple_for_list(duplicate) ) )

            itr += 1
            if(itr > 10 ** 6) :
                print("Probably not solvable!!")
                self.solvable = False
                return
    
    def print_grid(self, board) :
        for i in board :
            for j in i :
                print(j, end = " ")
            print()

    def print_seq(self) :
        if self.solvable :
            move_seq = []
            cur = self.tuple_for_list(self.final_state)
            while cur != self.trace_game[cur] :
                move_seq.append(cur)
                cur = self.trace_game[cur]
            move_seq.append(self.initial_state)
            move_seq.reverse()
            for _ in move_seq :
                self.print_grid(_)
                print()
        else :
            print("No sequence!!")

g = game()
g.play()
g.print_seq()
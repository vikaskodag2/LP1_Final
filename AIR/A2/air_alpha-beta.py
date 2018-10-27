import random, queue

class node :
    def __init__(self, val, child, alpha, beta) :
        self.val = val
        self.child = child
        self.alpha = alpha
        self.beta = beta 
        self.child_ptr = [None]*child

MAX = 10 ** 3

def randnum() :
    return random.randint(1, 100)

def no_branches() :
    return 2
    # return random.randint(1, 4)

def alpha_beta(depth, motive, alpha, beta, go_down) :
    if depth >= 3 :
        if not go_down :
            return(-1000, node(-1000, 0, -MAX, MAX))
        val = randnum()
        return (val, node(val, 0, -MAX, MAX))
    if motive :
        best = -MAX
        children = no_branches()
        p = node(best, children, alpha, beta)
        for i in range (children) :
            child = alpha_beta(depth + 1, (motive ^ 1), alpha, beta, go_down)
            p.child_ptr[i] = child[1]
            if go_down :
                best = max(best, child[0])
                alpha = max(best, alpha)
            if alpha >= beta :
                go_down = False
        p.val = best
        p.alpha = best
        p.beta = beta
        return (best, p)
    else :
        best = MAX
        children = no_branches()
        p = node(best, children, alpha, beta)
        for i in range (children) :
            child = alpha_beta(depth + 1, (motive ^ 1), alpha, beta, go_down)
            p.child_ptr[i] = child[1]
            if go_down :
                best = min(best, child[0])
                beta = min(best, beta)
            if alpha >= beta :
                go_down = False
        p.val = best
        p.beta = best
        p.alpha = alpha
        return (best, p)

def bfs(root) :
    q = queue.Queue()
    q.put(root)
    while q.empty() == False :
        cur = q.get()
        print (str(cur.child) + " " + str(cur.val) + " " + str(cur.alpha) + " " + str(cur.beta))
        for i in cur.child_ptr :
            if i != None :
                q.put(i)

def prune_bfs(root) :
    q = queue.Queue()
    q.put(root)
    while q.empty() == False :
        cur = q.get()
        print (str(cur.child) + " " + str(cur.val) + " " + str(cur.alpha) + " " + str(cur.beta))
        for i in cur.child_ptr :
            if i.val == MAX or i.val == -MAX :
                continue
            q.put(i)        

root = alpha_beta(0, 1, -MAX, MAX, True)[1]
bfs(root)
print()
prune_bfs(root)
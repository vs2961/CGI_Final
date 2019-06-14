import random
import os
import itertools

def makeBoard(m=3):
     n = m**2
     board = [[None for _ in range(n)] for _ in range(n)]
     def search(c=0):
        i, j = divmod(c, n)
        i0, j0 = i - i % m, j - j % m
        numbers = list(range(1, n + 1))
        random.shuffle(numbers)
        for x in numbers:
            if (x not in board[i]                     
                and all(rows[j] != x for rows in board)
                and all(x not in rows[j0:j0+m]         
                        for rows in board[i0:i])): 
                board[i][j] = x
                if c + 1 >= n**2 or search(c + 1):
                    return board
        else:
            board[i][j] = None
            return None
     return search()

def writePuzzle(fil, diff):
    board = makeBoard()
    counter = 0
    a = []
    b = []
    c = []
    for i, row in enumerate(board):
        for col, val in enumerate(row):
            if col // 3 == 0:
                a.append(val)
            elif col // 3 == 1:
                b.append(val)
            else:
                c.append(val)
        if (i + 1) // 3 > i // 3:
            for i in a + b + c:
                if random.random() > diff:
                    fil.write(f"{counter}:{str(i)}\n")
                else:
                    fil.write(f"{counter}:.\n")
                counter += 1
            a = []
            b = []
            c = []
    
def checkDifficulty(diff):
    if 0.7 <= diff < 0.9:
        return "Hard"
    elif 0.5 <= diff < 0.7:
        return "Normal"
    elif 0.3 <= diff < 0.5:
        return "Easy"
    else:
        return "???"
        
a = float(input("How difficult? "))
x = int(input("How many puzzles? "))
b = checkDifficulty(a)
for i in range(x):
    used_nums = os.listdir(f"./Puzzles/{b}/")
    count = 0
    while f"{count}.txt" in used_nums:
        count += 1

    fil = open(f"./Puzzles/{b}/{count}.txt", "w+")

    writePuzzle(fil, a)

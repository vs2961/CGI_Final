#!/usr/bin/python3

import cgi
import random
from timeit import default_timer as timer

print("""Content-type:text/html\n\n
        <!DOCTYPE html>
        <html lang="en-US">
        <head>
        <meta charset="utf-8">
        <link rel="shortcut icon" type="image/png" href="./Images/shortcut.png">
        <style>
            .table {
                padding-left:50px;
                padding-top:50px;
            }
            .hoverButton {
                background-color: white; 
                color: black; 
                border: 2px solid black;
                padding:20px;
                font-size:18pt;
            }
            .hoverButton:hover {
                background-color: #DCEEFF;
            }
            .footer {
                position:fixed;
                right:0;
                bottom:0;
                width:100%;
                background-color:white;
                color: black;
                text-align: right;
                padding-right: 30px;
                z-index:-1;
            }
        </style>
        <title>Sudoku</title>
        </head>
        <body>""")

def encode(data):
    counter = 0
    board = {}
    a = []
    b = []
    c = []
    for i, row in enumerate(data):
        for col, val in enumerate(row):
            if col // 3 == 0:
                a.append(val)
            elif col // 3 == 1:
                b.append(val)
            else:
                c.append(val)
        if (i + 1) // 3 > i // 3:
            for i in a + b + c:
                board[str(counter)] = str(i)
                counter += 1
            a = []
            b = []
            c = []
    return board

def processBoard(board, inputs):
    a = [[None for i in range(9)] for i in range(9)]
    counter = 0
    done = True
    for c in range(3):
        for b in range(3):
            for i in range(3):
                for j in range(3):
                    if board[str(counter)] != ".":
                        a[i + (c * 3)][j + (b * 3)] = board[str(counter)]
                    elif str(counter) in inputs:
                        a[i + (c * 3)][j + (b * 3)] = inputs.getvalue(str(counter))
                    else:
                        done = False
                        a[i + (c * 3)][j + (b * 3)] = "."
                    counter += 1
    seen = []
    for i, row in enumerate(a):
        for j, c in enumerate(row):
            check = [(c[-1],j),(i,c[-1]), (i // 3, j // 3, c[-1])]
            if (i, c[-1]) in seen:
                done = False
                for k in range(len(row)):
                    a[i][k] = "red" + a[i][k]
                check.remove((i, c[-1]))
            if (c[-1], j) in seen:
                done = False
                for k in range(len(a)):
                    a[k][j] = "red" + a[k][j]
                check.remove((c[-1], j))
            if (i // 3, j // 3, c[-1]) in seen:
                done = False
                for k in range(3):
                    for l in range(3):
                        a[(i // 3) * 3 + k][(j // 3) * 3 + l] = "red" + a[(i // 3) * 3 + k][(j // 3) * 3 + l]
                check.remove((i // 3, j // 3, c[-1]))
            if c[-1] != ".":
                seen += check
    return done, encode(a)
                

def solve(board):
    a = [[None for i in range(9)] for i in range(9)]
    counter = 0
    for c in range(3):
        for b in range(3):
            for i in range(3):
                for j in range(3):
                    a[i + (c * 3)][j + (b * 3)] = board[str(counter)]
                    counter += 1
    solve = Solver(a)
    return encode(solve.board)
    

class Solver:
    def __init__(self, board):
        self.solveSudoku(board)
    def solveSudoku(self, board):
        self.board = board
        self.val = self.PossibleVals()
        self.Solver()
    def PossibleVals(self):
        a = "123456789"
        d, val = {}, {}
        for i in range(9):
            for j in range(9):
                ele = self.board[i][j]
                if ele != ".":
                    d[("r", i)] = d.get(("r", i), []) + [ele]
                    d[("c", j)] = d.get(("c", j), []) + [ele]
                    d[(i//3, j//3)] = d.get((i//3, j//3), []) + [ele]
                else:
                    val[(i,j)] = []
        for (i,j) in val.keys():
            inval = d.get(("r",i),[])+d.get(("c",j),[])+d.get((i//3,j//3),[])
            val[(i,j)] = [n for n in a if n not in inval ]
        return val

    def Solver(self):
        if len(self.val)==0:
            return True
        kee = min(self.val.keys(), key=lambda x: len(self.val[x]))
        nums = self.val[kee]
        for n in nums:
            update = {kee:self.val[kee]}
            if self.ValidOne(n, kee, update): # valid choice
                if self.Solver(): # keep solving
                    return True
            self.undo(kee, update) # invalid choice or didn't solve it => undo
        return False

    def ValidOne(self, n, kee, update):
        self.board[kee[0]][kee[1]] = n
        del self.val[kee]
        i, j = kee
        for ind in self.val.keys():
            if n in self.val[ind]:
                if ind[0]==i or ind[1]==j or (ind[0]//3,ind[1]//3)==(i//3,j//3):
                    update[ind] = n
                    self.val[ind].remove(n)
                    if len(self.val[ind]) == 0:
                        return False
        return True

    def undo(self, kee, update):
        self.board[kee[0]][kee[1]]="."
        for k in update:            
            if k not in self.val:
                self.val[k]= update[k]
            else:
                self.val[k].append(update[k])
        return None

def printTable(data, inputs, seed, difficulty, done):
    counter = 0
    print("<form id='squares' action='sudoku.py' method='post' autocomplete='off'> </form>\n")
    print(f"<input type='text' value={seed} hidden='true' name='Seed' form='squares'>")
    print(f"<input type='text' value={difficulty} hidden='true' name='Diff' form='squares'>")
    print("<div class='table'>")
    print("<table align='left' border='2' cellspacing='0' cellpadding='0'>")
    for a in range(3):
        print("<tr>\n")
        for b in range(3):
            print("<td><table align='center' border='1' cellspacing='0' cellpadding='0'>")
            for c in range(3):
                print("<tr>")
                for d in range(3):
                    if data[str(counter)].startswith("red") and (inputs.getvalue(str(counter)) or data[str(counter)][-1] == ".") and not done:
                        print("""<td bgcolor="#FFBCBD" style='height:84px;width:30px;
                                padding-right:9px;padding-left:26px'>""")
                        print(f"""<input maxlength='1' name={counter} form='squares' 
                                value={inputs.getvalue(f'{counter}')}
                                type="number" max='9' min='1' autocomplete='new-password'
                                oninput="this.value = this.value.slice(0, this.maxLength);"
                                style='color:#4C90E1;background-color: #FFBCBD;float:middle;font-size:22pt;
                                border:0px solid;width:35px'>""")
                    elif (data[str(counter)] == "." or inputs.getvalue(str(counter))) and not done:
                        print("""<td style='height:84px;width:30px;
                                padding-right:9px;padding-left:26px'>""")
                        print(f"""<input maxlength='1' name={counter} form='squares' 
                                value={inputs.getvalue(f'{counter}')}
                                type="number" max='9' min='1' autocomplete='new-password'
                                oninput="this.value = this.value.slice(0, this.maxLength);"
                                style='color:#4C90E1;float:middle;font-size:22pt;
                                border:0px solid;width:35px'>""")
                    elif data[str(counter)].startswith("red") and not done:
                        print("<td bgcolor='FFBCBD' style='height:84px; width:70px;text-align:center;'>")
                        print(f"<h1>{data[str(counter)][-1]}</h1>")
                    else:
                        print("<td style='height:84px; width:70px;text-align:center;'>")
                        print(f"<h1>{data[str(counter)]}</h1>")
                    counter += 1
                    print("</td>")
                print("</tr>")
            print("</table>")
        print("</tr>")
    print("</table></div>")
    if not done:
        print("<button class='hoverButton' form='squares'>Check Answer</button>")
        print("<button class='hoverButton' name='giveUp' value='1' form='squares'>Give Up</button>")
        print("<form id='newPuzzle' action='index.html'></form>")
        print("<button class='hoverButton' form='newPuzzle'>Go Back</button>")
    else:
        print("<form id='newPuzzle' action='index.html'></form>")
        print("<button class='hoverButton' form='newPuzzle'>New Puzzle?</button>")
    

def main():
    inputs = cgi.FieldStorage()
    if inputs.getvalue("Difficulty") == "Hard":
        seed = random.randint(0, 99)
    elif inputs.getvalue("Difficulty") == "Normal":
        seed = random.randint(0, 99)
    elif inputs.getvalue("Difficulty") == "Easy":
        seed = random.randint(0, 99)
    else:
        seed = random.randint(0, 99)
    g = inputs.getvalue('Difficulty')
    if not g:
        seed = inputs.getvalue('Seed')
        g = inputs.getvalue('Diff')
    data = open(f"./Puzzles/{g}/{seed}.txt", "r")
    board = {}
    b = []
    for i in data:
        a = i
        b.append(a)
        print(a * 0)
    for j in b:
        c, d = j.split(":")
        board[c] = d.rstrip()
    done, nboard = processBoard(board, inputs)
    if inputs.getvalue("giveUp"):
        board = solve(board)
        nboard = board
        done = True
    printTable(nboard, inputs, seed, g, done)
    print("""<div class='footer'><h4>&copy; Copyright 2019 Victor Siu<br>
        Questions, Comments, Concerns? Email me at 
        <a href="mailto:vsiu10@stuy.edu">vsiu10@stuy.edu</h4></div>
        </body>""") 
    print("</html>")


if __name__ == "__main__":
    try:
        main()
    except:
        cgi.print_exception()

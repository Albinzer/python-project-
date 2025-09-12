def printBoard(xState, yState):
    board = ['X' if xState[i] else 'O' if yState[i] else str(i) for i in range(9)]
    for r in range(0, 9, 3):
        print(f"{board[r]} | {board[r+1]} | {board[r+2]}")
        if r < 6: print("--|---|--")

def checkWin(state):
    wins = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]
    for a,b,c in wins:
        if state[a] + state[b] + state[c] == 3: return True
    return False

def getMove(stateX, stateO):
    while True:
        try:
            v = int(input("Enter position (0–8): "))
            if v in range(9) and not (stateX[v] or stateO[v]): return v
        except: pass

xState = [0]*9
oState = [0]*9
turn = 1
print("Tic Tac Toe")
while True:
    printBoard(xState, oState)
    v = getMove(xState, oState)
    (xState if turn else oState)[v] = 1
    if checkWin(xState if turn else oState):
        printBoard(xState, oState)
        print("X won!" if turn else "O won!")
        break
    if all(x or o for x,o in zip(xState,oState)):
        printBoard(xState, oState)
        print("It's a Draw!")
        break
    turn = 1 - turn



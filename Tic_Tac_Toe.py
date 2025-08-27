
def PrintBoard(xState, yState):
    zero  = 'X' if xState[0] else ('O' if yState[0] else '0')
    one   = 'X' if xState[1] else ('O' if yState[1] else '1')
    two   = 'X' if xState[2] else ('O' if yState[2] else '2')
    three = 'X' if xState[3] else ('O' if yState[3] else '3')
    four  = 'X' if xState[4] else ('O' if yState[4] else '4')
    five  = 'X' if xState[5] else ('O' if yState[5] else '5')
    six   = 'X' if xState[6] else ('O' if yState[6] else '6')
    seven = 'X' if xState[7] else ('O' if yState[7] else '7')
    eight = 'X' if xState[8] else ('O' if yState[8] else '8')

    print(f"{zero} | {one} | {two}")
    print("--|---|--")
    print(f"{three} | {four} | {five}")
    print("--|---|--")
    print(f"{six} | {seven} | {eight}")

def checkWin(xState, yState):
    wins = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]
    for a,b,c in wins:
        if xState[a] + xState[b] + xState[c] == 3:
            print("X won the match")
            return 1
        if yState[a] + yState[b] + yState[c] == 3:
            print("O won the match")
            return 0
    return -1

def isDraw(xState, yState):
    return all(xState[i] or yState[i] for i in range(9))

def get_valid_move(prompt, xState, yState):
    while True:
        try:
            v = int(input(prompt))
        except ValueError:
            print("Invalid input! Enter a number 0–8.")
            continue
        if v < 0 or v > 8:
            print("Out of range! Enter 0–8.")
            continue
        if xState[v] or yState[v]:
            print("Number already taken! Try again.")
            continue
        return v

if __name__ == "__main__":
    xState = [0]*9
    yState = [0]*9
    turn = 1
    print("Welcome to Tic Tac Toe")
    while True:
        PrintBoard(xState, yState)
        if turn == 1:
            print("X's Chance")
            value = get_valid_move("Enter position (0–8): ", xState, yState)
            xState[value] = 1
        else:
            print("O's Chance")
            value = get_valid_move("Enter position (0–8): ", xState, yState)
            yState[value] = 1
        cwin = checkWin(xState, yState)
        if cwin != -1:
            PrintBoard(xState, yState)
            print("Match Over")
            break
        if isDraw(xState, yState):
            PrintBoard(xState, yState)
            print("It's a Draw!")
            break
        turn = 1 - turn

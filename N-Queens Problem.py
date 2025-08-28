def isSafe(board,row,col):
    for r in range(row):
        c=board[r]

        if c==col:
            return False
        if abs(row-r)==abs(col-c):
            return False
    return True

def solve_n_queens(board,n,row=0):
    if row == n:
        print(board)
        return 1

    count =0
    for col in range (n):
        if isSafe(board,row,col):
            board[row]=col
            count +=solve_n_queens(board,n,row+1)
            board[row]=-1
    return count

N=int(input(" Enter N for N-Queens :"))
board= [-1]*N
total_solutions=solve_n_queens(board,N)
print(f"Total solutions for N={N}: {total_solutions}")



    #Visual Chessboard


def print_board(board):
    n = len(board)
    for row in range(n):
        line = ""
        for col in range(n):
            if board[row] == col:
                line += "Q "
            else:
                line += ". "
        print(line)
    print("\n")

def is_safe(board, row, col):
    for prev_row in range(row):
        if board[prev_row] == col:
            return False
        if abs(board[prev_row] - col) == abs(row - prev_row):
            return False
    return True

def solve_n_queens(board, n, row=0):
    if row == n:
        print_board(board) 
    count = 0
    for col in range(n):
        if is_safe(board, row, col):
            board[row] = col
            count += solve_n_queens(board, n, row + 1)
            board[row] = -1  # Backtrack
    return count

            # Main program
N = int(input("Enter N for N-Queens: "))
board = [-1] * N
total_solutions = solve_n_queens(board, N)
print(f"Total solutions for N={N}: {total_solutions}")


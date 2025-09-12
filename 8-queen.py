def print_board(board):
    for row in board:
        print("".join("Q" if col else "." for col in row))
    print()

def is_safe(board, row, col, n):
    # Check column
    for i in range(row):
        if board[i][col]:
            return False
    # Check upper-left diagonal
    for i,j in zip(range(row-1,-1,-1), range(col-1,-1,-1)):
        if board[i][j]:
            return False
    # Check upper-right diagonal
    for i,j in zip(range(row-1,-1,-1), range(col+1,n)):
        if board[i][j]:
            return False
    return True

def solve_nqueens(board, row, n, solutions):
    if row == n:
        solutions.append([r[:] for r in board])
        return
    for col in range(n):
        if is_safe(board, row, col, n):
            board[row][col] = 1
            solve_nqueens(board, row+1, n, solutions)
            board[row][col] = 0  # backtrack

# User input
n = int(input("Enter the value of N: "))
board = [[0]*n for _ in range(n)]
solutions = []

solve_nqueens(board, 0, n, solutions)

print(f"\nTotal solutions for N={n}: {len(solutions)}\n")
for idx, sol in enumerate(solutions, 1):
    print(f"Solution {idx}:")
    print_board(sol)

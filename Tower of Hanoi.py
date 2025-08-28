    #tower of hanoi
def hanoi(n,source,target,auxiliary):
    if n==1:
        print(f"Move disc 1 from {source} to {target}")
    else:
        hanoi(n-1,source,auxiliary,target)

        print(f"Move discs {n} from {source} to {target}")
        hanoi(n-1,auxiliary,target,source)

hanoi(3,"A","C","B")




       # User define the discs number
def hanoi(n,source,target,auxiliary):
    if n==1:
        print(f"Move discs 1 from {source } to {target}")
    else:
        hanoi(n-1,source,auxiliary,target)
        print(f"Move discs {n} from {source} to {target}")
        hanoi(n-1,auxiliary,target,source)

num_discs=int(input("Enter the number of discs: "))
print(f" Number of discs: {num_discs} discs: \n")
hanoi(num_discs,'A','C','B')

        # Count the moves number
move_count = 0

def hanoi(n, source, target, auxiliary):
    global move_count
    if n == 1:
        move_count += 1
        print(f"Step {move_count}: Move disc 1 from {source} to {target}")
    else:
        hanoi(n - 1, source, auxiliary, target)
        move_count += 1
        print(f"Step {move_count}: Move disc {n} from {source} to {target}")
        hanoi(n - 1, auxiliary, target, source)

num_discs = int(input("Enter the number of discs: "))
print(f"Solution for {num_discs} discs:")
hanoi(num_discs, "A", "C", "B")
print(f"Total moves: {move_count} (formula check: {2**num_discs - 1})")

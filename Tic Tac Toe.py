import math
board=['-']*9
AI='AI'
YOU='am'
def print_board(board):
    for i in range(0,9,3):
        print(board[i] + '|' + board[i+1] + '|' + board[i+2])
    print()
def check_winner(board,player):
    winning_combinations=[
        [0, 1, 2],[3, 4, 5],[6, 7, 8],  
        [0, 3, 6],[1, 4, 7],[2, 5, 8],  
        [0, 4, 8],[2, 4, 6]]
    for combo in winning_combinations:
        if all(board[i]==player for i in combo):
            return True
    return False
def is_board_full(board):
    return all(cell!='-' for cell in board)
def minimax_alpha_beta(board,depth,alpha,beta,maximizing_player):
    if check_winner(board,AI):
        return 1
    elif check_winner(board,YOU):
        return -1
    elif is_board_full(board):
        return 0
    if maximizing_player:
        max_eval=-math.inf
        for i in range(9):
            if board[i]=='-':
                board[i]=AI
                eval=minimax_alpha_beta(board,depth+1,alpha,beta,False)
                board[i]='-'
                max_eval=max(max_eval,eval)
                alpha=max(alpha,eval)
                if beta<=alpha:
                    break
        return max_eval
    else:
        min_eval=math.inf
        for i in range(9):
            if board[i]=='-':
                board[i]=YOU
                eval=minimax_alpha_beta(board,depth+1,alpha,beta,True)
                board[i]='-'
                min_eval=min(min_eval,eval)
                beta=min(beta,eval)
                if beta<=alpha:
                    break
        return min_eval
def find_best_move(board):
    best_move=-1
    best_eval=-math.inf
    for i in range(9):
        if board[i]=='-':
            board[i]=AI
            eval=minimax_alpha_beta(board,0,-math.inf,math.inf,False)
            board[i]='-'
            if eval > best_eval:
                best_eval=eval
                best_move=i
    return best_move
while True:
    print_board(board)
    move=int(input("select your choice(0-8): "))
    if board[move]=='-':
        board[move]=YOU
        if check_winner(board,YOU):
            print_board(board)
            print("You win!")
            break
        elif is_board_full(board):
            print_board(board)
            print("It's a draw!")
            break
        ai_move=find_best_move(board)
        board[ai_move]=AI
        if check_winner(board,AI):
            print_board(board)
            print("AI wins!")
            break
        elif is_board_full(board):
            print_board(board)
            print("It's a draw!")
            break
    else:
        print("Cell already filled. Try again.")

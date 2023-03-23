import numpy as np
import sys
nodesExplored = 0
outerDepth = 0
pruning = False

def isOuterBoardTerminal(board):
    for arr in board:
        for ele in arr:
            if ele == '.':
                return False
    return True


def utilityScore(board, player1, player2, depth):
    if player1 == player2:
        # return 1
        return (1 - 0.1*(depth))
    # return -1
    return (-1 + 0.1*(depth))


def isTerminal(board, depth):
    gameFinished = True
    score = 0

    winArr = checkForWin(board)
    if (winArr[0]): # if a win is found by O or X
        return winArr + [False]
    #check for a tie after checking for a win
    if depth == 9:
        return [True, score, True]
    #depth isn't 9 or win condition isn't there, then the game is still going on
    return [False, 0, False]

def minscore(player, board, depth, move, alpha, beta):   
    global pruning
    global nodesExplored

    breakLoop = False

    value = 2
    terminalPair = isTerminal(board, depth)
    if terminalPair[0]: #the first element is if a win was found for x or o
        nodesExplored += 1
        if terminalPair[2] == True:
            return [0,  move]
        return [utilityScore(board, terminalPair[1], player, depth), move]
    
    opponent = ""
    if player == "X":
        opponent = 'O'
    else:
        opponent = "X"

    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == '.':
                newBoard = np.array(board)
                newBoard[i][j] = opponent
                moveArg = [i,j]
                valPair = maxscore(player, newBoard, depth + 1, moveArg, alpha, beta)
                if valPair[0] < value:
                    value = valPair[0]
                    move = moveArg
                if pruning:    
                    beta = min(beta, value)
                    if (beta <= alpha):
                        breakLoop = True
                        break
        if breakLoop:
            break
        #Have to make sure that you are pruning all the options, not just those found in the row (at the top of the tree, there are 9 options to choose from for example)

    # print("MIN", nodesExplored)
    return [value, move]

# C:\CSCE420\CSCE_420_Brian_Chong\programming_assignment_2\ttt.py
def maxscore(player, board, depth, move, alpha, beta):
    global pruning
    global outerDepth
    global nodesExplored
    value = -2
    breakLoop = False

    terminalPair = isTerminal(board, depth)
    if terminalPair[0]: #the first element is if a win was found for x or o
        nodesExplored += 1
        if terminalPair[2] == True:
            return [0,  move]
        return [utilityScore(board, terminalPair[1], player, depth), move]
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == '.':
                row = ""
                newBoard = np.array(board)
                newBoard[i][j] = player
                moveArg = [i,j]
                valPair = minscore(player, newBoard, depth + 1, moveArg, alpha, beta)
                if valPair[0] > value:
                    value = valPair[0]
                    move = moveArg
                if pruning:    
                    alpha = max(alpha, value)
                    if (beta <= alpha):
                        breakLoop = True
                        break
                
                # print("The board is ", board)
                # print("The new board is ", newBoard)
                                
                if i == 0:
                    row = "A"
                elif i == 1:
                    row = "B"
                else:
                    row = "C"
                
                if (depth == outerDepth):
                    print("move (", row,j+1, ") mm-score:", valPair[0])
        if breakLoop:
            break

    return [value, move]


def minimaxSearch(player, board, depth, alpha, beta):
    global nodesExplored
    move = [0,0]
    valMoveArr = maxscore(player, board, depth, move, alpha, beta)
    board[valMoveArr[1][0]][valMoveArr[1][1]] = player
    print("Number of nodes searched: ", nodesExplored)
    nodesExplored = 0
    return valMoveArr

def printBoard(board):
    print()
    for arr in board:
        boardLine = ""
        for piece in arr:
            boardLine += (piece + " ")
        print(boardLine)


def checkForWin(board):
    transposedBoard = np.transpose(np.array(board))
    # all(ele == lst[0] for ele in lst)
    for arr in board:
        # print(arr)
        if (arr[0] != '.'):
            win = all(ele == arr[0] for ele in arr)
            if win:
                return [win, arr[0]]
    for arr in transposedBoard:
        # print(arr)
        if (arr[0] != '.'):
            win = all(ele == arr[0] for ele in arr)
            if win:
                return [win, arr[0]]
    
    if (board[0][0] != '.'):
        if ((board[0][0] == board[1][1]) and (board[0][0] == board[2][2])):
            # print("MATCH")
            return [True, board[0][0]]
    if (board[0][2] != '.'):
        if ((board[0][2] == board[1][1]) and (board[0][2] == board[2][0])):
            # print("MATCH")
            return [True, board[0][2]]

    return [False, 'A']         

print("Tic-Tac-Toe")
gameStillGoing = True;
board = [['.','.','.'],['.','.','.'],['.','.','.']]
gameState = {"board":board, "depth":0}


#Main game loop below

#This is for preventing the same piece from being chosen twice
prevPiece = ""
depth = 0

while gameStillGoing:
    # print("A TURN IS OCCURRING NOW")
    if (isOuterBoardTerminal(gameState["board"])):
        printBoard(gameState["board"])
        print("Game Finished: Tie\n\n")
        print("Do you want to play again (y/n):", end="")
        playAgain = input()
        if playAgain.upper() == "Y":
            print("Restting game: \n")
            outerDepth = 0
            gameState["board"] = [['.','.','.'],['.','.','.'],['.','.','.']]
            prevPiece = ""
            print("The board is reset")
            continue
        break

    printBoard(gameState["board"])
    print("> ", end="")
    sys.stdout.flush()
    command = input()
    command = command.split()
    command[0] = command[0].upper()
    validChoice = False

    while not validChoice:
        if command[0] == 'MOVE':
            piece = command[1].upper()
            if (piece == prevPiece):
                break

            validChoice = True
            row = 2
            if command[2].upper() != 'C':
                if command[2].upper() != 'A':
                    row = 1
                else:
                    row = 0

            print(command)
            column = int(command[3]) - 1
            print("Row and column are : ")
            if ((gameState["board"])[row][column] != '.'):
                print("That space is already taken. Choose a different one")
                break

            (gameState["board"])[row][column] = piece
            prevPiece = piece
            outerDepth += 1

        elif command[0] == 'CHOOSE':
            piece = command[1].upper()
            if (piece == prevPiece):
                break
            validChoice = True

            alpha = -2
            beta = 2


            player = command[1].upper()

            print("CHOOSE:", player)
            valMoveArr = minimaxSearch(player, gameState["board"], outerDepth, alpha, beta)
            move = valMoveArr[1]
            gameState["board"][move[0]][move[1]] = piece
            #making sure the pieces alternate
            prevPiece = piece
            outerDepth += 1

        elif command[0] == 'RESET':
            outerDepth = 0
            gameState["board"] = [['.','.','.'],['.','.','.'],['.','.','.']]
            prevPiece = ""
            print("The board is reset")
            break
            
        elif command[0] == "SHOW":
            print("Current state of the board:")
            printBoard(gameState["board"])
            print("\n")
            break
            
        elif command[0] == "PRUNING":
            if len(command) == 1:
                print("Pruning status:", int(pruning), "\n")
            else:
                if command[1].upper() == "ON":
                    print("pruning=1")
                    pruning = 1
                elif command[1].upper() == "OFF":
                    print("pruning=0")
                    pruning = 0
                else:
                    print("Not a proper option for pruning. See PA2 Guide")

                print()

            break
        
        elif command[0] == "QUIT":
            exit()
        
        else:
            print("Not a valid choice: Refer to PA2 Guide\n\n")
            break

        

    if (checkForWin(gameState["board"]))[0]:
        player = command[1].upper()
        printBoard(gameState["board"])
        print("Game Finished: Player", player, "wins.\n\n")
        print("Do you want to play again (y/n):", end="")
        playAgain = input()
        if playAgain.upper() == "Y":
            print("Restting game: \n")
            outerDepth = 0
            gameState["board"] = [['.','.','.'],['.','.','.'],['.','.','.']]
            prevPiece = ""
            print("The board is reset")
            continue
        break




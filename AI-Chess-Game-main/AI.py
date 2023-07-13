import math
import random

pieceScore = {"K": 100, "Q": 10, "R": 5, "B": 3, "N": 3, "P": 1}
CHECKMATE = 1000
STALEMATE = 0
DEPTH = 3

Promotions = ['Q', 'B', 'R', 'N']

def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves)-1)]


def findBestMove(gs, validMoves)->int:
    global nextMove, counter
    nextMove = None
    counter = 0
    random.shuffle(validMoves)
    if gs.whiteToMove:
        bestAlphaBetaMinMaxMove(gs, validMoves, DEPTH, -CHECKMATE, CHECKMATE, 1)
    else:
        bestAlphaBetaMinMaxMove(gs, validMoves, DEPTH, -CHECKMATE, CHECKMATE, -1)
    print("Number of Moves checked: ", counter)
    return nextMove

def bestAlphaBetaMinMaxMove(gs, validMoves, depth, alpha, beta, turn)->int:
    global nextMove, counter
    if depth == 0:
        return turn * scoreBoard(gs)

    maxScore = -CHECKMATE
    for move in validMoves:
        if move.isPawnPromotion:
            move.AIPlaying = True
            move.AIPromotionKey = Promotions[random.randint(0, len(Promotions) - 1)]
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        # print("Number of Moves to Check: ", len(nextMoves))
        counter += len(nextMoves)
        score = -bestAlphaBetaMinMaxMove(gs, nextMoves, depth - 1, -beta, -alpha, -turn)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.undoMove()

        if maxScore > alpha:
            alpha = maxScore
        if alpha >= beta:
            break
    return maxScore


def scoreBoard(gs):

    if gs.checkMate:
        if gs.whiteToMove:
            return -CHECKMATE
        else:
            return CHECKMATE
    elif gs.staleMate:
        return STALEMATE
    score = 0
    for row in gs.board:
        for square in row:
            if square[0] == 'w':
                score += pieceScore[square[1]]
            if square[0] == 'b':
                score -= pieceScore[square[1]]
    return score


# def scoreMaterial(board):
#     score = 0
#     for row in board:
#         for square in row:
#             if square[0] == 'w':
#                 score += pieceScore[square[1]]
#             if square[0] == 'b':
#                 score -= pieceScore[square[1]]
#
#     return score
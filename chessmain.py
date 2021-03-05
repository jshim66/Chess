"""
this is our main driver file. responsible for handling user input
"""


import pygame as p
import chessengine

width = height = 512
dimension = 8 # dimensions of a chess board
sq_size = height // dimension
max_fps = 15 # for animations
images = {}

'''
Initialize a global dictionary of image. This will be called ONCE
'''
def loadImages():
    pieces = ['wp','wR','wN','wB','wQ','wK','bp','bR','bN','bB','bQ','bK']
    for piece in pieces:
        images[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (sq_size, sq_size))

'''
main driver - handle user input and updating board
'''
def main():
    p.init()
    screen = p.display.set_mode((width,height))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = chessengine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False

    loadImages()
    running = True
    sqSelected = () #keep track of last click of user
    playerClicks = [] #keep track of player clicks - two tuples
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            #mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() #x and y location of mouse
                col = location[0]//sq_size
                row = location[1]//sq_size
                if (sqSelected == (row,col)): #user clicked the same square twice
                    sqSelected = () #deselect
                    playerClicks = [] #clear
                else:
                    sqSelected = (row,col)
                    playerClicks.append(sqSelected) #append for both 1st and 2nd clicks
                
                if len(playerClicks) == 2: #after 2nd click
                    move = chessengine.Move(playerClicks[0], playerClicks[1],gs.board)
                    print(move)
                    print(move.getChessNotation())
                    for i in range(len(validMoves)):
                        if move == validMoves[i]:
                            gs.makeMove(validMoves[i])
                            moveMade = True
                            sqSelected = () #reset user clicks
                            playerClicks = []
                    if not moveMade:
                        playerClicks = [sqSelected]
            #key handler
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: #undo when z is pressed
                    gs.undoMove()
                    moveMade = True


        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False
        drawGameState(screen, gs)
        clock.tick(max_fps)
        p.display.flip()
'''
Responsible for all graphics
'''
def drawGameState(screen, gs):
    drawBoard(screen) #draw squares
    drawPieces(screen, gs.board) #draw pieces

'''
draw squares
'''
def drawBoard(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(dimension):
        for c in range(dimension):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen,color,p.Rect(c*sq_size, r*sq_size, sq_size, sq_size))


'''
draw pieces on board
'''
def drawPieces(screen, board):
    for r in range(dimension):
        for c in range(dimension):
            piece = board[r][c]
            if piece != "--":
                screen.blit(images[piece], p.Rect(c*sq_size, r*sq_size, sq_size, sq_size))

if __name__ == "__main__":
    main()


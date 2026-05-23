WIDTH = 800
HEIGHT = 800
FPS = 24
SIZE = (WIDTH, HEIGHT)
SQUARE_WIDTH = WIDTH/8
SQUARE_HEIGHT = HEIGHT/8

#colors
LIGHT = (238, 238, 210)
DARK = (118, 150, 86)

FEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'
#FEN = 'rnbqkbnr/8/8/8/8/8/8/RNBQKBNR'


def fen_to_board(fen: str):
    res = []
    segments = fen.split('/')
    for segment in segments:
        rank = ''
        for c in segment:
            if c.isdigit():
                rank += int(c)*' '
            else:
                rank+=c
        res += [list(rank)]
    return res

DEFAULT_BOARD = fen_to_board(FEN)
from collections import namedtuple, defaultdict
import time
import simpleaudio as sa

Cell = namedtuple('Cell', ['x', 'y'])


def getNeighbours(cell):
    for x in range(cell.x - 1, cell.x + 2):
        for y in range(cell.y - 1, cell.y + 2):
            if (x, y) != (cell.x, cell.y):
                yield Cell(x, y)


def getNeighbourCount(board):
    neighbour_counts = defaultdict(int)
    for cell in board:
        for neighbour in getNeighbours(cell):
            neighbour_counts[neighbour] += 1
    return neighbour_counts


def advanceBoard(board):
    new_board = set()
    for cell, count in getNeighbourCount(board).items():
        if count == 3 or (cell in board and count == 2):
            new_board.add(cell)
    return new_board


def generateBoard(desc):
    board = set()
    for row, line in enumerate(desc.split("\n")):
        for col, elem in enumerate(line):
            if elem == 'X':
                board.add(Cell(int(col), int(row)))
    return board


def boardToString(board, pad=0):
    if not board:
        return "empty"
    board_str = ""
    xs = [x for (x, y) in board]
    ys = [y for (x, y) in board]
    for y in range(min(ys) - pad, max(ys) + 1 + pad):
        for x in range(min(xs) - pad, max(xs) + 1 + pad):
            board_str += 'X' if Cell(x, y) in board else '.'
        board_str += '\n'

    x = len(board_str.strip())
    y = int(x/12)
    for ctr in range(y):
        for htr in range(12):
            htr += 1
            count = (ctr * 12) + (htr - 1)
            if board_str[count] == "X":
                soundstr = str(htr) + ".wav"
                wave_obj = sa.WaveObject.from_wave_file(soundstr)
                play_obj = wave_obj.play()
                time.sleep(0.05)
                #play_obj.wait_done()
            if board_str[count] != "X":
                #time.sleep(0.1)
                soundstr = "1.wav"
                wave_obj = sa.WaveObject.from_wave_file(soundstr)
                play_obj = wave_obj.play()
                time.sleep(0.05)


    return board_str.strip()


if __name__ == '__main__':
    f = generateBoard("......X.\nXX......\n.X...XXX")
    for _ in range(130):
        f = advanceBoard(f)
        print("\033[2J\033[1;1H" + boardToString(f, 2))
        #time.sleep(0.1)

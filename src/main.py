import pygame
import random

pygame.init()


BG_COLOR = "white"

ROWS = input("Rows: ")
COLS = input("Cols: ")
MINES = input("Mines: ")
if ROWS == "":
    ROWS = 15
else:
    ROWS = int(ROWS)
if COLS == "":
    COLS = 15
else:
    COLS = int(COLS)
if MINES == "":
    MINES = 20
else:
    MINES = int(MINES)

print("ROWS: ", ROWS)
print("COLS: ", COLS)
print("MINES: ", MINES)

SIZE = 50
WIDTH, HEIGHT = SIZE*COLS, SIZE*ROWS+100    

NUM_FONT = pygame.font.SysFont("comicsans-regular", 20)
NUM_COLORS = {1: "black", 2: "green", 3: "blue", 4: "orange", 5: "red", 6: "purple", 7: "pink", 8: "yellow"}

GOIN = pygame.image.load("../assets/goin1.png")
GOIN = pygame.transform.scale(GOIN, (SIZE, SIZE))

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("GoinSweeper")
pygame.display.set_icon(GOIN)

def get_neighbors(row, col, rows, cols):
    """
    Retruns a list of all the neighbor squares to a given squares
    """
    neighbors = []

    if row > 0:
        neighbors.append((row-1, col))
    if row < rows-1:
        neighbors.append((row+1, col))
    if col > 0:
        neighbors.append((row, col-1))
    if col < cols-1:
        neighbors.append((row, col+1))
    
    if row > 0 and col > 0:
        neighbors.append((row-1, col-1))
    if row > 0 and col < cols-1:
        neighbors.append((row-1, col+1))
    if row < rows-1 and col > 0:
        neighbors.append((row+1, col-1))
    if row < rows-1 and col < cols-1:
        neighbors.append((row+1, col+1))

    return neighbors

def make_map(rows, cols, mines):
    """
    Makes a map of the game containing where the bombs are placed
    """
    field = [[0 for i in range(cols)] for i in range(rows)]
    mine_positions = set()

    while len(mine_positions) < mines:
        row = random.randrange(0, rows)
        col = random.randrange(0, cols)
        pos = row, col

        if pos in mine_positions:
            continue

        mine_positions.add(pos)
        field[row][col] = -1
    
        neighbors = get_neighbors(*pos, rows, cols)

        for neighbor in neighbors:
            if neighbor not in mine_positions:
                field[neighbor[0]][neighbor[1]] += 1

    
    return field

def make_covered_map(rows, cols):
    """
    Makes a list containing what squares is covered
    """
    cover_field = [[1 for i in range(cols)] for i in range(rows)]
    return cover_field

def draw(field, cover_field):
    """
    Draws to the screen
    """
    WINDOW.fill(BG_COLOR)

    for i ,row in enumerate(field):
        y = SIZE*i
        for j, value in enumerate(row):
            x = SIZE*j
            if cover_field[i][j] == 0:
                pygame.draw.rect(WINDOW, (200,200,200), (x,y, SIZE, SIZE))
                pygame.draw.rect(WINDOW, "black", (x,y, SIZE, SIZE), 2)
                if value > 0:
                    text = NUM_FONT.render(str(value), 1, NUM_COLORS[value])
                    WINDOW.blit(text, (x+(SIZE/2 - text.get_width()/2), y+(SIZE/2 - text.get_height()/2)))
                elif value == -1:
                    WINDOW.blit(GOIN, (x,y, SIZE, SIZE))
            else:
                pygame.draw.rect(WINDOW, (100,100,100), (x,y, SIZE, SIZE))
                pygame.draw.rect(WINDOW, "black", (x,y, SIZE, SIZE), 2)

    pygame.display.update()

def main():
    """
    Game loop
    """
    running = True


    field = make_map(ROWS, COLS, MINES)
    cover_field = make_covered_map(ROWS, COLS)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    break
        draw(field, cover_field)
    
    pygame.quit()


if __name__ == "__main__":
    main()
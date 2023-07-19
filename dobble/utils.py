import math
import importlib.resources as pkg_resources
from PIL import Image, ImageDraw, ImageFont

from dobble import fonts

FONT_PATH = str(pkg_resources.files(fonts) / "SakalBharati.ttf")

COLOR_MAP = {
    "red": "\033[0;31m",
    "green": "\033[0;32m",
    "yellow": "\033[0;33m",
    "nocolor": "\033[0m"
}

def create_matrix(rows, cols, use_num_sequence = False, seq_start_from=None):
    if not use_num_sequence:
        return [[None for col in range(cols)] for row in range(rows)]
    else:
        seq_start_from = seq_start_from or 0
        return [[seq_start_from+col+(row*cols) for col in range(cols)] for row in range(rows)]


def transpose(matrix):
    """ Flip the matrix over its diagonal.

    NOTE: Works only for NxN matrix.
    """
    new = create_matrix(len(matrix), len(matrix))
    for row in range(len(matrix)):
        for col in range(row, len(matrix)):
            new[row][col], new[col][row] = matrix[col][row], matrix[row][col]
    return new


def shift_y(matrix, shift_array):
    """Roll or shift along y-axis based on the column wise shift parameters.
    For a 3X3 matrix with shift array as [0, 1, 2] will roll the matrix diagonally.

    roll_y([[5, 8, 11], [6, 9, 12], [7, 10, 13]]) => [[5, 9, 13], [6, 10, 11], [7, 8, 12]]

    NOTE: Works only for NxN matrix.
    """
    new = create_matrix(len(matrix), len(matrix))
    for row in range(len(matrix)):
        for col in range(len(matrix)):
            shifted_row = (row + shift_array[col]) % len(matrix)
            new[row][col] = matrix[shifted_row][col]
    return new


def get_diagonal_shifted_y_matrix_combs(matrix):
    """Get all the combinations(1 time shift, 2 time shift etc) of a diagonally Y-axis shifted square matrix.

    Analogy: Taken we have nXn players and "n players per team". Find team wise players for each game with the given conditions
    cond1: all teams should participate in each game.
    cond2: we shuffle teams in such a way that, "no 2 players play together in a team more than 
    once for the whole series of games".

    Given 9 players numbered 5 to 13, there will be 3 combinations. here is 3X3 combinations with 9 players=>  
    [[5, 8, 11], [6, 9, 12], [7, 10, 13]] & [[5, 9, 13], [6, 10, 11], [7, 8, 12]] & [[5, 10, 12], [6, 8, 13], [7, 9, 11]]
    (NOTE: Rotation gives correct combinations only when "n in prime" As we use modulo))

    Note: Works only for NxN matrix. 
    """
    combinations = []
    shift_array = range(len(matrix))

    comb = matrix
    for i in range(len(matrix)):
        combinations.append(comb)
        comb = shift_y(comb, shift_array)
    return combinations

### General Utils

def get_unique_path(directory, fname_pattern):
    """Generate a unique(non-existing) path in the given directory.
    """
    counter = 1
    directory.mkdir(exist_ok=True)
    while True:
        path = directory / fname_pattern.format(counter)
        counter += 1
        if not path.exists():
            return path

def is_prime(num):
    """Returns True when number is prime.
    """
    if num <= 1 or int(num) != num:
        return False

    for i in range(2, int(num*0.5)+1):
        if num % i == 0:
            return False
    return True 

def colored_text(text, color="red"):
    return COLOR_MAP.get(color.lower()) + text + COLOR_MAP["nocolor"]

### Image utils

def symbols_to_card_size(n):
    """Decide card size based on number of symbols it has to have.

    It returns width and height of the square that we use as a base shape.
    """
    min_size = 150
    side = max(min_size, int(math.log(n) * min_size))
    return side, side  # width and height

def create_card(symbols):
    """Returns card image after adding all the symbols to the card
    """
    w, h = symbols_to_card_size(len(symbols))
    shape = [(0, 0), (w, h)] # Base square shape

    img = Image.new("RGBA", (w, h), color="white")

    card = ImageDraw.Draw(img)
    card.ellipse(shape, outline = "blue")
    card_center = (h/2, w/2)
    card_radius = w/2
    unicode_font = ImageFont.truetype(FONT_PATH, 35)

    # First symbol goes into the center and others around it
    card.text(card_center, str(symbols[0]), font=unicode_font, anchor="mm", fill=(255, 0, 0))

    if len(symbols) <= 1:
        img.show()
        return img

    symbol_locations = get_reg_polygon_vertices(len(symbols)-1, 0.6*card_radius, card_center)
    for location, symbol in zip(symbol_locations, symbols[1:]):
        card.text(location, str(symbol), font=unicode_font, anchor="mm", fill=(255, 0, 0))
    # img.show()
    return img


def get_reg_polygon_vertices(no_vertices, circle_radius, circle_center):
    """Find the regular polygon coordinates on a circumscribed circle.
    """
    Xc, Yc = circle_center
    r = circle_radius
    angle_btw_vertices = (2*math.pi) / no_vertices; # In radians
    coordinates = []

    # consider one of the vertices point(P) inline with the center(C) and parallel to x-axis. 
    # as CP is parallel to x-axis, initial theta will be 0.
    theta = 0
    for i in range(no_vertices):
        Xp, Yp = Xc + (r * math.cos(theta)), Yc + (r * math.sin(theta))
        theta = theta + angle_btw_vertices
        coordinates.append((Xp, Yp))
    return coordinates

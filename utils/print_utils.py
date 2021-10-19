colors = {
    'r': (255, 0, 0),
    'g': (0, 255, 0),
    'b': (0, 0, 255),
    'y': (255, 255, 0),
    'black': (0, 0, 0),
    'white': (255, 255, 255),
    'cyan': (0, 255, 255),
    'magenta': (255, 0, 255),
    'dg': (0, 200, 0),
    'dr': (128, 0, 0),
    'db': (0, 0, 128),
    'dy': (200, 200, 0),
    'teal': (0, 128, 128)
}


def colored(text, col):
    r, g, b = col
    return "\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(r, g, b, text)


def print_colored(text, color=None):
    if color is None:
        print(text)
    else:
        print(colored(text, colors[color]))

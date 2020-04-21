import os
from PIL import Image
import math


def preprocess_input(filepath: str, root_dir: str, WIDTH: int, HEIGHT: int):
    output = open(os.path.join('the-simpsons-characters-dataset', 'preprocessed_localization.txt'), 'w')
    with open(filepath, 'r') as file:
        for line in file:
            line = line.replace('./characters/', '').replace('./characters2/', '').replace('/', '\\')
            line = line.strip().split(',')
            path = line[0]
            x_1, y_1, x_2, y_2 = list(map(int, line[1:5]))
            character = line[5]
            image_path = os.path.join(root_dir, path)
            image = Image.open(image_path)
            width, height = image.size
            x_1 = round(x_1 / width * WIDTH)
            x_2 = round(x_2 / width * WIDTH)
            y_1 = round(y_1 / height * HEIGHT)
            y_2 = round(y_2 / height * HEIGHT)
            x_1, x_2 = min(x_1, x_2), max(x_1, x_2)
            y_1, y_2 = min(y_1, y_2), max(y_1, y_2)
            print('%s,%d,%d,%d,%d,%s' % (image_path, x_1, y_1, x_2, y_2, character), file=output)
    output.close()


if __name__ == '__main__':
    MAX_HEIGHT = 1072
    MAX_WIDTH = 1912
    shrink = 8
    HEIGHT = MAX_HEIGHT // shrink
    WIDTH = MAX_WIDTH // shrink

    filepath = os.path.join('the-simpsons-characters-dataset', 'annotation.txt')
    preprocess_input(filepath, 'the-simpsons-characters-dataset\\simpsons_dataset', WIDTH, HEIGHT)

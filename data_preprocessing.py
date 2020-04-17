import os
import shutil
import math


def make_data_dir(root_dir: str):
    if 'dataset' in os.listdir():
        shutil.rmtree('dataset')
    data_path = 'dataset'
    os.mkdir(data_path)
    os.mkdir(os.path.join(data_path, 'train'))
    os.mkdir(os.path.join(data_path, 'validation'))
    os.mkdir(os.path.join(data_path, 'test'))
    return data_path


def define_classes(root_dir: str, classes_threshold):
    total_images = 0
    classes = {}
    all_classes = os.listdir(root_dir)
    for character in all_classes:
        character_dir = os.path.join(root_dir, character)
        counter = len(os.listdir(character_dir))
        if counter >= classes_threshold:
            total_images += counter
            classes[character] = [os.path.join(character_dir, image) for image in os.listdir(character_dir)]
    return classes, total_images


def split_to_test_and_train(classes: dict, data_dir: str, validation, test):
    file = open(os.path.join(data_dir, 'statistics.txt'), 'w')
    train_dir = os.path.join(data_dir, 'train')
    validation_dir = os.path.join(data_dir, 'validation')
    test_dir = os.path.join(data_dir, 'test')
    print('%-30s|%-6s|%-6s|%-6s|%-6s' % ('character', 'train', 'val', 'test', 'total'), file=file)
    print('-' * 30, '+', '-' * 6, '+', '-' * 6, '+', '-' * 6, '+', sep='', file=file)
    for character in classes:
        train_character = os.path.join(train_dir, character)
        os.mkdir(train_character)
        validation_character = os.path.join(validation_dir, character)
        os.mkdir(validation_character)
        test_character = os.path.join(test_dir, character)
        os.mkdir(test_character)
        total = len(classes[character])
        validation_num = math.ceil(total * validation)
        test_num = math.ceil(total * test)
        train_num = total - validation_num - test_num
        for image_path in classes[character][:train_num]:
            copy_image_path = os.path.join(train_character, os.path.basename(image_path))
            shutil.copy(image_path, copy_image_path)
        for image_path in classes[character][train_num:train_num + validation_num]:
            copy_image_path = os.path.join(validation_character, os.path.basename(image_path))
            shutil.copy(image_path, copy_image_path)
        for image_path in classes[character][train_num + validation_num:]:
            copy_image_path = os.path.join(test_character, os.path.basename(image_path))
            shutil.copy(image_path, copy_image_path)
        print('%-30s|%-6d|%-6d|%-6d|%-6d' % (character, train_num, validation_num, test_num, total), file=file)
    file.close()


path_to_source = 'the-simpsons-characters-dataset\\simpsons_dataset\\simpsons_dataset'
classes, total = define_classes(path_to_source, 200)
path_to_splitted_data = make_data_dir(path_to_source)
split_to_test_and_train(classes, path_to_splitted_data, 0.15, 0.15)

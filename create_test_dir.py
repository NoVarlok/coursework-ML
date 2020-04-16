import os
import shutil

string = 'hello_word_kappa_pride'
print(string.rfind('_'))
print(string[:string.rfind('_')])

path_to_dataset = 'the-simpsons-characters-dataset\\kaggle_simpson_testset\kaggle_simpson_testset'
classes = {}

with open('classes_threshold.txt', 'r') as file:
    for character in file:
        character = character.strip()
        classes[character] = []

for image in os.listdir(path_to_dataset):
    character = image[:image.rfind('_')]
    classes[character].append(os.path.join(path_to_dataset, image))

print('classes number:', len(classes))
print('total images:', len(os.listdir(path_to_dataset)), '\n')
with open('classes_threshold.txt', 'w') as file:
    for character, counter in sorted(classes.items(), key=lambda x: len(x[1]), reverse=True):
        print(character, '=', len(counter))
        print(character, file=file)

# waylon_smithers = 0
# maggie_simpson = 0
# groundskeeper_willie = 0
# barney_gumble = 0
# selma_bouvier = 0
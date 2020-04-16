import os

classes_threshold = 100
total_images = 0
classes = {}

path_to_dataset = 'the-simpsons-characters-dataset\\simpsons_dataset'

folders = os.listdir(path_to_dataset)
if 'simpsons_dataset' in folders:
    folders.remove('simpsons_dataset')

for character in folders:
    path_to_character_dir = os.path.join(path_to_dataset, character)
    count = len(os.listdir(path_to_character_dir))
    if count >= classes_threshold:
        total_images += count
        classes[character] = count

print('classes number:', len(classes))
print('total images:', total_images, '\n')
with open('classes_threshold.txt', 'w') as file:
    for character, counter in sorted(classes.items(), key=lambda x: x[1], reverse=True):
        print(character, '=', counter)
        print(character, file=file)


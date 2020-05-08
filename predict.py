import os
import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt


MAX_HEIGHT = 1072
MAX_WIDTH = 1912
shrink = 8
HEIGHT = MAX_HEIGHT // shrink
WIDTH = MAX_WIDTH // shrink
labels = ['abraham_grampa_simpson', 'apu_nahasapeemapetilon', 'bart_simpson', 'charles_montgomery_burns',
          'chief_wiggum', 'comic_book_guy', 'edna_krabappel', 'homer_simpson', 'kent_brockman', 'krusty_the_clown',
          'lisa_simpson', 'marge_simpson', 'milhouse_van_houten', 'moe_szyslak', 'ned_flanders', 'nelson_muntz',
          'principal_skinner', 'sideshow_bob']


def preprocess_image_nn(image):
    image = tf.image.decode_jpeg(image, channels=3)
    height, width, channel = image.shape
    image = tf.image.resize(image, [HEIGHT, WIDTH])
    image /= 255.0
    return image, height, width


def load_and_preprocess_nn(image_path):
    image = tf.io.read_file(image_path)
    return preprocess_image_nn(image)


def load_image(image_path):
    image = tf.io.read_file(image_path)
    image = tf.image.decode_jpeg(image, channels=3)
    height, width, channels = image.shape
    return image, height, width


def show_image(image, predicted_label):
    plt.imshow(image)
    plt.title(predicted_label)
    plt.xticks([])
    plt.yticks([])


def add_box(coords, color='red'):
    coords = list(map(int,coords))
    print(coords)
    plt.plot([coords[0], coords[2], coords[2], coords[0], coords[0]], [coords[1], coords[1], coords[3], coords[3], coords[1]], color=color, linewidth=5)


def show_ans(image, coords, color: str = 'red', label=''):
    fig = plt.imshow(image)
    plt.title(label)
    coords = list(map(int,coords[0]))
    plt.plot([coords[0], coords[2], coords[2], coords[0], coords[0]], [coords[1], coords[1], coords[3], coords[3], coords[1]], color=color, linewidth=5)
    plt.xticks([])
    plt.yticks([])
    plt.show()


def load_model(model_path = 'models/localizaion/localization_adam_533_9834.h5'):
  model = keras.models.load_model(model_path, compile=False)
  return model


def show_final_image(image_path, model, size = None):
    image, height, width = load_image(image_path)
    nn_image, _, _ = load_and_preprocess_nn(image_path)
    nn_image = tf.expand_dims(nn_image, 0)
    predicted_coords, predicted_labels = model.predict(nn_image)
    predicted_coords = predicted_coords
    predicted_label = predicted_labels[0].argmax()
    predicted_coords[0, 0] = predicted_coords[0, 0] / WIDTH * width
    predicted_coords[0, 2] = predicted_coords[0, 2] / WIDTH * width
    predicted_coords[0, 1] = predicted_coords[0, 1] / HEIGHT * height
    predicted_coords[0, 3] = predicted_coords[0, 3] / HEIGHT * height
    plt.figure(figsize=size)
    character = labels[predicted_label]
    probability = predicted_labels[0, predicted_label] * 100
    title = "%s\n%.2f%%" % (character, probability)
    show_ans(image, predicted_coords, 'red', title)
    # plt.show()
    plt.savefig('prediction.png')


if __name__ == '__main__':
  print('fine')
  model = load_model()
  show_final_image('the-simpsons-characters-dataset/simpsons_dataset/principal_skinner/pic_1013.jpg', model)


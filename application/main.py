import os
import tensorflow as tf
import cv2
from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox as mb


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
    image = tf.image.resize(image, [HEIGHT, WIDTH])
    image /= 255.0
    return image


def load_and_preprocess_nn(image_path):
    image = tf.io.read_file(image_path)
    return preprocess_image_nn(image)


def load_model(path='localization_adam_533_9834.h5'):
    model = tf.keras.models.load_model(path, compile=False)
    return model


def viewImage(image, name_of_window, coords):
    cv2.putText(image, name_of_window, coords, cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255))
    cv2.namedWindow(name_of_window, cv2.WINDOW_NORMAL)
    # cv2.namedWindow('Prediction', cv2.WINDOW_NORMAL)
    cv2.imshow(name_of_window, image)
    # cv2.imshow('Prediction', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def final_image(image_path, model):
    nn_image = load_and_preprocess_nn(image_path)
    nn_image = tf.expand_dims(nn_image, 0)
    predicted_coords, predicted_labels = model.predict(nn_image)
    predicted_coords = predicted_coords[0]
    predicted_label = predicted_labels[0].argmax()
    character = labels[predicted_label]
    probability = predicted_labels[0, predicted_label] * 100
    image = cv2.imread(image_path)
    height, width, _ = image.shape
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    predicted_coords[0] = predicted_coords[0] / WIDTH * width
    predicted_coords[2] = predicted_coords[2] / WIDTH * width
    predicted_coords[1] = predicted_coords[1] / HEIGHT * height
    predicted_coords[3] = predicted_coords[3] / HEIGHT * height
    cv2.rectangle(image, (predicted_coords[0], predicted_coords[1]), (predicted_coords[2], predicted_coords[3]),
                  (0, 0, 255), 5)
    title = "%s: %.2f%%" % (character, probability)
    viewImage(image, title, (0, height-3))


# if __name__ == '__main__':
#   print('fine')
#   model = load_model()
#   # path = 'C:\\Users\\YakhtinLeonid\\jupyter\\coursework\\the-simpsons-characters-dataset\\simpsons_dataset\\abraham_grampa_simpson\\pic_0001.jpg'
#   path = '200508081428-the-simpsons-coronavirus-exlarge-169.jpg'
#   final_image(path, model)


def add_path():
    image_path_entry.delete(0, 'end')
    file_name = fd.askopenfilename(filetypes=(("jpg files", "*.jpg"),
                                                ("jpeg files", "*.jpeg"),
                                                ("All files", "*.*")))
    image_path_entry.insert(INSERT, file_name)


def main_function():
    path = image_path_entry.get()
    path = path.strip()
    try:
        final_image(path, model)
    except Exception as e:
        mb.showerror("Ошибка", 'Файл не найден или не является изображением')


root = Tk()
root.title('Всерод')
root.resizable(False, False)
model = load_model()
message = Label(root, text='Путь до изображения', width=40)
image_path_entry = Entry(root, width=40)
load_button = Button(root, text='Загрузить изображение', command=add_path)
predict_button = Button(root, text='Определить', command=main_function)
message.pack()
image_path_entry.pack()
load_button.pack()
predict_button.pack()

root.mainloop()

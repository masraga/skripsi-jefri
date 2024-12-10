import os, cv2, numpy
import matplotlib.pyplot as plt

class crop_image:

  images=[]

  is_show_image=True

  image_path="public/upload"

  face_path="public/faces"

  def __init__(self):
    self.get_images()
    self.loop()

  def get_images(self):
    img_file=os.listdir(self.image_path)
    self.images=img_file

  def crop(self, image):
    cascade=cv2.CascadeClassifier('helpers/haarcascade_frontalface_default.xml')

    image_file=os.path.join(self.image_path, image)
    face_img=cv2.imread(image_file)
    face_rect = cascade.detectMultiScale(face_img, scaleFactor = 1.2, minNeighbors = 5)
    for (x, y, w, h) in face_rect:
      face_img = face_img[y:y+h, x:x+w]

    return face_img

  def loop(self):
    for image in self.images:
      if image.endswith(tuple([".jpg", '.jpeg', '.png'])):
        face = self.crop(image)
        if face is not None:
          print(image)
          cv2.imwrite(os.path.join(self.face_path, image), face)
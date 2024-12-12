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
    face_img=cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
    detected_faces = cascade.detectMultiScale(face_img, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    if len(detected_faces) > 0:
      face_img = face_img[detected_faces[0][1]:detected_faces[0][1] + detected_faces[0][3],
      detected_faces[0][0]:detected_faces[0][0] + detected_faces[0][2]]

    return face_img

  def loop(self):
    for image in self.images:
      if image.endswith(tuple([".jpg", '.jpeg', '.png'])):
        face = self.crop(image)
        if face is not None:
          print(image)
          cv2.imwrite(os.path.join(self.face_path, image), face)

def flip_image(filename):
  img=cv2.imread(filename)
  img=cv2.flip(img, 1)
  return cv2.imwrite(filename, img)
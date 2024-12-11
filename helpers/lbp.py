import os, numpy as np, cv2
import matplotlib.pyplot as plt

cascade=cv2.CascadeClassifier('helpers/haarcascade_frontalface_default.xml')
face_path="public/faces"
label={}
label_name={}

min_percentage=40 #minimal persentase kemiripan

#membuat database wajah / peluang kemiripan data wajah
def train_model(is_train=False):
  labels=[]
  faces=[]

  face_index=0
  for image in os.listdir(face_path):
    name=image.split("-")[0]
    if name not in label:
      label[name]=face_index
      face_index+=1
  
  label_name = {value: key for key, value in label.items()}

  print("[log] map image to label")
  for image in os.listdir(face_path):
    name=image.split("-")[0]
    face_img=cv2.imread(os.path.join(face_path, image))
    gray=cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
    faces.append(gray)
    labels.append(label[name])

  print("[log] train face data")
  recognizer = cv2.face.LBPHFaceRecognizer_create()
  if is_train:
    recognizer.train(faces, np.array(labels))
    recognizer.save('helpers/trained_model.xml')
  else:
    recognizer.read('helpers/trained_model.xml')
  return {"recognizer": recognizer, "label_name": label_name}

#memprediksi wajah
def face_predict(face):
  recognizer=train_model()
  face_image=cv2.imread(face)
  gray=cv2.cvtColor(face_image, cv2.COLOR_BGR2GRAY)
  faces = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

  # Recognize and label the faces
  if len(faces) > 0:
    label, conf= recognizer["recognizer"].predict(gray[faces[0][1]:faces[0][1] + faces[0][3],faces[0][0]:faces[0][0] + faces[0][2]])
    
    #confidence bukan menampilkan persentase kemiripan melainkan sebaliknya
    #semkain kecil valuenyanya berarti gambar semakin mendekati dengan kemiripan
    #itu sebabnya untuk mendapatkan persentase harus dikurangi 100
    #ref: https://answers.opencv.org/question/226714/confidence-value-in-lbph/
    conf=100-conf 
    is_error=True
    is_error=conf < min_percentage
    print(label_name)
    return {"face_id": recognizer["label_name"][label], "accuracy": conf, "is_error": is_error}
  else:
    return False
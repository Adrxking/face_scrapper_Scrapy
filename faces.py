from io import BytesIO
import cv2
from PIL import Image
import json
import numpy as np
import requests
import math

json_file = 'scrapy/faces/faces.json'
with open(json_file, 'r') as f:
  data = json.load(f)

images = []
for item in data:
  url = item['img']
  img = Image.open(BytesIO(requests.get(url).content))
  img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
  images.append(img)

# Detectar las caras de las imagenes
faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
faces_coords = []
face_count = 0
for img in images:
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  faces = faceCascade.detectMultiScale(
    gray,
    scaleFactor = 1.20,
    minNeighbors = 6,
    minSize = (30, 30)
  )
  faces_coords.append(faces)
  print("Found {0} Faces!".format(len(faces)))
  face_count += len(faces)

higuest_width = 0
parsed_images = []

# Obtener las caras de las imagenes
for idx, img in enumerate(faces_coords):
  for face in img:
    initial_hor = face[0]
    initial_ver = face[1]
    width = face[2]
    if width >= higuest_width:
      higuest_width = width
    height = face[3]
    image = images[idx][initial_ver:initial_ver+height, initial_hor:initial_hor+width]
    parsed_image = Image.fromarray(image)
    parsed_images.append(parsed_image)

# Redimensionar todas las imagenes al ancho más alto encontrado
face_counter = 0
for img in parsed_images:
  img = img.resize((100, 100))
  img.save(str(face_counter) + ".jpeg")
  parsed_images[face_counter] = img
  face_counter += 1

# Mosaico
## Obtener el tamaño que debe tener el mosáico
anchura = math.ceil(math.sqrt(face_counter))
altura = math.ceil(face_counter / anchura)

print(altura)
print(anchura)
print(len(parsed_images))

## Variables auxiliares
previous_hor_image = None
final_image = None
counter = 0

## Contruir el mosaico
for x in range(0, altura):
  for y in range(0, anchura):
    img = np.asarray(parsed_images[counter])
    if (previous_hor_image is not None):
      previous_hor_image = np.hstack((img, previous_hor_image))
    else:
      previous_hor_image = img
    if counter + 1 == face_counter:
      counter = 0
    else:
      counter += 1
  if (final_image is not None):
      final_image = np.vstack((final_image, previous_hor_image))
  else:
      final_image = previous_hor_image
  previous_hor_image = None

final_image = Image.fromarray(final_image)
final_image.save("final_mosaic.jpeg")
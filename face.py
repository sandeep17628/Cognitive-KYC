import face_recognition
from PIL import Image

class Face_Matcher:

  def __init__(self, id_card):
    self.id_card = id_card
    self.faces = []

  def get_faces(self):

    self.id_card = face_recognition.load_image_file(self.id_card)
    self.faces = face_recognition.face_locations(self.id_card)


  def verify(self):
    if len(self.faces) == 2:
      fcs = []
      for face_location in self.faces:
        top, right, bottom, left = face_location
        face_image = self.id_card[top:bottom, left:right]
        fcs.append(face_recognition.face_encodings(face_image)[0])
      results = face_recognition.compare_faces([fcs[0]], fcs[1])
      return True if results[0] else False
    else:
      return 'Less than two faces or more than 2 faces found'
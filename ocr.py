import cv2
from PIL import Image
import tempfile
import pytesseract

class OCR_Pipeline:

  def __init__(self, image_path = ''):
    if image_path != '':
      self.im = Image.open(image_path)
    else:
      self.im = None
    self.temp_filename = None
    self.normalized_image = None
  
  def rescale_dpi(self):
    """
    Credits : https://stackoverflow.com/questions/54001029/how-to-change-the-dpi-or-density-when-saving-images-using-pil
    """
    length_x, width_y = self.im.size
    factor = min(1, float(1024.0 / length_x))
    size = int(factor * length_x), int(factor * width_y)
    image_resize = self.im.resize(size, Image.ANTIALIAS)
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix= '1.png')
    self.temp_filename = temp_file.name
    image_resize.save(self.temp_filename, dpi=(300, 300))

  def clahe(self): #Binarization
    img = cv2.imread(self.temp_filename,0)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    self.normalized_image = clahe.apply(img)
  
  def smoothing(self):
    self.normalized_image = cv2.bilateralFilter(self.normalized_image, 3, 75, 75)
    #kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    #opening = cv2.morphologyEx(0.5, cv2.MORPH_OPEN, kernel, iterations=1)
    #self.normalized_image = 255 - opening

  def transform(self):
    self.rescale_dpi()
    self.clahe()
    #self.smoothing()
    cv2.imwrite('temp.jpg', self.normalized_image)
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    data = pytesseract.image_to_string('temp.jpg', lang='eng', config='--psm 6')
    return data

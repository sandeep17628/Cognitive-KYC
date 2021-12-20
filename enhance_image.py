import cv2

class Image_Loader_Utils:

  def __init__(self, image_path):
    self.image_path = image_path

  def convert_img_to_array(self):
    """
    Returns height, width, image as array, image in grey as array
    """
    image = cv2.imread(self.image_path)
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return image.shape[0], image.shape[1], image, image_gray

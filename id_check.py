import os
import numpy as np
import cv2
from enhance_image import Image_Loader_Utils#, Adjust_Bright_Illumination, Illumination_Finder, Adjust_Darkness

def correct_image_illumination(path):
  h,w,ci,gi = Image_Loader_Utils(path).convert_img_to_array()
  return ci

def template_matcher(template_gray, image_to_be_checked, image_to_be_checked_gray, threshold = 0.95):
  ct = 0
  w, h = template_gray.shape[::-1]
  res = cv2.matchTemplate(image_to_be_checked_gray, template_gray, cv2.TM_CCOEFF_NORMED)
  min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
  bottom_right = (min_loc[0] + w, min_loc[1] + h)
  loc = np.where(res >= threshold)
  for pt in zip(*loc[::-1]):
    ct += 1
    break
  return (True, 'Ok') if ct >= 1 else (False, 'Bad')


def find_card_type(image, t_card = ''):
  aadhar_folder = 'aadhar_templates'
  pan_folder = 'pan_templates'
  img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  ct, card = 0, 'Image size too small!'
  aadhar_template = cv2.imread(f'{aadhar_folder}/aadhar_template.jpg',0)
  pan_template = cv2.imread(f'{pan_folder}/pan_template.jpg',0)

  if template_matcher(aadhar_template, image, img_gray)[0] or t_card == 'aadhar':
    ct, card = 0, 'Aadhar'
    for template in os.listdir(aadhar_folder):
      if template != 'aadhar_template.jpg':
        temp = cv2.imread(f'{aadhar_folder}/{template}',0)
        if template_matcher(temp, image, img_gray):
          ct += 1
  elif template_matcher(pan_template, image, img_gray)[0] or t_card == 'pan':
    ct, card = 0, 'Pan'
    for template in os.listdir(pan_folder):
      if template != 'pan_template.jpg':
        temp = cv2.imread(f'{pan_folder}/{template}',0)
        if template_matcher(temp, image, img_gray):
          ct += 1
  return ct,  card if t_card == '' else t_card
        

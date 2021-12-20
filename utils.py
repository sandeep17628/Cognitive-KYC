import math
import random
import smtplib
import re
import json
import pandas as pd
import requests
from bs4 import BeautifulSoup


class PostalUtils:

  def __init__(self, pc):
    self.pc = str(pc)
    self.data = None

  def get_details(self):
    import requests
    self.data = requests.get(f'https://thezipcodes.com/api/v1/search?zipCode={str(self.pc)}&countryCode=IN&apiKey=66a4d8e95477daca5f139eedbca5ca3d')
    if self.data.status_code != 200:
      self.data = None
      
    
  def extract_info(self):
    self.data = json.loads(self.data.text)
    if self.data['success']:
        country = self.data['location'][0]['country']
        region = self.data['location'][0]['city']
        state = self.data['location'][0]['state']
        return region, state, country
    return 'Data unavailable. Check PINCODE!'

class OTP:

  def __init__(self):
    self.otp = None
  
  def generate_otp(self, leng = 6):
    digits="0123456789"
    OTP=""
    for i in range(leng):
      OTP+=digits[math.floor(random.random()*10)]
    return OTP

  def send_email(self, to_mail):
    try:
      s = smtplib.SMTP('smtp.gmail.com', 587)
      s.starttls()
      s.ehlo()
      s.login("hackathon.otp.dummy@gmail.com", "!1Abcderf")
      self.otp = self.generate_otp()
      s.sendmail("hackathon.otp.dummy@gmail.com", to_mail, self.otp)
      s.quit()
      return self.otp, 'Success'
    except Exception as e:
      return self.otp, e

def validate_details(otp, email_otp_field, dob, aadhar, pan, passport):
  from datetime import date 
  try:
    today = date.today()
    birthDate = dob
    age = today.year - birthDate.year - ((today.month, today.day) < (birthDate.month, birthDate.day))
    if age < 18:
      return 'Should be 18 years atleast!'
    elif not aadharNumVerify(aadhar):
      return 'Invalid Aadhar!'
    elif validate_pan(pan):
      return 'Invalid PAN'
    elif not passport_validator(passport):
      return 'Invalid passport number'
    elif str(email_otp_field) != str(otp):
      return 'Incorrect OTP!'
  except Exception as e:
    return e

def validate_pincode(pincode):
  try:
    postal_details = PostalUtils(pincode)
    postal_details.get_details()
    r,s,c = postal_details.extract_info()
    return r, s, c
  except Exception as e:
    return e
  
def validate_pan(pan, flag = 'individual'):
  pan = pan.upper()
  if flag == 'individual':
    regex = "[A-Z]{3}P[A-Z][0-9]{4}[A-Z]{1}"
    p = re.compile(regex)
    if not (re.search(p, pan) and len(pan) == 10):
      return True

def aadharNumVerify(aadhar) :
    """
    Reference : https://stackoverflow.com/questions/27686384/validating-the-aadhar-card-number-in-a-application
    """
    verhoeff_table_d = (
        (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
        (1, 2, 3, 4, 0, 6, 7, 8, 9, 5),
        (2, 3, 4, 0, 1, 7, 8, 9, 5, 6),
        (3, 4, 0, 1, 2, 8, 9, 5, 6, 7),
        (4, 0, 1, 2, 3, 9, 5, 6, 7, 8),
        (5, 9, 8, 7, 6, 0, 4, 3, 2, 1),
        (6, 5, 9, 8, 7, 1, 0, 4, 3, 2),
        (7, 6, 5, 9, 8, 2, 1, 0, 4, 3),
        (8, 7, 6, 5, 9, 3, 2, 1, 0, 4),
        (9, 8, 7, 6, 5, 4, 3, 2, 1, 0))

    verhoeff_table_p = (
        (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
        (1, 5, 7, 6, 2, 8, 3, 0, 9, 4),
        (5, 8, 0, 3, 7, 9, 6, 1, 4, 2),
        (8, 9, 1, 6, 0, 4, 3, 5, 2, 7),
        (9, 4, 5, 3, 1, 2, 6, 8, 7, 0),
        (4, 2, 8, 6, 5, 7, 3, 9, 0, 1),
        (2, 7, 9, 3, 8, 0, 6, 4, 1, 5),
        (7, 0, 4, 6, 9, 1, 3, 2, 5, 8))

    # verhoeff_table_inv = (0, 4, 3, 2, 1, 5, 6, 7, 8, 9)

    def checksum(aadhar_inner):
        """For a given number generates a Verhoeff digit and
        returns number + digit"""
        c = 0
        for i, item in enumerate(reversed(aadhar_inner)):
            c = verhoeff_table_d[c][verhoeff_table_p[i % 8][int(item)]]
        return c

    # Validate Verhoeff checksum
    return checksum(str(aadhar)) == 0 and len(str(aadhar)) == 12

def passport_validator(passp):
  skeleton = "^[A-PR-WYa-pr-wy][1-9]\\d\\s?\\d{4}[1-9]$"
  p = re.compile(skeleton)
  m = re.match(p, passp)
  if m is None or len(passp) != 8:
    return False
  else:
    return True

class Scraper_1:

  def __init__(self, c_name, cin):
    self.data = {}
    self.c_name = c_name
    self.cin = cin
    self.dins_reference = []
    self.link = f'https://www.zaubacorp.com/company/{self.c_name.replace(" ", "-").upper()}/{self.cin}'

  def scrape(self):
    try:
      table_MN = pd.read_html(self.link)
      if table_MN is not None:
        self.data = {table_MN[0].columns[0]:table_MN[0].columns[1]}
        self.data.update({value[0]:value[1] for value in table_MN[0].values})
        for value in table_MN[7].iloc[:,0].values:
          if value.isnumeric():
            self.dins_reference.append(value)
        self.dins_reference = set(self.dins_reference)
        response = requests.get(self.link)
        content = BeautifulSoup(response.text, "html.parser")
        add_c = content.find_all("div", class_= 'col-lg-6 col-md-6 col-sm-12 col-xs-12')[2].text.split('Address: ')[1]
        self.data['address'] = add_c
      else:
        return 'Incorrect name'
    except Exception as e:
      return e

def check_c(corporate_name, c_city, c_reg_no, cin_no, c_status, c_doi, c_DIN, c_gstin, c_pan, c_cat, f_ly, f_ly_2, v1, v2, c_address, c_state):
  score = 0
  scr = Scraper_1(corporate_name, cin_no)
  content = scr.scrape()
  err = ''
  if content is not None:
    return content
  else:
    if corporate_name == scr.data['Company Name'].upper():
      score += 1
    else:
      err += 'No such Corp. found with the given name;'
    if c_address in scr.data['address']:
      score += 1
    else:
      err += 'Address incorrect;'
    if c_city in scr.data['address']:
      score +=1
    else:
      err += 'Incorrect city;'
    if c_state in scr.data['address']:
      score +=1
    else:
      err += 'Incorrect State;'
    if c_status == scr.data['Company Status']:
      score += 1
    else:
      err += 'Incorrect company status;'
    if c_cat == scr.data['Company Sub Category']:
      score += 1
    else:
      err += 'Incorrect company category;'
    if c_reg_no == str(scr.data['Registration Number']):
      score += 1
    else:
      err += 'Incorrect registration number;'
    if cin_no == str(scr.data['CIN']):
      score += 1
    else:
      err += 'Incorrect CIN;'
    if set(c_DIN.split(';')) == scr.dins_reference:
      score += 1
    else:
      err += 'DINs missing or not mentioned completely;'
    regex = "^[0-9]{2}[A-Z]{5}[0-9]{4}" + "[A-Z]{1}[1-9A-Z]{1}" + "Z[0-9A-Z]{1}$"
    p = re.compile(regex)
    if (re.search(p, str(c_gstin))):
      score += 1
    else:
      err += 'Invalid GSTIN;'
    if str(c_gstin)[2:12] == c_pan:
      score += 1
    else:
      err += 'Invalid PAN;'
    if str(v1).replace(',', '') == str(f_ly) and str(v2).replace(',', '') == str(f_ly_2):
      score += 1
    else:
      err += 'Invalid financials'
      
  return err


import re
import datetime
import cv2
from PIL import Image
import streamlit as st
from streamlit_webrtc import VideoTransformerBase, webrtc_streamer
import tabula
from utils import PostalUtils, validate_pincode, validate_details, OTP, check_c
from id_check import correct_image_illumination, find_card_type
from ocr import OCR_Pipeline
from face import Face_Matcher




def main():

  st.title('Auto KYC Demo App')

  page = st.sidebar.radio('Page Navigation', ['Retail Banking', 'Retail Video KYC', 'Corporate Banking'])

  if page == 'Retail Banking':

      if 'otp_sent' not in st.session_state:
        st.session_state.otp_sent = False
      
      if 'otp' not in st.session_state:
        st.session_state.otp = None

      if 'otp_sent' not in st.session_state:
        st.session_state.otp_sent = False
      
      if 'submitted' not in st.session_state:
        st.session_state.submitted = False

      if 'name' not in st.session_state:
        st.session_state.name = None
      
      if 'address' not in st.session_state:
        st.session_state.address = None

      if 'dob' not in st.session_state:
        st.session_state.dob = None

      if 'aadhar' not in st.session_state:
        st.session_state.aadhar = None

      if 'pan' not in st.session_state:
        st.session_state.pan = None

      if 'pan' not in st.session_state:
        st.session_state.pan = None

      if 'passport' not in st.session_state:
        st.session_state.passport = None
      
      if 'gender' not in st.session_state:
        st.session_state.gender = None

      st.title('Welcome to Retail Banking')
      st.header('Please fill the following fields to continue')

      first_name = st.text_input(label = 'First Name')
      last_name = st.text_input(label = 'Sur Name')
      gen = st.radio('Gender', ('Male', 'Female'))
      address = st.text_input(label = 'Address')
      
      pin_code = st.number_input(label = 'Pin Code', min_value = 100001, max_value = 999999, format = '%d', step = 0)
      dob = st.date_input(label = 'Date Of Birth', min_value = datetime.date(1920, 1, 1), max_value = datetime.date(2022, 1, 1))
      
      PAN = st.text_input(label = 'PAN No.', max_chars = 10, help = ' Type in your 10 Digit PAN No.')
      aadhar = st.number_input(label = 'Aadhar No.', format = '%d', step = 0, help = ' Type in your 12 Digit Aadhar No.')      
      st.info('Aadhar without spaces')
      passport = st.text_input(label = 'Passport No.', max_chars = 8, help = ' Type in your 8 Digit passport No.')
      

      email = st.text_input(label = 'email')
      regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
      if not (re.fullmatch(regex, email)):
        st.error('Email blank or incorrect')
      else:
        if st.session_state.otp_sent is False and st.session_state.otp is None:
          email_otp = OTP()
          st.session_state.otp, email_status = email_otp.send_email(email)
          if email_status == 'Success':
            st.write(f'OTP has been sent to {email}')
            st.session_state.otp_sent = True
          else:
            st.session_state.otp = None
            st.error(email_status)

      email_otp_field = st.text_input(label = 'Email OTP')
      st.write(st.session_state.otp)

      mobile = st.number_input(label = 'mobile', format = '%d', step = 0, min_value = 5000000000, max_value = 9999999999)

      if st.button('Submit') and st.session_state.submitted is False:
        try:
          r, s, c = validate_pincode(pin_code)
        except:
          st.error(validate_pincode(pin_code))
        validation_fail = validate_details(st.session_state.otp, email_otp_field, dob, aadhar, PAN, passport)
        if validation_fail is None:
          try:
            st.success('Thanks for signing up! Now visit Retail Video KYC to complete process')
            st.session_state.aadhar = f'{str(aadhar)[:4]} {str(aadhar)[4:8]} {str(aadhar)[8:]}'
            st.session_state.name = f'{first_name} {last_name}'
            st.session_state.gender = gen
            st.session_state.submitted = True
            st.session_state.passport = passport
            st.session_state.address = address
            st.session_state.dob = dob
            st.session_state.pan = PAN      
          except Exception as e:
            st.write(e)
        else:
          st.error(validation_fail)

  elif page == 'Retail Video KYC':
    if st.session_state.submitted == True:
      ct = 0
      aadhar_checks, pan_checks, passport_checks = False, False, False

      pag =  st.radio('Type', ('Video KYC', 'Photo KYC'))

      if pag == 'Photo KYC':

      ######################### Aadhar check#####################
        st.info('Upload Aadhar here:')
        aadh = st.file_uploader("Choose an image...", key = 'aadh', type= ["jpg", "jpeg", "png"])
        if aadh is not None:
          with open('aadhar_temp.jpg',"wb") as f: 
            f.write(aadh.getbuffer()) 
          aadhar_number_validation, dob_verification, gender_validation  = False, False, False
          first_name_validation_aadhar = False
          surname_validation_aadhar = False
          try:
            aadhar_card_validation = find_card_type(cv2.imread('aadhar_temp.jpg'), 'aadhar')[0]/4
          except:
            aadhar_card_validation = 0
          ocr_arr = OCR_Pipeline()
          ocr_arr.im = Image.open(aadh)
          ocr_arr.rescale_dpi()
          image = correct_image_illumination(ocr_arr.temp_filename)
          aadhar_text = ocr_arr.transform()
          if st.session_state.aadhar in aadhar_text:
            aadhar_number_validation = True
          elif st.session_state.aadhar[:4] in aadhar_text or st.session_state.aadhar[4:8] in aadhar_text or st.session_state.aadhar[8:12] in aadhar_text:
            aadhar_number_validation = 'Partial Match'
          dob_format = str(st.session_state.dob).replace('/','-').split('-')
          if f'{dob_format[2]}-{dob_format[1]}-{dob_format[0]}' in aadhar_text:
            dob_verification  = True
          if st.session_state.gender in aadhar_text:
            gender_validation = True
          if 'GOVERNMENT' not in aadhar_text:
            aadhar_card_validation = 0.1
          else:
            aadhar_card_validation = 0.5
          if st.session_state.name.split()[0] in aadhar_text or st.session_state.name.split()[0].upper() in aadhar_text:
            first_name_validation_aadhar = True
          if st.session_state.name.split()[1] in aadhar_text or st.session_state.name.split()[1].upper() in aadhar_text:
            surname_validation_aadhar = True
          
          aadhar_checks = True

        ######################### PAN check#####################
        st.info('Upload PAN here:')
        pa = st.file_uploader("Choose an image...", key = 'p', type= ["jpg", "jpeg", "png"])
        if pa is not None:
          with open('pan_temp.jpg',"wb") as f: 
            f.write(pa.getbuffer())   
          pan_number_validation = False
          first_name_validation_pan = False
          surname_validation_pan = False
          pan_score = find_card_type(cv2.imread('pan_temp.jpg'), 'pan')[0]/6
          ocr_arr_1 = OCR_Pipeline()
          ocr_arr_1.im = Image.open(pa)
          ocr_arr_1.rescale_dpi()
          image = correct_image_illumination(ocr_arr_1.temp_filename)
          pan_text = ocr_arr_1.transform()
          if st.session_state.pan in pan_text:
            pan_number_validation = True
          if 'INCOME' not in pan_text or 'TAX' not in pan_text or 'DEPARTMENT' not in pan_text:
            pan_score = 0
          if st.session_state.name.split()[0] in aadhar_text or st.session_state.name.split()[0].upper() in aadhar_text:
            first_name_validation_pan = True
          if st.session_state.name.split()[1] in aadhar_text or st.session_state.name.split()[1].upper() in aadhar_text:
            surname_validation_pan = True
          pan_checks = True

        ######################### Passport check#####################

        st.info('Upload Passport here: **Only the front page** ')
        passp = st.file_uploader("Choose an image...", key = 'passp', type= ["jpg", "jpeg", "png"])
        if passp is not None:
          passp_number_validation, first_name_validation, surname_validation, face_match = False, False, False, False
          ocr_arr_2 = OCR_Pipeline()
          ocr_arr_2.im = Image.open(passp)
          ocr_arr_2.rescale_dpi()
          image = correct_image_illumination(ocr_arr_2.temp_filename)
          passp_text = ocr_arr_2.transform()
          if st.session_state.passport in passp_text:
            passp_number_validation = True
          if st.session_state.name.split()[0] in passp_text or st.session_state.name.split()[0].upper() in passp_text:
            first_name_validation = True
          if st.session_state.name.split()[1] in passp_text or st.session_state.name.split()[1].upper() in passp_text:
            surname_validation = True
          
          with open('passport_temp.jpg',"wb") as f: 
            f.write(passp.getbuffer())     
          face_matcher = Face_Matcher('passport_temp.jpg')
          face_matcher.get_faces()
          face_match = face_matcher.verify()
          passport_checks = True
      
        if st.button('Generate Check Report') and aadhar_checks and passport_checks and pan_checks:

          st.info(f'First name valid in passport? : {first_name_validation}')
          st.info(f'Sur name valid in passport? : {surname_validation}')
          st.info(f'First name valid in aadhar? : {first_name_validation_aadhar}')
          st.info(f'Sur name valid in aadhar? : {surname_validation_aadhar}')
          st.info(f'First name valid in pan? : {first_name_validation_pan}')
          st.info(f'Sur name valid in aadhar? : {surname_validation_pan}')
          
          st.info(f'DOB valid? : {dob_verification}')
          st.info(f'Gender valid? : {gender_validation}')
          st.write('-' * 40)
          
          st.info(f'Valid Aadhar number : {aadhar_number_validation}')
          st.info(f'Valid PAN number : {pan_number_validation}')
          st.info(f'Valid Passport number : {passp_number_validation}')

          st.write('-' * 40)

          st.info(f'Aadhar card validation score : {aadhar_card_validation * 100} % match')
          st.info(f'PAN card validation score : {pan_score * 100} % match')
          
          st.write('-' * 40)
          
          st.info(f'Face matches : {face_match}')
        
        elif aadhar_checks and passport_checks and pan_checks:
          st.success('Click Generate Report now!')
        else:
          st.error('You have not completed all checks')

      else:

        class VideoTransformer(VideoTransformerBase):

          def __init__(self):
              self.click = False

          def transform(self, frame):
              img = frame.to_ndarray(format="bgr24")

              if self.click:
                cv2.imwrite('image_capture.jpg', img)

              return img


        ctx = webrtc_streamer(key="video_on", video_transformer_factory= VideoTransformer)

        if ctx.video_transformer:
          ctx.video_transformer.click = st.button("Capture")

    else:
        st.error('Register first and visit this page!')

  else:
    st.title('Welcome to Corporate Banking')
    corporate_name = st.text_input(label = 'Corporate Name')
    c_address = st.text_input(label = 'Registered address')
    c_city = st.text_input(label = 'City')
    c_state = st.text_input(label = 'State')
    c_pin = st.text_input(label = 'Pincode')
    c_country = st.text_input(label = 'Country')
    c_reg_no = st.text_input(label = 'Registration Number')

    cin_no = st.text_input(label = 'CIN No.')
    c_status = st.radio('Company status', ('Active', 'Inactive'))
    c_cat = st.radio('Company category', ('Non-govt company', 'Govt company'))
    c_doi = st.date_input(label = 'Date of incorporation', min_value = datetime.date(1920, 1, 1), max_value = datetime.date(2022, 1, 1))
    c_pan = PAN = st.text_input(label = 'PAN No.', max_chars = 10, help = ' Type in your 10 Digit PAN No.')
    c_gstin = st.text_input(label = 'GSTIN')
    c_DIN = st.text_input(label = 'DINs')
    st.info('Separate with ";" for multiple DINs')
    f_ly = st.number_input(label = 'Financial revenue last year', format = '%d', step = 0)
    f_ly_2 = st.number_input(label = 'Financial revenue previous last year', format = '%d', step = 0)
    fin_report = st.file_uploader("Choose an PDF...", key = 'fin_rep', type= ["pdf"])
    if fin_report is not None:
      with open('fin_rep.pdf',"wb") as f: 
            f.write(fin_report.getbuffer())
    table = tabula.read_pdf('fin_rep.pdf',pages=11)
    v1,v2 = table[0].iloc[4,2], table[0].iloc[4,3]

    if st.button('Validate'):
      for err in check_c(corporate_name, c_city, c_reg_no, cin_no, c_status, c_doi, c_DIN, c_gstin, c_pan, c_cat, f_ly, f_ly_2, v1, v2, c_address, c_state).split(';'):
        st.error(err)
      st.success('Thank you for signing up!')
      
      


if __name__ == '__main__':
  main()
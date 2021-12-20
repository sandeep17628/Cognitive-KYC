#from face import Face_Matcher
#import PyPDF2
#from pdfminer.high_level import extract_text
import tabula

if __name__ == '__main__':
    #o1 = Face_Matcher('pan_test_1.jpeg')
    #o1.get_faces()
    #print(o1.verify())
    # creating an object 
    #FileName = "consolidated-fs.pdf"
    # To get text from Second Page. 
    #text_2nd_page=extract_text(FileName ,page_numbers=[11]) 
    #print(text_2nd_page)
    #table = tabula.read_pdf(FileName,pages=11)
    #print((table[0].iloc[4,2]))
    #print((table[0].iloc[4,3]))
    import requests
    import re
    from bs4 import BeautifulSoup
    response = requests.get('https://www.zaubacorp.com/company/BHARTI-AIRTEL-LIMITED/L74899HR1995PLC095967')
    content = BeautifulSoup(response.text, "html.parser")
    address = content.find_all("div", class_= 'col-lg-6 col-md-6 col-sm-12 col-xs-12')[2].text.split('Address: ')[1]


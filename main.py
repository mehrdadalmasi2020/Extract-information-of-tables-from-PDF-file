import cv2
import pdfplumber
from PIL import Image
import pytesseract
from pytesseract import Output
import pandas as pd
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

import pytesseract


List_ALL=[]
#Extract the names of all PDF files
path_="D:\\pdf\\"
import os
for e in os.listdir(path_):
    print(e)
    List_ALL.append(path_+e)

custom_config = r'-c preserve_interword_spaces=1 --oem 1 --psm 6 -l eng+fra+deu+ltz '


for file in List_ALL:

    addr= file 
#     wr=open(addrW+addr.split("\\")[-1].replace("pdf","txt"),'w')  

    print(addr)
    my_pdf= pdfplumber.open(addr)#1932 - 400dpi-ocr.pdf Lines-1932 - 400dpi-ocr.pdf
    i=0
    for i in range(0,int(str(my_pdf.pages[-1]).split(":")[1].split(">")[0])):
        im = my_pdf.pages[i].to_image(resolution=220)
        im.save("C:\\Users\\mehrdad.almasi\\Desktop\\temporary.png","PNG")
        Original_Image = Image.open("C:\\Users\\mehrdad.almasi\\Desktop\\temporary.png") 

#     # Rotate Image By 90 Degree 
#         rotated_image1 = Original_Image.rotate(-90) 
#         rotated_image1.save("C:\\Users\\mehrdad.almasi\\Desktop\\temporary1.png")
        addrW="C:\\Users\\mehrdad.almasi\\Desktop\\Sofi\\"
        image = cv2.imread("C:\\Users\\mehrdad.almasi\\Desktop\\temporary.png")
        text=extract_text(image)   
        print(text)
        where=addrW+addr.split("\\")[-1].replace(".pdf","")+"_page_"+str(i)
        wr=open(where+".txt",'w')  
        wr.write(text) 
    wr.close()


import cv2
import pdfplumber
from PIL import Image
import pytesseract
from pytesseract import Output
import pandas as pd
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

import pytesseract
Flag=False


def extract_text(image):
    try:
        gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    except:
        gray=image
        print("problem with gray")
    try:
        thresh = cv2.threshold(gray, 255, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    except:
        print("problem with thresh")
        thresh = image

    d = pytesseract.image_to_data(thresh, config=custom_config, output_type=Output.DICT)
    df = pd.DataFrame(d)
    df1 = df[(df.conf!='-1')&(df.text!=' ')&(df.text!='')]
    # sort blocks vertically
    sorted_blocks = df1.groupby('block_num').first().sort_values('top').index.tolist()
    text = ''
    for block in sorted_blocks:
        curr = df1[df1['block_num']==block]
        sel = curr[curr.text.str.len()>5]
        char_w = (sel.width/sel.text.str.len()).mean()
        prev_par, prev_line, prev_left = 0, 0, 0
        for ix, ln in curr.iterrows():
            # add new line when necessary
            if prev_par != ln['par_num']:
                text += '\n'
                prev_par = ln['par_num']
                prev_line = ln['line_num']
                prev_left = 0
            elif prev_line != ln['line_num']:
                text += '\n'
                prev_line = ln['line_num']
                prev_left = 0

            added = 0  # num of spaces that should be added
            if ln['left']/char_w > prev_left + 1:
                added = int((ln['left'])/char_w) - prev_left
                text += ' ' * added 
            text += ln['text'] + ' '
            prev_left += len(ln['text']) + added + 1
        text += " \n"
    return text

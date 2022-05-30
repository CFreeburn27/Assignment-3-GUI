
import torch, torchvision
import mmdet
import mmcv
from mmcv.ops import get_compiling_cuda_version, get_compiler_version
from PIL import Image
from mmocr.utils.ocr import MMOCR
import matplotlib.pyplot as plt
import re
import wordninja
from autocorrect import Speller
import spacy
from spacy import displacy
import requests

class MainOCR():
    def OCR(img_path):
        """

        Args:
            img_path: path of image to make prediction on

        Returns:
            Title prediction and Author Prediction as String

        """

        # Convert To Greyscale
        Image.open(img_path).convert('L')

        # Apply OCR to image
        mmocr = MMOCR(det = 'DRRG', recog = 'SEG')
        resultOut = mmocr.readtext(img_path)

        # Text returned from OCR
        textOutList = resultOut[0]['text']
        textOutString = ' '.join(textOutList)

        # Remove emails and word containing / from OCR string
        regex = r"\S*@\S*\s?"
        subst = ""
        result = re.sub(regex, subst, textOutString, 0)
        regex = r"\S*/\S*\s?"
        subst = ""
        result = re.sub(regex, subst, textOutString, 0)

        # Remove Words >14 characters long
        result = re.sub(r'\b\w{14,}\b', '', result)

        # Split concatenated words by probability using NLP
        result = wordninja.split(result)
        result = ' '.join(newResult)

        # Apply autocorrect to correct spelling (English)
        check = Speller(lang='en')
        result = check(result)

        # Apply Spacy NLP to extract names (Hopefully the Author)
        NER = spacy.load("en_core_web_sm")
        text1 = NER(result)
        guessAuthor=''
        for word in text1.ents:
            print(word.text,word.label_)
            guessAuthor+=" "+word.text

        # Remove the person names from title
        removeAuthor = result.replace(author,'')

        # predicted title and author
        predAuthor = guessAuthor
        predTitle = removeAuthor

        return predTitle, predAuthor

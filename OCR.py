#
# Created by Berke Akyıldız on 09/July/2019
#
import os
import sys
import pdf2image
import cv2
import pytesseract
from PIL import Image


pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract'


def processImage(filePath, options):
    # print(options)
    image = cv2.imread(filePath)
    text = "NOT FOUND"
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    if len(options) == 0:
        filename = "{}.png".format("temp")
        cv2.imwrite(filename, gray)
        text = pytesseract.image_to_string(Image.open(filename), lang='tur')
    else:
        if "-t" in options:
            gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
            filename = "{}.png".format("temp")
            cv2.imwrite(filename, gray)
            text = pytesseract.image_to_string(Image.open(filename), lang='tur')
        if "-g" in options:
            gray = cv2.medianBlur(gray, 3)
            filename = "{}.png".format("temp")
            cv2.imwrite(filename, gray)
            text = pytesseract.image_to_string(Image.open(filename), lang='tur')
    if os.path.exists("temp.png"):
        os.remove("temp.png")
    return text


def processPDF(filePath, options):
    text = ""
    pages = pdf2image.convert_from_path(filePath, 500)
    fileName = filePath.split(".")[0]
    count = 0
    for page in pages:
        temp = fileName + str(count) + ".jpg"
        page.save(temp, 'JPEG')
        text = text + "\n\n" + processImage(temp, options)
        count = count + 1
        if os.path.exists(temp):
            os.remove(temp)
    return text


def main():
    arguments = sys.argv
    size = len(arguments)
    testPath = ""
    usage = "USAGE:  python OCR.py [FILE PATH] [OPTIONS]"
    options = []
    if size == 1:
        print(usage)
    elif size == 2:
        testPath = arguments[1]
        testPath = testPath.replace("\\", "\\\\")
    elif size > 2:
        testPath = arguments[1]
        testPath = testPath.replace("\\", "\\\\")
        options = arguments[2:]
    try:
        if ".pdf" in testPath:
            text = processPDF(testPath, options)
        else:
            text = processImage(testPath, options)
        print(text)
        out = testPath.split('.')[0]
        out = out + "-OUTPUT.txt"
        # print(out)
        outfile = open(out, "w", encoding="utf-8")
        outfile.write(text)
        outfile.close()
    except Exception as e:
        # print(e.args)
        print(e.__cause__)


if __name__ == "__main__":
    main()

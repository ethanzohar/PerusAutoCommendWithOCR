import cv2
import numpy
import io
from google.oauth2 import service_account
from googlesearch import search
import pyautogui, sys
import time

def detect_text(path):
    """Detects text in the file."""
    from google.cloud import vision
    client = vision.ImageAnnotatorClient(credentials = service_account.Credentials.from_service_account_file('OCRForAhmed-aa7f2c711f20.json'))

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    textArray = []

    for text in texts:
    	vertices = []
    	for vertex in text.bounding_poly.vertices:
    		vertices.append((vertex.x, vertex.y))

    	textArray.append([text.description, vertices])

    return textArray


def clean(wordIn):
	badWords = ['perus', 'figure', 'chapter', 'section', 'table', 'appendix', 'equation']
	for word in badWords:
		if word in wordIn:
			return False

	return True

cap = cv2.imread("testImage.png")
time.sleep(3)
cap = pyautogui.screenshot()
hsv = cv2.cvtColor(cap,cv2.COLOR_BGR2HSV)

for i in range(len(hsv)):
	for j in range(len(hsv[i])):
		if hsv[i][j][0] < 150:
			hsv[i][j] = [0,0,0]
		else:
			hsv[i][j] = [0,0,255]


bgr = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)
cv2.imwrite('OCRIMAGE.png', bgr)

wordArray = detect_text("OCRIMAGE.png")
# print(wordArray)
# wordArray = [['Perus\nFigure 6.12\nFigure 6.12\nFigure 6.3\nengineering stress\ngage length\nengineering strairn\n', [(35, 386), (2130, 386), (2130, 1817), (35, 1817)]], ['Perus', [(35, 386), (254, 386), (254, 457), (35, 457)]], ['Figure', [(1919, 590), (2052, 584), (2054, 631), (1921, 637)]], ['6.12', [(2071, 583), (2128, 581), (2130, 627), (2073, 630)]], ['Figure', [(841, 804), (974, 798), (976, 845), (843, 851)]], ['6.12', [(991, 798), (1048, 796), (1050, 842), (993, 845)]], ['Figure', [(1066, 875), (1205, 869), (1207, 914), (1068, 920)]], ['6.3', [(1222, 873), (1284, 870), (1286, 908), (1224, 911)]], ['engineering', [(1584, 873), (1851, 872), (1851, 919), (1584, 920)]], ['stress', [(1863, 875), (2002, 875), (2002, 911), (1863, 911)]], ['gage', [(1672, 1633), (1771, 1633), (1771, 1677), (1672, 1677)]], ['length', [(1788, 1633), (1934, 1633), (1934, 1677), (1788, 1677)]], ['engineering', [(1706, 1773), (1960, 1773), (1960, 1817), (1706, 1817)]], ['strairn', [(1983, 1773), (2101, 1773), (2101, 1817), (1983, 1817)]]]
wordArray.pop(0)

combinedArray = []

for i in range(len(wordArray)-1):
	if abs(wordArray[i][1][0][1] - wordArray[i+1][1][1][1]) < 10 and  wordArray[i+1][1][0][0] - wordArray[i][1][1][0] < 20 and not "".join(wordArray[i][0].split(".")).isdigit() and clean(wordArray[i][0].lower()):
		combinedArray.append((wordArray[i][0] + " " + wordArray[i+1][0], [wordArray[i][1][0], wordArray[i+1][1][1], wordArray[i+1][1][2], wordArray[i][1][3]]))

print(combinedArray)

for i in combinedArray:
	website = list(search(i[0], tld='com', lang='en', num=1, stop=1, pause=2.0))[0]

	textString = "I have found this topic very interesting and I wanted to know more about " + i[0] + ". I googled this subject and found some very interesting results. One of which was this link that explained the topic further and helped improved my understanding. This is the link " + website

	startX = i[1][0][0]
	endX = i[1][1][0]
	averageY = int((i[1][0][1] + i[1][1][1]) / 2)

	pyautogui.moveTo(startX - 5, averageY)
	pyautogui.dragTo(endX + 5, averageY, 1,  button='left')
	pyautogui.typewrite(textString, interval=0.001)
	pyautogui.press('enter')

	break

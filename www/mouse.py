from pynput.mouse import Controller, Button
from pynput.keyboard import Controller as keyController
import time, pytesseract, base64, requests, json
from PIL import ImageGrab, Image
import www.util as util
import param as param

time.sleep(0.5)
mouse = Controller()
keyboard = keyController()


# mouse.position = (100,100)
# mouse.press(Button.left)
# keyboard.press('a')

def domain():
    mouse.position = (225, 752)  # 切换到EAS
    mouse.click(Button.left)

    # 关闭客户档案页签
    # time.sleep(0.2)
    # mouse.position = (357, 88)
    # util.clickTwice()

    im = ImageGrab.grab((314, 79, 395, 104))
    im.save('../im.png', 'png')

    # mouse.position = (365, 97)


# print(mouse.position)
# domain()


with open('../im.png', 'rb') as f:
    image = base64.b64encode(f.read())

request_url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic?access_token={}'.format(param.baidu_token)
params = {
    'image':image
}
headers = {'content-type': 'application/x-www-form-urlencoded'}

response = requests.post(request_url, data=params, headers=headers)
if response:
    res = response.json()
    for i in res['words_result']:
        print(i['words'])


# image = Image.open('..//im.png')
# content = pytesseract.image_to_string((image), lang='chi_sim+eng')
# content = pytesseract.image_to_string((image))
# print(content)


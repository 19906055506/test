from pynput.mouse import Controller, Button
from pynput.keyboard import Controller as keyController, Key
import time, base64, requests, json, chardet, io
from PIL import ImageGrab, Image
import www.util as util
import param as param
from www.log import log


def shibie(image):
    request_url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic?access_token={}'.format(param.baidu_token)
    image = base64.b64encode(image)
    params = {
        'image': image
    }
    headers = {'content-type': 'application/x-www-form-urlencoded'}

    response = requests.post(request_url, data=params, headers=headers)
    if response:
        return response.json()


mouse = Controller()
keyboard = keyController()

with open('../客户档案编辑未打开.png', 'rb') as f:
    customerBegin = f.read()
with open('../客户档案编辑.png', 'rb') as f:
    customerDetail = f.read()
with open('../客户档案Type1.png', 'rb') as f:
    customerType1 = f.read()
with open('../客户档案Type2.png', 'rb') as f:
    customerType2 = f.read()


def customer():
    time.sleep(0.5)
    mouse.position = (66, 66)  # 修改
    mouse.click(Button.left)

    while True:
        time.sleep(2)
        im = ImageGrab.grab((314, 80, 395, 104))
        o = io.BytesIO()
        im.save(o, format='PNG')
        if o.getvalue() == customerDetail:
            break

    # time.sleep(2)
    # mouse.position = (1281, 495)  # 区县
    # mouse.click(Button.left)

    # 修改县区
    # time.sleep(2)
    # mouse.position = (519, 274)  # 选择XM02
    # util.clickTwice()

    # 保存
    time.sleep(2)
    mouse.position = (66, 66)  # 保存
    mouse.click(Button.left)
    time.sleep(1)

    beginTime = time.time()

    while True:
        time.sleep(1)
        im = ImageGrab.grab((83, 59, 84, 60))  # 保存按钮 点击状态
        color = im.getcolors()

        mouse.position = (0, 0)
        # print(color)
        if 202 <= color[0][1][0] and color[0][1][0] <= 205 \
                and 225 <= color[0][1][1] and color[0][1][1] <= 230 \
                and 240 <= color[0][1][2] and color[0][1][2] <= 250:
            # == (203, 227, 241) or color[0][1] == (204, 230, 250):
            # print(1.1, float(time.time() - beginTime))
            time.sleep(1)
            keyboard.press(Key.enter)
            keyboard.release(Key.enter)

            # print(1.2, float(time.time() - beginTime))
            time.sleep(1)
            keyboard.press(Key.enter)
            keyboard.release(Key.enter)

            # print(1.3, float(time.time() - beginTime))
            time.sleep(7)
            keyboard.press(Key.enter)
            keyboard.release(Key.enter)

        else:
            break

    while True:
        time.sleep(0.5)
        im = ImageGrab.grab((83, 59, 84, 60))  # 保存按钮 正常状态
        color = im.getcolors()

        if color[0][1] == (60, 120, 173):
            time.sleep(0.5)
            im = ImageGrab.grab((314, 80, 395, 104))  # 客户档案编辑页面tab
            o = io.BytesIO()
            im.save(o, format='PNG')

            if o.getvalue() == customerDetail:
                # print('关闭', time.time() - beginTime)
                mouse.position = (1351, 94)  # 关闭
                # mouse.position = (345, 92)
                mouse.click(Button.left)
                break


def domain():
    mouse.position = (225, 752)  # 切换到EAS 开始菜单第四个图标
    mouse.click(Button.left)

    while True:
        t = time.time()
        time.sleep(1)
        im = ImageGrab.grab((314, 80, 395, 104))  # 客户档案页签
        o = io.BytesIO()
        im.save(o, format='PNG')
        if customerBegin == o.getvalue():
            customer()
            log.info('{:.2f}'.format(time.time() - t))


domain()

# time.sleep(2)
# im = ImageGrab.grab((83, 59, 84, 60))
# c = im.getcolors()
# print(c)

# time.sleep(2)
# im = ImageGrab.grab((314, 80, 395, 104)) #客户档案编辑, 未打开
# im.save('../客户档案编辑未打开.png', 'png')

# im = ImageGrab.grab((314, 80, 395, 104)) #客户档案列表
# im.save('../客户档案编辑.png', 'png')

# time.sleep(2)
# im = ImageGrab.grab((626, 279, 715, 302)) #客户档案type1
# im.save('../客户档案Type1.png', 'png')

# time.sleep(2)
# im = ImageGrab.grab((629, 277, 881, 315)) #客户档案type2
# im.save('../客户档案Type2.png', 'png')


# time.sleep(2)
# im = ImageGrab.grab((314, 80, 395, 104))
# o = io.BytesIO()
# im.save(o, format='PNG')
# print(o.getvalue())
# print(customerDetail)
# print(o.getvalue() == customerDetail)

# keyboard.press(Key.enter)

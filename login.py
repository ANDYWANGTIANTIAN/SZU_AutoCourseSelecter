from io import BytesIO
from tkinter import *
import cv2
import numpy as np
import requests
from PIL import Image
import settings
import util


# 请求协议头（请勿修改）
# 校外VPN


def get_vtoken():
    url = util.get_url("xsxkapp/sys/xsxkapp/student/4/vcode.do?timestamp={}").format(
        util.get_timestamp())
    r = requests.post(url, headers=settings.headers)
    return r.json()["data"]["token"]


def get_batch():
    url = util.get_url("xsxkapp/sys/xsxkapp/elective/batch.do?timestamp={}").format(
        util.get_timestamp())
    r = requests.post(url, headers=settings.headers)
    return r.json()["dataList"][0]["code"]


def get_vimage(vtoken):
    verifycode = ''
    loopflag = 4
    img_pos = []

    def mouse(event, x, y, flags, param):
        nonlocal loopflag, img_pos, verifycode
        if event == cv2.EVENT_LBUTTONDOWN:
            if loopflag >= 1:
                xy = "%d,%d" % (x, y)
                cv2.circle(img, (x, y), 1, (255, 255, 255), thickness=-1)
                cv2.putText(img, '*', (x, y), cv2.FONT_HERSHEY_PLAIN, 1.0, (0, 0, 255), thickness=2)
                img_pos.append((round(x / 2), round(y / 2)))
                cv2.imshow("image", img)
                loopflag = loopflag - 1
                if loopflag == 0:
                    verifycode = str(img_pos[0][0]) + "-" + str(img_pos[0][1]) + "," + str(img_pos[1][0]) + "-" + str(
                        img_pos[1][1]) + "," + str(img_pos[2][0]) + "-" + str(img_pos[2][1]) + "," + str(
                        img_pos[3][0]) + "-" + str(
                        img_pos[3][1])
                    cv2.destroyAllWindows()
            else:
                verifycode = str(img_pos[0][0]) + "-" + str(img_pos[0][1]) + "," + str(img_pos[1][0]) + "-" + str(
                    img_pos[1][1]) + "," + str(img_pos[2][0]) + "-" + str(img_pos[2][1]) + "," + str(
                    img_pos[3][0]) + "-" + str(
                    img_pos[3][1])
                cv2.destroyAllWindows()

    url = util.get_url(
        "xsxkapp/sys/xsxkapp/student/vcode/image.do?vtoken={}").format(vtoken)
    r = requests.get(url, headers=settings.headers)
    img = Image.open(BytesIO(r.content))
    img = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
    x, y = img.shape[0:2]
    img = cv2.resize(img, (int(y * 2), int(x * 2)), interpolation=cv2.INTER_CUBIC)
    cv2.namedWindow("image")
    cv2.imshow("image", img)
    cv2.setMouseCallback("image", mouse)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return verifycode


def LogIn(Code, Vtoken):
    url = util.get_url("xsxkapp/sys/xsxkapp/student/check/login.do")
    data = {'loginName': settings.user_id, 'loginPwd': settings.user_encrypted_pass, 'verifyCode': Code,
            'vtoken': Vtoken}
    r = requests.post(url, headers=settings.headers, data=data)
    if r.json()['code'] == '1':
        settings.user_isLogin = True
        Token = r.json()['data']['token']
        settings.token = Token
        settings.headers.update(token=Token)
        cookies = requests.utils.dict_from_cookiejar(r.cookies)  # 转成字典格式
        # 将dict格式的拼接成可以放到请求头中的字符串格式
        newCookie = "; ".join([str(x) + "=" + str(y)
                               for x, y in cookies.items()])
        cookie = newCookie + '; ' + settings.cookie
        settings.headers.update(Cookie=cookie)
        getData(settings.user_id)
    return r.json()


def getData(loginName):
    url = util.get_url("xsxkapp/sys/xsxkapp/student/{}.do").format(loginName)
    r = requests.post(url, headers=settings.headers, allow_redirects=False)
    settings.user_name = r.json()['data']['name']
    settings.user_id = r.json()['data']['code']
    settings.user_college = r.json()['data']['collegeName']
    settings.user_department = r.json()['data']['departmentName']
    settings.user_class = r.json()['data']['schoolClassName']
    settings.electiveBatchCode = r.json()['data']['electiveBatch']['code']


if __name__ == '__main__':
    vtoken = get_vtoken()
    Code = get_vimage(vtoken)

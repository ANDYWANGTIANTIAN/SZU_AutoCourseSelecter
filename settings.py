'''
系统设置
'''

Mode = 0  # 模式选择：0为账号密码模式，1为Cookie模式
user_id: str = ""
user_pass: str = ""
user_encrypted_pass: str = ""
user_name: str = ""
user_college: str = ""
user_department: str = ""
user_class: str = ""
user_isLogin: bool = False
cookie = ""
electiveBatchCode = ""
token = ""
isRunning: bool = False
# 课程
# id:课程序号   type:课程类别   name:课程名称(请求不需要 仅做前端提示用)    level:选课课组(请求不需要 仅为提高选课效率用)
# ['□', '202120221150003000401', '尹剑飞', '1-17周 星期四 第1-2节 致理楼L1-402,1-17周 星期四 第3-4节 南区计算机大楼328']
courses = []


def findInDict(_id):  # 在course中找到指定id并返回dict
    for item in courses:
        if item['id'] == _id:
            return item
    return -1


def deleteCoursesInDict(_name):  # 删除一个课的所有志愿
    for item in courses:
        if item['name'] == _name:
            courses.remove(item)
            return 1
    return 0


# 延迟
delayVariable: int = 1000
loopVariable: int = 10
# 请求协议头（请勿修改）,通过gui内SelMode()更改

# 校内直接选课
url: str = "http://bkxk.szu.edu.cn/"

headers: map = {
    "Cookie": cookie.strip(),
    "token": token.strip(),
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Host": "bkxk.szu.edu.cn",
    "Pragma": "no-cache"
}

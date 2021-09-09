import settings
import requests
import json
import os
import tkinter
import time

session = requests.session()
current_milli_time = lambda: int(round(time.time() * 1000))


# 返回当前时间戳
def get_timestamp():
    return str(current_milli_time())


# 返回session
def get_session():
    return session


def get_url(relavie_path):
    return "{}{}".format(settings.url, relavie_path)


def get_user_id():
    return settings.user_id

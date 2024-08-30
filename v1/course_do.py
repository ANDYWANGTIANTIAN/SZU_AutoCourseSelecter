import json
import settings
import util

session = util.get_session()
headers = settings.headers


# 查询选课结果（已经选中的课程）
def query_result():
    response = session.post(
        url=util.get_url("xsxkapp/sys/xsxkapp/elective/courseResult.do?timestamp={}&studentCode={}").format(
            util.get_timestamp(), settings.user_id),
        headers=settings.headers)

    json_data = json.loads(response.text)
    res = []
    for obj in json_data['dataList']:
        temp = [obj['teachingClassID'], obj['teacherName'], obj['courseName'], obj['teachingPlace']]
        res.append(temp)
    return res


# 进行选课
# 本班课程： 'TJKC'
# 方案内课程: 'FANKC'
# 方案外课程： 'FAWKC'
# 校公选课： 'XGXK'
# 慕课: "ＭOOC"，
# 辅修课程: "FXKC"，
# 体育课程:"TYKC"
def choose_course(class_id, teaching_class_type):
    form_data = {
        'addParam': (
                r'''{"data":{"operationType":"1","studentCode":%s,"electiveBatchCode":%s,"teachingClassId":%s,"isMajor":"1","campus":"01","teachingClassType":%s,"chooseVolunteer":"1"}}''' % (
            settings.user_id, settings.electiveBatchCode, class_id, teaching_class_type))
    }

    response = session.post(
        url=util.get_url("xsxkapp/sys/xsxkapp/elective/volunteer.do"),
        data=form_data,
        headers=headers)

    return response.json()


# 进行退课
def delete_course(class_id):
    form_data = {
        'deleteParam': (
                r'''{"data":{"operationType":"2","studentCode":%s,"electiveBatchCode":%s,"teachingClassId":%s,"isMajor": "1"}}''' % (
            settings.user_id, settings.electiveBatchCode, class_id))
    }

    response = session.post(
        url=util.get_url("xsxkapp/sys/xsxkapp/elective/deleteVolunteer.do?timestamp={}").format(util.get_timestamp()),
        data=form_data,
        headers=headers)

    return response.json()

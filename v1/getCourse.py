# 下载课程信息到本地
import json
import settings
import util

headers = settings.headers
session = util.get_session()


# 方案内课程
def in_course(page, query=''):
    form_data = {
        "querySetting": r'''{"data":{"studentCode":"%s","campus":"01","electiveBatchCode":"%s","teachingClassType":"FANKC","checkConflict":"2","isMajor":"1","queryContent":"MOOC:2,%s"},"pageSize":"10","pageNumber":"%s","order":"null","orderBy":"courseNumber"}''' % (
            settings.user_id, settings.electiveBatchCode, query, str(page))
    }
    response = session.post(util.get_url("xsxkapp/sys/xsxkapp/elective/programCourse.do"), headers=settings.headers,
                            data=form_data)
    return response.text


# 推荐班级课程
def recommended_course(page, query=''):
    url = util.get_url("xsxkapp/sys/xsxkapp/elective/recommendedCourse.do")
    form_data = {
        "querySetting": r'''{"data": {"studentCode": "%s", "campus": "01","electiveBatchCode": "%s", "isMajor": "1","teachingClassType": "TJKC", "checkConflict": "2", "checkCapacity": "2","queryContent": "MOOC:2,%s"}, "pageSize": "10", "pageNumber": %s, "order": "","orderBy": "courseNumber"}''' % (
            settings.user_id, settings.electiveBatchCode, query, str(page))
    }

    response = session.post(url=url, headers=headers, data=form_data)
    return response.text


# 方案外课程
def out_course(page, query=''):
    form_data = {
        "querySetting": r'''{"data": {"studentCode": "%s", "campus": "01","electiveBatchCode": "%s", "isMajor": "1","teachingClassType": "FAWKC", "checkConflict": "2", "checkCapacity": "2","queryContent": "MOOC:2,%s"}, "pageSize": "10", "pageNumber": %s, "order": "","orderBy": "courseNumber"}''' % (
            settings.user_id, settings.electiveBatchCode, query, str(page))
    }

    response = session.post(util.get_url("xsxkapp/sys/xsxkapp/elective/programCourse.do"), headers=settings.headers,
                            data=form_data)
    return response.text


# 公共课程
def public_course(page, query=''):
    form_data = {
        "querySetting": r'''{"data": {"studentCode": "%s", "campus": "01","electiveBatchCode": "%s", "isMajor": "1","teachingClassType": "XGXK", "checkConflict": "2", "checkCapacity": "2","queryContent": "MOOC:2,%s"}, "pageSize": "10", "pageNumber": %s, "order": "","orderBy": "courseNumber"}''' % (
            settings.user_id, settings.electiveBatchCode, query, str(page))
    }

    response = session.post(util.get_url("xsxkapp/sys/xsxkapp/elective/programCourse.do"), headers=settings.headers,
                            data=form_data)
    return response.text


# 体育课程
def sport_course(page, query=''):
    form_data = {
        "querySetting": r'''{"data": {"studentCode": "%s", "campus": "01","electiveBatchCode": "%s", "isMajor": "1","teachingClassType": "TYKC", "checkConflict": "2", "checkCapacity": "2","queryContent": "MOOC:2,%s"}, "pageSize": "10", "pageNumber": %s, "order": "","orderBy": "courseNumber"}''' % (
            settings.user_id, settings.electiveBatchCode, query, str(page))
    }

    response = session.post(util.get_url("xsxkapp/sys/xsxkapp/elective/programCourse.do"), headers=settings.headers,
                            data=form_data)
    return response.text


# 辅修课程
def fuxiu_course(page, query=''):
    form_data = {
        "querySetting": r'''{"data": {"studentCode": "%s", "campus": "01","electiveBatchCode": "%s", "isMajor": "1","teachingClassType": "FXKC", "checkConflict": "2", "checkCapacity": "2","queryContent": "MOOC:2,%s"}, "pageSize": "10", "pageNumber": %s, "order": "","orderBy": "courseNumber"}''' % (
            settings.user_id, settings.electiveBatchCode, query, str(page))
    }

    response = session.post(util.get_url("xsxkapp/sys/xsxkapp/elective/programCourse.do"), headers=settings.headers,
                            data=form_data)
    return response.text


# 慕课
def mooc(page, query=''):
    form_data = {
        "querySetting": r'''{"data": {"studentCode": "%s", "campus": "01","electiveBatchCode": "%s", "isMajor": "1","teachingClassType": "MOOC", "checkConflict": "2", "checkCapacity": "2","queryContent": "MOOC:2,%s"}, "pageSize": "10", "pageNumber": %s, "order": "","orderBy": "courseNumber"}''' % (
            settings.user_id, settings.electiveBatchCode, query, str(page))
    }

    response = session.post(util.get_url("xsxkapp/sys/xsxkapp/elective/programCourse.do"), headers=settings.headers,
                            data=form_data)
    return response.text


def getCourse(type, methods, query=''):
    res = []
    for i in range(1000):
        s = methods(page=i, query=query)
        data = json.loads(s)

        if data['dataList'] is None or len(data['dataList']) == 0:
            break
        for course in data['dataList']:
            for j in range(1000):
                if len(course['tcList']) <= j:
                    break
                temp = []
                temp.append(course['tcList'][j]['teachingClassID'])
                temp.append(course['tcList'][j]['teacherName'])
                temp.append(course['courseName'])
                temp.append(course['tcList'][j]['teachingPlace'])
                res.append(temp)
    return res

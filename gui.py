import json
import threading
import time
import webbrowser
from multiprocessing import Process, Pipe
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import *
from tkinter.ttk import Treeview
from PIL import Image, ImageTk
import course_do
import encrypt
import getCourse
import login
import settings

developer_png = None
donate_png = None


class CourseFrame(Frame):  # 7类课程全部使用本类实现
    def __init__(self, master=None, _type=''):
        Frame.__init__(self, master)
        self.root = master  # 定义内部变量root
        self.type = _type  # 本班课程： 'TJKC' 方案内课程: 'FANKC' 方案外课程： 'FAWKC' 校公选课： 'XGXK' 慕课: "MOOC" 辅修课程: "FXKC"，体育课程:"TYKC"
        self.char_ct = '☑'  # 复选框选中标识符
        self.char_cf = '□'  # 复选框未选中标识符
        self.search = StringVar()
        self.search.set('')
        self.code = getCourse.recommended_course
        self.name = '本班课程'
        if self.type == 'FANKC':
            self.code = getCourse.in_course
            self.name = '方案内课程'
        elif self.type == 'FAWKC':
            self.code = getCourse.out_course
            self.name = '方案外课程'
        elif self.type == 'XGXK':
            self.code = getCourse.public_course
            self.name = '校公选课'
        elif self.type == 'MOOC':
            self.code = getCourse.mooc
            self.name = '慕课'
        elif self.type == 'FXKC':
            self.code = getCourse.fuxiu_course
            self.name = '辅修课程'
        elif self.type == 'TYKC':
            self.code = getCourse.sport_course
            self.name = '体育课'
        self.createPage()

    def get_row_values_by_item(self, item):
        """
        获取一行的值内容，包含行头部信息
        :return: 元组,1为头部信息，1以后为表格信息
        """
        values = self.tree.item(item, 'values')
        return values

    def get_parent_by_item(self, item):
        return self.tree.parent(item)

    def exchange_check_by_item(self, item):
        """
        变换一行的复选状态
        """
        vals = self.get_row_values_by_item(item)
        if vals[1][0:1] != self.char_cf and vals[1][0:1] != self.char_ct:
            return
        check_str = vals[1][0:1]
        if check_str == self.char_ct:
            value = self.char_cf
            settings.courses.remove(settings.findInDict(vals[2]))  # 在选课名单中删除选中的课程
        else:
            value = self.char_ct
            parent = self.get_row_values_by_item(self.get_parent_by_item(item))  # 返回父级以获取课程名称
            assign = {'id': '', 'type': '', 'name': "", 'teachingPlace': '', 'teacherName': ''}
            assign.update(id=vals[2], type=self.type, name=parent[1], teachingPlace=vals[4], teacherName=vals[3])
            settings.courses.append(assign)  # 在选课名单中新增选中的课程
        col_str = '#%d' % 2
        self.tree.set(item, column=col_str, value=value)  # 修改单元格的值

    def change_check_on_select(self):
        """
        改变选中行的勾选状态
        """
        try:
            item = self.tree.selection()[0]  # 获取行对象
        except Exception:
            pass
        else:
            self.exchange_check_by_item(item)

    def on_click(self, event):
        """
        行单击事件
        """
        self.change_check_on_select()

    def createPage(self):
        frame1 = Frame(self, relief=RAISED, borderwidth=2)
        frame1.pack(side=TOP, fill=X, ipadx=13, ipady=13, expand=0)
        Label(frame1, text='\n%s' % self.name, font=12).pack(side='top')
        Entry(frame1, textvariable=self.search, width=60).pack(side=LEFT, expand=True)
        Button(frame1, text='刷新/搜索', command=lambda: self.refresh(self.code)).pack(side=LEFT, expand=True)

        ybar = Scrollbar(self, orient='vertical')  # 竖直滚动条
        self.tree = Treeview(self, show="headings", columns=('no', 'name', 'id', 'teacher', 'place'), height=20,
                             yscrollcommand=ybar.set)
        ybar['command'] = self.tree.yview
        self.tree.column('no', width=35, anchor='center')
        self.tree.column('name', width=150, anchor='center')
        self.tree.column('id', width=180, anchor='center')
        self.tree.column('teacher', width=80, anchor='center')
        self.tree.column('place', width=300, anchor='center')
        self.tree.heading('no', text='序号')
        self.tree.heading('name', text='课程名')
        self.tree.heading('id', text='课程总号')
        self.tree.heading('teacher', text='教师')
        self.tree.heading('place', text='上课时间及地点')
        self.refresh(self.code)
        self.tree.pack(side='left', expand='yes', fill='y')
        ybar.pack(side='left', expand='yes', fill='y')
        self.tree.bind('<ButtonRelease-1>', self.on_click)  # 绑定行单击事件

    def refresh(self, methods):
        x = self.tree.get_children()
        for item in x:
            self.tree.delete(item)  # 删除旧数据，准备插入新数据
        try:
            index = 1
            for i in range(1000):
                s = methods(page=i, query=self.search.get())
                data = json.loads(s)

                if data['dataList'] is None or len(data['dataList']) == 0:
                    break

                for course in data['dataList']:
                    mid = self.tree.insert('', 'end', values=(index, course['courseName'], '', '', ''))
                    index = index + 1
                    for j in range(1000):
                        if len(course['tcList']) <= j:
                            break
                        if settings.findInDict(course['tcList'][j]['teachingClassID']) == -1:
                            state = self.char_cf
                        else:
                            state = self.char_ct
                        temp1 = [state, course['tcList'][j]['teachingClassID'],
                                 course['tcList'][j]['teacherName'],
                                 course['tcList'][j]['teachingPlace']]
                        self.tree.insert(mid, 'end', values=("(%d" % (j + 1), temp1[0], temp1[1], temp1[2], temp1[3]))

            self.flag = 1
        except Exception as e:
            showinfo(title='错误', message='获取%s列表失败\n %s' % (self.name, e))


class SelectedCourseFrame(Frame):  # 继承Frame类
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.flag = 0  # 是否有缓存内容，若无则刷新
        self.root = master  # 定义内部变量root
        self.selectedCourse = []
        if self.flag == 0:
            try:
                self.selectedCourse = course_do.query_result()
                self.flag = 1

            except Exception as e:
                showinfo(title='错误', message='获取已选课程列表失败\n %s' % e)
        self.createPage()

    def createPage(self):
        Label(self, text='\n已选课程\n', font=12).pack(side='top')
        Button(self, text='刷新', command=self.refresh).pack(side='top')
        ybar = Scrollbar(self, orient='vertical')  # 竖直滚动条
        self.tree = ttk.Treeview(self, show="headings", columns=('no', 'id', 'name', 'teacher', 'place'), height=20,
                                 yscrollcommand=ybar.set)
        ybar['command'] = self.tree.yview
        self.tree.column('no', width=35, anchor='center')
        self.tree.column('id', width=180, anchor='center')
        self.tree.column('name', width=150, anchor='center')
        self.tree.column('teacher', width=80, anchor='center')
        self.tree.column('place', width=300, anchor='center')
        self.tree.heading('no', text='序号')
        self.tree.heading('id', text='课程总号')
        self.tree.heading('name', text='课程名')
        self.tree.heading('teacher', text='教师')
        self.tree.heading('place', text='上课时间及地点')
        for i in range(len(self.selectedCourse)):
            self.tree.insert('', i, values=(i + 1,
                                            self.selectedCourse[i][0], self.selectedCourse[i][2],
                                            self.selectedCourse[i][1],
                                            self.selectedCourse[i][3]))
        self.tree.pack(side='left', expand='yes', fill='both')
        ybar.pack(side='left', expand='yes', fill='y')

    def refresh(self):
        try:
            self.selectedCourse = course_do.query_result()
            x = self.tree.get_children()
            for item in x:
                self.tree.delete(item)
            for i in range(len(self.selectedCourse)):
                self.tree.insert('', i, values=(i + 1,
                                                self.selectedCourse[i][0], self.selectedCourse[i][2],
                                                self.selectedCourse[i][1],
                                                self.selectedCourse[i][3]))
            self.flag = 1

        except Exception as e:
            showinfo(title='错误', message='获取已选课程列表失败\n %s' % e)


class ChooseCourseThread(threading.Thread):
    def __init__(self, SelectedCourse):
        super().__init__()
        self.SelectedCourse = SelectedCourse
        self.setDaemon(True)
        self.start()

    def run(self):
        for i in range(settings.loopVariable):
            if not settings.isRunning:
                return
            for j in settings.courses:
                if not settings.isRunning:
                    return
                if not (self.SelectedCourse.count(j['id']) or self.SelectedCourse.count(j['name'])):
                    response = course_do.choose_course(j['id'], j['type'])
                    if response['code'] == '1':
                        settings.deleteCoursesInDict(j['name'])
                        self.SelectedCourse.append(j['id'])
                        self.SelectedCourse.append(j['name'])
                    Tree.insert('', 'end',
                                values=(
                                    j['id'], j['name'], j['teacherName'], response['msg'], j['teachingPlace']))
                    time.sleep(settings.delayVariable / 1000)


class StartChooseFrame(Frame):  # 继承Frame类
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.root = master  # 定义内部变量root
        self.SelectedCourse = []
        self.createPage()

    def createPage(self):
        Label(self, text='\n开始选课\n', font=12).pack(side='top')
        Button(self, text='开始选课', command=self.StartChoose).pack(side='top')
        Button(self, text='停止选课', command=self.StopChoose).pack(side='top')
        ybar = Scrollbar(self, orient='vertical')  # 竖直滚动条
        global Tree
        Tree = ttk.Treeview(self, show="headings", columns=('id', 'name', 'teacher', 'msg', 'place'), height=20,
                            yscrollcommand=ybar.set)
        ybar['command'] = Tree.yview
        Tree.column('id', width=180, anchor='center')
        Tree.column('name', width=150, anchor='center')
        Tree.column('teacher', width=80, anchor='center')
        Tree.column('msg', width=150, anchor='center')
        Tree.column('place', width=300, anchor='center')
        Tree.heading('id', text='课程总号')
        Tree.heading('name', text='课程名')
        Tree.heading('teacher', text='教师')
        Tree.heading('msg', text='选课结果')
        Tree.heading('place', text='上课时间及地点')
        Tree.pack(side='left', expand='yes', fill='both')
        ybar.pack(side='left', expand='yes', fill='y')

    def StartChoose(self):
        if settings.delayVariable < 300:
            showinfo(title='错误', message='请求发送延迟需大于300ms！')
            return
        if settings.loopVariable < 1 or settings.loopVariable > 10000:
            showinfo(title='错误', message='请求发送循环次数需在1到10000之间！')
            return
        settings.isRunning = True
        try:
            ChooseCourseThread(self.SelectedCourse)

        except Exception as e:
            showinfo(title='错误', message='选课错误！\n %s' % e)
            return

    def StopChoose(self):
        settings.isRunning = False


class SettingsFrame(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.flag = 0  # 是否有缓存内容，若无则刷新
        self.root = master  # 定义内部变量root
        self.selectedCourse = []
        self.delayVariable = StringVar()
        self.loopVariable = StringVar()
        if self.flag == 0:
            try:
                self.flag = 1

            except Exception as e:
                showinfo(title='错误', message='获取已选课程列表失败\n %s' % e)
        self.createPage()

    def createPage(self):
        frame1 = Frame(self, relief=RAISED, borderwidth=2)
        frame1.pack(side=TOP, fill=X, ipadx=13, ipady=13, expand=0)
        Label(frame1, text='选课参数设置', font=12).pack(side='top')
        Label(frame1, text='请求发送延迟(ms)', font=12).pack(side='left', padx=20)
        Spinbox(frame1, from_=300, to=800, increment=100, textvariable=self.delayVariable).pack(side='left', padx=20)
        Label(frame1, text='请求发送循环次数', font=12).pack(side='left', padx=20)
        Spinbox(frame1, from_=1, to=5, increment=1, textvariable=self.loopVariable).pack(side='left', padx=20)
        Label(self, text='\n选课计划(排序代表程序选课的先后次序）', font=8).pack(side='top')
        Button(self, text='保存并刷新', command=self.refresh).pack(side='top')
        ybar = Scrollbar(self, orient='vertical')  # 竖直滚动条
        self.tree = ttk.Treeview(self, show="headings", columns=('no', 'id', 'name', 'teacher', 'place'), height=20,
                                 yscrollcommand=ybar.set)
        ybar['command'] = self.tree.yview
        self.tree.column('no', width=35, anchor='center')
        self.tree.column('id', width=180, anchor='center')
        self.tree.column('name', width=150, anchor='center')
        self.tree.column('teacher', width=80, anchor='center')
        self.tree.column('place', width=300, anchor='center')
        self.tree.heading('no', text='序号')
        self.tree.heading('id', text='课程总号')
        self.tree.heading('name', text='课程名')
        self.tree.heading('teacher', text='教师')
        self.tree.heading('place', text='上课时间及地点')
        for i in range(len(settings.courses)):
            self.tree.insert('', i, values=(i + 1,
                                            settings.courses[i]['id'], settings.courses[i]['name'],
                                            settings.courses[i]['teacherName'], settings.courses[i]['teachingPlace']))
        self.tree.pack(side='left', expand='yes', fill='y')
        ybar.pack(side='left', expand='yes', fill='y')

    def refresh(self):
        try:
            if int(self.delayVariable.get()) < 300:
                showinfo(title='错误', message='请求发送延迟需大于300ms！')
            else:
                settings.delayVariable = int(self.delayVariable.get())

            if int(self.loopVariable.get()) < 1 or int(self.loopVariable.get()) > 10000:
                showinfo(title='错误', message='请求发送循环次数需在1到10000之间！')
            else:
                settings.loopVariable = int(self.loopVariable.get())
        except Exception as e:
            showinfo(title='错误', message='获取选课参数失败\n %s' % e)
            return

        try:
            self.selectedCourse = settings.courses
            x = self.tree.get_children()
            for item in x:
                self.tree.delete(item)
            for i in range(len(settings.courses)):
                self.tree.insert('', i, values=(i + 1,
                                                settings.courses[i]['id'], settings.courses[i]['name'],
                                                settings.courses[i]['teacherName'],
                                                settings.courses[i]['teachingPlace']))
            self.flag = 1

        except Exception as e:
            showinfo(title='错误', message='获取选课列表失败\n %s' % e)


class InfoPage(object):
    def __init__(self, master=None):
        self.root = master  # 定义内部变量root
        self.root.geometry('%dx%d' % (600, 600))  # 设置窗口大小
        self.root.resizable(0, 0)
        self.username = StringVar()
        self.password = StringVar()
        self.createPage()

    def createPage(self):
        self.page = Frame(self.root)  # 创建Frame
        self.page.pack()
        Label(self.page).grid(row=0, stick=W)
        img_open = Image.open("image/developer.png")
        global developer_png
        developer_png = ImageTk.PhotoImage(img_open.resize((400, 300), Image.ANTIALIAS))
        Label(self.page, image=developer_png, height=250).grid(row=1, column=0, columnspan=2)
        Label(self.page,
              text='本软件由:' + '\n' + 'Matt-Dong123(github.com/Matt-Dong123)' + '\n' + '和' + '\n' + 'ANDYWANGTIANTIAN(github.com/ANDYWANGTIANTIAN)'
                   + '\n' + '开发制作，项目地址https://github.com/Matt-Dong123/SZU_AutoCourseSelecter'
                            '，可以在深圳大学本科选课系统实现自动选课功能，详细使用方法请参考README.md'
                            '。本软件仅供学习交流使用，请勿用于真实选课环境中！！因使用本软件造成的一切后果均由软件使用者承担，软件开发者不承担任何责任！！如您同意以上免责声明，请点击“同意并进入”按钮，如不同意，请点击退出\n\n',
              font=12,
              wraplength=550).grid(row=2, column=0, columnspan=2)
        Button(self.page, text='同意并进入', font=12, command=self.GotoLoginPage, width=10).grid(row=5, column=0)
        Button(self.page, text='退出', width=10, font=12, command=self.page.quit).grid(row=5, column=1)

    def GotoLoginPage(self):
        self.page.destroy()
        LoginPage(self.root)


class AboutFrame(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.root = master  # 定义内部变量root
        self.createPage()

    def createPage(self):
        Label(self, text='如果觉得本软件好用，欢迎给我们打赏').grid(row=0, columnspan=2)
        img_open = Image.open("image/payment.jpg")
        global donate_png
        donate_png = ImageTk.PhotoImage(img_open.resize((300, 300), Image.ANTIALIAS))
        Label(self, image=donate_png, height=250).grid(row=1, column=0, columnspan=2)
        Label(self,
              text='本软件由:' + '\n' + 'Matt-Dong123(github.com/Matt-Dong123)' + '\n' + '和' + '\n' + 'ANDYWANGTIANTIAN(github.com/ANDYWANGTIANTIAN)'
                   + '\n' + '开发制作，可以在深圳大学本科选课系统实现自动选课功能，详细使用方法请参考README.md'
                            '。本软件仅供学习交流使用，请勿用于真实选课环境中！！因使用本软件造成的一切后果均由软件使用者承担，软件开发者不承担任何责任！如发现软件存在问题，欢迎点击下方按钮进行反馈\n',
              font=12,
              wraplength=550).grid(row=2, column=0, columnspan=2)

        Button(self, text='在github反馈问题', font=12, command=self.GoToGithub).grid(row=3, columnspan=2)

    def GoToGithub(self):
        webbrowser.open("http://www.baidu.com", new=0)


class LoginPage(object):
    def __init__(self, master=None):
        self.labelText1 = StringVar()
        self.labelText2 = StringVar()
        self.labelText3 = StringVar()
        self.labelEntry1 = StringVar()
        self.labelEntry2 = StringVar()
        self.labelEntry3 = StringVar()
        self.root = master  # 定义内部变量root
        self.root.geometry('%dx%d' % (600, 400))  # 设置窗口大小
        self.root.resizable(0, 0)
        self.var_SelUrl = IntVar()  # 选择校内、校外模式
        self.var_SelMode = IntVar()  # 选择登录方法（账户密码、Cookie）
        self.createPage()

    def createPage(self):
        self.labelText1.set("账号(学号)")
        self.labelText2.set("密码")
        self.labelText3.set("此项无需填写")
        self.var_SelUrl.set(0)
        self.var_SelMode.set(0)
        self.page = Frame(self.root)  # 创建Frame
        self.page.pack()

        Label(self.page, text='\n\n登录选课系统\n', font=12).grid(row=1, columnspan=2)
        Radiobutton(self.page, text="使用账户密码登录", variable=self.var_SelMode, value=0,
                    command=self.SelMode).grid(row=2)
        Radiobutton(self.page, text="使用Cookie登录", variable=self.var_SelMode, value=1,
                    command=self.SelMode).grid(row=2, column=1)
        Label(self.page, textvariable=self.labelText1).grid(row=3, pady=10)

        Entry(self.page, textvariable=self.labelEntry1).grid(row=3, column=1)
        Label(self.page, textvariable=self.labelText2).grid(row=4, pady=10)
        Entry(self.page, textvariable=self.labelEntry2, show='*').grid(row=4, column=1)
        Label(self.page, textvariable=self.labelText3).grid(row=5, pady=10)
        Entry(self.page, textvariable=self.labelEntry3).grid(row=5, column=1)
        Radiobutton(self.page, text="校内模式(bkxk.szu.edu.cn)", variable=self.var_SelUrl, value=0,
                    command=self.SelUrl).grid(row=6, column=0)
        Radiobutton(self.page, text="校外模式尚未完成(bkxk.webvpn.szu.edu.cn)", variable=self.var_SelUrl, value=1,
                    command=self.SelUrl, state="disabled").grid(row=6, column=1)
        Button(self.page, text='登录', command=self.loginCheck).grid(row=7, pady=10)
        Button(self.page, text='退出', command=self.page.quit).grid(row=7, column=1)
        Label(self.page, text='点击登录后，会有短暂的卡顿，请稍等', font=10).grid(row=8, columnspan=2)

    def loginCheck(self):
        if self.var_SelMode.get() == 1:
            settings.user_id = self.labelEntry1.get()
            settings.cookie = self.labelEntry2.get()
            settings.token = self.labelEntry3.get()
            settings.Mode = 1
        else:
            settings.Mode = 0
            settings.user_id = self.labelEntry1.get()
            settings.user_pass = self.labelEntry2.get()
            parent_conn, child_conn = Pipe()
            p = Process(target=encrypt.encrypt, args=(settings.user_pass, child_conn))
            p.start()
            p.join()
            settings.user_encrypted_pass = parent_conn.recv()
            StatusCode = settings.user_pass

            try:
                vtoken = login.get_vtoken()
                Code = login.get_vimage(vtoken)
                Status = login.LogIn(Code, vtoken)
            except ValueError:
                showinfo(title='错误', message='发生错误！请检查是否使用了代理，如使用，请关闭一切代理并重试！')
                return
            except Exception as e:
                showinfo(title='错误', message='未知错误 %s' % e)
                return

            if Status['code'] == '1':
                MainPage(self.root)
                self.page.destroy()
                showinfo(title='登录成功',
                         message='欢迎您!  ' + settings.user_name + "\n学号: " + settings.user_id + "\n学院: " + settings.user_college + "\n专业: " + settings.user_department + "\n班级: " + settings.user_class)
            else:
                showinfo(title='错误', message=Status['msg'])

    def SelMode(self):
        if self.var_SelMode.get() == 1:
            self.labelText2.set("Cookie")
            self.labelText3.set("Token")
            # self.tokenEntry.configure(state="disabled")
        else:
            self.labelText2.set("密码")
            self.labelText3.set("此项无需填写")
            # self.tokenEntry.configure(state="disabled")

    def SelUrl(self):
        dic = {0: '校内模式', 1: '校外模式'}
        s = "您选了" + dic.get(self.var_SelUrl.get())
        if self.var_SelUrl.get() == 0:
            settings.url = 'http://bkxk.szu.edu.cn/'
        else:
            settings.url = 'https://bkxk.webvpn.szu.edu.cn/'

    def MainPage(self):
        self.page.destroy()
        MainPage(self.root)


class MainPage(object):
    def __init__(self, master=None):
        self.root = master  # 定义内部变量root
        self.root.geometry('%dx%d' % (800, 600))  # 设置窗口大小
        self.root.resizable(0, 0)
        self.createPage()

    def createPage(self):
        # 本班课程： 'TJKC'
        # 方案内课程: 'FANKC'
        # 方案外课程： 'FAWKC'
        # 校公选课： 'XGXK'
        # 慕课: "MOOC"，
        # 辅修课程: "FXKC"，
        # 体育课程:"TYKC"
        self.SelectedCourse = SelectedCourseFrame(self.root)  # 创建不同Frame
        self.ClassCoursePage = CourseFrame(self.root, _type='TJKC')
        self.InCoursePage = CourseFrame(self.root, _type='FANKC')
        self.OutCoursePage = CourseFrame(self.root, _type='FAWKC')
        self.PublicCoursePage = CourseFrame(self.root, _type='XGXK')
        self.MOOCPage = CourseFrame(self.root, _type='MOOC')
        self.FuxiuPage = CourseFrame(self.root, _type='FXKC')
        self.SportCoursePage = CourseFrame(self.root, _type='TYKC')
        self.SettingsPage = SettingsFrame(self.root)
        self.StartChoosePage = StartChooseFrame(self.root)
        self.AboutPage = AboutFrame(self.root)
        self.SelectedCourse.pack()  # 默认显示数据录入界面
        menubar = Menu(self.root)
        menubar.add_command(label='已选课程', command=self.GotoSelectedCourse)
        menubar.add_command(label='本班课程', command=self.GotoClassCourse)
        menubar.add_command(label='方案内课程', command=self.GotoInCourse)
        menubar.add_command(label='方案外课程', command=self.GoToOutCourse)
        menubar.add_command(label='校公选课', command=self.GoToPublicCourse)
        menubar.add_command(label='慕课', command=self.GoToMoocCourse)
        menubar.add_command(label='辅修课程', command=self.GoToFuxiuCourse)
        menubar.add_command(label='体育课程', command=self.GoToSportCourse)
        menubar.add_command(label='参数设置', command=self.GoToSettings)
        menubar.add_command(label='开始选课', command=self.GoToStartChooseCourse)
        menubar.add_command(label='关于本软件', command=self.GoToAbout)
        self.root['menu'] = menubar  # 设置菜单栏

    def GotoSelectedCourse(self):
        self.SelectedCourse.pack()
        self.ClassCoursePage.pack_forget()
        self.InCoursePage.pack_forget()
        self.PublicCoursePage.pack_forget()
        self.OutCoursePage.pack_forget()
        self.MOOCPage.pack_forget()
        self.FuxiuPage.pack_forget()
        self.AboutPage.pack_forget()
        self.SportCoursePage.pack_forget()
        self.SettingsPage.pack_forget()
        self.StartChoosePage.pack_forget()

    def GotoClassCourse(self):
        self.SelectedCourse.pack_forget()
        self.InCoursePage.pack_forget()
        self.PublicCoursePage.pack_forget()
        self.OutCoursePage.pack_forget()
        self.MOOCPage.pack_forget()
        self.FuxiuPage.pack_forget()
        self.SportCoursePage.pack_forget()
        self.SettingsPage.pack_forget()
        self.AboutPage.pack_forget()
        self.ClassCoursePage.pack()
        self.StartChoosePage.pack_forget()

    def GotoInCourse(self):
        self.SelectedCourse.pack_forget()
        self.ClassCoursePage.pack_forget()
        self.PublicCoursePage.pack_forget()
        self.OutCoursePage.pack_forget()
        self.MOOCPage.pack_forget()
        self.FuxiuPage.pack_forget()
        self.SportCoursePage.pack_forget()
        self.SettingsPage.pack_forget()
        self.AboutPage.pack_forget()
        self.InCoursePage.pack()
        self.StartChoosePage.pack_forget()

    def GoToOutCourse(self):
        self.SelectedCourse.pack_forget()
        self.ClassCoursePage.pack_forget()
        self.InCoursePage.pack_forget()
        self.PublicCoursePage.pack_forget()
        self.MOOCPage.pack_forget()
        self.FuxiuPage.pack_forget()
        self.SportCoursePage.pack_forget()
        self.AboutPage.pack_forget()
        self.SettingsPage.pack_forget()
        self.OutCoursePage.pack()
        self.StartChoosePage.pack_forget()

    def GoToPublicCourse(self):
        self.SelectedCourse.pack_forget()
        self.ClassCoursePage.pack_forget()
        self.InCoursePage.pack_forget()
        self.OutCoursePage.pack_forget()
        self.MOOCPage.pack_forget()
        self.FuxiuPage.pack_forget()
        self.SportCoursePage.pack_forget()
        self.SettingsPage.pack_forget()
        self.AboutPage.pack_forget()
        self.PublicCoursePage.pack()
        self.StartChoosePage.pack_forget()

    def GoToMoocCourse(self):
        self.SelectedCourse.pack_forget()
        self.ClassCoursePage.pack_forget()
        self.InCoursePage.pack_forget()
        self.OutCoursePage.pack_forget()
        self.FuxiuPage.pack_forget()
        self.SportCoursePage.pack_forget()
        self.SettingsPage.pack_forget()
        self.PublicCoursePage.pack_forget()
        self.AboutPage.pack_forget()
        self.MOOCPage.pack()
        self.StartChoosePage.pack_forget()

    def GoToFuxiuCourse(self):
        self.SelectedCourse.pack_forget()
        self.ClassCoursePage.pack_forget()
        self.InCoursePage.pack_forget()
        self.OutCoursePage.pack_forget()
        self.SportCoursePage.pack_forget()
        self.SettingsPage.pack_forget()
        self.PublicCoursePage.pack_forget()
        self.MOOCPage.pack_forget()
        self.AboutPage.pack_forget()
        self.FuxiuPage.pack()
        self.StartChoosePage.pack_forget()

    def GoToSportCourse(self):
        self.SelectedCourse.pack_forget()
        self.ClassCoursePage.pack_forget()
        self.InCoursePage.pack_forget()
        self.OutCoursePage.pack_forget()
        self.FuxiuPage.pack_forget()
        self.SettingsPage.pack_forget()
        self.PublicCoursePage.pack_forget()
        self.MOOCPage.pack_forget()
        self.AboutPage.pack_forget()
        self.SportCoursePage.pack()
        self.StartChoosePage.pack_forget()

    def GoToSettings(self):
        self.SelectedCourse.pack_forget()
        self.ClassCoursePage.pack_forget()
        self.InCoursePage.pack_forget()
        self.OutCoursePage.pack_forget()
        self.FuxiuPage.pack_forget()
        self.SportCoursePage.pack_forget()
        self.PublicCoursePage.pack_forget()
        self.MOOCPage.pack_forget()
        self.AboutPage.pack_forget()
        self.SettingsPage.pack()
        self.StartChoosePage.pack_forget()

    def GoToStartChooseCourse(self):
        self.SelectedCourse.pack_forget()
        self.ClassCoursePage.pack_forget()
        self.InCoursePage.pack_forget()
        self.OutCoursePage.pack_forget()
        self.FuxiuPage.pack_forget()
        self.SportCoursePage.pack_forget()
        self.PublicCoursePage.pack_forget()
        self.MOOCPage.pack_forget()
        self.SettingsPage.pack_forget()
        self.AboutPage.pack_forget()
        self.StartChoosePage.pack()

    def GoToAbout(self):
        self.SelectedCourse.pack_forget()
        self.ClassCoursePage.pack_forget()
        self.InCoursePage.pack_forget()
        self.OutCoursePage.pack_forget()
        self.FuxiuPage.pack_forget()
        self.SportCoursePage.pack_forget()
        self.PublicCoursePage.pack_forget()
        self.MOOCPage.pack_forget()
        self.SettingsPage.pack_forget()
        self.StartChoosePage.pack_forget()
        self.AboutPage.pack()


def StartRun():
    root = Tk()
    root.title('SZU选课助手')
    root.iconbitmap('image/favicon.ico')
    InfoPage(root)
    root.mainloop()

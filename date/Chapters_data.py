import json
import shutil
from msilib.schema import Environment
from time import sleep

import yaml

from common.COM_path import *
from common.my_log import mylog
from date.Chapters_API import APiClass
import sqlite3


class UserData(APiClass):
    _instance = None

    def __init__(self):
        self.fashion_dir = {}
        self.story_info = {}
        self.story_cfg_chapter_dir = {}
        self.story_select_dir = {}
        self.check_list = []
        self.downloadbook_sign = False
        self.bookresult_dir = {}
        self.checkConf = {}
        print("导入用户数据成功")
        self.getdata()

    def getdata(self):
        self.clear()
        self.yamldata_conf()
        self.get_set()
        self.yaml_bookinfo()
        self.format_bookread_yml()
        self.yaml_bookread_result()
        self.getCheck()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance

    def getCheck(self):
        if self.checkConf:
            self.getCheckList_all()
        else:
            self.getCheckList()

    def yaml_bookinfo(self):
        """获取检测yaml"""
        yamlbook_listpath = os.path.join(Desktoppath, "bookCheck_result.yml")
        self.bookresult_dir = self.read_yaml(yamlbook_listpath)
        return self.bookresult_dir

    def yamldata_conf(self):
        # 读取yamlconf数据
        data = None
        loginInfo = {}
        path = os.path.join(path_YAML_FILES, "conf.yml")
        with open(path, encoding="utf-8") as f:
            data = yaml.load(f.read(), Loader=yaml.Loader)
        self.checkConf["is_all"] = data["CheckConf"]["is_all"]

    def getSumChapter(self,bookid):
        self.download_bookresource(bookid)
        bookpath = bookid + "\\data_s\\"
        path = os.path.join(path_resource, bookpath)
        data_s = os.listdir(path)
        return int(len(data_s) / 2)

    def getCheckList_all(self):
        """获取检测列表"""
        for bookchapter,v in self.bookresult_dir.items():
            # print(len(bookchapter))
            if v=="True":
                continue
            chapter = str(bookchapter)
            length = len(chapter)
            if length == 5:
                # bookid = bookchapter[:5]
                # chapterid = bookchapter[5:]
                index = self.getSumChapter(chapter)
                for i in range(1, index + 1):
                    s = "%03d" % i
                    mychapter = chapter + str(s)
                    print("检测章节", mychapter)
                    self.check_list.append(int(mychapter))
            elif length == 8 or length == 17:
                bookid = chapter[:5]
                # chapterid = chapter[5:]
                index = self.getSumChapter(bookid)
                for i in range(1, index + 1):
                    s = "%03d" % i
                    mychapter = bookid + str(s)
                    print("检测章节:", mychapter)
                    self.check_list.append(int(mychapter))
            else:
                print("书籍列表配置错误，请注意格式")
                return

    def getCheckList(self):
        """获取检测列表"""
        for bookchapter in self.bookresult_dir.keys():
            chapter = str(bookchapter)
            if len(chapter) == 5:
                index = self.getSumChapter(chapter)
                for i in range(1, index + 1):
                    s = "%03d" % i
                    mychapter = chapter + str(s)
                    print("检测章节", mychapter)
                    self.check_list.append(int(mychapter))
            elif len(chapter) == 8:
                if self.bookresult_dir[bookchapter] is None or type(self.bookresult_dir[bookchapter]) == int:
                    self.check_list.append(bookchapter)
                    print("单章节", bookchapter)
            elif len(chapter) == 17:
                if self.bookresult_dir[bookchapter] is None:
                    bookchapters = bookchapter.split("-")
                    beginchapter = bookchapters[0]
                    endchapter = bookchapters[1]
                    index = int(endchapter) - int(beginchapter)
                    for i in range(index + 1):
                        bookchapter = int(beginchapter) + i
                        print("章节区间", bookchapter)
                        self.check_list.append(bookchapter)
            else:
                print("书籍列表配置错误，请注意格式-->",chapter)
                return
        return self.check_list

    def update_record_bookread(self, chapter, result):
        """更新已经阅读的书籍信息"""
        file_path = os.path.join(Desktoppath, "bookCheck_result.yml")
        if type(self.bookresult_dir) != dict:
            self.bookresult_dir = {}
        self.bookresult_dir[chapter] = result
        with open(file_path, 'w+', encoding="utf-8") as f:
            yaml.dump(self.bookresult_dir, f, allow_unicode=True)
        return self.bookresult_dir

    def yaml_bookread_result(self):
        file_path = os.path.join(Desktoppath, "bookCheck_result.yml")
        with open(file_path, encoding='utf-8') as file:
            self.bookresult_dir = yaml.safe_load(file)
        return self.bookresult_dir

    def get_select(self):
        mylist = []
        for v in self.story_cfg_chapter_dir.values():
            if type(v) == dict and v["select_id"]:
                mylist.append(v["select_id"])
        mylist = list(set(mylist))

    def getDefaultFashion(self, bookid, role_id):
        """获取角色默认fashion"""
        role_id = str(role_id)
        role_id = str(role_id)
        if role_id not in self.fashion_dir:
            data = self.storyrole(book_id=bookid, role_ids=role_id)
            role_list = self.getfashion_list(data[len(data) - 1], role_id)
        else:
            role_list = self.fashion_dir[role_id]
        return role_list

    def getDIYFashion(self, fashion_id):
        """获取DIY装扮"""
        fashion_list = []
        if fashion_id is not None and fashion_id != "0":
            if fashion_id not in self.fashion_dir:
                fashion_id = str(fashion_id)
                data = self.fashionShowApi(fashion_ids=fashion_id)
                if len(data) > 0:
                    fashion_list = self.getfashion_list(data[len(data) - 1], fashion_id)
                    # fashion_list = self.getfashion_list(data[0], fashion_id)
                    self.fashion_dir[fashion_id] = fashion_list
                else:
                    content = "【fashion异常】：{}的内容为空".format(fashion_id)
                    MyData.error_dir[fashion_id] = content
                    mylog.error(content)
                    print(content)
            else:
                fashion_list = self.fashion_dir[fashion_id]
        return fashion_list

    def getfashion_list(self, data, fashion_id):
        """装扮列表"""
        list = ['body', 'cloth', 'hair', 'back1', 'back2', 'back3', 'back4', 'dec1', 'dec2', 'dec4', 'dec5', 'face1',
                'face2']
        fashion_list = []
        for i in list:
            if i in data.keys():
                if data[i]:
                    fashion_list.append({i: data[i]})
        self.fashion_dir[fashion_id] = fashion_list
        return fashion_list

    def r_yaml_fashion(self):
        """读角色fashion"""
        file_path = os.path.join(path_YAML_FILES, "yamlBookRead/rolefashion.yml")
        with open(file_path, encoding='utf-8') as file:
            self.fashion_dir = yaml.safe_load(file)
        if self.fashion_dir is None:
            self.fashion_dir = {'000000': ["Body"]}
        return self.fashion_dir

    def w_yaml_fashion(self):
        """写角色fashion"""
        file_path = os.path.join(path_YAML_FILES, "yamlBookRead/rolefashion.yml")
        with open(file_path, 'w+', encoding="utf-8") as f:
            yaml.dump(self.fashion_dir, f, allow_unicode=True)

    # def format_bookread_yml(self):
    #     """格式化书籍阅读记录yml"""
    #     mydir = {}
    #     if type(self.bookresult_dir) == dict:
    #         return
    #     list1 = self.bookresult_dir.split("第")
    #     if list1:
    #         for i in range(0, len(list1) - 1):
    #             if list1[i]:
    #                 list2 = list1[i].split("：")[1]
    #                 list3 = list2.split("[new]")[0]
    #                 mydir[list3] = None
    #     yamlbook_listpath = os.path.join(Desktoppath, "bookCheck_result.yml")
    #     with open(yamlbook_listpath, 'w+', encoding="utf-8") as f:
    #         yaml.dump(mydir, f, allow_unicode=True)
    def format_bookread_yml(self):
        """格式化书籍阅读记录yml"""
        mydir = {}
        # ast.literal_eval(user_info)
        if type(self.bookresult_dir) == dict:
            return
        list1 = self.bookresult_dir.split("[new]")
        if list1:
            for i in range(0, len(list1)-1):
                chapter =list1[i][len(list1[i])-8:len(list1[i])-3]
                mydir[chapter]=None
        yamlbook_listpath = os.path.join(Desktoppath, "bookCheck_result.yml")
        with open(yamlbook_listpath, 'w+', encoding="utf-8") as f:
            yaml.dump(mydir, f, allow_unicode=True)

    def download_bookresource(self, bookid):
        """拉取书籍资源"""
        file = os.path.join(path_resource, bookid)
        mybool = os.path.exists(file)
        if mybool:
            return True
        re=self.avgcontentApi(bookid)
        if re:
            print("下载书籍配置成功")
            return True
        else:
            return False
    def read_story_cfg_chapter(self, bookid, chapter_id):
        """读取当前章节信息txt"""
        bookpath = bookid + "\\data_s\\" + chapter_id + "_chat.txt"
        selectpath = bookid + "\\data_s\\" + chapter_id + "_select.txt"
        path = os.path.join(path_resource, bookpath)
        path1 = os.path.join(path_resource, selectpath)
        with open(path, "r", encoding='utf-8') as f:  # 设置文件对象
            data = f.read()  # 可以是随便对文件的操作
        data = eval(data)
        self.story_cfg_chapter_dir[chapter_id] = data
        with open(path1, "r", encoding='utf-8') as f:  # 设置文件对象
            selectdata = f.read()  # 可以是随便对文件的操作
        self.story_select_dir[chapter_id] = eval(selectdata)
        return self.story_cfg_chapter_dir[chapter_id]

    def read_yaml(self, filepath):
        with open(filepath, encoding='utf-8') as file:
            value = yaml.safe_load(file)
        return value

    def clear(self):
        """清空之前的报告和文件"""
        print("清空文件中")
        filelist = os.listdir(path_resource)
        for fileName in filelist:
            filepath = os.path.join(path_resource,fileName)
            if os.path.isdir(filepath):
                shutil.rmtree(filepath)
            else:
                os.remove(filepath)
        path = os.path.join(path_LOG_MY, "logging.log")
        with open(path, 'w') as f1:
            f1.seek(0)
            f1.truncate()
        self.w_yaml_fashion()
        print("完成清空文件")


MyData = UserData()
# print(MyData.check_list)

# newrole_list = self.getUserStoryData_fashion(self.UserData_dir["uuid"], bookid, role_id)
# bookid = "51603"
# role_id = "100005995"
# fashion_ids1 = "1000014944"
# data = MyData.storyrole(book_id=bookid, role_ids=role_id)
# print("默认角色",data)
# # # sun=len(data)-1
# # # data=data[sun]
# # # print("角色默认fashion", data)
# # list1=MyData.getDefaultFashion(bookid,role_id)
# # print("默认角色",MyData.fashion_dir)
# list2=MyData.getDIYFashion(fashion_ids1)
# print("DIY",list2)
# print("我的角色",MyData.fashion_dir)

# role_list = self.getfashion_list(date[len(date) - 1], role_id)
# fashion_ids1="1000050135"
# # role_id2="1605108"
# # # MyData.r_yaml_fashion()
# date = MyData.getfashion(bookid, role_id, fashion_ids1)
# print(date)

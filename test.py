import ast
import json
import shutil
from msilib.schema import Environment
from time import sleep

import yaml

from common.COM_path import *
from common.my_log import mylog
from date.Chapters_API import APiClass
import sqlite3


class Test(APiClass):
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
    def download_bookresource(self, bookid):
        """拉取书籍资源"""
        file = os.path.join(path_resource, bookid)
        mybool = os.path.exists(file)
        if mybool:
            return
        self.avgcontentApi(bookid)
        print("下载书籍配置成功")

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
            print(chapter,length)
            if length == 5:
                # bookid = bookchapter[:5]
                # chapterid = bookchapter[5:]
                index = self.getSumChapter(chapter)
                for i in range(1, index + 1):
                    s = "%03d" % i
                    mychapter = chapter + str(s)
                    print("整本书", mychapter)
                    self.check_list.append(int(mychapter))
            elif length == 8 or length == 17:
                bookid = chapter[:5]
                # chapterid = chapter[5:]
                index = self.getSumChapter(bookid)
                for i in range(1, index + 1):
                    s = "%03d" % i
                    mychapter = bookid + str(s)
                    print("整本书", mychapter)
                    self.check_list.append(int(mychapter))
            else:
                print("书籍列表配置错误，请注意格式")
                return

    def getCheckList(self):
        """获取检测列表"""
        print(self.bookresult_dir)
        for bookchapter in self.bookresult_dir.keys():
            # print(len(bookchapter))
            chapter = str(bookchapter)
            if len(chapter) == 5:
                # bookid = bookchapter[:5]
                # chapterid = bookchapter[5:]
                index = self.getSumChapter(chapter)
                for i in range(1, index + 1):
                    s = "%03d" % i
                    mychapter = chapter + str(s)
                    print("整本书", mychapter)
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
                print("书籍列表配置错误，请注意格式")
                print(chapter)
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
        print("记录阅读结果", self.bookresult_dir)
        return self.bookresult_dir

    def yaml_bookread_result(self):
        file_path = os.path.join(Desktoppath, "bookCheck_result.yml")
        with open(file_path, encoding='utf-8') as file:
            self.bookresult_dir = yaml.safe_load(file)
        return self.bookresult_dir



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

    def read_yaml(self, filepath):
        with open(filepath, encoding='utf-8') as file:
            value = yaml.safe_load(file)
        return value

    def clear(self):
        """清空之前的报告和文件"""
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


MyData = Test()
print(MyData.check_list)
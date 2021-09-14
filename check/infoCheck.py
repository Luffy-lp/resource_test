import os
from time import sleep

from pymediainfo import MediaInfo

from common.COM_path import path_resource
from common.my_log import mylog
from date.Chapters_data import MyData
from time import perf_counter, sleep


class Check():

    def __init__(self):
        self.bookid = None
        self.chapterid = None
        self.bookchapter = None
        self.downloadbook_sign = False
        self.initialize()
        self.error_dir = {}

    def initialize(self):
        """初始化"""
        MyData.story_cfg_chapter_dir = {}
        self.select_info = {}
        self.role_fashion_dir = {}
        self.bg_check_list = []
        self.bgm_check_list = []
        self.show_check_list = []
        self.sound_check_list = []
        self.face_check_dir = {}
        self.role_check_dir = {}
        self.role_resources_dir = {}
        self.bg_resources_list = []
        self.bgm_resources_list = []
        self.face_resources_list = []
        self.sound_resources_list = []

    def check(self):
        """单章检测流程"""

        MyData.download_bookresource(self.bookid)  # 拉取全书对白配置
        MyData.read_story_cfg_chapter(self.bookid, self.bookchapter)  # 存储章节对白配置
        chats_info = MyData.story_cfg_chapter_dir[self.bookchapter]  # 当前阅读章节信息
        self.select_info = MyData.story_select_dir[self.bookchapter]  # 当前阅读选项信息
        self.add_check_info(chats_info)  # 生成需要检测的信息
        MyData.download_bookresource(self.bookchapter)  # 拉取章节资源
        self.getfile_name()  # 获取资源文件用于对比
        self.contrast()  # 对比并给出结果

    def contrast(self):
        """对比"""
        for role_id, idlist in self.role_check_dir.items():
            self.error_dir[self.bookchapter][role_id] = []
            for parts in idlist:
                for part, file in parts.items():
                    result = self.role_fileCompare(part, role_id, file)
                    if result is False:
                        file_1 = file + "_1"
                        result = self.role_fileCompare(part, role_id, file_1)
                        if result is False:
                            content = "【角色资源异常】：角色包{0}中{1}未发现{2}文件".format(role_id, part, file)
                            mylog.error(content)
                            self.error_dir[self.bookchapter][role_id].append(content)
                    else:
                        content = "【角色资源正常】：角色包{0}中{1}发现{2}文件".format(role_id, part, file)
                        print(content)

        for role_id, fashionidlist in self.face_check_dir.items():
            for i in fashionidlist:
                if role_id not in self.role_resources_dir:
                    content = "【face资源文件夹异常】:资源包未找到{}的文件夹".format(role_id)
                    MyData.error_dir[role_id] = content
                    mylog.error(content)
                else:
                    k = i + ".png"
                    if k in self.role_resources_dir[role_id]:
                        content = "【face资源正常】:资源包{0}找到{1}的文件夹".format(role_id, k)
                        print(content)
                    else:
                        k1 = i + "_1" + ".png"
                        if k1 in self.role_resources_dir[role_id]:
                            content = "【face资源正常】:资源包{0}找到{1}的文件夹".format(role_id, k)
                            print(content)
                            continue
                        content = "【face资源异常】：角色包{0}中未发现{1} 资源".format(role_id, i)
                        mylog.error(content)
                        self.error_dir[self.bookchapter][role_id].append(content)

        for bg in self.bg_check_list:
            path = self.bookchapter + "/background/" + bg
            bgbool = self.fileCompare(path)
            self.com_result(bgbool, bg, "背景")
        for bgm in self.bgm_check_list:
            path = self.bookchapter + "/sound/bgm/" + bgm
            bgmbool = self.fileCompare(path)
            self.com_result(bgmbool, bgm, "音乐")

        for sound in self.sound_check_list:
            path = self.bookchapter + "/sound/sound/" + sound
            soundbool = self.fileCompare(path)
            self.com_result(soundbool, sound, "音效")

    def com_result(self, result, parInfo , des):
        """通用结果"""
        if result:
            content = "【{0}资源正常】：找到{1}资源".format(des, parInfo)
            print(content)
        else:
            content = "【{0}资源异常】：{1}资源丢失".format(des, parInfo)
            mylog.error(content)

    def add_check_info(self, chats_info):
        """添加检测信息"""
        for chat in chats_info.values():
            self.add_role_id(chat)
            self.add_friend_id(chat)
            self.add_bg_id(chat)
            self.add_bgm_id(chat)
            self.add_show_id(chat)
            self.add_video_id(chat)
            self.add_sound_name(chat)
        self.de_weight()
        self.get_roleFashionFilename()

    def de_weight(self):
        """去重"""
        self.bgm_check_list = set(self.bgm_check_list)
        self.bg_check_list = set(self.bg_check_list)
        self.show_check_list = set(self.show_check_list)
        self.sound_check_list = set(self.sound_check_list)

        # self.face_check_list = list(set(self.face_check_list))

        for i in self.role_fashion_dir:
            self.role_fashion_dir[i] = list(set(self.role_fashion_dir[i]))
        for i in self.face_check_dir:
            self.face_check_dir[i] = list(set(self.face_check_dir[i]))
        print("bgm_check_list", self.bgm_check_list)
        print("bg_check_list", self.bg_check_list)
        print("face_check_dir", self.face_check_dir)
        print("show_check_list", self.show_check_list)

    def get_roleFashionFilename(self):
        """获取路径，注意没有加png"""
        for role_id, role_list in self.role_fashion_dir.items():
            self.role_check_dir[role_id] = []
            Defaultlist = MyData.getDefaultFashion(self.bookid, role_id)  # 添加默认角色检测列表
            self.role_check_dir[role_id] = Defaultlist
            for fashion_id in role_list:
                fashionlist = MyData.getDIYFashion(fashion_id)
                for filename in fashionlist:
                    self.role_check_dir[role_id].append(filename)

    def add_bg_id(self, chat):
        bg_id = str(chat["scene_bg_id"])
        if bg_id and bg_id != "0":
            bg_id = bg_id + ".jpg"
            self.bg_check_list.append(bg_id)

    def add_bgm_id(self, chat):
        bgm_id = str(chat["bgm_id"])
        if bgm_id and bgm_id != "0":
            bgm_id = bgm_id + ".mp3"
            self.bgm_check_list.append(bgm_id)

    def add_role_id(self, chat):
        """增加角色以及相关"""
        role_id = str(chat["role_id"])
        select_id = str(chat["select_id"])
        if role_id and role_id != "0":
            if role_id not in self.role_fashion_dir:
                self.role_fashion_dir[role_id] = []
            if role_id not in self.role_check_dir:
                self.role_check_dir[role_id] = []
        else:
            return
        self.add_fashion_id(chat, role_id)
        self.add_select_id(chat, role_id, self.select_info, select_id)
        self.add_search_select_id(chat, role_id)
        self.add_face_id(chat, role_id)

    def add_fashion_id(self, chat, role_id):
        if "fashion_id" in chat:
            fashion_id = str(chat["fashion_id"])
            if fashion_id and fashion_id != "0":
                # if role_id=="100008873":
                #     print("myfashin",fashion_id)
                #     print("chat:",chat["id"])
                self.role_fashion_dir[role_id].append(fashion_id)

    def add_face_id(self, chat, role_id):
        face_id = str(chat["face_id"])
        if face_id and face_id != "0" and role_id and role_id != "0":
            if role_id not in self.face_check_dir:
                self.face_check_dir[role_id] = []
            self.face_check_dir[role_id].append(face_id)

    def add_select_id(self, chat, role_id, select_info, select_id, search=None):
        """添加信息"""
        self.role_check_dir[role_id]: list = []
        if select_id and select_id != "0":
            if select_id in select_info:
                for select in select_info[select_id].values():
                    if select["goodstype"]:
                        if select["goodstype"] == "fashion":
                            self.role_fashion_dir[role_id].append(select["goodsid"])
                        else:
                            self.role_check_dir[role_id].append(select["goodsid"])

            else:
                if search:
                    content = "【search_select_id反向查找配置异常】:id->{0}反向章节->{1}select配置中未找到{2}".format(search, chat["id"],
                                                                                                  select_id)
                    mylog.error(content)
                else:
                    content = "【select_id配置异常】:对白为id{0}的select_id{1}未找到".format(chat["id"], select_id)
                    mylog.error(content)

    def add_search_select_id(self, chat, role_id):
        """添加反向查找"""
        try:
            search_select_id = str(chat["search_select_id"])
        except:
            search_select_id = None
        if search_select_id and search_select_id != "0":
            chapters_id = search_select_id.split("*")[0]
            searchchapter = chapters_id
            book_id = chapters_id[:5]
            select_id = search_select_id.split("*")[1]
            MyData.download_bookresource(book_id)
            MyData.read_story_cfg_chapter(book_id, chapters_id)
            select_dir = MyData.story_select_dir[chapters_id]
            self.add_select_id(chat, role_id, select_dir, select_id, searchchapter)
            # self, chat, role_id, select_info, select_id, search = None

    # def add_content_check(self,chat):
    #     try:
    #         content = str(chat["content"])
    #         mind = str(chat["mind"])
    #     except:
    #         pass
    def mail(self, chat):
        mail_list = chat["mail"].split("#")
        try:
            if len(mail_list) > 1:
                mailTitle = mail_list[0]
                self.show_check_list.append(mail_list[1])
            else:
                mailTitle = mail_list[0]
        except:
            self.com_result(False, str(chat["id"]),"邮件配置")

    def add_chat_type(self, chat):
        chat_type = chat["chat_type"]
        if chat_type == 21:
            self.mail()

    def add_sound_name(self, chat):
        sound_name = str(chat["sound_name"])
        if sound_name and sound_name != "0":
            self.sound_check_list.append(sound_name)

    def add_show_id(self, chat):
        try:
            show_id = str(chat["show_id"])
        except:
            show_id = None
        if show_id and show_id != "0":
            self.show_check_list.append(show_id)

    def add_video_id(self, chat):
        try:
            video_id = str(chat["video_id"])
        except:
            video_id = None
        if video_id and video_id != "0":
            video_list = video_id.split("#")
            self.show_check_list.append(video_list[1])
            self.role_check_dir[video_list[0]]
            if video_list[0] not in self.role_check_dir:
                self.role_check_dir[video_list[0]] = []

    def add_friend_id(self, chat):
        friend_id = None
        if chat["chat_type"] == 8 or chat["chat_type"] == 15 or chat["chat_type"] == 16 or chat["chat_type"] == 19 or \
                chat["chat_type"] == 26 or chat["chat_type"] == 29 or chat["chat_type"] == 30:
            friend_id = str(chat["friend_id"])
            if friend_id and friend_id != "0":
                pass
            else:
                content = "【friend_id资源异常】:对白{}类型为{}的friend_id为空".format(chat["id"], chat["chat_type"])
                mylog.error(content)
                self.error_dir["friend_id"] = content

        if "friend_id" in chat:
            friend_id = str(chat["friend_id"])
            if friend_id and friend_id != "0":
                if friend_id not in self.role_fashion_dir:
                    self.role_fashion_dir[friend_id] = []
            else:
                return
        else:
            print("没有friend_id")
            return
        if "friend_fashion_id" in chat:
            friend_fashion_id = str(chat["friend_fashion_id"])
            if friend_fashion_id and friend_id != "0":
                self.role_fashion_dir[friend_id].append(friend_fashion_id)

    def fileCompare(self, filepath, size=10):
        """文件比较"""
        fileName = os.path.join(path_resource, filepath)
        print(fileName)
        filebool = os.path.exists(fileName)
        if filebool:
            mysize = os.path.getsize(fileName)
            if mysize > size:
                print(mysize)
            else:
                filebool = False
        return filebool

    def role_fileCompare(self, part, role_id, fileName, size=10):
        """角色文件比较"""
        file = self.bookchapter + "/role/" + role_id + '/' + part + '/' + fileName + ".png"
        fileName = os.path.join(path_resource, file)
        filebool = os.path.exists(fileName)
        if filebool:
            mysize = os.path.getsize(fileName)
            if mysize > size:
                print(mysize)
            else:
                filebool = False
        return filebool

    def getfile_name(self):
        for role_id in self.role_check_dir:
            file = self.bookchapter + "/role/" + role_id
            path = os.path.join(path_resource, file)
            self.role_resources_dir[role_id] = []
            for root, dirs, files in os.walk(path):
                self.role_resources_dir[role_id] = self.role_resources_dir[role_id] + files

    def clock(self, type=None):  # 计时器
        """stop结束返回时间"""
        global start_time
        if type == "stop":
            spendtime = '%.2f' % (perf_counter() - start_time)
            print("花费时间{}秒:".format(spendtime))
            return spendtime
        else:
            start_time = perf_counter()

    def result(self, bookchapter):
        if bookchapter not in MyData.bookresult_dir.keys():
            MyData.bookresult_dir[bookchapter] = 1
            print("newchapter is none")
        elif MyData.bookresult_dir[bookchapter] == "True" or MyData.bookresult_dir[bookchapter] == "False":
            print(bookchapter + "已存在结果{}".format(MyData.bookresult_dir[bookchapter]))
            # assert_equal(True, True, bookchapter + "已存在结果{}".format(MyData.bookresult_dir[bookchapter]))
            return True
        elif type(MyData.bookresult_dir[bookchapter]) == int:
            if MyData.bookresult_dir[bookchapter] >= 3:
                print(bookchapter + "失败3次跳过阅读")
                return True
            else:
                result = MyData.bookresult_dir[bookchapter] + 1
                MyData.update_record_bookread(bookchapter, result)
        else:
            MyData.update_record_bookread(bookchapter, 1)

    def getCheckList(self):
        """遍历检测"""
        for self.bookchapter in MyData.check_list:
            try:
                self.bookchapter = str(self.bookchapter)
                self.bookid = self.bookchapter[:5]
                self.chapterid = self.bookchapter[5:]
                self.clock()
                # mylog.info("=============================================================================")
                self.error_dir[self.bookchapter] = {}
                self.initialize()
                self.result(self.bookchapter)
                mylog.info(self.bookchapter + "======================>")
                # mylog.info("===开始" + self.bookchapter + "资源对比===")
                self.check()
                # mylog.info("===完成" + self.bookchapter + "资源对比===")
                MyData.update_record_bookread(self.bookchapter, "True")
                # mylog.info("=============================================================================")
                self.clock("stop")
            except Exception as e:
                mylog.error("执行失败：", e)
                MyData.update_record_bookread(self.bookchapter, "False")


if __name__ == '__main__':
    Check1 = Check()
    Check1.getCheckList()

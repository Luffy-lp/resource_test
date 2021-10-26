import os
from time import sleep

from common.COM_path import path_resource
from common.my_log import mylog
from date.Chapters_data import MyData
from time import perf_counter, sleep


class CheckManage():

    def __init__(self,bookid,chapterid,bookchapter):
        self.bookid = bookid
        self.chapterid = chapterid
        self.bookchapter = bookchapter
        self.initialize()

    def initialize(self):
        """初始化"""
        MyData.story_cfg_chapter_dir = {}
        self.select_info = {}
        self.role_fashion_dir = {}
        self.bg_check_list = []
        self.bgm_check_list = []
        self.show_check_list = []
        self.sound_check_list=[]
        self.face_check_dir = {}
        self.role_check_dir = {}
        self.role_resources_dir = {}
        self.bg_resources_list = []
        self.bgm_resources_list = []
        self.face_resources_list = []
        self.sound_resources_list=[]

    def add_bg_id(self, chat):
        """背景检测"""
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
        self.add_select_jump(chat, role_id, self.select_info, select_id)
        self.add_search_select_id(chat, role_id)
        self.add_face_id(chat, role_id)

    def add_is_finished(self, chat):
        """结束检测"""
        is_finished = str(chat["is_finished"])
        if is_finished == "1":
            self.chat.append(chat["id"])
            self.is_finished += 1
            if self.is_finished > 1:
                mylog.error(self.bookchapter + "is_finished数量:" + str(self.is_finished) + "对白:" + str(
                    self.chat[0]) + "||" + str(self.chat[1]))

    def add_fashion_id(self, chat, role_id):
        """fashion"""
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
        if select_id and select_id != 0 and select_id != "0":
            # print("select_id：",chat["id"],select_id)
            if select_id in select_info:
                for select in select_info[select_id].values():
                    if not select["jump_chat_id"] > 0:
                        content = "【jump_chat_id配置异常】:对白为id{0}的select_id{1}存在跳转为0".format(chat["id"], select_id)
                        mylog.error(content)
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

    def add_select_jump(self, chat, role_id, select_info, select_id, search=None):
        """jump信息查询"""
        self.role_check_dir[role_id]: list = []
        if select_id and select_id != 0 and select_id != "0":
            # print("select_id：",chat["id"],select_id)
            if select_id in select_info:
                select_dir = {}
                for select in select_info[select_id].values():
                    if not select["jump_chat_id"] in select_dir:
                        select_dir[select["jump_chat_id"]] = 1
                    else:
                        select_dir[select["jump_chat_id"]] += 1
                for key, vlus in select_dir.items():
                    if vlus == 2:
                        content = "【{3}】:对白为id{0}->select_id{1}->jump_chat_id：{2}存在跳转2次跳转".format(chat["id"], select_id,
                                                                                                  key, self.bookchapter)
                        mylog.error(content)
                    if not select["jump_chat_id"] > 0:
                        content = "【jump_chat_id配置异常】:对白为id{0}的select_id{1}存在跳转为0".format(chat["id"], select_id)
                        mylog.error(content)
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
            self.com_result(False, str(chat["id"]), "邮件配置")

    def add_chat_type(self, chat):
        chat_type = chat["chat_type"]
        if chat_type == 21:
            self.mail()

    def add_sound_name(self, chat):
        sound_name = str(chat["sound_name"])
        if sound_name and sound_name != "0":
            sound_name = sound_name + ".mp3"
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
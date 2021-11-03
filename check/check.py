import copy
import os
from threading import Thread
from time import sleep

from pymediainfo import MediaInfo

from common.COM_path import path_resource
from common.COM_utilities import report,fileCompare
from common.my_log import mylog
from date.Chapters_data import MyData
from time import perf_counter, sleep
# from check.checkData import CheckData
# from check.checkManage import CheckManage

class Check():
    def __init__(self,bookchapter):
        # self.bookid = None
        # self.chapterid = None
        # self.bookchapter = None
        # self.downloadbook_sign = False
        self.initialize(bookchapter)
    def initialize(self,bookchapter):
        """初始化"""
        self.chats_info = {}
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
        self.is_finished = 0
        self.chat = []
        self.bookchapter = str(bookchapter)
        self.bookid = self.bookchapter[:5]
        self.chapterid = self.bookchapter[5:]
        print("检测章节:", bookchapter)

    def getCheckList(self,bookchapter):
        """遍历检测"""
        # self.initialize(bookchapter)  # 初始化数据
        try:
            resultBool = self.result(self.bookchapter) #判断检查条件
            if resultBool: return
            self.download() #下载资源
            mylog.info(self.bookchapter + "======================>")
            self.add_check_info(self.chats_info)  #生成需要检测的信息
            self.getfile_name()  # 获取资源文件用于对比
            self.contrast()  # 对比并给出结果
            MyData.update_record_bookread(self.bookchapter, "True")
        except Exception as e:
            mylog.error("执行失败：", e)
            MyData.update_record_bookread(self.bookchapter, "False")
        print("完成检测章节:", bookchapter)

    def testing(self,chats_info):
        for chat in chats_info.values():
            re=self.roleId_check(self,chat)

    def add_check_info(self,chats_info):
        """添加检测信息"""
        for chat in chats_info.values():
            self.add_role_id(chat)
            self.add_select_jump(chat)
            self.add_is_finished(chat)
            self.add_friend_id(chat)
            self.add_bg_id(chat)
            self.add_bgm_id(chat)
            self.add_show_id(chat)
            self.add_video_id(chat)
            self.add_sound_name(chat)
        self.de_weight()
        self.get_roleFashionFilename()

    # def add_check_info(self,chats_info):
    #     """添加检测信息"""
    #     for chat in chats_info.values():
    #         self.add_test(chat)
    #     #     self.add_role_id(chat)
    #     #     self.add_is_finished(chat)
    #     #     self.add_friend_id(chat)
    #     #     self.add_bg_id(chat)
    #     #     self.add_bgm_id(chat)
    #     #     self.add_show_id(chat)
    #     #     self.add_video_id(chat)
    #     #     self.add_sound_name(chat)
    #     # self.de_weight()
    #     # self.get_roleFashionFilename()

    # def add_check_info(self,chats_info):
    #     """添加检测信息"""
    #     for chat in chats_info.values():
    #         self.add_test(chat)
    #     #     self.add_role_id(chat)
    #     #     self.add_is_finished(chat)
    #     #     self.add_friend_id(chat)
    #     #     self.add_bg_id(chat)
    #     #     self.add_bgm_id(chat)
    #     #     self.add_show_id(chat)
    #     #     self.add_video_id(chat)
    #     #     self.add_sound_name(chat)
    #     # self.de_weight()
    #     # self.get_roleFashionFilename()

    def download(self):
        """资源下载"""
        # try:
        print("书籍ID:",self.bookid)
        confresult = MyData.download_bookresource(self.bookid)  # 拉取全书对白配置
        if confresult is not True:
            report(False, "配置下载", self.bookchapter, "下载对白配置文件失败")
            return False
        resourceResult = MyData.download_bookresource(self.bookchapter)  # 拉取章节资源 555555555555555555555555555555555特殊处理
        if resourceResult is not True:
            report(False, "资源下载", self.bookchapter, "下载资源文件失败")
            return False
        self.chats_info = MyData.read_story_cfg_chat(self.bookid, self.bookchapter)  # 存储章节对白配置
        self.select_info = MyData.read_story_cfg_select(self.bookid, self.bookchapter)  # 当前阅读选项信息

    # def check(self):
    #     """单章检测流程"""
    # def report(self, result, type, chapter, des, roleID=None, chat=None):
    #     if not result:
    #         if chat:
    #             content = "{0}-->【{1}异常】-【角色{2}】-【对白{3}】：{4}".format(chapter, type, roleID, chat, des)
    #             mylog.error(content)
    #         else:
    #             content = "{0}-->【{1}异常】-【角色{2}】:{3}".format(chapter, type, roleID, des)
    #             mylog.error(content)\


    def role_fileCompare(self, part, role_id, fileName, size=10):
        """角色文件比较"""
        file = self.bookchapter + "/role/" + role_id + '/' + part + '/' + fileName + ".png"
        fileName = os.path.join(path_resource, file)
        filebool = os.path.exists(fileName)
        if filebool:
            mysize = os.path.getsize(fileName)
            if mysize > size:
                pass
                # print("文件大小正常")
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
            MyData.bookresult_dir[bookchapter] = None
            print("准备检测章节:", bookchapter)
        elif MyData.bookresult_dir[bookchapter] == "True" or MyData.bookresult_dir[bookchapter] == "False":
            print(bookchapter + "已存在结果{}".format(MyData.bookresult_dir[bookchapter]))
            # assert_equal(True, True, bookchapter + "已存在结果{}".format(MyData.bookresult_dir[bookchapter]))
            return True

    def contrast(self):
        """对比"""
        # if self.bookchapter == "52373001":
        #     for k, v in self.role_fashion_dir.items():
        #         print("52373001",k, v)
        for role_id, idlist in self.role_check_dir.items():
            for parts in idlist:
                for part, file in parts.items():
                    file=str(file)
                    result = self.role_fileCompare(part, role_id, file)
                    if result is False:
                        file_1 = file + "_1"
                        result = self.role_fileCompare(part, role_id, file_1)
                        if result is False:
                            content = "未发现{0}文件".format(file)
                            report(False, part+"资源", self.bookchapter, content, roleID=role_id)

        for role_id, fashionidlist in self.face_check_dir.items():
            for i in fashionidlist:
                if role_id not in self.role_resources_dir:
                    content = "未找到{0}的文件".format(role_id)
                    report(False, "face文件", self.bookchapter, content, roleID=role_id)
                else:
                    k = i + ".png"
                    if k in self.role_resources_dir[role_id]:
                        pass
                        # content = "未找到{0}的文件".format(k)
                        # report(False, "face资源", self.bookchapter, content, roleID=role_id)
                    else:
                        k1 = i + "_1" + ".png"
                        if k1 in self.role_resources_dir[role_id]:
                            continue
                        content = "未发现{0} 资源".format(i)
                        report(False, "face资源", self.bookchapter, content, roleID=role_id)

        for bg in self.bg_check_list:
            path = self.bookchapter + "/background/" + bg
            bgbool = fileCompare(path)
            content = "未发现{}资源".format(bg)
            report(bgbool, "background资源", self.bookchapter, content)
            # self.com_result(bgbool, bg, "背景")
        for bgm in self.bgm_check_list:
            path = self.bookchapter + "/sound/bgm/" + bgm
            bgmbool = fileCompare(path)
            content = "未发现{}资源".format(bgm)
            report(bgmbool, "bgm资源", self.bookchapter, content)

        for sound in self.sound_check_list:
            path = self.bookchapter + "/sound/sound/" + sound
            soundbool = fileCompare(path)
            content = "未发现{}资源".format(sound)
            report(soundbool, "sound资源", self.bookchapter, content)

    def com_result(self, result, parInfo, des):
        """通用结果"""
        if not result:
            content = "【{0}资源异常】：{1}资源丢失".format(des, parInfo)
            mylog.error(content)

    # def chat_type_check(self,chat):
    #     """对白类型逻辑判断"""

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
        # print("bgm_check_list", self.bgm_check_list)
        # print("bg_check_list", self.bg_check_list)
        # print("face_check_dir", self.face_check_dir)
        # print("show_check_list", self.show_check_list)

    def get_roleFashionFilename(self):
        """获取路径，注意没有加png"""
        for role_id, role_list in self.role_fashion_dir.items():
            self.role_check_dir[role_id] = []
            Defaultlist =copy.deepcopy(MyData.getDefaultFashion(self.bookid, role_id)) # 添加默认角色检测列表
            self.role_check_dir[role_id] = Defaultlist
            for fashion_id in role_list:
                fashionlist = copy.deepcopy(MyData.getDIYFashion(fashion_id))
                for filename in fashionlist:
                    self.role_check_dir[role_id].append(filename)

    def add_test(self, chat):
        """增加角色以及相关"""
        if str(chat["chat_type"])=="10":
            select_id=str(chat["select_id"])
            select_info=self.select_info
            for select in select_info[select_id].values():
                if select["goodstype"] and select["goodsid"]:
                    print(select["goodstype"],select["goodsid"])
                else:
                    content="select_id:{0}goodstype或者goodsid为空".format(select_id)
                    report(False, "goodstype配置", self.bookchapter, content, chat=chat["id"])

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
        self.add_select_jump(chat, role_id, self.select_info, select_id)
        self.add_search_select_id(chat, role_id)
        self.add_face_id(chat, role_id)

    def add_is_finished(self, chat):
        """结束检测"""
        # print("添加is_finished检测")
        try:
            if chat["is_finished"]:
                is_finished = str(chat["is_finished"])
                if is_finished == "1":
                    self.chat.append(chat["id"])
                    self.is_finished += 1
                    if self.is_finished > 1:
                        report(False, "is_finished数量", self.bookchapter, "is_finished=1数量超过1",
                                    str(self.chat[0]) + "||" + str(self.chat[1]))
        except:
            pass

    def add_fashion_id(self, chat, role_id):
        # print("添加fashion_id检测")
        if "fashion_id" in chat:
            fashion_id = str(chat["fashion_id"])
            if fashion_id and fashion_id != "0":
                self.role_fashion_dir[role_id].append(fashion_id)

    def add_face_id(self, chat, role_id):
        # print("添加face检测")
        face_id = str(chat["face_id"])
        if face_id and face_id != "0" and role_id and role_id != "0":
            if role_id not in self.face_check_dir:
                self.face_check_dir[role_id] = []
            self.face_check_dir[role_id].append(face_id)

    def add_select_id(self, chat, role_id, select_info, select_id, search=None):
        """添加信息"""
        # print("添加select_id检测")
        # self.role_check_dir[role_id]: list = []
        if role_id not in self.role_check_dir:
            self.role_check_dir[role_id] = []
        if select_id and select_id != 0 and select_id != "0":
            # print("select_id：",chat["id"],select_id)
            if select_id in select_info:
                for select in select_info[select_id].values():
                    # if not select["jump_chat_id"] > 0:
                    #     content = "【jump_chat_id配置异常】:对白为id{0}的select_id{1}存在跳转为0".format(chat["id"], select_id)
                    #     mylog.error(content)
                    #     report(False, "face", self.bookchapter, content, roleID=role_id)
                    if select["goodstype"]:
                        if select["goodstype"] == "fashion":
                            self.role_fashion_dir[role_id].append(select["goodsid"])
                        else:
                            self.role_check_dir[role_id].append(select["goodsid"])
            else:
                if search:
                    content = "id->{0}反向章节->select配置中未找到{2}".format(search, select_id)
                    report(False, "search_select_id", self.bookchapter, content, roleID=role_id, chat=chat["id"])
                else:
                    content = "未找到select_id{1}".format(select_id)
                    report(False, "select_id配置", self.bookchapter, content, roleID=role_id, chat=chat["id"])

    def add_select_jump(self, chat, role_id, select_info, select_id, search=None):
        """jump信息查询"""
        # print("添加jump_chat_id检测")
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
                    # for key,vlus in select_dir.items():
                    #     if vlus==2:
                    #         content = "【{3}】:对白为id{0}->select_id{1}->jump_chat_id：{2}存在跳转2次跳转".format(chat["id"], select_id,key,self.bookchapter)
                    #         mylog.error(content)
                    if not select["jump_chat_id"] > 0:
                        content = "select_id{1}存在跳转为0".format(chat["id"], select_id)
                        # mylog.error(content)
                        report(False, "jump_chat_id", self.bookchapter, content, roleID=role_id, chat=chat["id"])
                    if select["goodstype"]:
                        if select["goodstype"] == "fashion":
                            self.role_fashion_dir[role_id].append(select["goodsid"])
                        else:
                            self.role_check_dir[role_id].append(select["goodsid"])
            else:
                if search:
                    content = "id->{0}反向章节->{1}select配置中未找到{2}".format(search, chat["id"], select_id)
                    # mylog.error(content)
                    report(False, "select_id配置", self.bookchapter, content, roleID=role_id, chat=chat["id"])
                else:
                    content = "select_id{0}未找到".format(select_id)
                    # mylog.error(content)
                    report(False, "select_id配置", self.bookchapter, content, roleID=role_id, chat=chat["id"])

    def add_search_select_id(self, chat, role_id):
        """添加反向查找"""
        # print("添加search_select_id检测")
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
            re_chatinfo=MyData.read_story_cfg_select(book_id, chapters_id)
            self.add_select_id(chat, role_id, re_chatinfo, select_id, searchchapter)
            # self, chat, role_id, select_info, select_id, search = None

    def add_content_check(self,chat):
        try:
            content = str(chat["content"])
            mind = str(chat["mind"])
        except:
            pass
    def mail(self, chat):
        # print("添加mail检测")
        mail_list = chat["mail"].split("#")
        try:
            if len(mail_list) > 1:
                mailTitle = mail_list[0]
                self.show_check_list.append(mail_list[1])
            else:
                mailTitle = mail_list[0]
        except:
            # self.com_result(False, str(chat["id"]), )
            report(False, "mail", self.bookchapter, "邮件配置异常")

    def add_chat_type(self, chat):
        chat_type = chat["chat_type"]
        if chat_type == 21:
            self.mail()

    def add_sound_name(self, chat):
        # print("添加sound检测")
        sound_name = str(chat["sound_name"])
        if sound_name and sound_name != "0":
            sound_name = sound_name + ".mp3"
            self.sound_check_list.append(sound_name)

    def add_show_id(self, chat):
        # print("添加show_id检测")
        try:
            show_id = str(chat["show_id"])
        except:
            show_id = None
        if show_id and show_id != "0":
            self.show_check_list.append(show_id)

    def add_video_id(self, chat):
        # print("添加video_id检测")
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
        # print("添加friend_id检测")
        friend_id = None
        if chat["chat_type"] == 8 or chat["chat_type"] == 15 or chat["chat_type"] == 16 or chat["chat_type"] == 19 or \
                chat["chat_type"] == 26 or chat["chat_type"] == 29 or chat["chat_type"] == 30:
            friend_id = str(chat["friend_id"])
            if friend_id and friend_id != "0":
                pass
            else:
                content = "类型为{}的friend_id为空".format(chat["chat_type"])
                # mylog.error(content)
                report(False, "friend_id", self.bookchapter, content, chat=chat["id"])
                # self.error_dir["friend_id"] = content


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



    # def getCheckList(self):
    #     """遍历检测"""
    #     print("线程开始：",i)
    #     clock()
    #     for self.bookchapter in MyData.check_list:
    #         try:
    #             self.bookchapter = str(self.bookchapter)
    #             self.bookid = self.bookchapter[:5]
    #             self.chapterid = self.bookchapter[5:]
    #             # mylog.info("=============================================================================")
    #             self.initialize()
    #             resultBool=self.result(self.bookchapter)
    #             if resultBool:
    #                 continue
    #             mylog.info(self.bookchapter + "======================>")
    #             # mylog.info("===开始" + self.bookchapter + "资源对比===")
    #             self.check()
    #             # mylog.info("===完成" + self.bookchapter + "资源对比===")
    #             MyData.update_record_bookread(self.bookchapter, "True")
    #             # mylog.info("=============================================================================")
    #         except Exception as e:
    #             mylog.error("执行失败：", e)
    #             MyData.update_record_bookread(self.bookchapter, "False")
    #     time=clock("stop")
    #     print("线程结束：",i)


# if __name__ == '__main__':
#     clock()
#     for bookchapter in MyData.check_list:
#     # Check1.getCheckList()
#         threads = []
#     # for i in range(0,2):
#         thread = Thread(target=myCheck, args=(bookchapter,))
#         thread.start()
#         threads.append(thread)
#     time = clock("stop")
#     for thread in threads:
#         thread.join()



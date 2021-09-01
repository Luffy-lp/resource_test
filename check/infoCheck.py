import os
from time import sleep

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
        MyData.story_cfg_chapter_dir = {}
        self.role_fashion_dir = {}
        self.bg_check_list = []
        self.bgm_check_list = []
        self.face_check_dir = {}
        self.role_check_dir = {}
        self.story_select_dir = {}

        self.role_resources_dir = {}
        self.bg_resources_list = []
        self.bgm_resources_list = []
        self.face_resources_list = []
        self.error_dir = {}

    def initialize(self):
        MyData.story_cfg_chapter_dir = {}
        self.select_info = {}
        self.role_fashion_dir = {}
        self.bg_check_list = []
        self.bgm_check_list = []
        self.face_check_dir = {}
        self.role_check_dir = {}
        self.role_resources_dir = {}
        self.bg_resources_list = []
        self.bgm_resources_list = []
        self.face_resources_list = []

    def check(self):
        """单章检测流程"""
        MyData.download_bookresource(self.bookid)  # 拉取全书对白配置
        MyData.read_story_cfg_chapter(self.bookid, self.bookchapter)  # 存储章节对白配置
        chats_info = MyData.story_cfg_chapter_dir[self.bookchapter]  # 当前阅读章节信息
        self.select_info= MyData.story_select_dir[self.bookchapter] # 当前阅读选项信息
        self.add_check_info(chats_info)  # 生成需要检测的信息
        MyData.download_bookresource(self.bookchapter)  # 拉取章节资源
        self.getfile_name()  # 获取资源文件用于对比
        self.contrast()  # 对比并给出结果

    def contrast(self):
        """对比"""
        for role_id, idlist in self.role_check_dir.items():
            self.error_dir[self.bookchapter][role_id] = []
            for i in idlist:
                k = i + ".png"
                if k in self.role_resources_dir[role_id]:
                    print(role_id + "的" + k + "是ok的")
                else:
                    k1 = i + "_1" + ".png"
                    if k1 in self.role_resources_dir[role_id]:
                        print(role_id + "的" + k1 + "是ok的")
                        continue
                    content = "【角色资源异常】：角色包{0}中未发现{1} 资源".format(role_id, i)
                    mylog.error(content)
                    self.error_dir[self.bookchapter][role_id].append(content)

        for role_id, fashionidlist in self.face_check_dir.items():
            for i in fashionidlist:
                if role_id not in self.role_resources_dir:
                    content = "【face资源文件夹异常】:资源包未找到{}的文件夹".format(role_id)
                    MyData.error_dir[role_id] = content
                    mylog.error(content)
                else:
                    k = i + ".png"
                    print("facek", k)
                    if k in self.role_resources_dir[role_id]:
                        print(role_id + "的" + k + "是ok的")
                    else:
                        k1 = i + "_1" + ".png"
                        print("facek1", k1)
                        if k1 in self.role_resources_dir[role_id]:
                            print(role_id + "的" + k1 + "是ok的")
                            continue
                        content = "【face资源异常】：角色包{0}中未发现{1} 资源".format(role_id, i)
                        mylog.error(content)
                        self.error_dir[self.bookchapter][role_id].append(content)

        for bg in self.bg_check_list:
            self.error_dir[self.bookchapter]["Bg"] = []
            if bg in self.bg_resources_list:
                print(bg + "是ok的")
            else:
                content = "【背景资源异常】：{0}资源丢失".format(bg)
                mylog.error(content)
                self.error_dir[self.bookchapter]["Bg"].append(content)
        for bgm in self.bgm_check_list:
            self.error_dir[self.bookchapter]["Bgm"] = []
            if bgm in self.bgm_resources_list:
                print(bgm + "是ok的")
            else:
                content = "【音乐资源异常】：{0}资源丢失".format(bgm)
                mylog.error(content)
                self.error_dir[self.bookchapter]["Bgm"].append(content)

    def add_check_info(self, chats_info):
        """添加检测信息"""
        for chat in chats_info.values():
            self.add_role_id(chat)
            self.add_friend_id(chat)
            self.add_bg_id(chat)
            self.add_bgm_id(chat)
        self.de_weight()
        self.get_roleFashionFilename()

    def de_weight(self):
        """去重"""
        self.bgm_check_list = set(self.bgm_check_list)
        self.bg_check_list = set(self.bg_check_list)
        # self.face_check_list = list(set(self.face_check_list))

        for i in self.role_fashion_dir:
            self.role_fashion_dir[i] = list(set(self.role_fashion_dir[i]))
        for i in self.face_check_dir:
            self.face_check_dir[i] = list(set(self.face_check_dir[i]))
        print("bgm_check_list", self.bgm_check_list)
        print("bg_check_list", self.bg_check_list)
        print("face_check_dir", self.face_check_dir)

    def get_roleFashionFilename(self):
        """获取路径，注意没有加png"""
        print("role_fashion_dir", self.role_fashion_dir)
        for role_id, role_list in self.role_fashion_dir.items():
            self.role_check_dir[role_id] = []
            Defaultlist = MyData.getDefaultFashion(self.bookid, role_id)
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
        if role_id and role_id != "0":
            if role_id not in self.role_fashion_dir:
                self.role_fashion_dir[role_id] = []
            if role_id not in self.role_check_dir:
                self.role_check_dir[role_id] = []
        else:
            return
        self.add_fashion_id(chat,role_id)
        self.add_select_id(chat,role_id)
        self.add_face_id(chat,role_id)

    def add_fashion_id(self,chat,role_id):
        if "fashion_id" in chat:
            fashion_id = str(chat["fashion_id"])
            if fashion_id and fashion_id != "0":
                self.role_fashion_dir[role_id].append(fashion_id)

    def add_face_id(self, chat,role_id):
        face_id = str(chat["face_id"])
        if face_id and face_id != "0" and role_id and role_id != "0":
            if role_id not in self.face_check_dir:
                self.face_check_dir[role_id] = []
            self.face_check_dir[role_id].append(face_id)

    def add_select_id(self, chat,role_id):
        """添加信息"""
        select_id = str(chat["select_id"])
        self.role_check_dir[role_id]:list=[]
        if select_id and select_id != "0":
            if select_id in self.select_info:
                for select in self.select_info[select_id].values():
                    if select["goodstype"]:
                        if select["goodstype"]=="fashion":
                            print("添加select的fashion",select["goodsid"])
                            self.role_fashion_dir[role_id].append(select["goodsid"])
                        else:
                            print("添加非的fashion",select["goodsid"])
                            self.role_check_dir[role_id].append(select["goodsid"])

            else:
                content = "【select_id配置异常】:对白的select_id{}未找到".format(chat["id"], chat["chat_type"])
                mylog.error(content)


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

    # def get_selects(self,chat,role_id_list:list):
    #     select

    def getfile_name(self):
        for role_id in self.role_check_dir:
            file = self.bookchapter + "/role/" + role_id
            path = os.path.join(path_resource, file)
            self.role_resources_dir[role_id] = []
            for root, dirs, files in os.walk(path):
                self.role_resources_dir[role_id] = self.role_resources_dir[role_id] + files
        self.bg_resources_list = []
        self.bgm_resources_list = []
        self.role_resources_list = []
        file = self.bookchapter + "/background"
        path = os.path.join(path_resource, file)
        for root, dirs, files in os.walk(path):
            self.bg_resources_list = files
        file = self.bookchapter + "/sound/bgm"
        path = os.path.join(path_resource, file)
        for root, dirs, files in os.walk(path):
            self.bgm_resources_list = files
        # file = self.bookchapter + "/role/" + role_id+"face"
        # path = os.path.join(path_resource, file)
        # for root, dirs, files in os.walk(path):
        #     self.face_resources_list = files

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
            self.bookchapter = str(self.bookchapter)
            self.bookid = self.bookchapter[:5]
            self.chapterid = self.bookchapter[5:]
            self.clock()
            mylog.info("=============================================================================")
            self.error_dir[self.bookchapter] = {}
            self.initialize()
            self.result(self.bookchapter)
            mylog.info("===开始" + self.bookchapter + "资源对比===")
            self.check()
            mylog.info("===完成" + self.bookchapter + "资源对比===")
            MyData.update_record_bookread(self.bookchapter, "True")
            mylog.info("=============================================================================")
            self.clock("stop")


if __name__ == '__main__':
    Check1 = Check()
    Check1.getCheckList()

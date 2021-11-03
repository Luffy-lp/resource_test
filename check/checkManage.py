# # from common.my_log import mylog
# from check.checkData import CheckData
# from date.Chapters_data import MyData
# from check.check import Check
# from common.COM_utilities import report
#
#
# class CheckManage():
#
#     def nullJudgments(chat, item):
#         """为空和是否存在通用方法"""
#         if item not in chat:
#             return False
#         parameter = str(chat[item])
#         if parameter and parameter != 0:
#             return parameter
#         else:
#             return False
#
#     def roleId_check(self, check: Check, chat):
#         role_id = self.nullJudgments(chat, "role_id")
#         if role_id:
#             Defaultlist=MyData.getDefaultFashion(self.bookid, role_id)
#             if role_id not in check.role_fashion_dir:
#                 check.role_fashion_dir[role_id] = []
#             if role_id not in check.role_check_dir:
#                 check.role_check_dir[role_id] = []
#         return role_id
#
#     def get_roleFashionFilename(self):
#         """获取路径，注意没有加png"""
#         for role_id, role_list in self.role_fashion_dir.items():
#             self.role_check_dir[role_id] = []
#             Defaultlist = MyData.getDefaultFashion(self.bookid, role_id)  # 添加默认角色检测列表
#             self.role_check_dir[role_id] = Defaultlist
#             for fashion_id in role_list:
#                 fashionlist = MyData.getDIYFashion(fashion_id)
#                 for filename in fashionlist:
#                     self.role_check_dir[role_id].append(filename)
#
#     def fashionId_check(self, check: Check, chat, role_id):
#         if not role_id:
#             return False
#         fashion_id = self.nullJudgments(chat, "fashion_id")
#         if not fashion_id:
#             return False
#         check.role_fashion_dir[role_id].append(fashion_id)
#
#     def selectID_check(self, check: Check, chat, role_id, select_info, search=None):
#         select_id = self.nullJudgments(chat, "role_id")
#         if not role_id or select_id:
#             return False
#         if select_id in select_info:
#             for select in select_info[select_id].values():
#                 # if not select["jump_chat_id"] > 0:
#                 #     content = "【jump_chat_id配置异常】:对白为id{0}的select_id{1}存在跳转为0".format(chat["id"], select_id)
#                 #     mylog.error(content)
#                 #     report(False, "face", self.bookchapter, content, roleID=role_id)
#                 if select["goodstype"]:
#                     if select["goodstype"] == "fashion":
#                         check.role_fashion_dir[role_id].append(select["goodsid"])
#                     else:
#                         check.role_check_dir[role_id].append(select["goodsid"])
#         else:
#             if search:
#                 content = "id->{0}反向章节->select配置中未找到{2}".format(search, select_id)
#                 report(False, "search_select_id", self.bookchapter, content, roleID=role_id, chat=chat["id"])
#             else:
#                 content = "未找到select_id{1}".format(select_id)
#                 report(False, "select_id配置", self.bookchapter, content, roleID=role_id, chat=chat["id"])
#
#     def add_role_id(self, chat):
#         """增加角色以及相关"""
#         # role_id = str(chat["role_id"])
#         # select_id = str(chat["select_id"])
#         # self.add_fashion_id(chat, role_id)
#         # self.add_select_id(chat, role_id, self.select_info, select_id)
#         self.add_select_jump(chat, role_id, self.select_info, select_id)
#         self.add_search_select_id(chat, role_id)
#         self.add_face_id(chat, role_id)
#
#     def add_is_finished(self, chat):
#         """结束检测"""
#         # print("添加is_finished检测")
#         try:
#             if chat["is_finished"]:
#                 is_finished = str(chat["is_finished"])
#                 if is_finished == "1":
#                     self.chat.append(chat["id"])
#                     self.is_finished += 1
#                     if self.is_finished > 1:
#                         report(False, "is_finished数量", self.bookchapter, "is_finished=1数量超过1",
#                                str(self.chat[0]) + "||" + str(self.chat[1]))
#         except:
#             pass
#
#     def add_fashion_id(self, chat, role_id):
#         # print("添加fashion_id检测")
#         if "fashion_id" in chat:
#             fashion_id = str(chat["fashion_id"])
#             if fashion_id and fashion_id != "0":
#                 check.role_fashion_dir[role_id].append(fashion_id)
#
#     def add_face_id(self, chat, role_id):
#         # print("添加face检测")
#         face_id = str(chat["face_id"])
#         if face_id and face_id != "0" and role_id and role_id != "0":
#             if role_id not in self.face_check_dir:
#                 self.face_check_dir[role_id] = []
#             self.face_check_dir[role_id].append(face_id)
#
#     def add_select_id(self, check, chat, role_id, select_info, select_id, search=None):
#         """添加信息"""
#         check.role_check_dir[role_id]: list = []
#         if select_id and select_id != 0 and select_id != "0":
#             # print("select_id：",chat["id"],select_id)
#             if select_id in select_info:
#                 for select in select_info[select_id].values():
#                     # if not select["jump_chat_id"] > 0:
#                     #     content = "【jump_chat_id配置异常】:对白为id{0}的select_id{1}存在跳转为0".format(chat["id"], select_id)
#                     #     mylog.error(content)
#                     #     report(False, "face", self.bookchapter, content, roleID=role_id)
#                     if select["goodstype"]:
#                         if select["goodstype"] == "fashion":
#                             check.role_fashion_dir[role_id].append(select["goodsid"])
#                         else:
#                             check.role_check_dir[role_id].append(select["goodsid"])
#             else:
#                 if search:
#                     content = "id->{0}反向章节->select配置中未找到{2}".format(search, select_id)
#                     report(False, "search_select_id", self.bookchapter, content, roleID=role_id, chat=chat["id"])
#                 else:
#                     content = "未找到select_id{1}".format(select_id)
#                     report(False, "select_id配置", self.bookchapter, content, roleID=role_id, chat=chat["id"])
#
#     def add_select_jump(self, chat, role_id, select_info, select_id, search=None):
#         """jump信息查询"""
#         # print("添加jump_chat_id检测")
#         # check.role_check_dir[role_id]: list = []
#         if select_id and select_id != 0 and select_id != "0":
#             # print("select_id：",chat["id"],select_id)
#             if select_id in select_info:
#                 select_dir = {}
#                 for select in select_info[select_id].values():
#                     if not select["jump_chat_id"] in select_dir:
#                         select_dir[select["jump_chat_id"]] = 1
#                     else:
#                         select_dir[select["jump_chat_id"]] += 1
#                     # for key,vlus in select_dir.items():
#                     #     if vlus==2:
#                     #         content = "【{3}】:对白为id{0}->select_id{1}->jump_chat_id：{2}存在跳转2次跳转".format(chat["id"], select_id,key,self.bookchapter)
#                     #         mylog.error(content)
#                     if not select["jump_chat_id"] > 0:
#                         content = "select_id{1}存在跳转为0".format(chat["id"], select_id)
#                         # mylog.error(content)
#                         report(False, "jump_chat_id", self.bookchapter, content, roleID=role_id, chat=chat["id"])
#                     if select["goodstype"]:
#                         if select["goodstype"] == "fashion":
#                             check.role_fashion_dir[role_id].append(select["goodsid"])
#                         else:
#                             check.role_check_dir[role_id].append(select["goodsid"])
#             else:
#                 if search:
#                     content = "id->{0}反向章节->{1}select配置中未找到{2}".format(search, chat["id"], select_id)
#                     # mylog.error(content)
#                     report(False, "select_id配置", self.bookchapter, content, roleID=role_id, chat=chat["id"])
#                 else:
#                     content = "select_id{0}未找到".format(select_id)
#                     # mylog.error(content)
#                     report(False, "select_id配置", self.bookchapter, content, roleID=role_id, chat=chat["id"])
#
#     def add_search_select_id(self, chat, role_id):
#         """添加反向查找"""
#         # print("添加search_select_id检测")
#         try:
#             search_select_id = str(chat["search_select_id"])
#         except:
#             search_select_id = None
#         if search_select_id and search_select_id != "0":
#             chapters_id = search_select_id.split("*")[0]
#             searchchapter = chapters_id
#             book_id = chapters_id[:5]
#             select_id = search_select_id.split("*")[1]
#             MyData.download_bookresource(book_id)
#             re_chatinfo = MyData.read_story_cfg_select(book_id, chapters_id)
#             self.add_select_id(chat, role_id, re_chatinfo, select_id, searchchapter)
#             # self, chat, role_id, select_info, select_id, search = None
#
#     def mail(self, chat):
#         # print("添加mail检测")
#         mail_list = chat["mail"].split("#")
#         try:
#             if len(mail_list) > 1:
#                 mailTitle = mail_list[0]
#                 self.show_check_list.append(mail_list[1])
#             else:
#                 mailTitle = mail_list[0]
#         except:
#             # self.com_result(False, str(chat["id"]), )
#             report(False, "mail", self.bookchapter, "邮件配置异常")
#
#     def add_chat_type(self, chat):
#         chat_type = chat["chat_type"]
#         if chat_type == 21:
#             self.mail()
#
#     def add_sound_name(self, chat):
#         # print("添加sound检测")
#         sound_name = str(chat["sound_name"])
#         if sound_name and sound_name != "0":
#             sound_name = sound_name + ".mp3"
#             self.sound_check_list.append(sound_name)
#
#     def add_show_id(self, chat):
#         # print("添加show_id检测")
#         try:
#             show_id = str(chat["show_id"])
#         except:
#             show_id = None
#         if show_id and show_id != "0":
#             self.show_check_list.append(show_id)
#
#     def add_video_id(self, chat):
#         # print("添加video_id检测")
#         try:
#             video_id = str(chat["video_id"])
#         except:
#             video_id = None
#         if video_id and video_id != "0":
#             video_list = video_id.split("#")
#             self.show_check_list.append(video_list[1])
#             check.role_check_dir[video_list[0]]
#             if video_list[0] not in check.role_check_dir:
#                 check.role_check_dir[video_list[0]] = []
#
#     def add_friend_id(self, chat):
#         # print("添加friend_id检测")
#         friend_id = None
#         if chat["chat_type"] == 8 or chat["chat_type"] == 15 or chat["chat_type"] == 16 or chat["chat_type"] == 19 or \
#                 chat["chat_type"] == 26 or chat["chat_type"] == 29 or chat["chat_type"] == 30:
#             friend_id = str(chat["friend_id"])
#             if friend_id and friend_id != "0":
#                 pass
#             else:
#                 content = "类型为{}的friend_id为空".format(chat["chat_type"])
#                 # mylog.error(content)
#                 report(False, "friend_id", self.bookchapter, content, chat=chat["id"])
#                 # self.error_dir["friend_id"] = content
#
#         if "friend_id" in chat:
#             friend_id = str(chat["friend_id"])
#             if friend_id and friend_id != "0":
#                 if friend_id not in check.role_fashion_dir:
#                     check.role_fashion_dir[friend_id] = []
#             else:
#                 return
#         else:
#             print("没有friend_id")
#             return
#         if "friend_fashion_id" in chat:
#             friend_fashion_id = str(chat["friend_fashion_id"])
#             if friend_fashion_id and friend_id != "0":
#                 check.role_fashion_dir[friend_id].append(friend_fashion_id)
#
#     def content_check(self, chat):
#         re = chat["content"]
#         return re
#
#     def showId_check(self, chat):
#         pass
#
#     def roleId_check(self, chat):
#         pass
#
#     def friendID_check(self, chat):
#         pass
#
#     def default(self, chat):
#         pass
#
#     def setRoleName_check(self, chat):
#         """设置角色名"""
#         pass
#
#     def goodstype_check(self, chat):
#         pass
#
#     def scene_bg_id_check(self, chat):
#         pass
#
#     def narrationTitle_check(self, chat):
#         """叙述标题"""
#         pass
#
#     def mail_check(self, chat):
#         pass
#
#     def answer_phone(self, chat):
#         """打电话ui26"""
#         pass
#
#     def is_bg_play(self, chat):
#         """特殊特效动画"""
#         pass
#
#     def three_check(self, chat):
#         """三选竖版换装"""
#         pass
# # parameter=""
# # CheckManage1=CheckManage()
# # RE=CheckManage1.nullJudgments(parameter)
# # print(RE)

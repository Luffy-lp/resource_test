import json
import time
from time import sleep
import traceback
import requests
import sys, os, zipfile
from common.COM_path import *


class APiClass():
    Header = {"TIMECLOSE": "1"}
    url = "http://dev-chapters-int.stardustgod.com/"
    channel_id = "AVG10003"
    _response = None

    def get_set(self):
        self._response = None
        filepath = os.path.join(path_YAML_FILES, "apiconf.yml")
        print(filepath)
        with open(filepath, encoding='utf-8') as file:
            value = yaml.safe_load(file)
        self.channel_id = value["channel_id"]
        self.url = value["url"]
        return self.channel_id

    def try_APIlink(self, url, headers, body, name, trytime=100, timeout=10):
        """requests公共方法"""
        while (trytime >= 0):
            trytime = trytime - 1
            try:
                print("拉取{0}接口".format(name))  # 补充正则截取
                self._response = requests.post(url=url, headers=headers, data=body, timeout=10)
            except:
                # traceback.print_exc()
                print("拉取{0}接口失败，重试".format(name))
                sleep(1)
            else:
                # print(self._response.text)
                dir_json = json.loads(self._response.text)
                dir = eval(str(dir_json))
                # my_re=\n[\s\S]*
                print("拉取{0}接口成功".format(name))
                return dir

    def unzip_file(self, fz_name, path):
        """
        解压缩文件
        :param fz_name: zip文件
        :param path: 解压缩路径
        :return:
        """
        flag = False

        if zipfile.is_zipfile(fz_name):  # 检查是否为zip文件
            with zipfile.ZipFile(fz_name, 'r') as zipf:
                zipf.extractall(path)
                # for p in zipf.namelist():
                #     # 使用cp437对文件名进行解码还原， win下一般使用的是gbk编码
                #     p = p.encode('cp437').decode('gbk')  # 解决中文乱码
                #     print(fz_name, p,path)
                flag = True

        return {'file_name': fz_name, 'flag': flag}
        source_dir = os.getcwd() + "\\10009001"
        dest_dir = os.getcwd()
        print(source_dir)

    def downloardurl(self, address):
        # zp = None
        # source_dir = os.getcwd()
        path = "/resource"
        try:
            r = requests.get(address, stream=True)
            print("下载成功")
        except:
            print("下载失败")
        zip_file = zipfile.ZipFile('gamecfg_0805test_20201217_Q5yEz1.zip')
        zip_list = zip_file.namelist()
        folder_abs = path
        for f in zip_list:
            zip_file.extract(f, folder_abs)
        zip_file.close()

    def storyrole(self, book_id, role_ids=None):
        """书籍角色"""
        Header = {
            "language": "en-US",
            "platform": "Android",
            "Accept": "application/json"
        }
        role_ids = json.dumps(role_ids)
        url = self.url + "/na/story/v1/role/show/more?debug=true"
        body = {"channel_id": self.channel_id,
                "book_id": book_id,
                "role_ids": role_ids
                }
        data = self.try_APIlink(url=url, headers=Header, body=body, name="storyrole")
        return data["data"]
        # else:
        #     return False

    def storysaloonApi(self, uuid):
        """大厅首页接口 v2"""
        Header = {
            "language": "en-US",
            "platform": "Android",
            "Accept": "application/json"
        }
        print(self.channel_id)
        url = self.url + "/na/story/v1/saloon?debug=true"
        body = {"channel_id": self.channel_id,
                "version": "624.0.0",
                "is_not17k": "0",
                "uuid": uuid,
                }
        data = self.try_APIlink(url=url, headers=Header, body=body, name="storysaloonApi")
        return data["data"]

    def storysaloonViewApi(self, uuid, module_id):
        """大厅首页接口 v2"""
        Header = {
            "language": "en-US",
            "platform": "Android",
            "Accept": "application/json"
        }
        print(self.channel_id)
        url = self.url + "/na/story/v1/saloon/view?debug=true"
        body = {"channel_id": self.channel_id,
                "module_id": module_id,
                "uuid": uuid,
                "limit": "20"
                }
        data = self.try_APIlink(url=url, headers=Header, body=body, name="storysaloonApi")
        return data["data"]

    def fashionShowApi(self, fashion_ids):
        """书籍角色资源"""
        Header = {
            "language": "en-US",
            "platform": "Android",
            "Accept": "application/json"
        }
        fashion_ids = json.dumps(fashion_ids)
        url = self.url + "/na/story/v1/role/fashion/show/more?debug=true"
        body = {
            "fashion_ids": fashion_ids,
            "channel_id": self.channel_id,
        }
        data = self.try_APIlink(url=url, headers=Header, body=body, name="fashionShowApi")
        return data["data"]

    def getUserStoryDataApi(self, uuid, book_id):
        """拉取用户视觉小说书籍数据"""
        # Header = {
        #     "language": "en-US",
        #     "platform": "Android",
        #     "Accept": "application/json"
        # }
        url = self.url + "/Controllers/story/read/GetUserStoryDataApi.php?DEBUG=true"
        body = {
            "uuid": uuid,
            "book_id": book_id,
        }
        data = self.try_APIlink(url=url, headers=self.Header, body=body, name="fashionShowApi")
        return data["data"]

    def avgcontentApi(self, bookid, channel_id="AVG10005", country_code="CN"):
        """获取章节资源下载地址"""
        url = self.url + "avgcontentApi.Class.php?DEBUG=true"
        body = {"chapter_id": bookid,
                "source_type": "t0",
                "channel_id": self.channel_id,
                "country_code": country_code,
                }
        response = self.try_APIlink(url=url, headers=self.Header, body=body, name="avgcontentApi")
        address: str = response["address"]
        addresslist = address.split('/')
        address = address.replace("\\", "")
        time = 5
        while (time > 1):
            time = time - 1
            try:
                r = requests.get(address)
                path = os.path.join(path_resource, addresslist[len(addresslist) - 1])
                pathbook = os.path.join(path_resource, bookid)
                with open(path, "wb") as code:
                    code.write(r.content)
                sleep(5)
                code.close()
                file_zip = zipfile.ZipFile(path, 'r')
                sleep(2)
                file_zip.extractall(pathbook)
                file_zip.close()
                os.remove(path)
                # print("书籍资源下载成功")
                return
            except BaseException as e:
                sleep(2)
                print("书籍资源读取失败,重试", e)
            else:
                print("书籍资源读取成功")
        print("下载书籍资源失败")
#         # raise Exception("下载书籍资源失败")
# APiClass1 = APiClass()
# uuid="6177842"
# aa=APiClass1.storysaloonViewApi("6177842","12039")
# list=aa["items"]
# print(len(list))
# for i in list:
#     print(str(i["story_id"])+"001"+"-"+str(i["story_id"])+"0"+str(i["chapter_count"])+":",i["title"])

import oss2
import os
import subprocess
from threading import Thread
import json
import requests
import sys
from date.Chapters_data import MyData
import time
endpoint = "oss-cn-shenzhen.aliyuncs.com"
accesskey_id = "LTAI5tCiLzQTuHSHoyfAcvcC"
accesskey_secret = "YQiQrHdFLoIGmfJZ0XE2E9CFRKjueX"
bucket_name = "product-editor-back"
baseUploadPath = 'test-Tripp/'  # OSS文件目录
auth = oss2.Auth(accesskey_id, accesskey_secret)
bucket = oss2.Bucket(auth, endpoint, bucket_name)
url = 'http://product-editor-back.oss-accelerate.aliyuncs.com'
ding_list = []
urls_list = []
errors_list = []
dingrobot = MyData.EnvData_dir["DingUrl"]


def create_html(htmlpath):
    show_model = """<div style="display:inline-block">
        <div>
          <img style="width:300px;height:600px" src="{{url}}">
        </div>
        <span style="">{{error}}</span>
      </div>"""
    show_list = "<html>"
    for i in range(0, len(urls_list)):
        show_list = show_list + show_model.replace("{{url}}", urls_list[i]).replace("{{error}}", errors_list[i])
    show_list += "</html>"
    # 打开文件，准备写入
    f = open(htmlpath, 'w')
    f.write(show_list)
    f.close()


def localhost2oss(local_file):
    mytime=str(int(time.time()))
    for root, dirs, files in os.walk(local_file):
        oss_files = local_file.split('\\')[2]
        for file in files:
            if "html" in file:
                continue
            errors_list.append(file.split(".")[0])
            update_local_file = os.path.join(root, file)
            oss_files = local_file.split('\\')[2]
            oss_file = update_local_file.replace(local_file, '')
            oss_file = oss_file.replace('\\', '/')
            oss_file = baseUploadPath + oss_files + oss_file
            http_url = url + '/' + oss_file
            urls_list.append(http_url)
            bucket.put_object_from_file(oss_file, update_local_file)
        html_name = oss_files+"-"+mytime+ ".html"
        html_path = os.path.join(local_file, html_name)
        create_html(htmlpath=html_path)
        update_local_file = os.path.join(root, html_name)
        oss_files = local_file.split('\\')[2]
        oss_file = update_local_file.replace(local_file, '')
        oss_file = oss_file.replace('\\', '/')
        oss_file = baseUploadPath + oss_files + oss_file
        print(oss_files)
        http_url = url + '/' + oss_file
        bucket.put_object_from_file(oss_file, update_local_file)
        ding_list.append(http_url)
        return oss_files, http_url


def send_msg(time,num, error, http_url,chapterlist):
    headers = {'Content-Type': 'application/json;charset=utf-8'}
    strerror=""
    for i in chapterlist:
        strerror=strerror+i+","
    data_dict = {
        "msgtype": "markdown",
        "markdown": {
            "title": "自动化阅读",
            "text": "### "+time+"阅读结果\n\n"
                    "> **渠道号:** "+MyData.UserData_dir["channel_id"]+"\n\n"
                    "> **设备号:** "+MyData.EnvData_dir["ADBdevice"]+"\n\n"
                    "> **主版本号:** "+"622.0.0"+"\n\n"
                    "> **完成阅读章节:** "+str(num)+"\n\n"
                    "> **阅读失败章节:** "+str(error)+"\n\n"
                    "> **失败章节列表:** "+strerror+"\n\n"
                    '> **<font color = red size=6 face="微软雅黑">点击图片查看异常</font>**\n\n'
                    '[![screenshot](http://product-editor-back.oss-cn-shenzhen.aliyuncs.com/test-Tripp%2F2021-08-17%2Fcharpters.png)]'+"("+http_url+")"
        }
    }
    r = requests.post(dingrobot, data=json.dumps(data_dict), headers=headers)
    return r.text

# if __name__ == '__main__':
#     local_file = "D:\\Read_Result\\2021-08-17"
#     error = 20
#     chapterlist=["10001","10002"]
#     data = localhost2oss(local_file)
#     print(data)
#     aa=send_msg(num=28,error=error,date=data[0],http_url=data[1],chapterlist=chapterlist)
#     print(aa)
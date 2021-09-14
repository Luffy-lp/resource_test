import os

from pymediainfo import MediaInfo

from common.COM_path import path_resource


def role_fileCompare(bookchapter,part, role_id, fileName):
    """角色文件比较"""
    file = bookchapter + "/role/" + role_id + '/' + part + '/' + fileName + ".png"
    fileName = os.path.join(path_resource, file)
    print("角色", fileName)
    filebool = os.path.exists(fileName)
    print("filebool", filebool)
    return filebool

a="ddddd#222".split("#")
if len(a)>1:
    print(a[1])
else:
    print(a[0])
# bookchapter="10001017"
# role_id="10001"
# part="body"
# fileName="body_1_1"
# role_fileCompare(bookchapter,part,role_id,fileName)
import configparser
import os

# """
# [Synology]
# upload = 0
# IP = 
# PORT = 
# SECURE = 0
# USER = 
# PASSWORD = 
# """

def check_config_if_exist(file_name = "config.ini"):
    path = f"{os.getcwd()}.\{file_name}"
    if not os.path.isfile(path):
        return False
    else:
        return True

def load_config():
    config = configparser.ConfigParser()
    path = "./config.ini"
    config.read(path, encoding="utf-8")    

    syno_info = {
        'upload': config['Synology']['upload'],
        'IP': config['Synology']['IP'],
        'PORT': config['Synology']['PORT'],
        'PATH': config['Synology']['PATH'],
        'SECURE': True if config['Synology']['SECURE'] == 1 else False,
        'USER': config['Synology']['USER'],
        'PASSWORD' : config['Synology']['PASSWORD']
    }

    return syno_info

def make_config(path):
    print(f"[/]開始產生 config.ini")
    f = open(path, 'w', encoding="utf-8")
    f.write("[Synology]\n")
    f.write("; 若要開啟 Synology 自動上傳，將 upload 設為1\n")
    f.write("upload = \n")
    f.write("IP = \n")
    f.write("PORT = \n")
    f.write("; BT 下載之路徑\n")
    f.write("PATH = \n")
    f.write("; SECURE 預設為0\n")
    f.write("SECURE = 0\n")
    f.write("USER = \n")
    f.write("PASSWORD = ")
    f.close()
    path = f"{os.getcwd()}\{path[2:]}"
    print(f"[*]config.ini 產生成功 -> 檔案路徑: {path}")

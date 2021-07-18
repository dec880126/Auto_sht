import sys
import time
import os
import datetime
import pyperclip

def progress_bar(progress_Now, over = False):# 1~101
    '''
    Make progress bar by 0% ~ 100%

    type progress_Now: int
    '''
    if progress_Now > 99:
        if progress_Now == 100:
            print("\r",end="")
            print("[/]Download progress: {}%: ".format(progress_Now),"▋" * (progress_Now // 2),end="")
        else:
            progress_Now = 99
    if over:
        print("")
    else:
        print("\r",end="")
        print("[/]Download progress: {}%: ".format(progress_Now),"▋" * (progress_Now // 2),end="")
        sys.stdout.flush()
        time.sleep(0.05)


def make_html(input_list, fileName, titleList, magnetList, article_Code_List):
    '''
    Read the url in the input_list, and make the HTML file

    type input_list: list
    '''
    path = "./" + fileName

    print(f"[/]{fileName} 產生中...")
    f = open(path, 'w', encoding="utf-8")

    # HTML declaration
    f.write(f"""<!doctype html>\n<html>\n\t<head>\n\t\t<title>Auto SHT Picture Viewer</title>\n\t</head>\n""")

    # CSS declaration
    f.write("""\t<style>\n\t\tbody{\n\t\t\tbackground: #ebe9f9; /* Old browsers */\n\t\t\tbackground: -moz-linear-gradient(top, #ebe9f9 0%, #d8d0ef 50%, #cec7ec 51%, #c1bfea 100%); /* FF3.6-15 */\n\t\t\tbackground: -webkit-linear-gradient(top, #ebe9f9 0%,#d8d0ef 50%,#cec7ec 51%,#c1bfea 100%); /* Chrome10-25,Safari5.1-6 */\n\t\t\tbackground: linear-gradient(to bottom, #ebe9f9 0%,#d8d0ef 50%,#cec7ec 51%,#c1bfea 100%); /* W3C, IE10+, FF16+, Chrome26+, Opera12+, Safari7+ */\n\t\t\tfilter: progid:DXImageTransform.Microsoft.gradient( startColorstr='#ebe9f9', endColorstr='#c1bfea',GradientType=0 ); /* IE6-9 */\n\t\t}\n\t</style>\n""")

    # HTML body writing
    f.write("""\t<body>\n\t\t<div style="text-align:center;">\n""")
    pageNum = 0
    for url in input_list:
        title = titleList[pageNum]
        article_Code = article_Code_List[pageNum]
        article_URL = "https://www.sehuatang.org/thread-" + article_Code + "-1-1.html"
        if url == "None":
            continue
        elif url == "end of page":
            to_write = "\t\t\t\t<br>\n\t\t\t\t<h3>" + magnetList[pageNum] + "</h3>\n"
            f.write(to_write)
            f.write("\t\t\t<hr />\n")
            pageNum += 1
        elif url == "Head of Page":
            f.write(f"""\t\t\t<h2><a href="{article_URL}"  target="_blank">{title}</a></h2>\n""")
        else:
            f.write("\t\t\t\t<img src = " + str(url) + """ width=auto""" + """ height=auto loading="lazy"  class="center">\n""")

    f.write("""\t\t\t<a>Copyright © 2021.</a><a href = "https://github.com/dec880126" target="_blank">Cyuan</a><a>&nbsp&nbspAll rights reserved. </a>\n\t\t</div>\n\t</body>\n</html>""")
    f.close()
    path = f"{os.getcwd()}\{path[2:]}"
    
    print(f"[*]{fileName} 產生成功! -> 檔案路徑: {path}")
    return path, fileName


def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)


def getYesterday(how_many_day_pre): 
    today=datetime.date.today() 
    oneday=datetime.timedelta(days=how_many_day_pre) 
    yesterday=today-oneday  
    return yesterday


def choose_type():
    typeList_Chinese = ["無碼", "有碼", "國產", "歐美", "中文"]
    print('[*]===============================================') 
    print("[*]                 1. 無碼")
    print("[*]                 2. 有碼")
    print("[*]                 3. 國產")
    print("[*]                 4. 歐美")
    print("[*]                 5. 中文")
    print('[*]===============================================') 
    while True:     
        typeChoose = int(input(f"[?]請選擇分區(1~5):"))
        if typeChoose >= 1 and typeChoose <= 5:
            print(f'[*]選擇的是 {typeChoose}. {typeList_Chinese[typeChoose-1]} 分區')
            print('[*]===============================================') 
            return typeChoose


def changeDate():
    print('[*]===============================================')
    today = str(time.strftime("%Y-%m-%d", time.localtime()))
    print(f"[*]今天是 {today}")
    print(f"[*](昨天: -1, 前天: -2...)")
    print('[*]===============================================')
    date = input("[?]請問日期要更改為?:")
    if int(date) < 0 and int(date) > -4:
        return getYesterday(abs(int(date)))


def Write_into_Clipboard(List):
    # """
    # Read the input List and write the List content into clipboard end with "\r\n"
    # """
    text_to_write = ""
    for element in List:
        text_to_write = text_to_write + element + '\r\n'
    pyperclip.copy(text_to_write)

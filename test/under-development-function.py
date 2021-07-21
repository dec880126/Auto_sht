
def get_publish_time(URL):
    """
    Input URL and get the publish time of article

    type URL: str
    rtype str
    """ 
    response = requests.get(URL)
    bs = bs4.BeautifulSoup(response.text, "html.parser")
    row = bs.find_all('div', 'authi', limit = 2)
    date = row[1].find_all('span', limit = 2)    

    return date[1].get('title')


def make_html(pic_link_List, fileName, titleList, magnetList, article_Code_List, publish_time_List):
    '''
    Read the url in the pic_link_List(article Code), and make the HTML file

    type pic_link_List, titleList, magnetList, article_Code_List, publish_time_List: List
    type fileName: str
    '''
    timeNow = time.strftime("%H:%M:%S", time.localtime())
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
    for url, publish_time in zip(pic_link_List, publish_time_List):
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
            # f.write(f"<a>{publish_time}</a>")
            # f.write(f"<a>{how_long_ago(timeNow, publish_time)}</a>")
        else:
            print(f"image found!!!")
            f.write("\t\t\t\t<img src = " + str(url) + """ width=auto""" + """ height=auto loading="lazy"  class="center">\n""")

    f.write("""\t\t\t<a>Copyright © 2021.</a><a href = "https://github.com/dec880126" target="_blank">Cyuan</a><a>&nbsp&nbspAll rights reserved. </a>\n\t\t</div>\n\t</body>\n</html>""")
    f.close()
    path = f"{os.getcwd()}\{path[2:]}"
    
    print(f"[*]{fileName} 產生成功! -> 檔案路徑: {path}")
    return path, fileName


def how_long_ago(timeNow, timeTarget):
    """
    type timeNow, timeTarget -> str: MUST end with HH-MM-SS
    rtype str
    """
    getSec = lambda hour, min, sec: hour*3600 + min*60 + sec
    now_in_sec = getSec(int(timeNow[-8:-6]), int(timeNow[-5:-3]), int(timeNow[-2:]))
    tar_in_sec = getSec(int(timeTarget[-8:-6]), int(timeTarget[-5:-3]), int(timeTarget[-2:]))

    delta_in_sec = now_in_sec - tar_in_sec
    delta_min = delta_in_sec//60
    if delta_min >= 60 and delta_min < 1440:
        # 一小時以上 一天以內
        delta_hour = delta_min // 60
        delta_min -= delta_hour * 60
        return f"{delta_hour} 小時 {delta_min} 分鐘前"
    elif delta_min < 60 and delta_min > 1:
        # 一小時內
        return f"{delta_min} 分鐘前"
    elif delta_min < 1:
        # 一分鐘內
        return f"{delta_in_sec} 秒前"
    elif delta_min >= 1440:
        # 超過一天
        delta_day = delta_min // 1440
        delta_hour = (delta_min - delta_day*1440) // 60
        return f"{delta_day} 天 {delta_hour} 小時前"


def get_ALL(today_list):
    """
    Get title, magnet and make HTML files of picture in one operation

    type today_list: List
    rtype: Dict
    """
    article_Num = 0
    publish_time_List = []
    title_List = []
    magnet_List = []
    pic_link_List = []
    magnet_error_List = []
    article_Code_error_List = []

    for article_Code in today_list:
        URL = "https://www.sehuatang.org/thread-" + article_Code + "-1-1.html"
        article_Num += 1
        progress_bar(int(article_Num/30*99))
        response_of_pages = requests.get(URL)
        bs_pages = bs4.BeautifulSoup(response_of_pages.text,"html.parser")
        row = bs_pages.find_all('div', 'authi', limit=2)

        try:
            # Get publish time
            publish_time_List.append(row[1].find_all('span', limit=2)[1].get('title'))

            # Get magnet
            magnet_List.append(bs_pages.find('div','blockcode').get_text().removesuffix('复制代码'))

            #Get title
            title_List.append(bs_pages.find('span', attrs={'id' : 'thread_subject'}).get_text())            

            # Get image link
            img_block = bs_pages.find_all('ignore_js_op')
            pic_link_List.append("Head of Page")
            for block in img_block[:-1]:
                pic_link = block.find('img').get('file')
                if pic_link != None:
                    pic_link_List.append(pic_link)
            pic_link_List.append("end of page")
        except:
            # 例外處理: 中文區偶爾會有特殊格式發生，沒有 magnet 連結，只有torrent
            magnet_error_List.append(bs_pages.find('span', attrs={'id' : 'thread_subject'}).get_text())
            article_Code_error_List.append(article_Code)
    
    progress_bar(100, over = True)
    if magnet_error_List:
        # 無 magnet 報錯，並提供彈性處理方案
        for title, article_Code_error in zip(magnet_error_List, article_Code_error_List):
            print(f"\n{title} ")
            print(f"    無 magnet 請開啟連結: " + "https://www.sehuatang.org/thread-" + article_Code_error + "-1-1.html" + "  確認...")    

    return dict(zip(title_List, magnet_List)), pic_link_List, publish_time_List


# if extractChoose_mean == 'choose':
#                     # Ensure Data exist
#                     if len(workSpace.title_magnet) == 0:
#                         workSpace.title_magnet, pic_link_List[fourmChoose-1], publish_time_List = get_ALL(today_list[fourmChoose-1])

#                     # Make HTML files
#                     workSpace.picture_path, workSpace.fileName = make_html(pic_link_List=pic_link_List[fourmChoose-1], fileName="Auto_SHT_Pic_" + fourmList_Chinese[fourmChoose-1] + ".html", \
#                         titleList=[title for title in workSpace.title_magnet.keys()], 
#                         magnetList=[magnet for magnet in workSpace.title_magnet.values()], 
#                         article_Code_List=today_list[fourmChoose-1],
#                         publish_time_List=publish_time_List
#                         )

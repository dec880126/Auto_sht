from tool_function import progress_bar, make_html
import requests
import bs4
import number_parser

def get_today_article(fourm, home_code, today):
    """
    To get the article published today
    type fourm, home_code, today: str
    rtype: list <- today list
    """
    print(f"[/]{today} 的 {str(fourm)} 區 的文章清單獲取中...")

    # list of "article code"
    today_list = []

    for url_pageNum_of_home in range(1, 6):
        # choose home_code
        url_home = "https://www.sehuatang.org/forum-" + str(home_code) + "-" + str(url_pageNum_of_home) + ".html"        
        
        # request to sehuatang
        response_of_home = requests.get(url_home)

        # bs4 analysis
        bs_home = bs4.BeautifulSoup(response_of_home.text,"html.parser")

        # change the date to extract the data if you want    
        tbody = bs_home.find_all('tbody')

        # extract article code
        for x in tbody:
            date = x.find('span', attrs={'title':today})
            if date == None:
                continue
            id = x.get('id')
            if "normalthread" in str(id):
                today_list.append(id[-6:])      # extract article_Code
            continue     
        url_pageNum_of_home += 1
    print(f"[*]{today} 的文章清單獲取完成!")
    return today_list   # List of article_Code


def get_title(today_list):
    """
    Read the article_Code and print all title that correspond to the parameter "today"
    type today_list: List (article_Code)
    rtype: List
    """
    titleNum = 0
    title_list = []

    print("[/]Title 提取中...")
    for article_Code in today_list:        
        titleNum += 1
        progress_bar(int(titleNum/30*99))
        response_of_article = requests.get("https://www.sehuatang.org/thread-" + article_Code + "-1-1.html")
        bs_article = bs4.BeautifulSoup(response_of_article.text,"html.parser")

        title = bs_article.find('span', attrs={'id' : 'thread_subject'}).get_text()
        title_list.append(title)
    progress_bar(100, over = True)

    print("[*]Title 已提取完畢" + "一共抓取了" + str(titleNum) + "個 title")
    print('[*]===============================================')    
    return title_list


def get_magnet(today_list):
    """
    Read the article_Code and print all magnet that correspond to the parameter "today"
    type today_list: List
    rtype: List
    """            
    magNum = 0
    magnet_List = []

    print("[/]Magnet 提取中...")
    for article_Code in today_list:
        magNum += 1
        progress_bar(int(magNum/30*99))
        response_of_pages = requests.get("https://www.sehuatang.org/thread-" + article_Code + "-1-1.html")
        bs_pages = bs4.BeautifulSoup(response_of_pages.text,"html.parser")

        magnet = bs_pages.find('div','blockcode').get_text()
        magnet_List.append(magnet.removesuffix('复制代码'))
    progress_bar(100, over = True)
    
    print("[*]Magnet 已提取完畢" + "一共抓取了" + str(magNum) + "個 magnet")
    print('[*]===============================================')
    return magnet_List


def get_pic_urlList(today_list):
    """
    Read the article_Code and print all URL of picture that correspond to the parameter "today"
    
    type today_list: list
    rtype: List
    """            
    picNum = 0
    pic_link_List = []
    
    for article_Code in today_list:        
        progress_bar(int(picNum/60*99))
        response_of_pages = requests.get("https://www.sehuatang.org/thread-" + article_Code + "-1-1.html")
        soup = bs4.BeautifulSoup(response_of_pages.text,"html.parser")

        img_block = soup.find_all('ignore_js_op')
        for block in img_block[:-1]:
            picNum += 1            
            pic_link = block.find('img').get('file')
            if pic_link != None:
                pic_link_List.append(pic_link)        
    progress_bar(100, over = True)

    print("[*]Pic URL 已提取完畢" + "一共抓取了" + str(picNum) + "個 Pic URL")    
    path, fileName = make_html(pic_link_List, "Auto_SHT_Pic.html")        
    return path, fileName


def get_ALL(today_list, fourmType):
    """
    Get title, magnet and make HTML files of picture in one operation
    type today_list: List
    rtype: Dict
    """
    article_Num = 0
    title_List = []
    magnet_List = []
    pic_link_List = []
    magnet_error_List = []
    article_Code_error_List = []

    for article_Code in today_list:
        article_Num += 1
        progress_bar(int(article_Num/len(today_list)*99))
        response_of_pages = requests.get("https://www.sehuatang.org/thread-" + article_Code + "-1-1.html")
        bs_pages = bs4.BeautifulSoup(response_of_pages.text,"html.parser")

        try:
            title = bs_pages.find('span', attrs={'id' : 'thread_subject'}).get_text()

            # 於有碼區自動挑除素人系列
            if number_parser.is_shirouto(title) and fourmType == '有碼':
                continue

            title_List.append(title)
            magnet_List.append(bs_pages.find('div','blockcode').get_text().removesuffix('复制代码'))                        
            img_block = bs_pages.find_all('ignore_js_op')
            pic_link_List.append("Head of Page")
            for block in img_block[:-1]:
                pic_link = block.find('img').get('file')
                if pic_link != None:
                    pic_link_List.append(pic_link)
            pic_link_List.append("end of page")
        except:
            magnet_error_List.append(bs_pages.find('span', attrs={'id' : 'thread_subject'}).get_text())
            article_Code_error_List.append(article_Code)
    
    progress_bar(100, over = True)
    if magnet_error_List:
        for title, article_Code_error in zip(magnet_error_List, article_Code_error_List):
            print(f"\n{title} ")
            print(f"    無 magnet 請開啟連結: " + "https://www.sehuatang.org/thread-" + article_Code_error + "-1-1.html" + "  確認...")    

    return dict(zip(title_List, magnet_List)), pic_link_List




# today_list = get_today_article('have碼', '37', '2021-07-18')

# today_list = [
#     '560232', '560230', '560229', '560228', '560227', '560225', '560224', 
#     '560222', '560221', '560220', '560211', '560203', '560193', '560187', 
#     '560182', '560181', '560040', '560039', '560038', '560036', '560034', 
#     '560033', '560032', '560031', '560026', '560023'
# ]

# titleList = get_title(today_list)

# titleList = [
#     'madv-510 後ろからデカチン即ズボっ密着洗体大原理央', 
#     'katu-085 乳首びんびんどすけべスナックママ 爆乳痴女', 
#     'gnax-057 夫には絶対見せられない白昼の絶叫熟練巨乳妻彩奈リナ', 
#     'genm-087 極・摂精の天才 深田えいみ', 
#     'genm-086 低身長Gカップ！思わず持ち上げたくなる美少女 新條ひな', 
#     'genm-085 誘惑SEX激ピストン！-誘った男がガチ腰振り- 高杉麻里', 
#     'enki-039 日米変態合戦勃発！青い目の性欲モンスタージ', 
#     'daya-016 個人撮影 巨 乳の変態淫語オバサマと濃厚ドスケベプレイ 滝川恵理', 
#     'bhg-039 誘惑する 発情期シスターず', 
#     'avsa-174 池袋Tube ほろ酔いでブクロをフラフラ歩い', 
#     'apns-250 悲劇の山岳部女教師輩達からの輪僚教師に種付けされた私.宮崎リン', 
#     'apns-249 堕とされた美人弁護士 平井栞奈', 
#     'apkh-182 淫乱絶頂 ・愛人ラブホテル 変態したくて疼美波こづえ', 
#     'apkh-181 裏取引・巨乳女性社員 淫乱枕営業セックス温泉旅高敷るあ', 
#     'apak-196 先生とラブホに来ちゃった... 体操部前乃菜々', 
#     'agav-059 最高尻～19歳の94センチ超デカ美尻女子が降臨～ 琴羽みおな', 
#     '413INST-140 幼児体形のつるぺたギャルももかちゃん 裏垢', 
#     '345SIMM-654 現役J○の美尻に元担任が激ピス！元気いっぱ', 
#     '421OCN-023 理沙ちゃん', '421OCN-022 ゆうこちゃん', 
#     '421OCN-021 ま いちゃん', '083PPP-2190 整体師の俺がお義母さんのきわどい部分をマッ', 
#     '083PPP-2189 交際している四十路女の連れ子(女子大生)が過', 
#     '083PPP-2188 モザイク無し！美女20人の本気イキオナニー全', 
#     '083PPP-2187 発情20連発！ごく普通の人妻から淫乱熟女まで', 
#     '083PPP-2186 やりすぎヤリマン伝説～一般女性のとんでもSEX'
# ]

# for t in titleList:
#     if not number_parser.is_shirouto(t):
#         print(t)

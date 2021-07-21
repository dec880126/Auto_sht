from tool_function import progress_bar, make_html
import requests
import bs4
import number_parser

title_List = []
magnet_List = []
pic_link_List = []
magnet_error_List = []
article_Code_error_List = []
article_Num = 0
title_magnet = {}
today_list = []

def get_today_article(fourm, home_code, today, pageNum):
    """
    To get the article published today
    type fourm: str
    type home_code: str
    type today: str
    type pageNum: int
    rtype: list <- today list
    """
    global today_list        

    # for url_pageNum_of_home in range(1, 6):
    # choose home_code
    url_home = "https://www.sehuatang.org/forum-" + str(home_code) + "-" + str(pageNum) + ".html"        
    
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


def get_title(article_Code):
    """
    Read the article_Code and print all title that correspond to the parameter "today"
    type today_list: List (article_Code)
    rtype: List
    """
    # titleNum = 0
    global title_list

    # print("[/]Title 提取中...")  

    # titleNum += 1
    response_of_article = requests.get("https://www.sehuatang.org/thread-" + article_Code + "-1-1.html")
    bs_article = bs4.BeautifulSoup(response_of_article.text,"html.parser")

    title = bs_article.find('span', attrs={'id' : 'thread_subject'}).get_text()
    title_list.append(title)
    # progress_bar(100, over = True)

    # print("[*]Title 已提取完畢" + "一共抓取了" + str(titleNum) + "個 title")
    print('[*]===============================================')   


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


def initial_param():
    global article_Num
    global title_List
    global magnet_List
    global pic_link_List
    global magnet_error_List
    global article_Code_error_List

    title_List = []
    magnet_List = []
    pic_link_List = []
    magnet_error_List = []
    article_Code_error_List = []
    article_Num = 0


def get_ALL(article_Code, fourmType):
    """
    Get title, magnet and make HTML files of picture in one operation
    type today_list: List
    rtype: Dict
    """
    global article_Num
    global title_List
    global magnet_List
    global pic_link_List
    global magnet_error_List
    global article_Code_error_List
    global title_magnet

    article_Num += 1
    response_of_pages = requests.get("https://www.sehuatang.org/thread-" + article_Code + "-1-1.html")
    bs_pages = bs4.BeautifulSoup(response_of_pages.text,"html.parser")

    try:
        title = bs_pages.find('span', attrs={'id' : 'thread_subject'}).get_text()

        # 有碼區自動挑除素人系列
        if number_parser.is_shirouto(title) and fourmType == '有碼':
            raise ValueError

        title_List.append(title)
        magnet_List.append(bs_pages.find('div','blockcode').get_text().removesuffix('复制代码'))                        
        img_block = bs_pages.find_all('ignore_js_op')
        pic_link_List.append("Head of Page")
        for block in img_block[:-1]:
            pic_link = block.find('img').get('file')
            if pic_link != None:
                pic_link_List.append(pic_link)
        pic_link_List.append("end of page")
    except ValueError:
        pass
    except:
        magnet_error_List.append(bs_pages.find('span', attrs={'id' : 'thread_subject'}).get_text())
        article_Code_error_List.append(article_Code)

    if magnet_error_List:
        for title, article_Code_error in zip(magnet_error_List, article_Code_error_List):
            print(f"\n{title} ")
            print(f"    無 magnet 請開啟連結: " + "https://www.sehuatang.org/thread-" + article_Code_error + "-1-1.html" + "  確認...")    

    
def get_titles_magnets() -> dict:
    global title_magnet
    global title_List
    global magnet_List

    title_magnet =  dict(zip(title_List, magnet_List))    
    return title_magnet

def get_picLinkList() -> list:
    global pic_link_List
    return pic_link_List

def get_todays() -> list:
    global today_list
    return today_list


from tool_function import progress_bar, make_html
import requests
import bs4

def today_article(home_code, today):
    """
    To get the article published today
    rtype: list
    """
    print("[/]正在獲取本日文章清單...")

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
    print("[*]本日文章清單獲取完成!")
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
    path = make_html(pic_link_List, "Auto_SHT_Pic.html")    
    print('[*]===============================================')
    return path
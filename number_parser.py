import re

def is_shirouto(title):
    number_from_shirouto = re.compile(r'\d+\D+-\d+')
    # number_from_studio = re.compile(r'\D+-\d+')

    try:
        # 先檢查是否為素人 ex: 498DDH-023(數字英文-數字)
        is_shirouto = True
        video_num = number_from_shirouto.search(title).group()
    except AttributeError:
        # 否則為一般番號 ex: STARS-401(英文-數字)
        is_shirouto = False
    return is_shirouto
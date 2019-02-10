import re
import csv
import os
from selenium import webdriver


article_id_reg = re.compile('articleid=(?P<articleid>[0-9]+)')
total_count_reg = re.compile('search.totalCount=(?P<totalcount>[0-9]+)')
board_id_reg = re.compile('cafe.naver.com/ArticleList.nhn[?]search.clubid=[0-9]+&search.menuid=(?P<menuid>[0-9]+)')


def get_extension(string: str):
    ext = re.compile('(?P<ext>[.][a-z]{3,4})$')
    e = ext.search(string)
    return e.group('ext')


def get_article_id(url: str):
    m = article_id_reg.search(url)
    return m.group('articleid')


def get_board_id(url: str):
    m = board_id_reg.search(url)
    if bool(m):
        return m.group('menuid')
    else:
        return None


def get_total_count(url: str):
    m = total_count_reg.search(url)
    return m.group('totalcount')


def make_board_url_by_id(cafe_id: int, board_id: int):
    cafe_query_string = f'search.clubid={str(cafe_id)}'
    board_query_string = f'search.menuid={str(board_id)}'
    board_type_query_string = 'search.boardtype=L'  # 리스트 타입 게시판
    url = 'https://cafe.naver.com/ArticleList.nhn?' \
          + cafe_query_string + '&' \
          + board_query_string + '&' \
          + board_type_query_string

    return url


def make_post_url_by_id(blog_id: str, log_no: int):
    blog_query_string = f'blogId={str(blog_id)}'
    logno_query_string = f'logNo={str(log_no)}'
    url = 'http://blog.naver.com/PostView.nhn?' \
          + blog_query_string + '&' \
          + logno_query_string

    return url


def get_list_of_board(driver: webdriver, cafe_id: int):
    list_of_menu = list()
    url = f'https://cafe.naver.com/MyCafeIntro.nhn?clubid={cafe_id}'
    driver.get(url)
    menu_tags = driver.find_elements_by_css_selector('ul.cafe-menu-list > li > a.gm-tcol-c')
    for menu_tag in menu_tags:
        url = menu_tag.get_attribute('href')
        board_id = get_board_id(url)
        if board_id:
            board_name = menu_tag.get_attribute('innerText').strip()
            list_of_menu.append((board_id, board_name))

    return list_of_menu


def make_csv_of_cafe(cafe_id: int, list_of_board: list, dir_path: str):
    real_dir_path = os.path.join(dir_path, 'cafe_inform.csv')
    with open(real_dir_path, 'w', encoding='utf-8', newline='') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(['cafe_id', cafe_id])
        # csv_writer.writerow(['menu_name', self.board_name])
        csv_writer.writerow(['menu_id', 'menu_name'])
        for post_tuple in list_of_board:
            csv_writer.writerow([post_tuple[0], post_tuple[1]])


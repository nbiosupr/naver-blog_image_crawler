# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.common.exceptions import NoSuchFrameException
from bs4 import BeautifulSoup
from urllib import request
from urllib.parse import urlparse
from urllib.parse import quote
from urllib.error import HTTPError
from utility import make_post_url_by_id
import re
import os


# 게시글 내 이미지들의 원본 주소를 얻기 위한 정규 표현식
# Regular expression to get original path of images in article
reg = re.compile('src="http://postfiles[0-9]+[.]naver[.]net(?P<img>/[^ ]*[.][a-zA-Z]{3,4})[?]')

# 네트워크가 끊겼을 경우 다시 다운로드 시도할 횟수 제한
LIMIT_DOWNLOAD_RETRYING = 5


# scrap_by_id
# 게시글 내 이미지들의 원본 URL을 list로 묶어 반환합니다.
# This function return list of original url of image in article

# driver : webdriver
# 셀레니엄 드라이버입니다.
# This is Selenium driver

# blog_id : str
# 카페의 아이디입니다.
# ID of cafe

# log_no : int
# 게시글의 아이디입니다.
# ID of article
def scrap_by_id(driver: webdriver, blog_id: str, log_no: int):
    url = make_post_url_by_id(blog_id, log_no)
    images = list()

    driver.get(url)

    soup = BeautifulSoup(driver.page_source, 'lxml')

    lines = soup.select('div.se_component_wrap.sect_dsc.__se_component_area img')

    for line in lines:
        m = reg.search(str(line))
        if bool(m):
            images.append('http://blogfiles.naver.net' + str(m.group('img')))

    return images

# extract_file_name
# URL로 부터 파일의 이름을 추출하기 위한 함수 입니다.
# The function to extract file name from url

# url : str
# 이미지가 위치하고 있는 URL 주소
# URL Address which image is located

def extract_file_name(url: str):
    parsed_url = urlparse(url)
    return os.path.basename(parsed_url.path)


# download_image
# URL을 이용하여 이미지를 저장하기 위한 함수 입니다.
# The function to save image using url

# url : str
# 이미지가 위치하고 있는 URL 주소
# URL Address which image is located

# dir_path : str
# 이미지를 저장할 폴더의 주소
# directory path to save image

def download_image(url: str, dir_path: str):
    file_name = extract_file_name(url)
    url = quote(url.encode('utf8'), '/:')
    try:
        request.urlretrieve(url, os.path.join(dir_path,file_name))
    except HTTPError:
        print('[e] Wrong Image URL. 이미지가 존재하지 않습니다.')


class NotFoundImage(Exception):
    def __init__(self, value):
        self.value = value

    # 생성할때 받은 value 값을 확인 한다.
    def __str__(self):
        return f'Message: Wrong Image URL. 이미지가 존재하지 않습니다. ( Received URL: { self.value } )'


class InvalidURLException(Exception):
    # 생성할때 value 값을 입력 받는다.
    def __init__(self, value):
        self.value = value

    # 생성할때 받은 value 값을 확인 한다.
    def __str__(self):
        return f'Message: May be, You inserted URL that is not cafe article ( Received URL: { self.value } )'

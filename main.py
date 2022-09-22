import zipfile
import subprocess
import shutil
import time
import requests
import os
import undetected_chromedriver
from pathlib import Path
from lxml import html

headers = {
    'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
}


def get_latest_pubpage():
    resp = requests.get(
        "https://mp.weixin.qq.com/mp/appmsgalbum?action=getalbum&album_id=2329805780276838401", headers)
    if resp.status_code != 200:
        raise "无法获取列表"
    tree = html.fromstring(resp.content)
    list = tree.xpath('//li/@data-link')
    return list[0]


def get_latest_download_link(pubpage):
    resp = requests.get(pubpage, headers)
    if resp.status_code != 200:
        raise "无法获取发布页"
    tree = html.fromstring(resp.content)
    download_link = tree.xpath(
        '//span[starts-with(text(), "https://")]/text()')[0]
    return download_link


def chrome_download_file(url):
    driver = undetected_chromedriver.Chrome(use_subprocess=True)
    driver.get(url)
    time.sleep(60)
    driver.quit()


def get_download_path(url):
    filename = url.split('/')[-1]
    return Path.home().joinpath("Downloads", filename)


def download_zip() -> str:
    pubpage = get_latest_pubpage()
    download_link = get_latest_download_link(pubpage)
    chrome_download_file(download_link)
    return get_download_path(download_link)


def unzip(filepath):
    with zipfile.ZipFile(filepath, 'r') as zip_ref:
        zip_ref.extractall()


def install():
    subprocess.check_call(["setup.exe", "/VERYSILENT"])


filepath = download_zip()
unzip(filepath)
install()
dbpath = "C:\Program Files (x86)\cz88.net\ip\qqwry.dat"
licensepath = "C:\Program Files (x86)\cz88.net\ip\License.txt"
os.mkdir("db")
shutil.copy2(dbpath, "./db/")
shutil.copy2(licensepath, "./db/")

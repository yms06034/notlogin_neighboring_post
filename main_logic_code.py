from subprocess import CREATE_NO_WINDOW
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import *

from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup as BS
from urllib.parse import urlparse, parse_qs
from datetime import datetime

import pandas as pd
import numpy as np
import time
import pyperclip
import warnings
import random

import os

warnings.filterwarnings(action='ignore')

def find_css(css_selector, browser):
    return browser.find_element(By.CSS_SELECTOR, css_selector)
def finds_css(css_selector, browser):
    return browser.find_elements(By.CSS_SELECTOR, css_selector)

def find_xpath(xpath, browser):
    return browser.find_element(By.XPATH, xpath)
def finds_xpath(xpath, browser):
    return browser.find_elements(By.XPATH, xpath)

def find_id(e_id, browser):
    return browser.find_element(By.ID, e_id)

def find_className(cn, browser):
    return browser.find_element(By.CLASS_NAME, cn)
def finds_className(cn, browser):
    return browser.find_elements(By.CLASS_NAME, cn)

def find_linktext(lt, browser):
    return browser.find_element(By.LINK_TEXT, lt)

def open_browser():
    options = webdriver.ChromeOptions()
    options.add_argument('--no--sandbox')
    options.add_argument('no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1080,800')
    options.add_argument('incognito')

    chrome_service = Service('chromedriver')
    chrome_service.creationflags = CREATE_NO_WINDOW
    chrome_service = Service(executable_path="chromedriver.exe")
    browser = webdriver.Chrome(service=chrome_service, options=options)

    return browser

def naver_login(NAVER_ID, NAVER_PW, browser):
    browser.get("https://nid.naver.com/nidlogin.login")
    browser.implicitly_wait(2)
    
    input_id = find_id('id', browser)
    input_pw = find_id('pw', browser)
    
    pyperclip.copy(NAVER_ID)
    input_id.send_keys(Keys.CONTROL, "v")
    
    time.sleep(1)
    
    pyperclip.copy(NAVER_PW)
    input_pw.send_keys(Keys.CONTROL, "v")
    
    time.sleep(1)
    
    input_pw.send_keys("\n")
    
    try:
        no_save_btn = find_id('new.dontsave', browser)
        no_save_btn.click()
    except:
        pass


def neighborhood_new_post(browser, new_cmt_list):
    new_cmt_write_urls = []
    new_cmtNicks = []
    new_n_n_list = []

    while True:
        new_cmt_write_urls.clear()
        new_n_n_list.clear()
        new_cmtNicks.clear()

        for a_i in range(1, 2+1):
            browser.get(f'https://section.blog.naver.com/BlogHome.naver?directoryNo=0&currentPage={a_i}')
            time.sleep(1.5)

            soup = BS(browser.page_source, 'html.parser')
            title_a = soup.find_all(class_='desc_inner')

            for a in title_a:
                new_n_n_list.append(a['href'])


        for i in range(len(new_n_n_list)):
            browser.get(new_n_n_list[i])
            time.sleep(.5)
            
            cmt = random.choice(new_cmt_list)
            
            try:
                try:
                    browser.switch_to.frame("mainFrame")
                except:
                    pass
                time.sleep(1)

                a_test = find_css('div.area_comment.pcol2 > a', browser)
                browser.execute_script("arguments[0].click();", a_test)
                time.sleep(1)

                a_test = find_css('span.u_cbox_secret_tag > input', browser)
                browser.execute_script("arguments[0].click();", a_test)

                time.sleep(2)

                nicknames = finds_className('u_cbox_nick', browser)
                my_nickname = find_className('u_cbox_write_name', browser).text
                print(my_nickname)
                print(cmt)

                if nicknames:
                    for nc in nicknames:
                        new_cmtNicks.append(nc.text)

                    if my_nickname in new_cmtNicks:
                        print('이미 적은 댓글이 있습니다.')
                        continue
                    else:
                        time.sleep(1.5)
                        cmt_textarea = find_className('u_cbox_text_mention', browser)

                        cmt_textarea.send_keys(' ')

                        pyperclip.copy(cmt)
                        cmt_textarea.send_keys(Keys.CONTROL, 'v')

                        time.sleep(1)

                        commit_btn = find_css('div.u_cbox_upload > button.u_cbox_btn_upload', browser)
                        # commit_btn.click()

                        new_cmt_write_urls.append(browser.current_url)
                        time.sleep(3)
                        try:
                            alert = browser.switch_to.alert
                            alert.accept()
                        except:
                            pass
                else:
                    time.sleep(1)
                    cmt_textarea = find_className('u_cbox_text_mention', browser)

                    cmt_textarea.send_keys(' ')

                    pyperclip.copy(cmt)
                    cmt_textarea.send_keys(Keys.CONTROL, 'v')

                    time.sleep(1)

                    commit_btn = find_css('div.u_cbox_upload > button.u_cbox_btn_upload', browser)
                    # commit_btn.click()

                    new_cmt_write_urls.append(browser.current_url)
                    time.sleep(3)
                    try:
                        alert = browser.switch_to.alert
                        alert.accept()
                    except:
                        pass

            except Exception as ex:
                print('댓글작성 금지 및 경고창의 이유로 댓글을 적을 수 없습니다.')
                continue

        print('한턴 끝')
        time.sleep(600)
        
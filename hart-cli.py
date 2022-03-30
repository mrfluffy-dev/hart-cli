#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import os
import subprocess
import pyperclip as clip
os.system('clear')
download_path = os.environ['HOME']+"/Pictures/hart-cli"
item = 0
page_num = 1
URL = "https://yande.re/post?page="+str(page_num)
page = requests.get(URL)
links_arr_full = []
links_arr_preview = []
def get_new_urls():
    global URL
    global page
    global page_num
    global soup
    global main_content
    global links_full
    global links_arr_full
    global links_preview
    global links_arr_preview
    links_arr_full.clear
    links_arr_full.clear
    URL = "https://yande.re/post?page="+str(page_num)
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    main_content = soup.find(id="post-list-posts")
    main_content = str(main_content)
    main_content = main_content.replace("smallimg","largeimg")
    main_content = BeautifulSoup(main_content, features="lxml")
    main_content = main_content.find(id="post-list-posts")
    links_full = main_content.find_all_next("a", class_="directlink largeimg")
    links_arr_full = []
    links_preview = main_content.find_all_next("img",  class_="preview")
    links_arr_preview = []
    for link in links_full:
        link_url = link["href"]
        links_arr_full.append(link_url)
    for link in links_preview:
        link_url = link["src"]
        links_arr_preview.append(link_url)

def next():
    global item
    global page_num
    if item != len(links_arr_preview)-1:
        item+=1
        os.system('clear')
    else:
        page_num+=1
        item=1
        get_new_urls()
        os.system('clear')

def previus():
    global item
    global page_num
    global links_arr_preview
    if item != 1:
        item-=1
        os.system('clear')
    else:
        page_num-=1
        get_new_urls()
        item= len(links_arr_preview)-1
        os.system('clear')

def download():
    global item
    global links_arr_full
    global download_path
    command = 'echo ' + links_arr_full[item] + ' | cut -d "%" -f 2 |cut -b 3-8'
    name = subprocess.check_output(command, shell=True, text=True, encoding='utf_8')
    name = name.strip('\n')
    name = str(name)+".jpg"
    command = "curl -s -o " + download_path + "/" + name + " " + links_arr_full[item]
    os.system(command)
    os.system('clear')

get_new_urls()

while True:
    command = "curl -s -o /tmp/hart-preview.jpg " + links_arr_preview[item]
    os.system(command)
    command = "convert /tmp/hart-preview.jpg -resize 500x500 /tmp/hart-preview.jpg"
    os.system(command)
    command = "kitty +icat --place 100x100@0x0 /tmp/hart-preview.jpg"
    os.system(command)
    print("next:\t\tn")
    print("previous:\tp")
    print("download:\td")
    print("copy URL:\tc")
    print("quit:\t\tq")
    choice= input()
    if choice == "n":
        next()
    elif choice == "p":
        previus()
    elif choice == "d":
        download()
    elif choice == "c":
        clip.copy(links_arr_full[item])
        os.system('clear')
    elif choice == "q":
        os.system('clear')
        exit()
    else:
        print("invaled awnser")

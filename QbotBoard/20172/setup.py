#  -*-coding:utf-8 -*-
'''
Created on 2017. 9. 11.
실행파일 만들기 위한 setup
1. pip install cx_Freeze
2. project folder 에 setup.py 생성
3. python setup.py build  

@author: cspri
'''
import sys

from cx_Freeze import setup, Executable

setup(
    name = "news-scrapy",
    version="1.0",
    description="연합신문 중아일보를 읽어오기",
    author="spring",
    executables=[Executable("scrapy crawl two", base="Win32GUI")])
    

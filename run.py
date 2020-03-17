'''
@Description: Oh My Kindle Clipping
@version: 2.0
@Author: Chandler Lu
@Date: 2020-03-14 15:54:28
@LastEditTime: 2020-03-17 22:05:05
'''
# -*- coding: utf-8 -*-

import sys
import os

import datetime
import time
import re
import json
import copy
import json2md as jmd

'''
宏定义
'''

# [索引, 书名, 作者, 页码, 开始位, 结束位, 时间戳, 内容]

INDEX_LOC = 0
NAME_LOC = 1
WRITER_LOC = 2
PAGE_LOC = 3
START_LOC = 4
END_LOC = 5
TIME_LOC = 6
BODY_LOC = 7

'''
存储结构
'''

book_json = {
    "index": 0,
    "name": "",
    "writer": "",
    "num": 0,
    "note": []
}

note_json = {
    "page": 0,
    "content_start": 0,
    "content_end": 0,
    "time": 0,
    "body": ""
}

'''
栈结构
'''


class Stack(object):
    def __init__(self):
        self._val = []

    def push(self, val):
        self._val.append(val)

    def pop(self):
        return self._val.pop()

    def peek(self):
        return self._val[self.size()-1]

    def is_empty(self):
        return self._val == None

    def size(self):
        return len(self._val)


def get_book_message(text):
    count = 0
    book_data = []
    stack = Stack()
    first_line = re.match(r'[\s\S]+(?=(\n|\r)-)', text).group()
    for i in range(len(first_line), 0, -1):
        if first_line[i - 1] == ')' or first_line[i - 1] == '）':
            stack.push(first_line[i - 1])
            count += 1
        if first_line[i - 1] == '(' or first_line[i - 1] == '（':
            count -= 1
        if i != (len(first_line) - 1) and count == 0:
            writer_split = i
            break

    '''
    TODO: 学习 BOM 问题处理
    '''
    book_name = first_line[:(writer_split - 2)
                           ].encode('utf-8').decode('utf-8-sig')

    if not book_name in all_book_name:
        all_book_name.append(book_name)
        index = len(all_book_name) - 1
    else:
        index = all_book_name.index(book_name)

    second_line = re.search(r'(- [\s\S]+)(?=(\r|\n))', text).group()
    try:
        book_page = int(
            re.search(r'(?<=您在第\s)[0-9]+(?=\s页)', second_line).group())
    except AttributeError:
        book_page = -1

    try:
        content_start = int(re.search(r'([0-9]+(?=-))', second_line).group())
    except AttributeError:
        content_start = -1

    try:
        content_end = int(re.search(r'(?<=-)[0-9]+', second_line).group())
    except AttributeError:
        content_end = -1

    try:
        note_time = re.search(
            r'[0-9]{4}年[0-9]{1,2}月[0-9]{1,2}日星期[\u4e00-\u9fa5]{1}\s[\u4e00-\u9fa5]{2}[0-9]{1,2}:[0-9]{1,2}:[0-9]{1,2}', second_line).group()
        note_time = re.sub(r'星期[\u4e00-\u9fa5]\s?', '-', note_time)
        note_time = re.sub(r'上午', 'AM-', note_time)
        note_time = re.sub(r'下午', 'PM-', note_time)
        note_time = int(time.mktime(time.strptime(
            note_time, "%Y年%m月%d日-%p-%I:%M:%S")))
    except AttributeError:
        note_time = re.search(
            r'((January|February|March|April|May|June|July|August|September|October|November|December)|((Jan|Feb|Mar|Apr|Aug|Sept|Oct|Nov|Dec)(\.?)))( ?)(\d+)((st|nd|rd|th)?),( ?)(\d{2,})( ?)(\d+){1,2}:(\d+){1,2}:(\d+){1,2}\s(AM|PM)', second_line).group()
        note_time = int(time.mktime(time.strptime(
            note_time, "%B %d, %Y %I:%M:%S %p")))

    body = re.search(r'(.*)$', text).group()

    book_data.insert(INDEX_LOC, index)
    book_data.insert(NAME_LOC, book_name)
    book_data.insert(WRITER_LOC, first_line[writer_split:-1])
    book_data.insert(PAGE_LOC, book_page)
    book_data.insert(START_LOC, content_start)
    book_data.insert(END_LOC, content_end)
    book_data.insert(TIME_LOC, note_time)
    book_data.insert(BODY_LOC, body)
    all_book_data.append(book_data)


'''
def get_all_book_name(all_book_data):
    resultList = []
    for item in all_book_data:
        if not item[0] in resultList:
            resultList.append(item[0])
    return resultList
'''

def sort_with_start_loc(all_book_data):
    all_book_data.sort(key=lambda x:x[START_LOC])

def output_json(all_book_name):
    for i in range(len(all_book_name)):
        count = 0  # 当前书籍条目计数器
        current_book_json = copy.deepcopy(book_json)
        current_book_json['index'] = i
        current_book_json['name'] = all_book_name[i]

        for k in range(len(all_book_data)):
            if all_book_data[k][0] == i:
                current_book_json['writer'] = all_book_data[k][WRITER_LOC]
                continue

        for j in range(len(all_book_data)):
            if all_book_data[j][0] == i:
                current_note_json = copy.deepcopy(note_json)
                current_note_json['page'] = all_book_data[j][PAGE_LOC]
                current_note_json['content_start'] = all_book_data[j][START_LOC]
                current_note_json['content_end'] = all_book_data[j][END_LOC]
                current_note_json['time'] = all_book_data[j][TIME_LOC]
                current_note_json['body'] = all_book_data[j][BODY_LOC]
                current_book_json['note'].append(current_note_json)
                count += 1
        current_book_json['num'] = count
        all_book_list.append(current_book_json)

    with open(os.path.join(work_path, str(ticks), 'book-' + str(ticks) + '.json'), 'w') as f:
        print(json.dumps(all_book_list), file=f)
        # print(json.dumps(all_book_list, ensure_ascii=False), file=f)


if __name__ == '__main__':
    '''
    变量定义
    '''
    work_path = os.getcwd()
    clip_path = sys.argv[1]
    all_book_name = []  # 存储所有书目的名称
    all_book_data = []  # 存储所有书目的原始数据
    all_book_list = []  # 存储所有书目的 json 数据
    ticks = int(time.time())

    '''
    My Clippings 读取
    '''
    try:
        with open(clip_path, encoding='utf-8-sig') as k:
            kindle_clip = k.read()
    except FileNotFoundError:
        print('文件路径不对哦 (〃⁠＾⁠▽⁠＾⁠〃)')
        sys.exit(0)

    first_clip = re.match(r'([\s\S]+?)(?=\n==========)', kindle_clip)
    clip = re.findall(
        r'(?<===========[\n|\r])([\S\s]+?)(?=\n==========)', kindle_clip)   # Other Clip
    try:
        clip.insert(0, first_clip.group())  # All Clip
    except AttributeError:
        print('您的书读的太少了，没有读取到标注哦 凸⁠(•̀△•́⁠＋)')
        sys.exit(0)

    for i in range(len(clip)):
        get_book_message(clip[i])

    sort_with_start_loc(all_book_data)

    '''
    Output
    '''
    os.mkdir(os.path.join(work_path, str(ticks)))
    output_json(all_book_name)
    jmd.json_to_md(work_path, ticks)

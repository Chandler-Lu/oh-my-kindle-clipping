'''
@Description: Kindle Clippings to Markdown from JSON
@version: 1.0
@Author: Chandler Lu
@Date: 2020-03-14 22:14:24
@LastEditTime: 2020-03-14 23:43:28
'''

import json
import os
import time
import datetime

def json_to_md(work_path, ticks):
    book_md = ''
    with open(os.path.join(work_path, str(ticks), 'book-' + str(ticks) + '.json'), 'r') as f:
        book_json = json.load(f)
    for i in range(len(book_json)):
        name = book_json[i]['name']
        writer = book_json[i]['writer']
        '''
        书名作者
        '''
        book_md = '# ' + name + '\n' + '## ' + writer + '\n'

        '''
        正文内容
        '''
        for j in range(len(book_json[i]['note'])):
            if book_json[i]['note'][j]['body'] != '':
                book_md = book_md + '> ' + \
                    book_json[i]['note'][j]['body'] + '\n\n'  # 正文
            else:
                continue
            book_md = book_md + 'TIME: ' + \
                str(time.strftime("%Y-%m-%d %H:%M",
                                  time.localtime(book_json[i]['note'][j]['time']))) + '  '  # 时间
            if book_json[i]['note'][j]['page'] != -1:
                book_md = book_md + 'PAGE: ' + \
                    str(book_json[i]['note'][j]['page']) + '  '  # 页码
            if book_json[i]['note'][j]['content_start'] != -1:
                book_md = book_md + 'LOC: #' + \
                    str(book_json[i]['note'][j]['content_start']) + \
                    '-'  # 起始位置
            if book_json[i]['note'][j]['content_end'] != -1:
                book_md = book_md + \
                    str(book_json[i]['note'][j]['content_end']) + \
                    '\n\n'  # 终止位置
            else:
                book_md = book_md +'\n\n'
        with open(os.path.join(work_path, str(ticks), name + '.md'), 'w') as f:
            print(book_md, file=f)


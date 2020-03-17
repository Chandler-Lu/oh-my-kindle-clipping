'''
@Description: Kindle Clippings to Markdown from JSON
@version: 1.2
@Author: Chandler Lu
@Date: 2020-03-14 22:14:24
@LastEditTime: 2020-03-17 19:43:28
'''

import os
import time
import datetime
import json
import re


def json_to_md(work_path, ticks):
    book_md = ''
    with open(os.path.join(work_path, str(ticks), 'book-' + str(ticks) + '.json'), 'r') as f:
        book_json = json.load(f)
    for i in range(len(book_json)):
        name = book_json[i]['name']
        writer = book_json[i]['writer']
        # Windows 不支持的文件命名
        file_name = re.sub(
            r'(\\)|(\/)|(\:)|(\*)|(\?)|(\")|(\<)|(\>)|(\|)', '-', name)
        '''
        书名作者
        '''
        book_md = '# ' + name + '\n\n' + '## ' + writer + '\n\n'

        for j in range(len(book_json[i]['note'])):
            if book_json[i]['note'][j]['body'] != '':
                book_md = book_md + str(time.strftime("%Y-%m-%d %a %H:%M", time.localtime(
                    book_json[i]['note'][j]['time']))) + ' | '  # 时间
                if book_json[i]['note'][j]['page'] != -1:
                    book_md = book_md + 'P' + \
                        str(book_json[i]['note'][j]['page']) + ' | '  # 页码
                if book_json[i]['note'][j]['content_start'] != -1:
                    book_md = book_md + '#' + \
                        str(book_json[i]['note'][j]
                            ['content_start']) + '-'  # 起始位置
                if book_json[i]['note'][j]['content_end'] != -1:
                    book_md = book_md + \
                        str(book_json[i]['note'][j]
                            ['content_end']) + '\n\n'  # 终止位置
                else:
                    book_md = book_md + '\n\n'
                book_md = book_md  + '**' + book_json[i]['note'][j]['body'] + '**'+ '\n\n'  # 正文
            else:
                continue
        with open(os.path.join(work_path, str(ticks), file_name + '.md'), 'w') as f:
            print(book_md, file=f)

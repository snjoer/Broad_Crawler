#!/usr/bin/env python
# -*- encoding:utf-8 -*-

import re
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


def isDate(hypo_date):
    strLen = len(hypo_date)
    digit_count = 0
    for v in hypo_date:
        if v.isdigit():
            digit_count += 1
    if 30 > strLen > 5 and 0.5 < digit_count * 1.0 / strLen < 0.9 and digit_count > 8:
        return 1
    else:
        return 0


def find_first_digit_index(hypo_date):
    for k, v in enumerate(hypo_date):
        if v.isdigit():
            return k+1
    else:
        return 0


def pre_process(dates):
    # \u5e74\u6708\u65e5
    # dates = [re.subn(r'[\u4e00-\u5e73]|[\u5e75-\u6707]', '', tm)[0] for tm in dates]
    # dates = [re.subn(r'[\u6709-\u65e4]|[\u65e6-\u9fa5]', '', tm)[0] for tm in dates]
    # 取一半
    dates = dates[:int(len(dates) / 2)]
    # 取长度小于100部分
    dates = [d for d in dates if 100 > len(d) > 0]
    # 去除一些特殊符号
    dates = [d.replace('\n', ' ').replace('\t', ' ').replace('\b', ' ').replace('&nbsp;', ' ') for d in dates]
    # 去除前后空格，合并多空格为一空格
    new_dates = []
    for v in dates:
        v = re.sub('\A\s*', '', v)
        v = re.sub('\s*\Z', '', v)
        v = re.sub('\s+', ' ', v)
        new_dates.append(v)
    # 只取有数字的部分且去除该部分首位数字之前的内容
    shorter_dates = []
    for v in new_dates:
        ffdi = find_first_digit_index(v)
        if ffdi:
            shorter_dates.append(v[ffdi-1:])
    return shorter_dates


def h1index(title, dates):
    find_hi_index = 1
    index = len(dates) - 1
    dates = dates[::-1]
    i = 0
    while i < index and find_hi_index:
        try:
            a = dates[i][0]
        except IndexError:
            print 'ERROR index', i
        else:
            b = title
        if a in b:
            find_hi_index -= 1
        i += 1
    return i


def obtain_d(response):
    data = response.body
    try:
        chatset = response.encoding
        data = data.decode(chatset, errors='ignore')
    except UnicodeDecodeError as e:
        print e
        raise UnicodeDecodeError
    else:
        dates = re.findall(r'>[\s\n]*(.*?)[\s\n]*<', data)
        shorter_dates = pre_process(dates)
        start_i = 0
        # start_i = h1index(title,shorter_dates)
        for i in range(start_i, len(shorter_dates)):
            d = shorter_dates[i]
            if isDate(d):
                return d
        else:
            return ''

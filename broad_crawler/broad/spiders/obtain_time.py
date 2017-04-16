#!/usr/bin/env python
# -*- encoding:utf-8 -*-

import re
import sys


reload(sys)
sys.setdefaultencoding('utf-8')


def isTime(d):
    strLen = len(d)
    digit_count = 0
    for dd in d:
        if dd.isdigit():
            digit_count += 1
    if 30 > strLen > 5 and digit_count * 1.0 / strLen > 0.5 and digit_count > 8:
        return 1
    else:
        return 0


def pre_process(times):
    # \u5e74\u6708\u65e5
    # times = [re.subn(r'[\u4e00-\u5e73]|[\u5e75-\u6707]', '', tm)[0] for tm in times]
    # times = [re.subn(r'[\u6709-\u65e4]|[\u65e6-\u9fa5]', '', tm)[0] for tm in times]
    times = times[:int(len(times) / 2)]
    times = [tm.replace('\n', '').replace('\t', '').replace('\b', '').replace('&nbsp;', '') for tm in times]
    times = [tm for tm in times if 100 > len(tm) > 0]
    return times


def h1index(title, times):
    find_hi_index = 1
    index = len(times) - 1
    times = times[::-1]
    i = 0
    while i < index and find_hi_index:
        try:
            a = times[i][0]
        except IndexError:
            print 'ERROR index', i
        else:
            b = title
        if a in b:
            find_hi_index -= 1
        i += 1
    return i

def xx(response):
    data = response.body
    try:
        chatset = response.encoding
        data = data.decode(chatset, errors='ignore')
    except UnicodeDecodeError as e:
        print e
        raise UnicodeDecodeError
    else:
        times = re.findall(r'>[\s\n]*(.*?)[\s\n]*<', data)
        times = pre_process(times)
        start_i = 0
        # start_i = h1index(title,times)
        for i in range(start_i, len(times)):
            tm = times[i]
            if isTime(tm):
                return tm
                break
        else:
            return "none"

#!/usr/bin/env python
# coding: utf-8
'''
@Date    : 7/26/2022
@Author  : wp
'''

import os
import configparser


cur_path = r"D:\\"
conf_path = os.path.join(cur_path, 'utool_conf.ini')
config = configparser.ConfigParser()
config.read(conf_path, encoding="utf-8")


def get_values(section):
    keys = config.options(section)
    values = [config.get(section, key).split("\n") for key in keys]
    pairs = dict(zip(keys, values))

    return pairs


if __name__ == '__main__':

    print(get_values(section="local_file"))


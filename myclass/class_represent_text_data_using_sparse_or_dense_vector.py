# -*- coding: utf-8 -*-
# !/usr/bin/python
################################### PART0 DESCRIPTION #################################
# Filename: class_represent_text_data_using_sparse_or_dense_vector.py
# Description:  Using sparse or dense vector represents text data.
#


# Author: Shuai Yuan
# E-mail: ysh329@sina.com
# Create: 2015-9-16 10:08:00
# Last:
__author__ = 'yuens'
################################### PART1 IMPORT ######################################
import logging
import time
import os
import math
import numpy as np
from compiler.ast import flatten
################################### PART2 CLASS && FUNCTION ###########################
class UsingVectorRepresentText(object):
    def __init__(self):
        self.start = time.clock()

        logging.basicConfig(level = logging.DEBUG,
                  format = '%(asctime)s  %(levelname)5s %(filename)19s[line:%(lineno)3d] %(funcName)s %(message)s',
                  datefmt = '%y-%m-%d %H:%M:%S',
                  filename = './main.log',
                  filemode = 'a')
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s  %(levelname)5s %(filename)19s[line:%(lineno)3d] %(funcName)s %(message)s')
        console.setFormatter(formatter)

        logging.getLogger('').addHandler(console)
        logging.info("START.")



    def __del__(self):
        logging.info("END.")
        self.end = time.clock()
        logging.info("The function run time is : %.03f seconds" % (self.end - self.start))



    def remove_stopword_in_title_list(self, title_list, stopword_file_read_directory):
        # sub-function
        def filter_and_unicode(ch):
            if ch == '\n':
                ch = " "
            return unicode(ch, "utf8").replace("\n", "")
        # sub-function
        def remove_stopword_in_title(title, stopword_list):
            stopword_removed_title = filter(lambda char: char not in stopword_list, title)
            return title

        try:
            f = open(stopword_file_read_directory)
            lines = f.readlines()
            stopword_list = map(filter_and_unicode, lines)
            logging.info("open file %s successfully." % stopword_file_read_directory)
        except Exception as e:
            logging.error(e)
        finally:
            f.close()

        logging.info("type(stopword_list):%s" % type(stopword_list))
        logging.info("len(stopword_list):%s" % len(stopword_list))
        logging.info("type(stopword_list[0]):%s" % type(stopword_list[0]))
        logging.info("stopword_list[0:10]:%s" % stopword_list[0:10])

        stopword_removed_title_list = map(lambda title: remove_stopword_in_title(title = title, stopword_list = stopword_list), title_list)
        logging.info("type(stopword_removed_title_list):%s" % type(stopword_removed_title_list))
        logging.info("len(stopword_removed_title_list):%s" % len(stopword_removed_title_list))
        logging.info("type(stopword_removed_title_list[0]):%s" % type(stopword_removed_title_list[0]))
        logging.info("stopword_removed_title_list[0:10]:%s" % stopword_removed_title_list[0:10])

        return stopword_removed_title_list



    def get_word_map_tuple_list(self, title_list, word_map_file_save_directory):
        # sub-function
        def save_word_map(word_map_tuple_list, word_map_file_save_directory):
            try: os.mkdir("./data")
            except Exception as e: logging.info(e)

            f = open(word_map_file_save_directory, "w")
            word_map_tuple_list = map(lambda word_map_tuple: (str(word_map_tuple[0]), word_map_tuple[1].encode("utf8")), word_map_tuple_list)
            map(lambda word_map_tuple: f.write(word_map_tuple[0] + " " + word_map_tuple[1] + "\n"), word_map_tuple_list)
            f.close()

        word_string = "".join(title_list)
        word_set = set(word_string)
        word_set_len_xrange = xrange(len(word_set))
        word_map_tuple_list = map(lambda id, word: (id, word), word_set_len_xrange, word_set)
        save_word_map(word_map_tuple_list = word_map_tuple_list, word_map_file_save_directory = word_map_file_save_directory)

        logging.info("len(word_string):%s" % len(word_string))
        logging.info("len(word_set):%s" % len(word_set))
        logging.info("len(word_set_len_xrange):%s" % len(word_set_len_xrange))
        return word_map_tuple_list



    def title_list_2_title_index_and_title_id_list_tuple_list(self, title_list, word_map_tuple_list, title_id_file_save_directory):
        # sub-function
        def title_2_id_list(title, word_map_tuple_list):
            title_id_vector = map(lambda char: char_2_id(char = char, word_map_tuple_list = word_map_tuple_list), title)
            return title_id_vector
        # sub-function
        def save_title_and_id_2_file(title_list, title_id_2d_list, title_id_file_save_directory):
            title_list = map(lambda title: title.encode("utf8"), title_list)
            #id_2d_list = map(lambda title_id_list: map(lambda id: id, title_id_list), title_id_2d_list)
            id_2d_list = title_id_2d_list

            f = open(title_id_file_save_directory, "w")
            count = xrange(len(title_list))
            map(lambda title, id_list, counter: f.write(str(counter) + " " + title + " " + str(id_list) + "\n"), title_list, id_2d_list, count)
            f.close()
        # sub-function
        def char_2_id(char, word_map_tuple_list):
            id = filter(lambda (id, word): char == word, word_map_tuple_list)[0][0]
            return id

        title_and_id_2d_list = map(lambda title: title_2_id_list(title = title, word_map_tuple_list = word_map_tuple_list), title_list)
        save_title_and_id_2_file(title_list = title_list, title_id_2d_list = title_and_id_2d_list, title_id_file_save_directory = title_id_file_save_directory)
        title_index_and_title_id_list_tuple_list = map(lambda index, one_title_id_list: (index, one_title_id_list), xrange(len(title_and_id_2d_list)), title_and_id_2d_list)
        return title_index_and_title_id_list_tuple_list



    # [[title_index, [(k1, v1), (k2, v2), ...]]]
    def title_index_and_title_id_list_tuple_list_2_word_key_value_pair_tuple_list(self, title_index_and_title_id_list_tuple_list):
        # sub-function
        def title_2_word_id_frequency_statistic_tuple(id_title):
            id_frequency_tuple_list = map(lambda word_id: (word_id, 1), id_title)
            id_frequency_tuple_list = reduceByKey(id_frequency_tuple_list)
            return id_frequency_tuple_list
        # sub-function
        def reduceByKey(tuple_list_obj):
            kv_dict = {}
            key_set = set(map(lambda record: record[0], tuple_list_obj))
            for key in key_set: kv_dict[key] = 0
            for tup in iter(tuple_list_obj): kv_dict[tup[0]] += 1
            tuple_list = map(lambda key, value: (key, value), kv_dict.keys(), kv_dict.values())
            return tuple_list

        id_title_list = map(lambda title_index_and_title_id_list_tuple: title_index_and_title_id_list_tuple[1], title_index_and_title_id_list_tuple_list)
        word_key_value_pair_tuple_list = map(lambda title: title_2_word_id_frequency_statistic_tuple(title), id_title_list)
        return word_key_value_pair_tuple_list
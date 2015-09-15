# -*- coding: utf-8 -*-
# !/usr/bin/python
################################### PART0 DESCRIPTION #################################
# Filename: class_get_text_data_from_database.py
# Description:
#


# Author: Shuai Yuan
# E-mail: ysh329@sina.com
# Create: 2015-9-7 17:07:32
# Last:
__author__ = 'yuens'
################################### PART1 IMPORT ######################################
import logging
import MySQLdb
import time
from compiler.ast import flatten
################################### PART2 CLASS && FUNCTION ###########################
class GetTextDataFromDB(object):
    def __init__(self, database_name):
        self.start = time.clock()

        logging.basicConfig(level = logging.DEBUG,
                  format = '%(asctime)s  %(levelname)5s %(filename)19s[line:%(lineno)3d] %(funcName)s %(message)s',
                  datefmt = '%y-%m-%d %H:%M:%S',
                  filename = '../main.log',
                  filemode = 'a')
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s  %(levelname)5s %(filename)19s[line:%(lineno)3d] %(funcName)s %(message)s')
        console.setFormatter(formatter)

        logging.getLogger('').addHandler(console)
        logging.info("START.")

        try:
            self.con = MySQLdb.connect(host='localhost', user='root', passwd='931209', db = database_name, charset='utf8')
            logging.info("Success in connecting MySQL.")
        except MySQLdb.Error, e:
            logging.error("Fail in connecting MySQL.")
            logging.error("MySQL Error %d: %s." % (e.args[0], e.args[1]))

    def __del__(self):
        logging.info("")
        self.con.close()
        logging.info("Success in quiting MySQL.")
        logging.info("END.")

        self.end = time.clock()
        logging.info("The function run time is : %.03f seconds" % (self.end - self.start))



    def count_essay_num(self, database_name):
        # sub function
        def count_record(cursor, database_name, table_name):
            try:
                cursor.execute("""SELECT COUNT(*) FROM %s.%s""" % (database_name, table_name))
                return  int(cursor.fetchone()[0])
            except:
                logging.error("Failed in selecting record num. of table %s in database %s" % (table_name, database_name))
                return "None"
        # sub function
        def print_name_num(record):
            logging.info("table name:%s, record num: %s" % (record[0], record[1]))

    #def count_essay_num(self, database_name):
        try:
            con = MySQLdb.connect(host = "localhost", user = "root", passwd = "931209", db = database_name, charset = "utf8")
            cursor = con.cursor()
            logging.info("Success in connecting MySQL.")
        except MySQLdb.Error, e:
            logging.info("Fail in connecting MySQL.")
            logging.info("MySQL Error %d: %s." % (e.args[0], e.args[1]))

        try:
            sql = "SHOW TABLES"
            cursor.execute(sql)
            table_name_list = map(lambda essay_tuple: essay_tuple[0],cursor.fetchall())
            table_record_num_list = map(lambda table_name: count_record(cursor = cursor, database_name = database_name, table_name = table_name), table_name_list)
        except MySQLdb.Error, e:
            logging.error("Failed in counting tables in database %s." % database_name)
            logging.error("MySQL Error %d: %s." % (e.args[0], e.args[1]))
        finally:
            cursor.close()

        table_tuple_list = map(lambda name, num: (name, num), table_name_list, table_record_num_list)
        map(print_name_num, table_tuple_list)
        logging.info("table sum num.: %s, sum record num:%s" % (len(table_name_list), sum(table_record_num_list)))
        return table_name_list



    def get_title_list_in_db(self, database_name, table_name_list):
        all_essay_title_2d_list = map(self.get_title_list, table_name_list)
        all_essay_title_list = flatten(all_essay_title_2d_list)
        return all_essay_title_list



    def get_title_list(self, table_name):
        cursor = self.con.cursor()
        sql = """SELECT title FROM %s""" % table_name
        try:
            cursor.execute(sql)
            title_list = map(lambda title: title[0], cursor.fetchall())
        except MySQLdb.Error, e:
            logging.error("Failed in attaining essay's titles in table %s." % table_name)
            logging.error("MySQL Error %d: %s." % (e.args[0], e.args[1]))
        finally:
            cursor.close()
        return title_list

################################### PART3 CLASS TEST ##################################
# Initial parameters and construct variables.
database_name = "essayDB"

GetTextData = GetTextDataFromDB(database_name = database_name)
table_name_list = GetTextData.\
    count_essay_num(database_name = database_name)

# Get title data(title list) from database.
title_list = GetTextData.get_title_list_in_db(database_name = database_name,\
                                           table_name_list = table_name_list)
logging.info("title_list[1:4]:%s" % str(title_list[1:4]))
logging.info("title_list[0]:%s" % title_list[0])
logging.info("type(title_list[0]):%s" % type(title_list[0]))
logging.info("len(title_list):%s" % len(title_list))
logging.info("type(title_list):%s" % type(title_list))
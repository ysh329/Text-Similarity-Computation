# -*- coding: utf-8 -*-
# !/usr/bin/python
################################### PART0 DESCRIPTION #################################
# Filename: main.py
# Description:
#


# Author: Shuai Yuan
# E-mail: ysh329@sina.com
# Create: 2015-9-15 21:19:37
# Last:
__author__ = 'yuens'
################################### PART1 IMPORT ######################################
from myclass.class_compute_title_similarity import *
from myclass.class_get_text_data_from_database import *
################################### PART2 MAIN ########################################
def main():
    # Initial parameters and construct variables.
    database_name = "essayDB"
    GetTextData = GetTextDataFromDB(database_name = database_name)
    table_name_list = GetTextData.\
        count_essay_num(database_name = database_name)

    stopword_file_name = "stopword.txt"
    stopword_file_path = "./data/input"
    stopword_file_read_directory = os.path.join(stopword_file_path,\
                                           stopword_file_name)

    word_map_file_name = "word_map.txt"
    word_map_file_path = "./data/output"
    word_map_file_save_directory = os.path.join(word_map_file_path,\
                                                word_map_file_name)

    title_id_file_name = "title_id.txt"
    title_id_file_path = "./data/output"
    title_id_file_save_directory = os.path.join(title_id_file_path,\
                                                title_id_file_name)

    cosine_similarity_result_file_name = "cosine_similarity_result.txt"
    cosine_similarity_result_file_path = "./data/output"
    cosine_similarity_result_file_save_directory = os.path.join(cosine_similarity_result_file_path,\
                                                                cosine_similarity_result_file_name)

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




    # Compute the Cosine Similarity of titles.
    CosineComputer = ComputeTitleSimilarity()
    logging.info("table_name_list:%s" % table_name_list)

    # Get word map from all titles and save it.
    word_map_tuple_list = CosineComputer.\
        get_word_map_tuple_list(title_list = title_list,\
                                word_map_file_save_directory = word_map_file_save_directory)
    logging.info("word_map_tuple_list[:10]: %s" % word_map_tuple_list[:10])

    # Remove stop words in titles.
    stopword_removed_title_list = CosineComputer.\
        remove_stopword_in_title_list\
        (title_list = title_list,\
         stopword_file_read_directory = stopword_file_read_directory)

    # Transform title list into title index and title id list tuple list form.
    title_index_and_title_id_list_tuple_list = CosineComputer.\
        title_list_2_title_index_and_title_id_list_tuple_list\
        (title_list = stopword_removed_title_list,\
         word_map_tuple_list = word_map_tuple_list,\
         title_id_file_save_directory = title_id_file_save_directory)
    logging.info("title_index_and_title_id_list_tuple_list[0:10]:%s" % title_index_and_title_id_list_tuple_list[0:10])
    logging.info("title_index_and_title_id_list_tuple_list[0][0]:%s" % title_index_and_title_id_list_tuple_list[0][0])

    # Transform title id list into word-frequency form tuple list.
    word_key_value_pair_tuple_list = CosineComputer.\
        title_index_and_title_id_list_tuple_list_2_word_key_value_pair_tuple_list\
        (title_index_and_title_id_list_tuple_list = title_index_and_title_id_list_tuple_list)
    logging.info("word_key_value_pair_tuple_list[0]:%s" % str(word_key_value_pair_tuple_list[0]))
    logging.info("word_key_value_pair_tuple_list[0:5]:%s" % str(word_key_value_pair_tuple_list[0:5]))
    logging.info("word_key_value_pair_tuple_list[0][0]:%s" % str(word_key_value_pair_tuple_list[0][0]))

    # Compute similarity of all titles.
    similarity_trigram_tuple_list = CosineComputer.\
        compute_title_similarity\
        (id_title_tuple_2d_list = word_key_value_pair_tuple_list)
    logging.info("len(similarity_trigram_tuple_list):%s" % len(similarity_trigram_tuple_list))
    logging.info("similarity_trigram_tuple_list[0]:%s" % str(similarity_trigram_tuple_list[0]))

    # Filter the results, whose similarity is 0.
    filtered_similarity_trigram_tuple_list = filter\
        (lambda trigram_tuple: trigram_tuple[2] != 0, similarity_trigram_tuple_list)

    # Sort the similarity result.
    sorted_similarity_trigram_tuple_list = sorted(filtered_similarity_trigram_tuple_list,
                                                  key = lambda trigram_tuple: -trigram_tuple[2])
    logging.info("sorted_similarity_trigram_tuple_list[0]:%s" % str(sorted_similarity_trigram_tuple_list[0]))
    logging.info("sorted_similarity_trigram_tuple_list[1]:%s" % str(sorted_similarity_trigram_tuple_list[1]))

    # Save the sorted similarity result into text.
    CosineComputer.save_compute_similarity_result\
        (sorted_similarity_trigram_tuple_list = sorted_similarity_trigram_tuple_list,
         cosine_similarity_result_file_save_directory = cosine_similarity_result_file_save_directory)
################################ PART4 EXECUTE ########################################
if __name__ == "__main__":
    main()
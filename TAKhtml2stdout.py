#!/usr/bin/env python3

import os
import sys
from bs4 import BeautifulSoup
import hashlib

data_table = {}

def get_options(div, card_header_text_white):
    nquestion = div.find('span', class_ = 'badge badge-pill badge-light mr-2').text
    question_text = div.find('div', class_ = card_header_text_white).text
    question = question_text.replace(nquestion, '')
    question_only = question.replace('\n', ' ').replace('\r', ' ').strip()
    hash_question_only = hashlib.sha256(question_only.replace(' ', '').lower().encode('utf-8')).hexdigest()
    if not hash_question_only in data_table:
        #print("*"*80)
        print(f"= \t{question_only}")
        #print("*"*80)
        options = div.find_all('div', class_ = 'd-flex w-100')
        answer_string_list = []
        for option in options:
            if None != option.find('i', class_ = 'fa fas fa-check'):
                check_flag = True
            else:
                check_flag = False                    
            answer_string_list.append((check_flag, option.text))
            print(("+" if check_flag else "."), f" \t{option.text}")
            #print("-"*80)
        data_table[hash_question_only] = (question_only, answer_string_list)
        print(" \t ")


def html_to_tab(html_file):
    with open(html_file) as fp:
        soup = BeautifulSoup(fp, 'html.parser')
        divs_success = soup.find_all('div', class_ = 'card mt-3 border-success')
        divs_danger = soup.find_all('div', class_ = 'card mt-3 border-danger')
        #print(f"Found {len(divs_success)} success tables and {len(divs_danger)} danger tables")
        for div in divs_success:
            get_options(div, 'card-header text-white bg-success border-success')

        for div in divs_danger:
            #print(div.text)
            #print(div.prettify())
            get_options(div, 'card-header text-white bg-danger border-danger')

        #print(soup.prettify())


if __name__ == '__main__':
    """
    Чтение строк из HTML файлов в папке и их запись в файл XLSX одной таблицей
    Usage: Html2Excel.py /path file.xlsx
    """
    if len(sys.argv) > 2:
        try:
            with os.scandir(sys.argv[1]) as it:
                file_names = [f for f in it if f.is_file() and (f.name.endswith('.html') or f.name.endswith('.htm'))]
            for file_name in file_names:
                html_to_tab(file_name)
            print(f"Found {len(file_names)} files which contain {len(data_table)} unique questions")
            #print(data_table)
            sys.exit(0)
        except Exception as error:
            print(f"Unexpected error: {error}")
            sys.exit(1)
    else:
        print("Usage: Html2Excel.py /path file.xlsx")
        sys.exit(1)

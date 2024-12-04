#!/usr/bin/env python3

import os
import sys
from bs4 import BeautifulSoup

def find_web_files(directory):
    #return [f for f in os.listdir(directory) if (f.endswith('.html') or f.endswith('.htm'))]
    with os.scandir(directory) as it:
        names = [f for f in it if f.is_file() and (f.name.endswith('.html') or f.name.endswith('.htm'))]
    return names

def get_options(div, card_header_text_white):
    print("*"*80)
    #print(div.text)
    #print(div.prettify())
    nquestion = div.find('span', class_ = 'badge badge-pill badge-light mr-2').text
    question_text = div.find('div', class_ = card_header_text_white).text
    question = question_text.replace(nquestion, '')
    question_only = question.strip()
    options = div.find_all('div', class_ = 'd-flex w-100')
    print(question_only)
    print("*"*80)
    for option in options:
        #print(option.prettify())
        if None != option.find('i', class_ = 'fa fas fa-check'):
            check_flag = "+"
        else:
            check_flag = " "                    
        #answer_text = option.find('div', class_ = 'col').prettify()
        answer_text = option.text
        print(f"{check_flag} : {answer_text}")
        print("-"*80)
    print("\n\n")


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
    Чтение таблиц из HTML файлов в папке и их запись в файл XLSX одной таблицей
    Usage: Html2Excel.py /path file.xlsx
    """
    if len(sys.argv) > 2:
        try:
            list_files = find_web_files(sys.argv[1])
            #print(f"Found {len(list_files)} files")
            for item_file in list_files:
                html_to_tab(item_file)

            sys.exit(0)
        except Exception as error:
            print(f"Unexpected error: {error}")
            sys.exit(1)
    else:
        print("Usage: Html2Excel.py /path file.xlsx")
        sys.exit(1)

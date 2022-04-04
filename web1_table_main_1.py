#### test_names, matrix_list, type_list,
#ـــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــ
from bs4 import BeautifulSoup
# from BeautifulSoup import BeautifulSoup
#import urllib2  ## instead : from urllib.request import urlopen
from urllib.request import urlopen
import re

import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from os import listdir
from os.path import isfile, join
import PyPDF2
from os import listdir
from os.path import isfile, join



from tabula import read_pdf
from tabulate import tabulate
import pandas as pd
from PyPDF2 import PdfFileReader

import numpy as np
#import geopandas
import pandas as pd
import camelot
import difflib

from check_for_column_repetition import check_for_column_repetition
from matrix_type_test_in_pdf import get_matrix_type_test_in_pdf
from check_for_column_repetition import change_column_names
from get_drug_name import get_drug_name_list
from get_test_name_list import get_test_name_list

from getting_tables_of_pdfs_in_a_file_main3 import get_tables_from_pdfs, is_keyword_in_table, which_keyword_in_table
from getting_tables_of_pdfs_in_a_file_main3 import sjoin,is_number,check_string_row,change_drug_name

from compare_tables_sample_twoTables_main2 import compare_tables


def extract_tables_from_web(file_directory_tables_wo_change, file_directory_tables_after_change, drug_names,  keywords, fields):
    url = 'https://www.idexx.com/en/milk/products/'
    # def extract_desired_pdfs_from_link(save_file_directory):

    # url = "https://www.charm.com/wp-content/uploads/"
    #html_page = urlopen(url)

    driver = webdriver.Chrome('chromedriver.exe')
    driver.get(url)

    html_page1 = urlopen(url)
    soup2 = BeautifulSoup(html_page1, 'lxml')
    tag_a_list2 = soup2.findAll('a')

    ### tables without modifications (without colum change/ drug name change/
    ### getting only the desired columns/ adding the test name,matrix, type/ adding the link)
    # save_tables_path_1 = 'D:\_GRA projects/tables_from_web_wo_change'
    # save_tables_path_2 = 'D:\_GRA projects/tables_from_web_after_change'
    save_tables_path_1 = file_directory_tables_wo_change
    save_tables_path_2 = file_directory_tables_after_change

    links = soup2.findAll('a', attrs={'href': re.compile("en/milk/dairy-tests/")})

    links1 = []
    for i in range(len(links)):
        if links[i].text == 'View product':
            links1.append(links[i])

    url ='https://www.idexx.com'
    test_name_list=[]
    for i in range(len(links1)):
        driver = webdriver.Chrome('chromedriver.exe')

        h = links1[i].get('href')
        link1 =  url + h
        driver.get(link1)

        current_link = driver.current_url
        html_page = urlopen(current_link)
        soup3 = BeautifulSoup(html_page, 'lxml')

        headline = soup3.find_all("h1")
        test_name = headline[1].text.replace(u'\xa0', u' ').strip(' ').strip('/n').strip('Test').strip(' ')
        # if test_name != 'SNAP Beta-Lactam ST Plu':
        #     continue
        print('test_name',test_name)
        print('#######################################################################################')

        cur_link = driver.current_url

        html = requests.get(cur_link).content
        df_list = pd.read_html(html)

        if (len(df_list)):
            df1 = df_list[-1]
            levels = df1.columns.nlevels
            if levels > 1:
                # for il in range(1, levels+1):
                df1 = df1.droplevel(1, axis=1)

            # if isinstance(df1.index, pd.MultiIndex):
            #     df1.index = df1.reset_index(level=1, drop=True)
            # df1.reset_index(inplace=True) #### the format of some tables are different; like:
            #### SNAP Beta-Lactam ST Plu
            #### df12_col MultiIndex([(                                                'Drug', ...),
            ####    (                                        'European MRL', ...),
            ####   (                                       'FDA Tolerance', ...),
            ####   ('SNAP Beta ST Plus Detection Level (at or below), ppb', ...)],
            df1.to_csv(save_tables_path_1 + '/'  +  'www.idexx.com' + test_name + '.csv')
            #
            # # cur_url = driver.get(current_link)
            # # print(cur_url)
            # break

            if is_keyword_in_table(df1, keywords):
                df30 = df1.copy()

                df31 = change_column_names(fields, df30)
                # print('df30')
                # print(df30)
                # print(df30.columns)
                # print('df31')
                # print(df31)
                # print(df31.columns)
                df32 = check_for_column_repetition(df31)
                ####new
                df32 = df32.loc[:, ~df32.columns.duplicated()]
                #### new
                df32_0 = df32.dropna(how='all')
                # print('df32')
                # print(df32)
                # print(df32.columns)
                df32_1 = df32_0.copy()
                df32_2 = check_string_row(df32_1)
                print('df32_2')
                print(df32_2)
                print(df32_2.columns)
                ###  if the extracted table have repeated column name, change_drug_name function gives error,
                ### df.at[] dose not work in this case ---> so i just extracted the part neede.
                ### when you want to add MRL you should take it in to account. for now, I chane all the columns
                ### that are some kind of MRL to MRL. This is for dealing with tables like the one in "2018_06_99_MRK-852.pdf"
                col2 = df32_2.columns
                if ('Drug' in col2) and ('Sensitivity' in col2):
                    df32_3 = df32_2[['Drug', 'Sensitivity']]
                else:
                    # # not_interested +=1
                    # list_pdfs_with_tables_wo_intended_var.append(file)
                    # df33 = df32_2.copy()
                    continue
                df32_4 = change_drug_name(df32_3, drug_names)
                print('df32_4')
                print(df32_4)
                df33 = df32_4.copy()

                #### all of the tables in this link are for milk
                df33['Matrix'] = 'Milk'
                df33['Test'] = test_name
                df33['Type'] = np.nan
                df33['URL/ Contact email'] = cur_link
                # df33 = df33.replace('\*', '', regex=True).astype(float)
                # df33 = df33.replace('\‡', '', regex=True).astype(float)
                # df33 = df33.applymap(lambda x: str(x).rstrip('*'))
                # df33 = df33.applymap(lambda x: str(x).rstrip('‡'))
                # df33 = df33.applymap(lambda x: str(x).rstrip('§'))
                df33 = df33.applymap(lambda x: str(x).rstrip('ppb'))
                print('df33')
                print(df33)

                # df33.to_csv(save_tables_path_2 + '/' + 'www.idexx.com_' + test_name + '.csv')
                writer = pd.ExcelWriter(save_tables_path_2 + '/' + 'www.idexx.com_' + test_name + '.xlsx', engine='xlsxwriter')
                df33.to_excel(writer, index=False)
                writer.save()

                # df33.to_excel(writer, sheet_name='Table' + str(n), index=False)
                # writer.save()

            # test_name_list.append(headline[1].text.replace(u'\xa0', u' '))


# ###############______________________________________ main
# ############# if want to just run this code uncomment the below:
#
#
# import pandas as pd
# from bs4 import BeautifulSoup
# # from BeautifulSoup import BeautifulSoup
# #import urllib2  ## instead : from urllib.request import urlopen
# from urllib.request import urlopen
# import re
#
# import requests
# from selenium import webdriver
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
#
#
#
#
# from os import listdir
# from os.path import isfile, join
# import PyPDF2
# from os import listdir
# from os.path import isfile, join
#
#
#
# from tabula import read_pdf
# from tabulate import tabulate
# import pandas as pd
# from PyPDF2 import PdfFileReader
#
# import numpy as np
# #import geopandas
# import pandas as pd
# import camelot
# import difflib
#
# ### import external functions from other .py files in this folder
# from check_for_column_repetition import check_for_column_repetition
# from matrix_type_test_in_pdf import get_matrix_type_test_in_pdf
# from check_for_column_repetition import change_column_names
# from get_drug_name import get_drug_name_list
# from get_test_name_list import get_test_name_list
#
# from getting_tables_of_pdfs_in_a_file_main3 import get_tables_from_pdfs
# from compare_tables_sample_twoTables_main2 import compare_tables
#
#
# from getting_tables_of_pdfs_in_a_file_main3 import is_keyword_in_table
# from getting_tables_of_pdfs_in_a_file_main3 import check_string_row
# from getting_tables_of_pdfs_in_a_file_main3 import change_drug_name
# # from getting_tables_of_pdfs_in_a_file_main3 import
#
#
#
# #_______________________define the list of test_name/matix/type
#
# # keywords to be looked up in the tables we are getting from pdf
# from get_test_name_list import get_test_name_list
# test_names = get_test_name_list()
# matrix_list =['Milk','Honey','Serum','Tissue','Kidney','Dairy','Aquaculture','Urine']
# type_list =['Sequential', 'Competitive','Quantitative']
#
# ### define the desirable keywords in the pdf
# # keywords = ['ppb', 'milk', 'safety','honey','serum','tissue','kidney','ppm','dairy','Aquaculture','MRL','Urine','Sensitivity','Tolerance'
# #             , 'CONCENTRATIONFORPOSITIVEPPB','CHARMSL','SENSITIVITY','TESTSENSITIVITY', 'CONCENTRATION', 'POSITIVECONCENTRATION', 'DETECTIONLEVEL', 'DETECTIONRANGE'
# #             , 'CODEX','TECHNICALREGULATION','MRPL','FEDERATION','REGULATION','IMPORTREGULATION'
# #             , 'ACTIONLEVEL','SAFELEVEL','TOLERANCE']
#
#
# keywords = ['ppb', 'milk', 'safety','honey','serum','tissue','kidney','ppm','dairy','Aquaculture','MRL','Urine','Sensitivity'
#             , 'CONCENTRATIONFORPOSITIVEPPB','CHARMSL','SENSITIVITY','TESTSENSITIVITY', 'CONCENTRATION', 'POSITIVECONCENTRATION', 'DETECTIONLEVEL', 'DETECTIONRANGE'
#             ]
#
# ### the following dictionary is used for chnaging the column fields in the tables.
# ### Note that for just extracting the sensitivity from the tables, different kinds of MRL are just replaced by MRL
# ### (so for later use, if you are interested in extracting MRL you need to consider it).
# ### We changed them to MRL, since some tables have coulmn repetition and we want to merge them
#
# fields = {'Drug':{'DRUG','ACTIVEINGREDIENT','RESIDUESDETECTED', 'ANTIMICROBIALDRUG', 'ANTIMICROBIALAGENT','BETALACTAMDRUG', 'BETALACTAMS','TETRACYCLINES', 'QUINOLONEDRUG'}
#           , 'Test':{'TEST','TEST NAME'}
#           , 'Sensitivity':{'CONCENTRATIONFORPOSITIVEPPB','CHARMSL','SENSITIVITY','TESTSENSITIVITY', 'CONCENTRATION', 'POSITIVECONCENTRATION', 'DETECTIONLEVEL', 'DETECTIONRANGE','DETECTIONRANGEPPB'}
#           , 'Matrix': {'MATRIX','SPECIMEN'}
#           ,'Type': {'TYPE'}
#           , 'MRL': {'MRL', 'CODEX','TECHNICALREGULATION','MRPL','FEDERATION','REGULATION','IMPORTREGULATION','MRLPPB'}
#           ,'Tolerance':{'ACTIONLEVEL','SAFELEVEL','TOLERANCE'}}
#
# ## read the excel file containing the drug name and their other names
# ## I got this list based on the tests in "Rapid tests_Downloaded_2020_Jan_14_1.excel" file and also based on the pdfs Tara gave me
# ## (the code is in get_drug_name.py if needed)
# drug_names = get_drug_name_list()
# #########__________________________________
# file_directory_tables_wo_change = 'D:\_GRA projects/tables_from_web_wo_change'
# file_directory_tables_after_change = 'D:\_GRA projects/tables_from_web_after_change'
# extract_tables_from_web(file_directory_tables_wo_change, file_directory_tables_after_change, drug_names, keywords, fields)

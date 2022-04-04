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


### import external functions from other .py files in this folder
from check_for_column_repetition import check_for_column_repetition
from matrix_type_test_in_pdf import get_matrix_type_test_in_pdf
from check_for_column_repetition import change_column_names
from get_drug_name import get_drug_name_list
from get_test_name_list import get_test_name_list

from getting_tables_of_pdfs_in_a_file_main3 import get_tables_from_pdfs, is_keyword_in_table, which_keyword_in_table
from getting_tables_of_pdfs_in_a_file_main3 import sjoin,is_number,check_string_row,change_drug_name

from compare_tables_sample_twoTables_main2 import compare_tables
from web1_table_main_1 import extract_tables_from_web
pd.set_option("display.max_columns", 1000)


#_______________________define the list of test_name/matix/type

# keywords to be looked up in the tables we are getting from pdf
from get_test_name_list import get_test_name_list
test_names = get_test_name_list()
matrix_list =['Milk','Honey','Serum','Tissue','Kidney','Dairy','Aquaculture','Urine']
type_list =['Sequential', 'Competitive','Quantitative']

### define the desirable keywords in the pdf
# keywords = ['ppb', 'milk', 'safety','honey','serum','tissue','kidney','ppm','dairy','Aquaculture','MRL','Urine','Sensitivity','Tolerance'
#             , 'CONCENTRATIONFORPOSITIVEPPB','CHARMSL','SENSITIVITY','TESTSENSITIVITY', 'CONCENTRATION', 'POSITIVECONCENTRATION', 'DETECTIONLEVEL', 'DETECTIONRANGE'
#             , 'CODEX','TECHNICALREGULATION','MRPL','FEDERATION','REGULATION','IMPORTREGULATION'
#             , 'ACTIONLEVEL','SAFELEVEL','TOLERANCE']


keywords = ['ppb', 'milk', 'safety','honey','serum','tissue','kidney','ppm','dairy','Aquaculture','MRL','Urine','Sensitivity'
            , 'CONCENTRATIONFORPOSITIVEPPB','CHARMSL','SENSITIVITY','TESTSENSITIVITY', 'CONCENTRATION', 'POSITIVECONCENTRATION', 'DETECTIONLEVEL', 'DETECTIONRANGE'
            ]

### the following dictionary is used for chnaging the column fields in the tables.
### Note that for just extracting the sensitivity from the tables, different kinds of MRL are just replaced by MRL
### (so for later use, if you are interested in extracting MRL you need to consider it).
### We changed them to MRL, since some tables have coulmn repetition and we want to merge them

fields = {'Drug':{'DRUG','ACTIVEINGREDIENT','RESIDUESDETECTED', 'ANTIMICROBIALDRUG', 'ANTIMICROBIALAGENT','BETALACTAMDRUG', 'BETALACTAMS','TETRACYCLINES', 'QUINOLONEDRUG','STANDARD'}
          , 'Test':{'TEST','TEST NAME'}
          , 'Sensitivity':{'CONCENTRATIONFORPOSITIVEPPB','CHARMSL','SENSITIVITY','TESTSENSITIVITY', 'CONCENTRATION', 'POSITIVECONCENTRATION', 'DETECTIONLEVEL', 'DETECTIONRANGE','DETECTIONRANGEPPB'}
          , 'Matrix': {'MATRIX','SPECIMEN'}
          ,'Type': {'TYPE'}
          , 'MRL': {'MRL', 'CODEX','TECHNICALREGULATION','MRPL','FEDERATION','REGULATION','IMPORTREGULATION','MRLPPB'}
          ,'Tolerance':{'ACTIONLEVEL','SAFELEVEL','TOLERANCE'}}

## read the excel file containing the drug name and their other names
## I got this list based on the tests in "Rapid tests_Downloaded_2020_Jan_14_1.excel" file and also based on the pdfs Tara gave me
## (the code is in get_drug_name.py if needed)
drug_names = get_drug_name_list()

# ### main_______________________________________________________________________________________________________________
#
# # ### 1 _________________________ get_tables_from_pdfs
# # ### where the pdfs are in
# # file_directory = "D:/_GRA projects/Epapers1"
# file_directory = "D:\_GRA projects\latest_version_1\Epapers1"
#
# ### where you want to save the extracted tables
# # file_directory_tables = "D:\_GRA projects\Charm\extracted_tables"
# file_directory_tables = "D:\_GRA projects\latest_version_1\extracted_tables"
#
# df330, list_pdfs_with_no_extracted_tables, list_pdfs_with_tables_wo_intended_var, except_files = get_tables_from_pdfs(file_directory, file_directory_tables, drug_names, test_names, matrix_list, type_list,keywords,fields)
#
#
# ### if you want to only compare the tabales, only uncomment the below block (2) and comment block 1
# ### 2_________________________ get_tables_from_pdfs
# file_directory_other_files = "D:\_GRA projects\latest_version_1\extracted_tables"
# file_directory_main_file = 'D:\_GRA projects\Charm'+ '/Rapid tests_for_comparison.xlsx'
#
# compare_tables(file_directory_other_files,file_directory_main_file)
#


## if you want to only get tables from url and compare it with the main file, only uncomment the below block (3) and comment block 1 and 2
## 3_________________________ get_tables_from_pdfs
file_directory_tables_wo_change = 'D:\_GRA projects/tables_from_web_wo_change'
file_directory_tables_after_change = 'D:\_GRA projects/tables_from_web_after_change'
extract_tables_from_web(file_directory_tables_wo_change, file_directory_tables_after_change, drug_names, keywords, fields)

file_directory_main_file = 'D:\_GRA projects\Charm'+ '/Rapid tests_for_comparison.xlsx'
file_directory_other_files_1 = "D:\_GRA projects/tables_from_web_after_change"
compare_tables(file_directory_other_files_1, file_directory_main_file)
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

### import external functions from other .py files in this folder
from check_for_column_repetition import check_for_column_repetition
from matrix_type_test_in_pdf import get_matrix_type_test_in_pdf
from check_for_column_repetition import change_column_names
from get_drug_name import get_drug_name_list



###### function ________________________________________________

def is_keyword_in_table(df, keywords):
    '''
    function for checking a set of desirable keywords in the table
    :param df: table
    :param keywords: list of keywords
    :return: true if any of the keywords were found in the pdf, False otherwise
    '''

    keyword_in_table = False
    r = (df.index.values).tolist()
    #print('r',r)
    #print('type_r',type(r))
    c = (df.columns).tolist()
    #print('c', c)
    #print('type_c', type(c))
    rc=r
    rc.extend(c)
    #print('rc', rc)
    #print('type_rc', type(rc))

    for i in rc:
        if keyword_in_table:
            break
        for j in keywords:
            if str(j).upper() in str(i).upper():
                keyword_in_table = True
                break
    if not keyword_in_table:
        for col in df:
            if keyword_in_table:
                break
            for j in keywords:
                if sum(df[col].str.contains(j,case=False)):
                    keyword_in_table = True
                    break
    return keyword_in_table

###### function ________________________________________________

def which_keyword_in_table(df, keywords):
    '''
    function for getting the test_name/type/matrix in pdf
    :param df: pdf
    :param keywords: the desiarable
    :return: the keyword that was found in the pdf
    '''
    import numpy as np
    keyword_in_table = False
    r = (df.index.values).tolist()
    print('r',r)
    print('type_r',type(r))
    c = (df.columns).tolist()
    print('c', c)
    print('type_c', type(c))
    rc=r
    rc.extend(c)
    print('rc', rc)
    print('type_rc', type(rc))
    word = np.nan

    for i in rc:
        for j in keywords:
            if str(j).upper() in str(i).upper():
                keyword_in_table = True
                word=j
                break
    if not keyword_in_table:
        for col in df:
            for j in keywords:
                if sum(df[col].str.contains(j,case=False)):
                    keyword_in_table = True
                    word=j
                    break
    return word

###### function ________________________________________________
def sjoin(x): return ';'.join(x.astype(str))


###### function ________________________________________________
def is_number(s):
    try:
        float(s)
        return True
    except:
        return False
###### function ________________________________________________
def check_string_row(df100):
    col = df100.columns
    row_num = df100.shape[0]
    index_to_remove =[]
    extracted_num_cell=[]
    for rn in range(row_num):
        for col_name in col:
            cell = df100.iloc[rn][col_name]
            if isinstance(cell,str):
                contain_number = False
                for s in cell.split():
                    if is_number(s):
                        contain_number = True
                        break
                if contain_number:
                    break

                # extracted_num_cell = [int(s) for s in cell.split() if s.isdigit()]
                # if len(extracted_num_cell):
                #     break
        # if not len(extracted_num_cell):
        #     index_to_remove.append(rn)
        if not contain_number:
            index_to_remove.append(rn)

    if len(index_to_remove):
        df101 = df100.drop(df100.index[index_to_remove])
        df101 = df101.reset_index(drop=True)
    else:
        df101 = df100.copy()

    return df101

###### function ________________________________________________
def change_drug_name(df190, drug_name_dict):
    '''
    it changes the name of the drugs according to the given list
    (sometimes by mistake some letters or numbers will be added to a drug
    or it has several names and it should be considered since different tables are compared based on the drug name)

    :param df200: given table
    :param drug_name_dict: given drug name (it is obtained based on an excel file,
                           if you encountered with a new drug you can add it to this list)
    :return: the new table with the fixed drug name
    '''
    df200 = df190.copy()
    col = df190.columns
    # print('col',col)
    # print('df190')
    # df190
    row_num = df190.shape[0]

    if 'Drug' in col:
        for rn in range(row_num):
            # print('rn',rn)
            cell = df190.iloc[rn]['Drug']

            # cell1 = []
            if '(' in cell:
                cell0 = cell.strip(')').split('(')
            else:
                cell0 = [cell]

            # cell1 = ''.join(e for e in cell if e.isalnum()).upper()
            cell1 = [''.join(e for e in sub_cell_i if e.isalnum()).upper() for sub_cell_i in cell0]
            drug_in_list = False
            for k, v in drug_name_dict.items():
                if drug_in_list:
                    break
                new_list = []
                # print('k', k)
                # print('v', v)
                new_list.extend(v)
                new_list.append(k)
                # print('new_list', new_list)

                for tt in new_list:
                    # print('tt', tt)
                    tt1 = ''.join(e for e in tt if e.isalnum()).upper()
                    # print('tt1',tt1)
                    tt1_in_cell1 = False
                    for sub_cell in cell1:
                        if tt1 in sub_cell:
                            tt1_in_cell1 = True
                            tt1_match_subcell = int(difflib.SequenceMatcher(None, tt1, sub_cell).ratio() * 100) > 95
                            break

                    if (tt1_in_cell1) and tt1_match_subcell:
                    # if (tt1 in cell1) and int(difflib.SequenceMatcher(None, tt1, cell1).ratio() * 100) > 95:
                        drug_in_list = True
                        # print("df200[rn]['Drug']", df200.iloc[rn]['Drug'])
                        df200.at[rn, 'Drug'] = k

                        break
                        # df200.at[rn,'Drug'] = k
                        # df200.iat[rn,'Drug'] = k  ### wrong
                        # df200.iloc[rn]['Drug'] = k ### wrong
                        # df200[rn]['Drug'] = k  ### wrong

        df201 = df200.copy()
    else:
        df201 = df200.copy()

    return df201
###### main ________________________________________________

def get_tables_from_pdfs(file_directory, file_directory_tables, drug_names, test_names, matrix_list, type_list,keywords,fields):
    #_______________________define the list of test_name/matix/type
    # list the name of all pdfs, for witch no tables were extracted
    list_pdfs_with_no_extracted_tables =[]
    list_pdfs_with_tables_wo_intended_var = []
    except_files = []
    #
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
    #           , 'Sensitivity':{'CONCENTRATIONFORPOSITIVEPPB','CHARMSL','SENSITIVITY','TESTSENSITIVITY', 'CONCENTRATION', 'POSITIVECONCENTRATION', 'DETECTIONLEVEL', 'DETECTIONRANGE'}
    #           , 'Matrix': {'MATRIX','SPECIMEN'}
    #           ,'Type': {'TYPE'}
    #           , 'MRL': {'MRL', 'CODEX','TECHNICALREGULATION','MRPL','FEDERATION','REGULATION','IMPORTREGULATION'}
    #           ,'Tolerance':{'ACTIONLEVEL','SAFELEVEL','TOLERANCE'}}
    #
    #
    # ## read the excel file containing the drug name and their other names
    # ## I got this list based on the tests in "Rapid tests_Downloaded_2020_Jan_14_1.excel" file and also based on the pdfs Tara gave me
    # ## (the code is in get_drug_name.py if needed)
    # drug_names = get_drug_name_list()

    ## file_directory the directory of the file contaning well-formatted tables
    # file_directory = "D:/_GRA projects/Epapers"
    # file_directory = "D:/_GRA projects/Epapers1"

    onlyfiles = [f for f in listdir(file_directory) if isfile(join(file_directory, f))]


    n=1
    for file in onlyfiles:
        try:
            # not_interested = 0
            # if file == '2018_06_1_MRK-003.pdf' or file == '2018_06_74_MRK-371-email.pdf':
            #     continue
            table_found_in_pdf = False
            print('file', file)

            paper_path = file_directory + "/" + file
            pdf = PdfFileReader(open(paper_path, 'rb'))
            PN = pdf.getNumPages()
            print('PN',PN)

            writer = pd.ExcelWriter(file_directory_tables+'/'+file +'.xlsx', engine='xlsxwriter')

            # with pd.ExcelWriter(file + '.xlsx') as writer:
            for i in range(1, PN+1):
                # try:

                df = read_pdf(paper_path, pages=i, output_format="json")
                print('df',df)
                print('len(df)', len(df))

                if len(df):
                    for j in range(len(df)):

                        top = df[j]['top']
                        left = df[j]['left']
                        bottom = df[j]['height'] + top
                        right = df[j]['width'] + left

                        df1 = read_pdf(paper_path, pages=i, spreadsheet=True, area=(top - 1, left+1, bottom, right))
                        print('df1', df1)

                        # ##### ***** from here

                        ### if it was not successful for extracting any tables from pdf we want to store the fils name in a list.
                        ### ...
                        if not table_found_in_pdf and df1 is not None:
                            table_found_in_pdf = True
                        ### ...

                        if (df1 is not None) and is_keyword_in_table(df1, keywords):

                            a = list(df1.columns.str.match('Unnamed'))
                            ## to do: have a stronger condition to recognize if the first row does not include the tiltes
                            if a.count(True) > 0 and len(df1.index): ##df.shape[1]-1  and len(df1.index)
                                if list(df1.iloc[0, :].isnull()).count(True) == 0:

                                    ### sometimes all the elements of a column are Nan (we need to remove this column)
                                    df1.dropna(axis=1, how='all')


                                    df1.rename(columns = df1.iloc[0,:], inplace=True)
                                    df1 = df1.reset_index(drop=True)
                                    df1 = df1.drop(df1.index[[0]])
                                    df1 = df1.reset_index(drop=True)


                                else:
                                    ### sometimes all the elements of a column are Nan (we need to remove this column)
                                    df1 = df1.dropna(axis=1, how='all')

                                    while(list(df1.iloc[0, :].isnull()).count(True)):
                                        df1 = df1.drop(df1.index[[0]])
                                        df1 = df1.reset_index(drop=True)

                                    df1.rename(columns = df1.iloc[0,:], inplace=True)
                                    df1 = df1.reset_index(drop=True)
                                    df1 = df1.drop(df1.index[[0]])
                                    df1 = df1.reset_index(drop=True)

                            #res = df.DataFrame({i: df[i].values.T.ravel() for i in set(df.columns)})
                            df1.groupby(level=0, axis=1).apply(lambda x: x.apply(sjoin, axis=1))

                            #df.to_excel(writer, sheet_name='Sheet_name_' + str(n), index=False)
                            # df1.to_excel(writer, sheet_name='Table' + str(n), index=False)
                            # writer.save()
                        # #### ****** to here (commment from here to here if you want to check whether you get the tables without remoivng unnamed rows)
                        #### if commenting the lines below (uncomment the folowing line)
                            #df33 = df1.copy()   ### remove it

                        if (df1 is not None) and is_keyword_in_table(df1, keywords):
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
                            print(df32.columns)
                            df32_1 = df32_0.copy()
                            df32_2 = check_string_row(df32_1)
                            # print('df32_2')
                            # print(df32_2)
                            print(df32_2.columns)
                            ###  if the extracted table have repeated column name, change_drug_name function gives error,
                            ### df.at[] dose not work in this case ---> so i just extracted the part neede.
                            ### when you want to add MRL you should take it in to account. for now, I chane all the columns
                            ### that are some kind of MRL to MRL. This is for dealing with tables like the one in "2018_06_99_MRK-852.pdf"
                            col2 = df32_2.columns
                            if ('Drug' in col2) and ('Sensitivity' in col2):
                                df32_3 = df32_2[['Drug','Sensitivity']]
                            else:
                                # not_interested +=1
                                list_pdfs_with_tables_wo_intended_var.append(file)
                                df33 = df32_2.copy()
                                continue
                            df32_4 = change_drug_name(df32_3, drug_names)
                            df33 = df32_4.copy()

                            # df30 = df1.copy()
                            # df30_1 = change_drug_name(df30, drug_names)
                            # df31 = change_column_names(fields, df30_1)
                            # df32 = check_for_column_repetition(df31)
                            # df32_0 = df32.dropna()
                            # df32_1 = df32_0.copy()
                            # df32_2 = check_string_row(df32_1)
                            # # df32_3 = change_drug_name(df32_2, drug_names)
                            # df33 = df32_2.copy()


                            ### MatrixTestType is a dictionary like:
                            ### MatrixTestType = {'Matrix': ['Milk'], 'Test': ['Charm Quad'], 'Type': []}
                            ### if the len of list for each key is 0; it was not found in the pdf
                            MatrixTestType = get_matrix_type_test_in_pdf(paper_path, test_names, matrix_list, type_list)
                            if len(MatrixTestType['Matrix']):
                                df33['Matrix'] = MatrixTestType['Matrix'][0]
                            else:
                                df33['Matrix'] = np.nan
                            if len(MatrixTestType['Test']):
                                df33['Test'] = MatrixTestType['Test'][0]
                            else:
                                df33['Test'] = np.nan
                            if len(MatrixTestType['Type']):
                                df33['Test'] = MatrixTestType['Type'][0]
                            else:
                                df33['Type'] = np.nan

                            b = file.strip('~$')
                            b = b.split('_')
                            cur_link = "https://www.charm.com/wp-content/uploads/"+b[0]+"/"+b[1]+"/"+b[3]
                            df33['URL/ Contact email'] = cur_link
                            df33.to_excel(writer, sheet_name='Table' + str(n), index=False)
                            writer.save()
                # except:
                #     pass
            n = n + 1

            print('file_number:',n)
            ### ...
            if not table_found_in_pdf:
                list_pdfs_with_no_extracted_tables.append(file)
        except:
            except_files.append(file)
    return df33, list_pdfs_with_no_extracted_tables, list_pdfs_with_tables_wo_intended_var, except_files




#
# n=1
# with pd.ExcelWriter('output2.xlsx') as writer:
#     for file in onlyfiles:
#         try:
#
#
#             pdf = PdfFileReader(open("D:/_GRA projects/Charm/files"+"/"+file, 'rb'))
#             PN = pdf.getNumPages()
#
#             if PN ==1:
#                 N = 1
#             else:
#                 N=2
#
#             df = read_pdf("D:/_GRA projects/Charm/files"+"/"+file, pages=N, output_format="json")
#
#             top = df[0]['top']
#             left = df[0]['left']
#             bottom = df[0]['height'] + top
#             right = df[0]['width'] + left
#
#             df = read_pdf(file, pages=N, spreadsheet=True, area=(top - 1, left, bottom, right))
#
#             a = list(df.columns.str.match('Unnamed'))
#             ## to do: have a stronger condition to recognize if the first row does not include the tiltes
#             if a.count(True) > 0: ##df.shape[1]-1
#                 if list(df.iloc[0, :].isnull()).count(True) == 0:
#                     df.rename(columns = df.iloc[0,:], inplace=True)
#                     df = df.reset_index(drop=True)
#                     df = df.drop(df.index[[0]])
#                     df = df.reset_index(drop=True)
#                 else:
#
#                     while(list(df.iloc[0, :].isnull()).count(True)):
#                         df = df.drop(df.index[[0]])
#                         df = df.reset_index(drop=True)
#
#                     df.rename(columns = df.iloc[0,:], inplace=True)
#                     df = df.reset_index(drop=True)
#                     df = df.drop(df.index[[0]])
#                     df = df.reset_index(drop=True)
#
#             #res = df.DataFrame({i: df[i].values.T.ravel() for i in set(df.columns)})
#             df.groupby(level=0, axis=1).apply(lambda x: x.apply(sjoin, axis=1))
#
#             #df.to_excel(writer, sheet_name='Sheet_name_' + str(n), index=False)
#             df.to_excel(writer, sheet_name=file + str(n), index=False)
#             n = n + 1
#         except:
#             continue


    # fileReader = PyPDF2.PdfFileReader(open(file,'rb'))
    #
    # count = 0
    #
    # while count < 3:
    #
    #     pageObj = fileReader.getPage(count)
    #     count +=1
    #     text = pageObj.extractText()

# with pd.ExcelWriter('output1.xlsx') as writer:
#     df.to_excel(writer, sheet_name='Sheet_name_1')
#     a.to_excel(writer, sheet_name='Sheet_name_2')
#


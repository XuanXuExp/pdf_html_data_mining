import pandas as pd

from os import listdir
from os.path import isfile, join
import PyPDF2
from os import listdir
from os.path import isfile, join

# file_directory_other_files = "D:\_GRA projects\Charm\extracted_tables"
# file_directory_main_file = 'D:\_GRA projects\Charm'+ '/Rapid tests_for_comparison.xlsx'


def compare_tables(file_directory_other_files,file_directory_main_file):
    onlyfiles = [f for f in listdir(file_directory_other_files) if isfile(join(file_directory_other_files, f))]
    #
    #
    # n=1
    for file in onlyfiles:
        print('file', file)
        print(type(file))

        file_directory_next_file = file_directory_other_files+ '/' + file.strip('~$')
        df = pd.read_excel(file_directory_next_file , None)

        df_test = pd.read_excel(file_directory_main_file, None)

        ### converting the "OrderedDict" format (format of df_test and df) to dataframe format
        ###df
        a = df.keys()
        b = list(a)
        y = df[b[0]].columns
        df1 = df[b[0]]

        ###df_test
        a1 = df_test.keys()
        b1 = list(a1)
        df_test1 = df_test[b1[0]]
        df_test1 = df_test1.loc[:, ~df_test1.columns.str.contains('^Unnamed')]
        if 'sensitivity_update' in df_test1.columns:
            df_test1 = df_test1.drop(['sensitivity_update'], axis=1)

        #....................................... the code in this part checks for repetitions in the columns (down)


        ############## renaming the columns: actually some Columns are the same, but they will be read differently.
        #########check for repeted colunm names
        # ###############https://stackoverflow.com/questions/48298328/how-to-combine-columns-with-same-name
        #
        # import difflib
        # yy = [''.join(e for e in i if e.isalnum()) for i in y]
        # replication = True
        # if (len(yy) % 2 == 0):
        #     yy2 = int(len(yy) / 2)
        #     for i in range(yy2):
        #         if int(difflib.SequenceMatcher(None, yy[i], yy[i + yy2]).ratio() * 100) < 85:
        #             replication = False
        #
        # ## for copying df, you need to use one of the following commands:
        # ## (since df uses call_by_reference not call_by_value)
        # # from copy import deepcopy
        # # df2 = deepcopy(df1)
        # # or
        # # df2 = df1.copy()
        #
        # col = dict()
        # df1_col = df1.columns
        # if replication:
        #     for i in range(yy2):
        #         #         df1.rename(columns[df1_col[i+yy2]]=df1_col[i], inplace = True)
        #         col[df1_col[i + yy2]] = df1_col[i]
        #
        # df1.rename(columns=col, inplace=True)
        # # df1.rename(col, inplace = True)
        # df1.rename(col)
        #
        # #### if there is any repeated column name,
        # ## cut those rows and concatenate them to the corresponding column
        # if replication:
        #     df12 = df1.iloc[:, 0:yy2]
        #     df3 = df1.iloc[:, yy2:len(yy) + 1]
        #     #print(df12)
        #     frames = [df12, df3]
        #     df4 = pd.concat(frames)
        #
        # # df4
        #
        # ### reset the index in the resulting merged_table
        # ## df4.reset_index()
        # df4 = df4.reset_index(drop=True)
        # ## test = test.reset_index(drop=True)
        # # df4
        # #....................................... the code in this part checks for repetitions in the columns (up)

        ### I already checked the repetition in another code, so I commented above and copy df1 to df4
        df4 = df1.copy()

        ############copy df_test1
        df_test2 = df_test1.copy()


        # df4=df4.rename(columns = {df4.columns[0]:'Drug'})
        # df4=df4.rename(columns = {df4.columns[1]:'sensitivity'})
        # df_test2=df_test2.rename(columns = {df_test2.columns[0]:'Drug'})
        # df_test2=df_test2.rename(columns = {df_test2.columns[1]:'sensitivity'})

        import numpy as np

        # df_test2['sensitivity_update']=False
        # iterating over rows using iterrows() function
        # df_result = pd.DataFrame()
        index_add = 0
        row_num = df_test2.shape[0]

        df_result = df_test2.copy()
        df_result['sensitivity_update'] = False
        index = set()

        for i1, j1 in df_test2.iterrows():
            for i2, j2 in df4.iterrows():

                if j1['Drug'] == j2['Drug']:
                    #print("j1['Drug']", j1['Drug'])
                    # test_cndtn = ((j1['test'] is np.nan and j2['test'] is np.nan ) or j1['test']==j2['test'])
                    # type_cndtn = ((j1['Type'] is np.nan and j2['Type'] is np.nan) or j1['Type'] == j2['Type'])
                    # note that np.nan is np.nan is false; i had a lot of issues with that. so you need to use np.isnan() function
                    # for checking if the cell is nan or not
                    # np.nan is np.nan -->  false
                    # np.isnan(np.nan) -->  true
                    # np.isnan() dose not work for str type
                    # if (type(j1['Type']) not in [np.float64, float]):
                    #     if (type(j2['Type']) not in [np.float64, float]):
                    #         type_cndtn = (j1['Type'] == j2['Type'])
                    #     else:
                    #         type_cndtn = False
                    # elif (type(j2['Type']) in [np.float64, float]):
                    #     type_cndtn = (np.isnan(j1['Type']) and np.isnan(j2['Type']))
                    # else:
                    #     type_cndtn = False


                    # try:
                    #     if np.isnan(type(j1['Type'])) and np.isnan(type(j2['Type'])):
                    #         type_cndtn = True
                    #     elif (np.isnan(type(j1['Type']))) ^ (np.isnan(type(j2['Type']))):
                    #         type_cndtn = False
                    #     else:
                    #         type_cndtn = (j1['Type'] == j2['Type'])
                    # except:
                    #     type_cndtn = (j1['Type'] == j2['Type'])


                    try:
                        if np.isnan(j1['Type']):
                            j1_nan = True
                    except:
                        j1_nan = False

                    try:
                        if np.isnan(j2['Type']):
                            j2_nan = True
                    except:
                        j2_nan = False

                    if not (j1_nan):
                        if not (j2_nan):
                            type_cndtn = (j1['Type'] == j2['Type'])
                        else:
                            type_cndtn = False
                    elif (j2_nan):
                        type_cndtn = True
                    else:
                        type_cndtn = False

                    #print("type_cndtn1", type_cndtn)
                    if type_cndtn:
                        if (j1['Matrix'] == j2['Matrix']) and (j1['Test'] == j2['Test']):
                            #print('if')
                            #print('i1',i1)
                            #print("j1['Drug']", j1['Drug'])
                            #print("(j1['Matrix'] == j2['Matrix'])", (j1['Matrix'] == j2['Matrix']))
                            #print("(j1['Test'] == j2['Test'])", (j1['Test'] == j2['Test']))
                            #### note that if matrix or type of one table is nan is may give the wrong answer so it needs changing
                            #### same as the one for type when it is nan
                            # print('if')
                            # print("j1['Drug']", j1['Drug'])
                            if (j1['Sensitivity'] != j2['Sensitivity']):
                                # print("j1['Drug']", j1['Drug'])
                                df_result.loc[i1, 'Sensitivity'] = df4.loc[i2, 'Sensitivity']
                                df_result.loc[i1, 'sensitivity_update'] = True
                                df_result.loc[i1, 'URL/ Contact email'] = df4.loc[i2, 'URL/ Contact email']
                            index.add(i2)

        # print('i2',i2)

        for i2, j2 in df4.iterrows():
            if i2 not in index:
                new_index = row_num + index_add
                df_result.loc[new_index, 'Drug'] = df4.loc[i2, 'Drug']
                df_result.loc[new_index, 'Sensitivity'] = df4.loc[i2, 'Sensitivity']
                df_result.loc[new_index, 'Matrix'] = df4.loc[i2, 'Matrix']
                df_result.loc[new_index, 'Test'] = df4.loc[i2, 'Test']
                df_result.loc[new_index, 'Type'] = df4.loc[i2, 'Type']
                df_result.loc[new_index, 'sensitivity_update'] = True
                df_result.loc[new_index, 'URL/ Contact email'] = df4.loc[i2, 'URL/ Contact email']
                index_add = index_add + 1



        def hightlight_cell(row):
            ret = ["" for _ in row.index]
            if row.sensitivity_update == True:
                ret[row.index.get_loc("Sensitivity")] = "background-color: yellow"
            return ret

        # df_result.style.apply(hightlight_cell, axis=1).to_excel('styled.xlsx', engine='openpyxl')
        df_result.style.apply(hightlight_cell, axis=1).to_excel(file_directory_main_file, engine='openpyxl')



import difflib
import pandas as pd

###### function ________________________________________________

'''
fields = {'Drug':{'DRUG','ACTIVEINGREDIENT','RESIDUESDETECTED', 'ANTIMICROBIALDRUG', 'ANTIMICROBIALAGENT','BETALACTAMDRUG', 'BETALACTAMS','TETRACYCLINES', 'QUINOLONEDRUG'}
          , 'Test':{'TEST','TEST NAME'}
          , 'Sensitivity':{'CONCENTRATIONFORPOSITIVEPPB','CHARMSL','SENSITIVITY','TESTSENSITIVITY', 'CONCENTRATION', 'POSITIVECONCENTRATION', 'DETECTIONLEVEL', 'DETECTIONRANGE'}
          , 'Matrix': {'MATRIX','SPECIMEN'}
          ,'Type': {'TYPE'}
          , 'MRL': {'MRL', 'CODEX','TECHNICALREGULATION','MRPL','FEDERATION','REGULATION','IMPORTREGULATION'}
          ,'Tolerance':{'ACTIONLEVEL','SAFELEVEL','TOLERANCE'}}
'''
def change_column_names(fields, df21):
    df12 = df21.copy()

    df12_col = df12.columns
    print('df12_col',df12_col)
    print('lf',list(df12_col))

    col = dict()
    for c in list(df12_col):
        found = False
        for k, v in fields.items():
            for tt in v:
                #tt1 = ''.join(e for e in tt if e.isalnum()).upper()
                # if tt1 in c:
                c1 = ''.join(e for e in c if e.isalnum()).upper()
                if tt in c1:
                    col[c] = k
                    found = True
                    break
            if found:
                break

    df12.rename(columns=col, inplace=True)
    # df11.rename(col, inplace = True)
    df12.rename(col)

    return df12


# df40 = change_column_names(fields, df33)


###### function ________________________________________________
def check_for_column_repetition(df20):
    df11 = df20.copy()
    y = df11.columns
    yy = [''.join(e for e in i if e.isalnum()) for i in y]
    replication = True
    yy2 = int(len(yy) / 2)
    if (len(yy) % 2 == 0):
        # yy2 = int(len(yy) / 2)
        for i in range(yy2):
            if int(difflib.SequenceMatcher(None, yy[i], yy[i + yy2]).ratio() * 100) < 85:
                replication = False
    else:
        replication = False

    ## for copying df, you need to use one of the following commands:
    ## (since df uses call_by_reference not call_by_value)
    # from copy import deepcopy
    # df2 = deepcopy(df11)
    # or
    # df2 = df11.copy()

    col = dict()
    df11_col = df11.columns
    if replication:
        for i in range(yy2):
            #         df11.rename(columns[df11_col[i+yy2]]=df11_col[i], inplace = True)
            col[df11_col[i + yy2]] = df11_col[i]

    df11.rename(columns=col, inplace=True)
    # df11.rename(col, inplace = True)
    df11.rename(col)

    #### if there is any repeated column name,
    ## cut those rows and concatenate them to the corresponding column
    if replication:
        df112 = df11.iloc[:, 0:yy2]
        df3 = df11.iloc[:, yy2:len(yy) + 1]  #### ********* recheck:   I think it should be from yy2+1:len(yy)+1
        #print(df112)
        frames = [df112, df3]
        df4 = pd.concat(frames)
        df4 = df4.reset_index(drop=True)

    # df4

    ### reset the index in the resulting merged_table
    ## df4.reset_index()
    # df4 = df4.reset_index(drop=True)
    if not replication:
        df4=df11.copy()
    ## test = test.reset_index(drop=True)
    # df4
    #....................................... the code in this part checks for repetitions in the columns (up)

    return df4
    # ############copy df_test1
    # df_test2 = df_test1.copy()
    # #fields = {'Drug', 'Test', 'Sensitivity', 'Matrix')
    # # if str(j).upper() in str(i).upper():
    #
    # for i in range(len(df4.columns)):
    #     for k, v in fields.items():
    #         for j in v:
    #             # print('k',k)
    #             column_name_isalumn = ''.join(e for e in df4.columns[i] if e.isalnum())
    #             if j in column_name_isalumn.upper():
    #                 df4 = df4.rename(columns={df4.columns[i]: k})
    #                 continue
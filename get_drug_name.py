import pandas as pd
import numpy as np


## read the excel file containing the drug name and their other names
## I got this list based on the tests in "Rapid tests_Downloaded_2020_Jan_14_1.excel" file and also based on the pdfs Tara gave me

def get_drug_name_list():
    df = pd.read_excel('antimicrobial_drug_and_classes_main_1.xlsx', None)

    a=df.keys()
    b=list(a)
    y = df[b[0]].columns
    df1=df[b[0]]


    ## removing the comment columns
    df2 = df1.drop(columns=['class','sub_class','comments'])
    # yourdf.drop(['columnheading1', 'columnheading2'], axis=1, inplace=True)

    df3 = df2.set_index('drug').transpose()
    temp = df3.to_dict('list')
    ### if you wanted the results as a set of lists
    ### res = {k:[elem for elem in v if elem is not np.nan] for k,v in temp.items()}
    drug_names = {k:{elem for elem in v if elem is not np.nan} for k,v in temp.items()}
    return drug_names
## it is a set of set: the drug name and its other names in a list in front of it
'''
{'Benzylpenicillin': set(),
 'Benethamine penicillin': set(),
 'Benzylpenicillin procaine': {'Benzathine penicillin'},
 'Penethamate': {'hydroiodide'},
 'Mecillinam ': set(),
 'Ampicillin': set(),
 'Ampicillin-sulbactam': {'Ampicillin + Sulbactam',
  'Ampicillin and Sulbactam'},
 'Amoxicillin': set(),
 'Amoxicillin-clavulanic acid': {'Amoxicillin + Clavulanic Acid',
  'Amoxicillin and Clavulanic Acid'},
 'Aspoxicillin ': set(),
 'Hetacillin': set(),
 'Piperacillin': {' '},
 'Piperacillin-tazobactam': {'Piperacillin + Tazobactam'},
 'Ticarcillin': set(),
 'Ticarcillin-clavulanic acid': set(),
'''
### main_______________________________
### if you want to run just this file, uncomment the below
#drug_names = get_drug_name_list()
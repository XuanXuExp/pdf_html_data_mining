import pandas as pd
import numpy as np


## read the excel file containing the test name and their other names/abbreviations
## I got this list based on the tests in "Rapid tests_Downloaded_2020_Jan_14_1.excel" file and searching these names
## in google and find their abbreviations
## also getting some test name from https://www.charm.com/products/test-and-kits/antibiotic-tests/ website
## (the code is in get_test_names.py if needed)
def get_test_name_list():
    df = pd.read_excel('test_name_file.xlsx', None)

    a=df.keys()
    b=list(a)
    y = df[b[0]].columns
    df1=df[b[0]]


    ## removing the comment columns
    df2 = df1.drop(columns=['comment'])

    df3 = df2.set_index('Test').transpose()
    temp = df3.to_dict('list')
    ### if you wanted the results as a set of lists
    ### res = {k:[elem for elem in v if elem is not np.nan] for k,v in temp.items()}
    test_names = {k:{elem for elem in v if elem is not np.nan} for k,v in temp.items()}
    return test_names
## it is a set of set: the test name and its other names/abbreviations in a list in front of it
'''{'2,4-D RaPID Assay': set(),
 'Atrazine RaPID Assay': set(),
 'Benomyl RaPID Assay': set(),
 'Beta Star 4D': {'Beta Star 4 D'},
 'BetaStar 4D Beta-Lactam, Tetracycline, Streptomycin, Chloramphenicol': set(),
 'BetaStar Advanced for Beta-Lactams': set(),
 'BetaStar Advanced for Tetracycline': set(),
 'BetaStar S for Sulfonamides': set(),
 'BetaStar for Quinolone': set(),
 'Charm 3 SL3 Beta-Lactam': {'Charm 3 SL3'},
 'Charm B. stearothermophilus Tablet Disc Assay': {'BSDA','Charm Bacillus stearothermophilus Disc Assay'},
 ....} '''
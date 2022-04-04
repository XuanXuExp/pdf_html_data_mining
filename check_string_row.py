###### function ________________________________________________
def check_string_row(df100):
    col = df100.columns
    row_num = df100.shape[0]
    index_to_remove =[]
    for rn in row_num:
        for col_name in col:
            s = df100.iloc[rn, col_name]
            extracted_num_cell = [int(s) for s in str.split() if s.isdigit()]
            if len(extracted_num_cell):
                break
        if not len(extracted_num_cell):
            index_to_remove.append(rn)

    if len(index_to_remove):
        df101 = df100.drop(df100.index[index_to_remove])
    else:
        df101 = df100.copy()

    return df101






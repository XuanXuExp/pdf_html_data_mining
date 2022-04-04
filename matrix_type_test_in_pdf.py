import PyPDF2
from PyPDF2 import PdfFileReader



def get_matrix_type_test_in_pdf(paper_path, test_names, matrix_list, type_list):
    '''
    it searches for the matrix, type, and test in the given pdf
    :param test_names: list of test names
    :param matrix_list:
    :param type_list:
    :return: a dictionary MatrixTestType which has the name of Matrix, Test and type as the keys
            # and a list contanning their values (one or no elements); for example:
            # {'Matrix': ['Milk'], 'Test': ['Charm Quad'], 'Type': []}
    '''

    # read the pdf in the directory
    pdf = PdfFileReader(open(paper_path , 'rb'))
    PN = pdf.getNumPages()

    # print('PN', PN)
    matrix_in_pdf = False
    type_in_pdf = False
    test_in_pdf = False

    MatrixTestType = dict()
    MatrixTestType['Matrix']=[]
    MatrixTestType['Test'] = []
    MatrixTestType['Type'] =[]

    for i4 in range(PN):

        content = pdf.getPage(i4).extractText()  ### note that here the pages will be from 0 to PN-1 (first page is 0)
        content1 = ''.join(e for e in content if e.isalnum()).upper()

        if not matrix_in_pdf:
            for m in matrix_list:
                m1 = ''.join(e for e in m if e.isalnum()).upper()
                if m1 in content1:
                    matrix_in_pdf = True
                    MatrixTestType['Matrix'].append(m)
                    break

        if not type_in_pdf:
            for t in type_list:
                t1 = ''.join(e for e in t if e.isalnum()).upper()
                if t1 in content1:
                    type_in_pdf = True
                    MatrixTestType['Type'].append(t)
                    break

        if not test_in_pdf:
            for k, v in test_names.items():
                if test_in_pdf:
                    break
                new_list = []
                # print('k', k)
                # print('v', v)
                new_list.extend(v)
                new_list.append(k)

                for tt in new_list:
                    tt1 = ''.join(e for e in tt if e.isalnum()).upper()
                    if tt1 in content1:
                        test_in_pdf = True
                        MatrixTestType['Test'].append(k)
                        break
    return MatrixTestType

### main__________________________________

### uncomment the below if you want to use only this .py file
#
# from get_test_name_list import get_test_name_list  ### send
# test_names = get_test_name_list()
# matrix_list =['Milk','Honey','Serum','Tissue','Kidney','Dairy','Aquaculture','Urine']
# type_list =['Sequential', 'Competitive','Quantitative']
#
# file_directory = "D:/_GRA projects/Epapers1"  ### the path to the desired papers
# file = '2018_06_99_MRK-852.pdf'               ### the name of the desired paper
# paper_path = file_directory + "/" + file      ### the desired paper path
#
#
# MatrixTestType = get_matrix_type_test_in_pdf(paper_path, test_names, matrix_list, type_list)
#
#
# print ('MatrixTestType', MatrixTestType)
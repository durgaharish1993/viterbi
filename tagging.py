#from viterbi import Viterbi
from collections import defaultdict


def parse_bigram_wfsa(list_a):
    data_dict = defaultdict(lambda : defaultdict(float))
    for i in range(len(list_a))
        temp_str = list_a[i]







#jhggj
def parse_flower_wfst(list_a):
    data_dict = defaultdict(lambda : defaultdict(float))
    for i in range(len(list_a)):
        temp_str=list_a[i]
        if ')' in temp_str:
            temp_str=temp_str.split(')')[0]
            temp_str=temp_str.split('(')[-1]
            temp_list = temp_str.split(' ')
            data_dict[temp_list[1]][temp_list[2]] = float(temp_list[3])

    return data_dict









def read_file(file_name):
    data =[]
    fp=open(file_name)
    for line in fp.readlines():
        if line!='\n':
            data+=[line.split('\n')[0]]

    return data









if __name__ == '__main__':
    file_name = 'lexicon.wfst'
    file_name1 = 'bigram.wfsa'
    ########
    data=read_file(file_name)
    w_t_data=parse_flower_wfst(data)
    #####
    data = read_file(file_name1)
    essential_mapping = {'s1':'<BOS>','s2':'pro','s3':'det','s4':'n',''}
    print(data)




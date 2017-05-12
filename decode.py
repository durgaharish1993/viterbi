from collections import defaultdict
from viterbi import Viterbi
import sys
import time
import fileinput




def read_file(file_name):
    data =[]
    fp=open(file_name)
    for line in fp.readlines():
        if line!='\n':
            data+=[line.split('\n')[0]]

    return data


def get_prob(data,Noise=False):

    data_dict = defaultdict(lambda :defaultdict(float))

    if Noise:
        input_unique_words = set()
        output_unique_words = set()
    else:
        input_unique_words = set()
        output_unique_words =[ None ]

    for i in range(len(data)):
        if Noise:
            temp_list = data[i].split(':')
            input = temp_list[0]
            output = temp_list[1].split('#')[0].strip()
            prob = float(temp_list[1].split('#')[-1])
            input = input.strip()

            data_dict[input][output] = prob


            output_unique_words.add(output)
            for temp in input.split(' ')[:-1]:
                input_unique_words.add(temp)
        else:

            temp_list = data[i].split(':')
            input = temp_list[0]
            output = temp_list[1].split('#')[0].strip()
            prob = float(temp_list[1].split('#')[-1])
            input_tuple = tuple(input.split(' ')[:-1])
            data_dict[input_tuple][output] = prob

            input_unique_words.add(output)
            for temp in input.split(' ')[:-1]:
                input_unique_words.add(temp)




    return data_dict,[list(input_unique_words),list(output_unique_words)]



def forward_new(p_noise_channel,p_prior,u_prior,u_i_noise,u_o_noise,letter_list,start_tag,end_tag,markov_order):
    '''
    best : stores the best probability till now.  it takes length of the sentence completed, and for a (index,w1,w2)
    :return:
    '''
    ##### Intialization for the probabilities
    s1 = time.clock()
    #Stores the prob.
    best = defaultdict(float)
    #start_gram = tuple([start_tag for i in range(markov_order)])
    #print(start_gram)
    #Initialization for <s> and <s> tag
    best[(-1,'<s>','<s>')] = 1.0
    #######Intialization for the best path
    best_path = defaultdict(lambda : defaultdict(str))
    ######


    def find_best(n, best, u, v):
        if n==-1 and (u,v)!=(start_tag,start_tag):
            return best[(n,u,v)]

        if (n,u,v) in best:
            return best[(n,u,v)]


        x_list = []
        if n >= 2:
            x_list += [(3,letter_list[n - 2] + ' ' + letter_list[n - 1] + ' ' + letter_list[n])]
            x_list += [(2,letter_list[n - 1] + ' ' + letter_list[n])]
            x_list += [(1, letter_list[n])]
        if n == 1:
            x_list += [(2,letter_list[n - 1] + ' ' + letter_list[n])]
            x_list += [(1, letter_list[n])]
        if n == 0:
            x_list += [(1, letter_list[n])]



        max_str = None
        max_num = float('-inf')
        for i in range(len(u_prior)):
            w = u_prior[i]
            for (n1,x) in x_list:

                temp_num = find_best(n - n1, best, w, u) * p_prior[(w,u)][v] * p_noise_channel[v][x]
                if temp_num > max_num:
                    max_num = temp_num
                    max_str = w
                    num = n-n1

        best[(n,u, v)] = max_num
        best_path[n][(u,v)] = (max_str,num)

        return best[(n,u,v)]

    ############################


    max_num = float('-inf')
    max_str = None
    n=len(letter_list)
    temp_best=defaultdict(float)
    for i in range(len(u_prior)):
        for j in range(len(u_prior)):
            u = u_prior[i]
            v = u_prior[j]

            if (u,v) not in temp_best:
                temp_best[(u,v)] = find_best(n-1, best, u, v) * p_prior[(u,v)][end_tag]


            if temp_best[(u,v)]> max_num:
                max_num = temp_best[(u,v)]
                max_str = (u,v)
    best_path[len(letter_list)][max_str] = ('</s>',1)
    s2 = time.clock()
    print('Forward Tracking',s2-s1)
    back_result = backward_new(best_path,letter_list)
    print('Back tracking',time.clock()-s2)
    return max_num,back_result






def backward_new(best_path,letter_list):
    leng=len(letter_list)
    max_str = []
    while True:
        if leng==len(letter_list):
            key=list(best_path[leng].keys())[0]
            max_str+=[key[1],key[0]]
            leng-=1
        else:

            letter = best_path[leng][key][0]
            leng =best_path[leng][key][1]
            if letter == '<s>':
                break
            max_str+=[letter]
            key = (letter,key[0])





    return ' '.join(max_str[::-1])








#def __init__(self,p_noise_channel,p_prior,u_prior,u_i_noise,u_o_noise,word_list, start_tag='<s>', end_tag='<\s>',markov_order=2):
if __name__=='__main__':

    arguments = sys.argv




    file_name = 'epron.probs'
    file_name1 = 'epron-jpron.probs'
    start_tag = '<s>'
    end_tag = '</s>'
    markov_order = 2
    letter_list = 'N A I T O'.split()
    #sys.argv


    s1 = time.clock()
    ######
    epron_data = read_file(file_name)
    p_prior,unique_words = get_prob(epron_data)

    if unique_words[1]==[None]:
        u_prior = unique_words[0]

    data  = read_file(file_name1)
    p_noise_channel, unique_words = get_prob(data,Noise=True)
    u_i_noise,u_o_noise=unique_words[0], unique_words[1]

    print('Time to read the files :',time.clock()-s1)





    for input in fileinput.input():
        print('#####')
        letter_list=input.split('\n')[0].split()
        #v=Viterbi(p_noise_channel,p_prior,u_prior,u_i_noise,u_o_noise,letter_list,start_tag,end_tag,markov_order)
        s1 = time.clock()
        #print(p_noise_channel)
        a=forward_new(p_noise_channel,p_prior,u_prior,u_i_noise,u_o_noise,letter_list,start_tag,end_tag,markov_order)
        print(a)
        print('Running the algorithms:',time.clock()-s1)




































































# def forward_new_v1(p_noise_channel, p_prior, u_prior, u_i_noise, u_o_noise, letter_list, start_tag, end_tag,
#                    markov_order):
#     '''
#     best : stores the best probability till now.  it takes length of the sentence completed, and for a (index,w1,w2)
#     :return:
#     '''
#     ##### Intialization for the probabilities
#     s1 = time.clock()
#     # Stores the prob.
#     best = defaultdict(float)
#     # start_gram = tuple([start_tag for i in range(markov_order)])
#     # print(start_gram)
#     # Initialization for <s> and <s> tag
#     best[(-1, '<s>', '<s>')] = 1.0
#     #######Intialization for the best path
#     best_path = defaultdict(lambda: defaultdict(str))
#
#     ######
#
#
#     def find_best(n, best, u, v):
#         if n == -1 and (u, v) != (start_tag, start_tag):
#             return best[(n, u, v)]
#
#         if (n, u, v) in best:
#             return best[(n, u, v)]
#
#         x_list = []
#         if n >= 2:
#             x_list += [(3, letter_list[n - 2] + ' ' + letter_list[n - 1] + ' ' + letter_list[n])]
#             x_list += [(2, letter_list[n - 1] + ' ' + letter_list[n])]
#             x_list += [(1, letter_list[n])]
#         if n == 1:
#             x_list += [(2, letter_list[n - 1] + ' ' + letter_list[n])]
#             x_list += [(1, letter_list[n])]
#         if n == 0:
#             x_list += [(1, letter_list[n])]
#
#         max_str = None
#         max_num = float('-inf')
#         for i in range(len(u_prior)):
#             w = u_prior[i]
#             for (n1, x) in x_list:
#
#                 temp_num = find_best(n - n1, best, w, u) * p_prior[(w, u, v)] * p_noise_channel[(v, x)]
#                 if temp_num > max_num:
#                     max_num = temp_num
#                     max_str = w
#                     num = n - n1
#
#         best[(n, u, v)] = max_num
#         best_path[n][(u, v)] = (max_str, num)
#
#         return best[(n, u, v)]
#
#     ############################
#
#
#     max_num = float('-inf')
#     max_str = None
#     n = len(letter_list)
#     for i in range(len(u_prior)):
#         for j in range(len(u_prior)):
#             u = u_prior[i]
#             v = u_prior[j]
#
#             temp_num1 = find_best(n - 1, best, u, v)
#             temp_num2 = p_prior[(u, v, end_tag)]
#
#             temp_num = temp_num1 * temp_num2
#             if temp_num > max_num:
#                 max_num = temp_num
#                 max_str = (u, v)
#     best_path[len(letter_list)][max_str] = ('</s>', 1)
#     s2 = time.clock()
#     print('Forward Tracking', s2 - s1)
#     back_result = backward_new(best_path, letter_list)
#     print('Back tracking', time.clock() - s2)
#     return max_num, back_result





# def get_prob_v1(data,Noise=False):
#
#     data_dict = defaultdict(float)
#
#     if Noise:
#         input_unique_words = set()
#         output_unique_words = set()
#     else:
#         input_unique_words = set()
#         output_unique_words =[ None ]
#
#     for i in range(len(data)):
#         if Noise:
#             temp_list = data[i].split(':')
#             input = temp_list[0]
#             output = temp_list[1].split('#')[0].strip()
#             prob = float(temp_list[1].split('#')[-1])
#             input = input.strip()
#
#             data_dict[(input,output)] = prob
#
#
#             output_unique_words.add(output)
#             for temp in input.split(' ')[:-1]:
#                 input_unique_words.add(temp)
#         else:
#
#             temp_list = data[i].split(':')
#             input = temp_list[0]
#             output = temp_list[1].split('#')[0].strip()
#             prob = float(temp_list[1].split('#')[-1])
#             input_tuple = tuple(input.split(' ')[:-1]+[output])
#             data_dict[input_tuple] = prob
#
#             input_unique_words.add(output)
#             for temp in input.split(' ')[:-1]:
#                 input_unique_words.add(temp)
#
#
#
#
#     return data_dict,[list(input_unique_words),list(output_unique_words)]


from collections import defaultdict
from viterbi import Viterbi
import sys
import time
import fileinput
import heapq

import numpy as np

def read_file(file_name):
    data =[]
    fp=open(file_name)
    for line in fp.readlines():
        if line!='\n':
            data+=[line.split('\n')[0]]

    return data


def get_prob(data,Noise=False,three=False):

    if three:
        data_dict = defaultdict(lambda : defaultdict(lambda : defaultdict(float)))
    else:
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
            u=input_tuple[0]
            v=input_tuple[1]

            if three:
                data_dict[output][v][u] = prob #k,k-1,k-2
            else:
                data_dict[input_tuple][output] = prob

            input_unique_words.add(output)
            for temp in input.split(' ')[:-1]:
                input_unique_words.add(temp)




    return data_dict,[list(input_unique_words),list(output_unique_words)]



def farword_bottom_top(p_noise_channel,p_prior,u_prior,u_i_noise,u_o_noise,letter_list,start_tag,end_tag,markov_order,letter):
    s1 = time.clock()
    best = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))
    best[-1]['<s>']['<s>'] = 1.0
    x_dict = defaultdict(list)



    for i in range(len(letter_list)+1):
        x_dict ={}
        for v in p_prior:
            for u in p_prior[v]:
                if i not in x_dict and i!=len(letter_list):

                    if i >= 2:
                        x_dict[i] = [(3, letter_list[i - 2] + ' ' + letter_list[i - 1] + ' ' + letter_list[i]),
                                     (2, letter_list[i - 1] + ' ' + letter_list[i]), (1, letter_list[i])]
                    if i == 1:
                        x_dict[i] = [(2, letter_list[i- 1] + ' ' + letter_list[i]), (1, letter_list[i])]
                    if i == 0:
                        x_dict[i] = [(1, letter_list[i])]
                    x_list = x_dict[i]
                else:
                    if i!=len(letter_list):
                        x_list = x_dict[i]

                if i == len(letter_list):

                    best[i][u][v] = max(best[i-1][t][u]*p_prior[v][u][t] for t in p_prior[v][u])
                else:
                    best[i][u][v]=max(best[i - n1][t][u] * p_prior[v][u][t] * p_noise_channel[v][x]
                for t in p_prior[v][u] for (n1,x) in x_list)

    max_val = max([best[i][v]['</s>'] for v in p_prior['</s>']])
    s2 = time.clock()
    print 'Forward Tracking', s2 - s1
    # back_result = backward_new(best_path,letter_list)
    print 'Back tracking', time.clock() - s2
    # , back_result
    return max_val





if __name__=='__main__':

    arguments = sys.argv




    file_name = 'epron.probs'
    file_name1 = 'epron-jpron.probs'
    start_tag = '<s>'
    end_tag = '</s>'
    markov_order = 2
    letter = 'P I A N O'
    letter_list = letter.split()
    #sys.argv


    s1 = time.clock()
    ######
    epron_data = read_file(file_name)
    p_prior,unique_words = get_prob(epron_data,three=True)

    if unique_words[1]==[None]:
        u_prior = unique_words[0]

    data  = read_file(file_name1)
    p_noise_channel, unique_words = get_prob(data,Noise=True)
    u_i_noise,u_o_noise=unique_words[0], unique_words[1]

    print 'Time to read the files :',time.clock()-s1
    #
    a = farword_bottom_top(p_noise_channel, p_prior, u_prior, u_i_noise, u_o_noise, letter_list, start_tag, end_tag,
                           markov_order, letter)

    print a
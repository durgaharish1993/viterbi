#! /usr/bin/python
import fileinput
from collections import defaultdict
import time
import math
import heapq
import sys
def forward_bottom_top(transition,emission,word_list):
    best = defaultdict(lambda :defaultdict(lambda : defaultdict(float)))
    best_path = defaultdict(lambda: defaultdict(lambda: defaultdict(str)))

    best[-1]['<s>']['<s>'] = 1



    for i in range(len(word_list)):
        if i>=2: x_list=[(3,' '.join(word_list[i-2:i+1])),(2,' '.join(word_list[i-1:i+1])),(1,' '.join(word_list[i:i+1]))];
        if i==1: x_list=[(2,' '.join(word_list[i-1:i+1])),(1,' '.join(word_list[i:i+1]))]
        if i==0: x_list=[(1,' '.join(word_list[i:i+1]))]
        v_list=[]
        for (_, x) in x_list: v_list+=(list(emission[x].keys()))
        print(v_list)
        for v in v_list:
            for u in transition[v]:
                max_val = 0;max_n1 = None;max_w = None
                for (n1, x1) in x_list:
                    for w in transition[v][u]:
                        #y1 = (n1, w, best[i - n1][u][w] * transition[v][u][w] * emission[x1][v])
                        temp_val = best[i - n1][u][w] * transition[v][u][w] * emission[x1][v]
                        if temp_val> max_val:
                            max_val = temp_val
                            max_n1= n1
                            max_w = w

                best_path[i][v][u] = (max_n1,max_w,max_val)
                best[i][v][u] = max_val
                '''
                This was previous attempt.
                '''
                #best_path[i][v][u],best[i][v][u]=max( (((n1,w,best[i-n1][u][w]*transition[v][u][w] * emission[x1][v]),best[i-n1][u][w]*transition[v][u][w] * emission[x1][v]) for w in transition[v][u] for(n1,x1) in x_list),key=lambda tup:tup[1])

    len_word = len(word_list)-1
    max_val = max(best[len_word][word_list[len_word]][u] for u in best[len_word][word_list[len_word]])
    (last_str,(_,_,max_val)) = max(((u,best_path[len_word][word_list[len_word]][u]) for u in best_path[len_word][word_list[len_word]]), key= lambda tup:tup[1][2])
    #print('I am here')
    max_path = back_track(best_path,last_str,word_list[len_word],len_word,n=0)
    return max_val,max_path





def back_track(best_path,u,v,leng,n):
    max_list = []

    while True:
        n1,u1,_=best_path[leng][v][u]

        leng -=n1
        v=u
        u = u1

        if v=='<s>':
            break
        max_list += [v]
    return ' '.join(max_list[::-1])







if __name__=='__main__':

    s1=time.clock()
    argu=sys.argv
    if len(argu)>1:
        epron_file = argu[1]
        epron_jpron_file = argu[2]
    else:
        epron_file = 'epron.probs'
        epron_jpron_file= 'epron-jpron.probs'

    #print(argu[-1],epron_file,epron_jpron_file)


    file_name =epron_file
    fp = open(file_name)
    transition = defaultdict(lambda : defaultdict(lambda :defaultdict(float)))
    for line in fp.readlines():
        input = line[:-1].split(':')
        output = input[1].split('#')[0].strip()
        prob = float(input[1].split('#')[1].strip())
        k_2, k_1 =  input[0].strip().split(' ')

        transition[output][k_1][k_2] = prob
    ###########################################################################

    file_name = epron_jpron_file
    fp = open(file_name)
    emission = defaultdict(lambda : defaultdict(float))
    for line in fp.readlines():
        input = line[:-1].split(':')
        e = input[0].strip()
        o = input[1].split('#')
        j,p = o[0].strip(),float(o[1].strip())
        emission[j][e] = p
    emission['</s>']['</s>'] =1

    #letter_list = 'H E E S U B U KK U R I S A A TCH I S A I E N T I S U T O'.split()+['</s>']
    #letter_list = 'N A I T O'.split()+['</s>']
    #letter_list = 'P I A N O'.split() + ['</s>']
    #letter_list = 'B I D E O T E E P U'.split() + ['</s>']
    #s2 = time.clock()
    #print('Time take to read files',s2-s1)
    #a1=forward_bottom_top(transition,emission,letter_list)
    #a2=forward_bottom_top(transition,emission,letter_list)

    #print(a2[1], ' # ', a2[0])

    # s3 = time.clock()
    # print('Time taken to run the algorithm',s3-s2)
    # print('TIME TAKEN TO RUN :',s3-s1)
    #
    #
    #

    for input in sys.stdin:
        letter = input.split('\n')[0]
        letter_list=letter.split()+['</s>']
        #v=Viterbi(p_noise_channel,p_prior,u_prior,u_i_noise,u_o_noise,letter_list,start_tag,end_tag,markov_order)
        #s1 = time.clock()
        #print(p_noise_channel)
        #print(letter_list)
        a=forward_bottom_top(transition,emission,letter_list)
        print(str(a[1])+ ' # '+ str('%.6e')%a[0])

    s3=time.clock()
    print('Time taken:',s3-s1)
#! /usr/bin/python
import fileinput
from collections import defaultdict
import time
import math
import heapq
import sys
def forward_bottom_top_kbest_v2(transition,emission,letter_list,k_best_orginal=1):

    k_best=k_best_orginal*4
    best = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda : [0]*k_best)))
    best_path = defaultdict(lambda : defaultdict(lambda : defaultdict(lambda : [None]*k_best)))
    temp_list =[0] * (k_best - 1)
    best[-1]['<s>']['<s>'] = [1]+temp_list

    '''
    This function takes best[.][.]=[list-->length k_best],i (the previous pointer), u(k-1),v(k),p_prior is the transition probability matrix
    '''
    for i in range(len(letter_list)):
        if i>=2: x_list=[(3,' '.join(letter_list[i-2:i+1])),(2,' '.join(letter_list[i-1:i+1])),(1,' '.join(letter_list[i:i+1]))];
        if i==1: x_list=[(2,' '.join(letter_list[i-1:i+1])),(1,' '.join(letter_list[i:i+1]))]
        if i==0: x_list=[(1,' '.join(letter_list[i:i+1]))]
        v_list = []
        for (_, x) in x_list: v_list += (list(emission[x].keys()))
        '''
        '''
        for v in v_list:
            for u in transition[v]:
                temp_arr = []; temp_t_arr = []
                for (n1,x) in x_list:

                    best_copy = defaultdict(lambda : [0]*k_best)
                    for t in best[i-n1][u]:
                        best_copy[t] = best[i-n1][u][t]
                    inital_heap=[]
                    for o in range(k_best):
                        val, t, p,inital_heap = pop_heapq_v2(best_copy, i - n1, u, v, transition,inital_heap)


                        temp_val1 = val * p * emission[x][v]
                        temp_val2 = val
                        temp_arr += [temp_val1]


                        if temp_val1==0:
                            log_temp_val1 = float('-inf')
                        else:
                            log_temp_val1 = math.log(temp_val1)

                        if temp_val2==0:
                            log_temp_val2 = float('-inf')
                        else:
                            log_temp_val2 = math.log(temp_val2)
                        temp_t_arr += [(t,n1, log_temp_val1,u,v,x,log_temp_val2)]



                best[i][v][u]=sorted(temp_arr,reverse=True)
                best_path[i][v][u] = sorted(temp_t_arr,key= lambda tup:tup[2],reverse = True)


    best_copy = defaultdict(list)
    for u,list_a in best_path[len(letter_list)-1]['</s>'].items():
        best_copy[u] = list_a
    #print(best_copy)
    k_best_list = []

    for i in range(k_best_orginal):
        list_a =[best_copy[u][0] for u in best_copy]
        tupe=max(list_a,key= lambda tup:tup[2])
        #print(tupe)
        best_copy[tupe[3]] = best_copy[tupe[3]][1:]
        k_best_list+=[tupe]

    leng_word = len(letter_list)-1
    #result=back_track_kbest(k_best_list, best_path, leng_word)
    result = back_track_k_best(k_best_list, best_path,leng_word)

    return result



def pop_heapq_v2(best_copy, j, u, v, transition,inital_heap=[]):
    if inital_heap==[]:
        for t in transition[v][u]:
            if best_copy[t] != []:
                heapq.heappush(inital_heap,(-best_copy[t][0],t, u))





    if inital_heap==[]:
        return 1,1,None,[]
    else:
        max_num, max_t, u_max=heapq.heappop(inital_heap)
        max_num  = -max_num
        max_p = transition[v][u][max_t]
        best_copy[max_t] = best_copy[max_t][1:]
        if best_copy[max_t]!=[]:
            heapq.heappush(inital_heap,(-best_copy[max_t][0],max_t,u_max))
        return max_num,max_t,max_p,inital_heap

def back_track_k_best(k_best_list, best_path,leng):
    #best_path[5]['</s>']['OW'][0][2] / (transition['</s>']['OW']['N'] * emission['</s>']['</s>'])
    result_list = []
    check_list =[]
    keep_track = defaultdict(lambda : defaultdict(lambda :defaultdict(int)))

    for i in range(len(k_best_list)):
        str_list = []
        temp_len = leng
        t,n,val,u,v,x,nex_val = k_best_list[i]
        temp_val = val
        temp_i = next((j for j,tup in enumerate(best_path[temp_len][v][u])  if tup[2]==temp_val),None)


        while True:

            t,n1,_,u,v,x,next_pointer=best_path[temp_len][v][u][temp_i]

            if u=='<s>':
                break
            str_list+=[u]
            v=u;u=t;temp_len-=n1
            temp_i = next((j for j,tup in enumerate(best_path[temp_len][v][u])  if tup[2]-next_pointer<1e-10),None)
        result_list+=[(' '.join(str_list[::-1]),math.exp(val))]
    return result_list





if __name__=='__main__':
    s1=time.clock()
    argu=sys.argv
    if len(argu)>1:
        epron_file = argu[1]
        epron_jpron_file = argu[2]
        k_best = int(argu[3])
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
    #letter_list = 'T O R A B E R A A Z U TCH E KK U'.split()+['</s>']
    #a1 = forward_bottom_top_kbest_v2(transition, emission, letter_list, 3)
    #print(a1)
    #
    # s2 = time.clock()
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
        a1=forward_bottom_top_kbest_v2(transition,emission,letter_list,k_best)
        for a in a1:
            print(str(a[0])+ ' # '+ str('%.6e')%a[1])
    #     #print('##################')
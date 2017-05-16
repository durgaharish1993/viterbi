import fileinput
from collections import defaultdict
import time

def forward_bottom_top(transition,emission,word_list):
    best = defaultdict(lambda :defaultdict(lambda : defaultdict(float)))

    best[-1]['<s>']['<s>'] = 1



    for i in range(len(word_list)):
        if i>=2: x_list=[(3,' '.join(word_list[i-2:i+1])),(2,' '.join(word_list[i-1:i+1])),(1,' '.join(word_list[i:i+1]))];
        if i==1: x_list=[(2,' '.join(word_list[i-1:i+1])),(1,' '.join(word_list[i:i+1]))]
        if i==0: x_list=[(1,' '.join(word_list[i:i+1]))]
        v_list=[]
        for (_, x) in x_list: v_list+=(list(emission[x].keys()))

        for v in v_list:
            for u in transition[v]:
                best[i][v][u]=max( best[i-n1][u][w]*transition[v][u][w] * emission[x1][v] for w in transition[v][u] for(n1,x1) in x_list)

    return max(best[len(word_list)-1][word_list[len(word_list)-1]][u] for u in best[len(word_list)-1][word_list[len(word_list)-1]])






def forward_bottom_top_kbest(transition,emission,letter_list,k_best_orginal=1):

    s1 = time.clock()

    k_best=k_best_orginal*2
    best = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda : [0]*k_best)))
    best_path = defaultdict(lambda : defaultdict(lambda : defaultdict(lambda : [None]*k_best)))
    temp_list =[0] * (k_best - 1)
    best[-1]['<s>']['<s>'] = [1]+temp_list


    '''
    This function takes best[.][.]=[list-->length k_best],i (the previous pointer), u(k-1),v(k),p_prior is the transition probability matrix
    '''

    for i in range(len(letter_list)):
        x = letter_list[i]
        for v in emission[x]:
            for u in transition[v]:
                if v=='</s>' and u =='N':
                    print('I am hre')
                temp_arr = []
                temp_t_arr = []
                best_copy = defaultdict(lambda : [0]*k_best)
                for t in best[i-1][u]:
                    best_copy[t] = best[i-1][u][t]

                for o in range(k_best):
                    val,t,p=pop_heapq(best_copy, i - 1, u, v,transition)
                    temp_arr+=[ val*p*emission[x][v] ]
                    temp_t_arr+=[(t,val*p*emission[x][v])]
                best[i][v][u] = sorted(temp_arr,reverse=True)
                best_path[i][v][u] = sorted(temp_t_arr,key= lambda tup:tup[1],reverse = True)

    k_best_list = []
    best_copy = defaultdict(lambda : [0]*k_best)
    for u,list_a in best[len(letter_list)-1]['</s>'].items():
        best_copy[u] = list_a

    for i in range(k_best_orginal):
        list_a =[(u,best_copy[u][0]) for u in best_copy]
        u,val=max(list_a,key= lambda tup:tup[1])
        best_copy[u] = best_copy[u][1:]
        k_best_list+=[(u,val)]



    return k_best_list


def pop_heapq(best_copy, j, u, v, transition):
    list_a=[(t, u, best_copy[t][0]) for t in transition[v][u] if best_copy[t]!=[] ]
    if list_a==[]:
        return 1,None,1
    else:
        max_t,u_max,max_num=max(list_a, key=lambda tup:tup[2])
        max_p = transition[v][u][max_t]
        best_copy[max_t] = best_copy[max_t][1:]
        return max_num, max_t, max_p






if __name__=='__main__':
    s1=time.clock()

    file_name ='epron.probs'
    fp = open(file_name)
    transition = defaultdict(lambda : defaultdict(lambda :defaultdict(float)))
    for line in fp.readlines():
        input = line[:-1].split(':')
        output = input[1].split('#')[0].strip()
        prob = float(input[1].split('#')[1].strip())
        k_2, k_1 =  input[0].strip().split(' ')

        transition[output][k_1][k_2] = prob
    ###########################################################################

    file_name = 'epron-jpron.probs'
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
    letter_list = 'P'.split()+['</s>']
    s2 = time.clock()
    print('Time take to read files',s2-s1)
    a1=forward_bottom_top_kbest(transition,emission,letter_list,k_best_orginal=3)
    #a2=forward_bottom_top(transition,emission,letter_list[3:])

    print(a1)






























































    # for input in fileinput.input():
    #     print('#####')
    #     letter = input.split('\n')[0]
    #     letter_list=letter.split()+['</s>']
    #     #v=Viterbi(p_noise_channel,p_prior,u_prior,u_i_noise,u_o_noise,letter_list,start_tag,end_tag,markov_order)
    #     #s1 = time.clock()
    #     #print(p_noise_channel)
    #     a=forward_bottom_top(transition,emission,letter_list)
    #     print(a)


    s3 = time.clock()
    print('Time taken to run the algorithm',s3-s2)
    print('TIME TAKEN TO RUN :',s3-s1)



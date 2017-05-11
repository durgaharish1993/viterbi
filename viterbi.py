
from collections import defaultdict

class Viterbi(object):

    def __init__(self,p_noise_channel,p_prior,u_prior,u_i_noise,u_o_noise,word_list, start_tag='<s>', end_tag='</s>',markov_process=2):
        #Probability distribution of noise channel
        self.p_noise_channel = p_noise_channel
        #Probability distribution of prior distri
        self.p_prior = p_prior
        #all possible inputs to prior
        self.u_prior = u_prior
        #all inputs to noise channel
        self.u_i_noise = u_i_noise
        #all outputs to noise channel
        self.u_o_noise = u_o_noise
        #Start Tag
        self.start_tag = start_tag
        #End Tag
        self.end_tag = end_tag
        #kind of markov process
        self.markov_process = markov_process
        #What is the input
        self.word_list = word_list

    def farword(self):
        '''
        best : stores the best probability till now.  it takes length of the sentence completed, and for a (index,w1,w2)

        :return:
        '''

        ##### Intialization for the probabilities
        best = defaultdict(lambda : defaultdict(float))
        best_val = float('-inf')

        start_gram = tuple([self.start_tag for i in range(self.markov_process)])
        #print(start_gram)

        best[-1][start_gram] = 1.0

        for i in range(len(self.u_prior)):
            for j in range(len(self.u_prior)):

                u,v = self.u_prior[i],self.u_prior[j]
                if (u,v)!=(self.start_tag,self.start_tag):
                    best[-1][(u,v)] = 0




        #######################


        #######Intialization for the best path
        best_path = defaultdict(lambda : defaultdict(str))
        ######


        def find_best( n, best, u, v, best_val):

            if n in best:
                if (u,v) in best[n]:

                    return best[n][(u,v)]


            x_list = {}
            if n >= 2:
                x_list[3] = self.word_list[n - 2] + ' ' + self.word_list[n - 1] + ' ' + self.word_list[n]
                x_list[2] = self.word_list[n - 1] + ' ' + self.word_list[n]
                x_list[1] = self.word_list[n]
            if n == 1:
                x_list[2] = self.word_list[n - 1] + ' ' + self.word_list[n]
                x_list[1] = self.word_list[n]
            if n == 0:
                x_list[1] = self.word_list[n]



            max_str = None
            temp_str = None
            max_num = float('-inf')
            for i in range(len(self.u_prior)):
                w = self.u_prior[i]
                for n1,x in x_list.items():
                    if n-n1 in best and (w,u) in best[n-n1]:
                        temp_num = best[n-n1][(w,u)] * self.p_prior[(w,u)][v] * self.p_noise_channel[v][x]
                    else:
                        temp_num = find_best(n - n1, best, w, u, best_val) * self.p_prior[(w,u)][v] * self.p_noise_channel[v][x]
                    if temp_num > max_num:
                        max_num = temp_num
                        max_str = w
                        temp_str = x
                        num = n-n1

            best[n][(u, v)] = max_num
            best_path[n][(u,v)] = (max_str,num)

            return best[n][(u,v)]

        ############################


        max_num = float('-inf')
        max_str = None
        n=len(self.word_list)
        for i in range(len(self.u_prior)):
            for j in range(len(self.u_prior)):
                u = self.u_prior[i]
                v = self.u_prior[j]
                temp_num1 = find_best(n-1, best, u, v,best_val)
                temp_num2 = self.p_prior[(u,v)][self.end_tag]

                temp_num = temp_num1*temp_num2
                if temp_num> max_num:
                    max_num = temp_num
                    max_str = (u,v)
        best_path[len(self.word_list)][max_str] = ('</s>',1)

        return max_num,self.backward(best_path)





    def backward(self,best_path):
        leng=len(self.word_list)
        max_str = []
        while True:




            if leng==len(self.word_list):
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
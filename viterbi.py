
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
        best_path = defaultdict(str)
        ######


        def find_best( n, best, u, v, best_val):

            if n in best:
                if (u,v) in best[n]:

                    return best[n][(u,v)]


            max_num = float('-inf')
            max_str = None
            for i in range(len(self.u_prior)):
                w = self.u_prior[i]
                x = self.word_list[n]

                temp_num = find_best(n - 1, best, w, u, best_val) * self.p_prior[(w,u)][v] * self.p_noise_channel[v][x]
                if temp_num > max_num:
                    max_num = temp_num
                    max_str = w

            best[n][(u, v)] = max_num
            best_path[n] = max_str
            best_val = max(best_val,max_num)
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
                    max_str = str(u)+' '+str(v)
        best_path[n] = max_str
        for key in best:
            if key!=-1:
                best_val  = max(max(best[key].values()),best_val)


        return max(best_val,max_num)





    def backward(self,best_path):
        str_data = ''
        for i in range(len(self.word_list)):

            str_data+=best_path[i]+' '
        return str_data
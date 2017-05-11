from collections import defaultdict
from viterbi import Viterbi





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




            ####

            ######
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




#def __init__(self,p_noise_channel,p_prior,u_prior,u_i_noise,u_o_noise,word_list, start_tag='<s>', end_tag='<\s>',markov_process=2):
if __name__=='__main__':

    file_name = 'epron.probs'
    file_name1 = 'epron-jpron.probs'
    start_tag = '<s>'
    end_tag = '</s>'
    markov_process = 2
    word_list = 'D U R G A'.split()


    ######
    epron_data = read_file(file_name)
    p_prior,unique_words = get_prob(epron_data)

    if unique_words[1]==[None]:
        u_prior = unique_words[0]









    #####

    data  = read_file(file_name1)
    p_noise_channel, unique_words = get_prob(data,Noise=True)
    u_i_noise,u_o_noise=unique_words[0], unique_words[1]

    v=Viterbi(p_noise_channel,p_prior,u_prior,u_i_noise,u_o_noise,word_list,start_tag,end_tag,markov_process)

    a=v.farword()
    print(a)








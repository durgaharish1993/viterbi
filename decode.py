from collections import defaultdict

FILEPATH_EPRON_JPRON_PROBS = 'epron-jpron.probs'
FILEPATH_EPRON_PROBS = 'epron.probs'
START = '<s> <s>'
END_TAG = '</s>'

def build_lexicon_model(filename):
    model = defaultdict(lambda: defaultdict(float))
    states = defaultdict(list)
    with open(filename, 'r') as fp:
        for line in fp:
            lparts = line.split('#')
            p = lparts[0].split(':')
            lparts = [p[0].strip(), p[1].strip(), float(lparts[1])]            
            model[lparts[1]][lparts[0]] = lparts[2]
            states[lparts[0]] += [lparts[1]]
    return model, states

def build_bigram_model(filename_probs):
    model = defaultdict(lambda: defaultdict(float))
    with open(filename_probs, 'r') as fp:
        for line in fp:
            sb_ln = line.split()
            prev_state = sb_ln[0] + ' ' + sb_ln[1]
            
            if sb_ln[3] == END_TAG:
                cur_state = END_TAG
            else:
                cur_state = sb_ln[1] + ' ' + sb_ln[3]                
            model[cur_state][prev_state] = float(sb_ln[5])
    return model

def create_state_list(possible_transitions, bi_transitions):
    st = defaultdict(int)
    for tr in possible_transitions:
        for tup in bi_transitions[tr]:
            st[tup[1]] += 1
    return st.keys()


def Viterbi(obs, bigram, lexicon):    
    states = [START] + bigram.keys()  
    N = len(states)
    T = len(obs)    

    #initialization
    viterbi = [[0.0]*T for i in xrange(N)]
    backpointer = [[-1]*T for i in xrange(N)]
    for en_tr, tr_prob in lexicon[obs[0]].items():        
        viterbi[states.index('<s> '+ en_tr)][0] = bigram['<s> '+ en_tr][START] * tr_prob
        backpointer[states.index('<s> '+ en_tr)][0] = states.index(START)        
        
    #recursion
    for t in xrange(1,T):
        possible_transitions = lexicon[obs[t]].keys()
        # st_list = create_state_list(possible_transitions, bi_transitions)
        # for cur_state in st_list:
        #     s = states.index(cur_state)
        for s in xrange(N):
            cur_state = states[s]
            if cur_state == START or cur_state == END_TAG:
                continue
            trans = cur_state.split()[1]
            if lexicon[obs[t]][trans] == 0.0:
                continue
            max_index = ()                                     
            max_index = max((viterbi[states.index(s_p)][t-1]*bigram[cur_state][s_p]*lexicon[obs[t]][trans], states.index(s_p))
                            for s_p in bigram[cur_state])
            if max_index[0] == 0.0:                
                continue

            viterbi[s][t] = max_index[0]
            backpointer[s][t] = max_index[1]
     
    max_index = max((viterbi[states.index(s_p)][T-1]*bigram[END_TAG][s_p], states.index(s_p))
                                for s_p in bigram[END_TAG])
    viterbi[states.index(END_TAG)][T-1] = max_index[0]
    backpointer[states.index(END_TAG)][T-1] = max_index[1]

    st = states.index(END_TAG)
    st = backpointer[st][T-1]
    path = []
    for t in xrange(T-1,-1, -1):
        path += [states[st]]
        st = backpointer[st][t]    
    path = ' '.join([x.split()[1] for x in path[::-1]])
    return path, viterbi[states.index(END_TAG)][T-1] 


if __name__ == '__main__':
    lexicon, s = build_lexicon_model(FILEPATH_EPRON_JPRON_PROBS)
    bigram = build_bigram_model(FILEPATH_EPRON_PROBS)    
    obs = 'P I A N O'
    obs = obs.split()
    print Viterbi(obs, bigram, lexicon)


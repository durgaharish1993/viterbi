from collections import defaultdict

FILEPATH_EPRON_JPRON_PROBS = 'epron-jpron.probs'
FILEPATH_EPRON_PROBS = 'epron.probs'
START = '<s> <s>'
END_TAG = '</s>'

def import_probs(filename):
    probs = defaultdict(lambda: defaultdict(float))
    states = defaultdict(list)
    with open(filename, 'r') as fp:
        for line in fp:
            lparts = line.split('#')
            p = lparts[0].split(':')
            lparts = [p[0].strip(), p[1].strip(), float(lparts[1])]            
            probs[lparts[1]][lparts[0]] = lparts[2]
            states[lparts[0]] += [lparts[1]]
    return probs, states

def build_bigram_model(filename_probs):
    model = defaultdict(lambda: defaultdict(float))
    transit_to_state = defaultdict(list)
    with open(filename_probs, 'r') as fp:
        for line in fp:
            sb_ln = line.split()
            prev_state = sb_ln[0] + ' ' + sb_ln[1]
            

            if prev_state == START: #To increase performance in viterbi
                cur_state = sb_ln[1] + ' ' + sb_ln[3]
                transit_to_state[START] += [(prev_state, cur_state, float(sb_ln[5]))]
            if sb_ln[3] == END_TAG:
                cur_state = END_TAG
                transit_to_state['*e*'] += [(prev_state, cur_state, float(sb_ln[5]))]            
            else:
                cur_state = sb_ln[1] + ' ' + sb_ln[3]
                transit_to_state[sb_ln[3]] += [(prev_state, cur_state, float(sb_ln[5]))]
            model[cur_state][prev_state] = float(sb_ln[5])
    return model, transit_to_state, 

def create_state_list(possible_transitions, bi_transitions):
    st = defaultdict(int)
    for tr in possible_transitions:
        for tup in bi_transitions[tr]:
            st[tup[1]] += 1
    return st.keys()


def Viterbi(obs, bigram_models, tag_wrd_prob):    
    bi_model = bigram_models[0]
    bi_transitions = bigram_models[1]
    states = [START] + bi_model.keys()  
    N = len(states)
    T = len(obs)    

    #initialization
    viterbi = [[0.0]*T for i in xrange(N)]
    backpointer = [[0]*T for i in xrange(N)]
    for s in bi_transitions[START]:
        trans = s[1].split()[1]
        viterbi[states.index(s[1])][0] = bi_model[s[1]][START] * tag_wrd_prob[obs[0]][trans]

    #recursion
    for t in xrange(1,T):
        possible_transitions = tag_wrd_prob[obs[t]].keys()
        st_list = create_state_list(possible_transitions, bi_transitions)
        # for cur_state in st_list:
        #     s = states.index(cur_state)
        for s in xrange(N):
            cur_state = states[s]
            if cur_state == START or cur_state == END_TAG:
                continue
            max_pair = ()                         
            trans = cur_state.split()[1]                
            max_pair = max((viterbi[states.index(s_p)][t-1]*bi_model[cur_state][s_p]*tag_wrd_prob[obs[t]][trans], states.index(s_p))
                            for s_p in bi_model[cur_state])
            viterbi[s][t] = max_pair[0]
            backpointer[s][t] = max_pair[1]
    
    max_pair = max((viterbi[states.index(s_p)][T-1]*bi_model[END_TAG][s_p], states.index(s_p))
                                for s_p in bi_model[END_TAG])
    viterbi[states.index(END_TAG)][T-1] = max_pair[0]
    backpointer[states.index(END_TAG)][T-1] = max_pair[1]
    path = ''
    st = states.index(END_TAG)
    for t in xrange(T-1,-1, -1):
        path += states[st] + ' '
        print states[st]
        st = backpointer[st][t]
    return viterbi[states.index(END_TAG)][T-1], path


if __name__ == '__main__':
    epron_jpron_probs, s = import_probs(FILEPATH_EPRON_JPRON_PROBS)
    bi_models = build_bigram_model(FILEPATH_EPRON_PROBS)    
    obs = 'P I A N O'
    obs  = 'R A M P'
    obs = obs.split()
    print Viterbi(obs, bi_models, epron_jpron_probs)


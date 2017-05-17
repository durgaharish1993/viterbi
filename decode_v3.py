from collections import defaultdict
import sys
import time


FILEPATH_EPRON_JPRON_PROBS = 'epron-jpron.probs'
FILEPATH_EPRON_PROBS = 'epron.probs'
START = '<s> <s>'
END_TAG = '</s>'

def build_lexicon_model(filename):
    model = defaultdict(lambda: defaultdict(float))    
    with open(filename, 'r') as fp:
        for line in fp:
            lparts = line.split('#')
            p = lparts[0].split(':')
            lparts = [p[0].strip(), p[1].strip(), float(lparts[1])]            
            model[lparts[1]][lparts[0]] = lparts[2]            
    return model

def build_trigram_model(filename_probs):
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

def Viterbi(obs, bigram, lexicon):        
    states = [START] + bigram.keys()
    N = len(states)
    T = len(obs)

    #initialization
    viterbi = [[0.0]*T for i in xrange(N)]
    backpointer = [[(-1,-1)]*T for i in xrange(N)]
    for k in xrange(3):
        cur_obs = ' '.join(obs[0:k+1])        
        for en_tr, tr_prob in lexicon[cur_obs].items():        
            viterbi[states.index('<s> '+ en_tr)][0+k] = bigram['<s> '+ en_tr][START] * tr_prob
            backpointer[states.index('<s> '+ en_tr)][0+k] = (states.index(START), k+1)
        
    #recursion
    valid_obs = lexicon.keys()
    for t in xrange(1,T):
        max_index_list = []
        for k in xrange(3):
            if t+k >= T:
                continue
            cur_obs = ' '.join(obs[t:t+k+1])
            if cur_obs not in valid_obs:
                continue
            possible_transitions = lexicon[cur_obs].keys()
            for s, cur_state in enumerate(states):                
                if cur_state == START or cur_state == END_TAG:
                    continue
                trans = cur_state.split()[1]
                if lexicon[cur_obs][trans] == 0.0:
                    continue                
                max_index = ()                                     
                max_index = max((viterbi[states.index(s_p)][t-1]*bigram[cur_state][s_p]*lexicon[cur_obs][trans], states.index(s_p))
                                for s_p in bigram[cur_state])
                if max_index[0] == 0.0:                
                    continue

                if max_index[0] > viterbi[s][t+k]:
                    viterbi[s][t+k] = max_index[0]
                    backpointer[s][t+k] = (max_index[1],k+1)
     
    max_index = max((viterbi[states.index(s_p)][T-1]*bigram[END_TAG][s_p], states.index(s_p))
                                for s_p in bigram[END_TAG])
    viterbi[states.index(END_TAG)][T-1] = max_index[0]
    backpointer[states.index(END_TAG)][T-1] = (max_index[1], 0)

    st = states.index(END_TAG)
    st = backpointer[st][T-1][0]
    k = backpointer[st][T-1][1]
    path = []
    t = T-1
    while t >= 0:
        path += [states[st]]
        st,k = backpointer[st][t]
        t -= k
    path = ' '.join([x.split()[1] for x in path[::-1]])
    return viterbi[states.index(END_TAG)][T-1], path

if __name__ == '__main__':
    s1 = time.clock()
    f = sys.stdin
    lines = f.readlines()

    arg = sys.argv
    if len(arg) > 1:        
        FILEPATH_EPRON_PROBS = arg[1]
        FILEPATH_EPRON_JPRON_PROBS = arg[2]

    lexicon = build_lexicon_model(FILEPATH_EPRON_JPRON_PROBS)
    bigram = build_trigram_model(FILEPATH_EPRON_PROBS)    
    
    for obs_str in lines:
        result = Viterbi(obs_str.strip().split(), bigram, lexicon)
        print result[1], result[0]
    
    s2 = time.clock()
    print 'time: ',s2-s1
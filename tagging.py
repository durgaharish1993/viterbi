from collections import defaultdict
import sys

FILEPATH_LEXICON_PROBS = 'lexicon.wfst'
FILEPATH_BIGRAM_PROBS = 'bigram.wfsa'
START_TAG = '<s>'
END_TAG = '</s>'

def build_lexicon_model(filename):
    model = defaultdict(lambda: defaultdict(float))
    states = defaultdict(list)
    with open(filename, 'r') as fp:
        for line in fp:            
            lparts = line.strip().split('#')            
            p = lparts[0].split(':')
            lparts = [p[0].strip(), p[1].strip(), float(lparts[1].strip())]            
            model[lparts[1]][lparts[0]] = lparts[2]
            states[lparts[0]] += [lparts[1]]
    return model, states

def build_bigram_model(filename_probs):
    model = defaultdict(lambda: defaultdict(float))
    with open(filename_probs, 'r') as fp:
        for line in fp:
            sb_ln = line.split()
            prev_state = sb_ln[0]
            cur_state = sb_ln[2]
            model[cur_state][prev_state] = float(sb_ln[4])
    return model

def Viterbi(obs, bigram, lexicon):    
    states = [START_TAG] + bigram.keys()  
    N = len(states)
    T = len(obs)

    #initialization
    viterbi = [[0.0]*T for i in xrange(N)]
    backpointer = [[-1]*T for i in xrange(N)]
    for en_tr, tr_prob in lexicon[obs[0]].items():        
        viterbi[states.index(en_tr)][0] = bigram[en_tr][START_TAG] * tr_prob
        backpointer[states.index(en_tr)][0] = states.index(START_TAG)        
        
    #recursion
    for t in xrange(1,T):        
        for s in xrange(N):
            cur_state = states[s]
            if cur_state == START_TAG or cur_state == END_TAG:
                continue
            trans = cur_state
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
    path = ' '.join([x.split()[0] for x in path[::-1]])
    return viterbi[states.index(END_TAG)][T-1], path

def convert_lexicon_to_prob(filename):
    with open(filename, 'r') as fp:
        lines = []
        for l in fp:
            l = l.replace('(','').replace(')','').strip()
            if l != '':
                lines += [l.split()]
    
    with open('lexicon.prob', 'w') as fp:
        for l in lines[1:]:
            fp.write(l[2]+' : '+l[3]+' # '+l[4]+'\n')

def convert_bigram_to_prob(filename):
    with open(filename, 'r') as fp:        
        lines = []
        for l in fp:
            l = l.replace('(','').replace(')','').strip()
            if l != '':
                lines += [l.split()]
    
    states = defaultdict(str)
    states[lines[0][0]] = END_TAG
    states[lines[1][0]] = START_TAG
    with open('bigram.prob', 'w') as fp:        
        for l in lines[1:]:
            if l[2] == '*e*':
                l[2] = END_TAG
            if l[1] not in states:
                states[l[1]] = l[2]        
            fp.write(states[l[0]]+' : '+l[2]+' # '+l[3]+'\n')    

if __name__ == '__main__':
    f = sys.stdin
    obs_str = f.readline()

    arg = sys.argv
    if len(arg) > 1:        
        FILEPATH_BIGRAM_PROBS = arg[1]
        FILEPATH_LEXICON_PROBS = arg[2]

    convert_lexicon_to_prob(FILEPATH_LEXICON_PROBS)
    convert_bigram_to_prob(FILEPATH_BIGRAM_PROBS)
    

    lexicon, s = build_lexicon_model('lexicon.prob')
    bigram = build_bigram_model('bigram.prob')        

    obs = obs_str.split()
    tagging =  Viterbi(obs, bigram, lexicon)
    print tagging[1], tagging[0]
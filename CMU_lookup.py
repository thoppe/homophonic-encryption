import collections
from HPE.ARPAbet import ARPAstat
import numpy as np

# Load the dictionary
f_CMU_dict = "CMUdict/cmudict-0.7b"

# Load the top word set
f_top_words = "top_50000_words.txt"
VALID_WORDS = set()
with open(f_top_words) as FIN:
    for line in FIN:
        count,word = line.split()
        VALID_WORDS.add(word)
        
def load_CMU():
    '''
    Returns a dict of key/val, word/list of phones AND
    Returns a dict of dicts, index by number of phones then word.
    '''
    
    CMU = {}
    CMU_LOOKUP = collections.defaultdict(dict)
    with open(f_CMU_dict) as FIN:
        for line in FIN:
            if str.isalpha(line[0]):
                tokens = line.strip().split()
                word, tokens = tokens[0], tokens[1:]
                word = word.lower()
                if word.isalpha() and word:
                    CMU[word] = tokens
                    CMU_LOOKUP[len(tokens)][word] = tokens
    return CMU, CMU_LOOKUP

def hamming(s,t):
    if len(s) != len(t):
        return 100
    return sum([1 for x,y in zip(s,t) if x!=y])
            
def levenshtein(s, t):
        ''' From Wikipedia article; Iterative with two matrix rows. '''
        if s == t: return 0
        elif len(s) == 0: return len(t)
        elif len(t) == 0: return len(s)
        v0 = [None] * (len(t) + 1)
        v1 = [None] * (len(t) + 1)
        for i in range(len(v0)):
            v0[i] = i
        for i in range(len(s)):
            v1[0] = i + 1
            for j in range(len(t)):
                cost = 0 if s[i] == t[j] else 1
                v1[j + 1] = min(v1[j] + 1, v0[j + 1] + 1, v0[j] + cost)
            for j in range(len(v0)):
                v0[j] = v1[j]
                
        return v1[len(t)]
    
'''
// len_s and len_t are the number of characters in string s and t respectively
int LevenshteinDistance(string s, int len_s, string t, int len_t)
{ int cost;

  /* base case: empty strings */
  if (len_s == 0) return len_t;
  if (len_t == 0) return len_s;

  /* test if last characters of the strings match */
  if (s[len_s-1] == t[len_t-1])
      cost = 0;
  else
      cost = 1;

  /* return minimum of delete char from s, delete char from t, and delete char from both */
  return minimum(LevenshteinDistance(s, len_s - 1, t, len_t    ) + 1,
                 LevenshteinDistance(s, len_s    , t, len_t - 1) + 1,
                 LevenshteinDistance(s, len_s - 1, t, len_t - 1) + cost);

'''


class homophonic_word_translate(object):

    def __init__(self,beta=10.0):
        self.CMU,self.CMUX = load_CMU()
        self.A = ARPAstat(1.0)

        self.min_cutoff = 1.25
        self.beta  = beta

    def __call__(self,w1):
        c1 = self.CMU[w1]
       
        CLOSE = {}
        for w2 in self.CMUX[len(c1)]:
            if w2 not in VALID_WORDS: continue
            c2 = self.CMU[w2]
            dx = sum([self.A.delta(x,y) for x,y in zip(c1,c2)]) / len(c1)
            if dx < self.min_cutoff and w1!=w2:
                CLOSE[w2] = dx

        WORDS = CLOSE.keys()
        E  = np.array([CLOSE[word] for word in WORDS])
        Z  = np.exp(-E*self.beta)
        prob = np.exp(-E*self.beta)/Z.sum()
        return np.random.choice(WORDS, p=prob)


#S = "hello english language learners"
S = "little red riding hood"
S = "mary had a little lamb  little lamb  little lamb"
#S = "Once upon a time there lived in a certain village a little country girl, the prettiest creature who was ever seen. Her mother was excessively fond of her; and her grandmother doted on her still more. This good woman had a little red riding hood made for her. It suited the girl so extremely well that everybody called her Little Red Riding Hood."

word_translator = homophonic_word_translate(beta=7.5)

S = "homo phonic encryption"
print map(word_translator, S.split())

for word in S.split():
    print word, word_translator(word)


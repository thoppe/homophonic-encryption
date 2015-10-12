import collections
from HPE.ARPAbet import ARPAstat

# Load the dictionary
f_CMU_dict = "CMUdict/cmudict-0.7b"

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
                if word.isalpha():
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

        


CMU,CMUX = load_CMU()
A = ARPAstat(0.75)
#w1 = "english"
#w1 = "language"
w1 = "hello"

c1 = CMU[w1]

CLOSE = {}
for w2 in CMUX[len(c1)]:
    print w2
    c2 = CMU[w2]
    dx = sum([A.delta(x,y) for x,y in zip(c1,c2)])
    if dx < 5 and w1!=w2:
        CLOSE[w2] = dx

from pprint import pprint
pprint(CLOSE)

#import seaborn as sns
#sns.distplot(DELTA)
#sns.plt.show()
#print DELTA


exit()


min_dist = 20
matching_words = []

for w2,c2 in CMU.items():
    if w1 == w2: continue
    
    #lx = levenshtein(c1,c2)
    lx = hamming(c1,c2)
    if lx <= 3:
        print w2, c1,c2, lx

    #if lx < min_dist:
    #    min_dist = lx
    #    matching_words = []
    #    print "New matching levenshtein distance", lx
    #if lx == min_dist:
    #    print "New word found", w2, lx
    #    matching_words.append(w2)

print matching_words

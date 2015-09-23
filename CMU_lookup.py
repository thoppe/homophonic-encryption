# Load the dictionary
f_CMU_dict = "CMUdict/cmudict-0.7b"

def load_CMU():
    CMU = {}
    with open(f_CMU_dict) as FIN:
        for line in FIN:
            if str.isalpha(line[0]):
                tokens = line.strip().split()
                word, tokens = tokens[0], tokens[1:]
                word = word.lower()
                CMU[word] = tokens
    return CMU

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


CMU = load_CMU()
w1 = "english"
#w1 = "language"


c1 = CMU[w1]
#c2 = CMU[w2]

print c1
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

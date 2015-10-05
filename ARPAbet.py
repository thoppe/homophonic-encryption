import itertools
import numpy as np
import pandas as pd

f_vowels = "confusion_matrices/confusion_vowels_poor.csv"
f_consonants = "confusion_matrices/confusion_consonants_poor.csv"

def load_confusion_matrix(f_matrix):
    df = pd.read_csv(f_matrix,index_col=0)

    # Make the matrices symmetric
    df += df.T
    df /= 2.0
    return df

confusion = {}
confusion["vowel"] = load_confusion_matrix(f_vowels)
confusion["consonant"] = load_confusion_matrix(f_consonants)

phoneme_types = {
    "monophthong" : "vowel",
    "diphthong"   : "vowel",
    "rcolored"    : "vowel",
    "semivowel"   : "consonant",
    "stop"        : "consonant",
    "affricate"   : "consonant",
    "fricative"   : "consonant",
    "nasal"       : "consonant",
    "liquid"      : "consonant",
    "aspirate"    : "consonant",
}

phonemes={
    'AA':'monophthong',
    'AE':'monophthong',
    'AH':'monophthong',
    'AO':'monophthong',
    'AW':'diphthong',
    'AY':'diphthong',
    'B':'stop',
    'CH':'affricate',
    'D':'stop',
    'DH':'fricative',
    'EH':'monophthong',
    'ER':'rcolored',
    'EY':'diphthong',
    'F':'fricative',
    'G':'stop',
    'HH':'aspirate',
    'IH':'monophthong',
    'IY':'monophthong',
    'JH':'affricate',
    'K':'stop',
    'L':'liquid',
    'M':'nasal',
    'N':'nasal',
    'NG':'nasal',
    'OW':'diphthong',
    'OY':'diphthong',
    'P':'stop',
    'R':'liquid',
    'S':'fricative',
    'SH':'fricative',
    'T':'stop',
    'TH':'fricative',
    'UH':'monophthong',
    'UW':'monophthong',
    'V':'fricative',
    'W':'semivowel',
    'Y':'semivowel',
    'Z':'fricative',
    'ZH':'fricative',
}

def get_phoneme_type(p):
    p_object = phonemes[p]
    return phoneme_types[p_object]

'''
For the phonemes missing in the confusion matrix study,
we map them to linear combinations of the known values.
'''
missing_phoneme_mappings = {
    "AO" : ["EH",],
    "AY" : ["AA","IH"],
    "AW" : ["AA","AH"],
    "OY" : ["EH","IH"],
    "CH" : ["SH","TH"],
    "JH" : ["SH","ZH"],
    "HH" : ["Y",],
    "NG" : ["N","G"],
    "W"  : ["B",],
}

# Fill in the missing phonemes with linear combinations
for key,values in missing_phoneme_mappings.items():
    df = confusion[get_phoneme_type(key)]
    row = df[values].mean(axis=1)
    row[key] = row[values].mean()

    # Add a new column
    df [key]  = row

    # Add a new row
    df.loc[key] = row

    
class araphet_phoneme(object):

    def __init__(self, val):

        self.stress = None
        
        if len(val)==3:
            val,self.stress = val[:2],int(val[2])

        self.symbol  = val
        self.phoneme = phonemes[self.symbol]
        self.ptype   = phoneme_types[self.phoneme]

    def __repr__(self):
        if self.stress is not None:
            return self.symbol + str(self.stress)
        return self.symbol

    def delta(self, y):
        if self.ptype != y.ptype:
            return 1.0
        if self.phoneme != y.phoneme:
            return 0.75
        if self.symbol != y.symbol:
            return 0.50
        if self.stress != y.stress:
            return 0.25
        return 0.0

class ARPAstat(object):
    '''
    A phoneme-based model for language using a combination of ARPAbet 
    and statistical mechanics.
    '''
    def __init__(self, kT=1.0):
        self.kT = kT
        self.confusion = confusion
        self.energy = {}
        self.Z = {}

        for key in confusion:
            self.energy[key] = E = confusion[key].copy()

            # Convert the confusion matrix into a probability
            E /= E.sum(axis=0)

            # Blank values (from linear combinations) are set to lowest
            E[E==0] = E[E>0].min().min()

            # Convert probability to energy at baseline kT=1.0
            self.energy[key] = -np.log(E)

            # Symmetrize
            self.energy[key] = (self.energy[key]+self.energy[key].T)/2

            # Scale for numerical reasons
            self.energy[key] -= self.energy[key].values.mean()

            # Reasonable partition function
            self.Z  = np.exp(self.energy[key]/self.kT).sum(axis=0)
            self.Z /= self.Z.shape[0]
        
    def delta(self,x,y):
        '''
        Returns a cost scaled between 0,1
        '''
        
        a,b = map(araphet_phoneme, [x,y])

        if a.ptype != b.ptype:
            EA = self.energy[a.ptype]
            EB = self.energy[b.ptype]
            E = max(EA.values.max(), EB.values.max())
        else:
            E_matrix = self.energy[a.ptype]
            E = E_matrix[a.symbol][b.symbol]

        z = (self.Z[a.symbol]+self.Z[b.symbol])/2
        return np.exp(E/self.kT)/z

#C = confusion["vowel"]
#print C
#C /= C.sum(axis=0)
#print -np.log(C)
#exit()

A = ARPAstat(0.75)
x,y = 'AE','AE'
print "Exact", A.delta(x,y), A.delta(y,x)
print

x,y = 'AE','AA'
print "Close", A.delta(x,y), A.delta(y,x)
print

x,y = 'AE','AO'
print "Far  ", A.delta(x,y), A.delta(y,x)
print

exit()
        
a = araphet_phoneme('AO1')
b = araphet_phoneme('AE2')
c = araphet_phoneme('AE')
d = araphet_phoneme('ZH')

print confusion["vowel"]

for x,y in itertools.combinations([a,b,c,d,a],r=2):
    print x,y,x.delta(y)




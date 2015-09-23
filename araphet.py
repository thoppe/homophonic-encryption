import itertools

phoneme_types = {
    "monophthong" : "vowel",
    "diphthong"   : "vowel",
    "rcolored"    : "vowel",
    "semivowel"   : "vowel",
    "stop"        : "consonant",
    "affricate"   : "consonant",
    "fricative"   : "consonant",
    "nasals"      : "consonant",
    "liquid"      : "consonant",    
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


a = araphet_phoneme('AO1')
b = araphet_phoneme('AE2')
c = araphet_phoneme('AE')
d = araphet_phoneme('ZH')

for x,y in itertools.combinations([a,b,c,d,a],r=2):
    print x,y,x.delta(y)

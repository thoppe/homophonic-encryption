# Homophonic Encryption

Uses the [CMU pronouncing dictionary](http://www.speech.cs.cmu.edu/cgi-bin/cmudict) to map words to the [ARPAbet](https://en.wikipedia.org/wiki/Arpabet), a reduced set of the IPA.

Using this reduced mapping, homophonic encryption attempts to reconstruct sentences with phonetically similar (but semantically meaningless) equivalents to produces something that "sounds like" the original.
If successful, this will make it very hard for a machine to deduce what is actually being said since it relies on the acoustical representation.
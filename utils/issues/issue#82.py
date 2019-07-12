
import mlconjug

verbList = ['rob', 'mob']

default_conjugator = mlconjug.Conjugator(language='en')
verbs_with_Nones = []
mlOutput = []
for item in verbList:
    pp = default_conjugator.conjugate(item).conjug_info
    for mood, tense in pp.items():
        if None in tense.values():
            verbs_with_Nones.append(item)
    mlOutput.append(pp)

pass

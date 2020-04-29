
import mlconjug3

verbList = ['arise', 'awake', 'be', 'bear', 'beat', 'become', 'begin', 'bend', 'bet', 'bind', 'bite', 'bleed', 'blow',
            'break', 'breed', 'bring', 'broadcast', 'build', 'burn', 'burst', 'buy', 'be', 'catch', 'choose', 'clung',
            'come', 'cost', 'creep', 'cut', 'delt', 'dig', 'do', 'dream', 'drunk', 'drive', 'eat', 'fall', 'feed',
            'feel', 'fight', 'find', 'fly', 'forbid', 'forget', 'forgive', 'freeze', 'get', 'give', 'go', 'ground',
            'grow', 'hang', 'have', 'hear', 'hide', 'hit', 'hold', 'hurt', 'keep', 'knelt', 'know', 'lay', 'lead',
            'learn', 'leave', 'lend', 'lie', 'lie', 'light', 'lose', 'make', 'ment', 'meet', 'mow', 'overtaken', 'pay',
            'put', 'read', 'ride', 'ring', 'rise', 'run', 'sawn', 'say', 'see', 'sell', 'send', 'set', 'sew', 'shake',
            'shed', 'shine', 'shoot', 'show', 'shrink', 'shut', 'sing', 'sink', 'sit', 'sleep', 'slide', 'smell', 'sow',
            'speak', 'spell', 'spend', 'spill', 'spat', 'spread', 'stand', 'steal', 'stick', 'sting', 'stunk', 'strike',
            'swear', 'sweep', 'swell', 'swum', 'swing', 'take', 'teach', 'tear', 'tell', 'think', 'throw', 'understand',
            'wake', 'wear', 'weep', 'win', 'wound', 'write']

problematic_verbs = ['beat', 'bet', 'broadcast', 'burn', 'burst', 'clung', 'cost', 'cut', 'delt', 'dream', 'drunk',
                     'ground', 'hear', 'hit', 'knelt', 'learn', 'ment', 'mow', 'overtaken', 'put', 'read', 'ring',
                     'sawn', 'set', 'sew', 'shed', 'show', 'shut', 'smell', 'sow', 'spell', 'spill', 'spat', 'stunk',
                     'wound']

default_conjugator = mlconjug3.Conjugator(language='en')
verbs_with_Nones = []
mlOutput = []
for item in verbList:
    pp = default_conjugator.conjugate(item).conjug_info
    for mood, tense in pp.items():
        if None in tense.values():
            verbs_with_Nones.append(item)
    mlOutput.append(pp)

pass

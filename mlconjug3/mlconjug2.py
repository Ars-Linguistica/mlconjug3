class Conjugator:
    def __len__(self):
        return len(self.conjugations)
    
    def __format__(self, format_spec):
        return self.infinitive + ' ' + format_spec + ' ' + self.conjugations

    def __getattr__(self, name):
        return self.conjugations.get(name, None)

    def __getitem__(self, key):
        return self.conjugations[key]

    def __iter__(self):
        return iter(self.conjugations)

    def __contains__(self, item):
        return item in self.conjugations

    def __add__(self, other):
        return self.conjugations + other.conjugations

    def __eq__(self, other):
        return self.infinitive == other.infinitive

    def __str__(self):
        return self.infinitive + ': ' + str(self.conjugations)

    def __bool__(self):
        return bool(self.conjugations)

    def __call__(self, mood, tense, person):
        return self.conjugations.get((mood, tense, person), None)

      
class Dataset:
    def __init__(self, infinitive, conjugations):
        self.infinitive = infinitive
        self.conjugations = conjugations

    def __len__(self):
        return len(self.conjugations)

    def __format__(self, format_spec):
        return 'Infinitive: {}\nConjugations: {}'.format(self.infinitive, self.conjugations)

    def __getattr__(self, name):
        return self.conjugations.get(name)

    def __getitem__(self, key):
        return self.conjugations[key]

    def __iter__(self):
        return iter(self.conjugations)

    def __contains__(self, item):
        return item in self.conjugations

    def __add__(self, other):
        if self.infinitive != other.infinitive:
            raise ValueError("Cannot concatenate conjugations of different verbs.")
        return Dataset(self.infinitive, {**self.conjugations, **other.conjugations})

    def __eq__(self, other):
        return self.infinitive == other.infinitive

    def __str__(self):
        return 'Infinitive: {}\nConjugations: {}'.format(self.infinitive, self.conjugations)

    def __bool__(self):
        return bool(self.conjugations)

    def __call__(self, mood, tense, person):
        return self.conjugations.get((mood, tense, person))

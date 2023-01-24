import pkg_resources

RESOURCE_PACKAGE = 'mlconjug3'

LANGUAGES = ('default', 'fr', 'en', 'es', 'it', 'pt', 'ro')

SUPPORTED_LANGUAGES = ('default', 'en', 'es', 'fr', 'it', 'pt', 'ro')

TRANSLATED_LANGUAGES = SUPPORTED_LANGUAGES[2:]

LANGUAGE_FULL = {'fr': 'Français',
                  'en': 'English',
                  'es': 'Español',
                  'it': 'Italiano',
                  'pt': 'Português',
                  'ro': 'Română',
                  }

TRANSLATIONS_PATH = pkg_resources.resource_filename(RESOURCE_PACKAGE, 'locale')

VERBS_RESOURCE_PATH = {'fr': '/'.join(('data', 'conjug_manager', 'verbs-fr.json')),
                        'it': '/'.join(('data', 'conjug_manager', 'verbs-it.json')),
                        'es': '/'.join(('data', 'conjug_manager', 'verbs-es.json')),
                        'en': '/'.join(('data', 'conjug_manager', 'verbs-en.json')),
                        'pt': '/'.join(('data', 'conjug_manager', 'verbs-pt.json')),
                        'ro': '/'.join(('data', 'conjug_manager', 'verbs-ro.json')),}

CONJUGATIONS_RESOURCE_PATH = {'fr': '/'.join(('data', 'conjug_manager', 'conjugation-fr.json')),
                               'it': '/'.join(('data', 'conjug_manager', 'conjugation-it.json')),
                               'es': '/'.join(('data', 'conjug_manager', 'conjugation-es.json')),
                               'en': '/'.join(('data', 'conjug_manager', 'conjugation-en.json')),
                               'pt': '/'.join(('data', 'conjug_manager', 'conjugation-pt.json')),
                               'ro': '/'.join(('data', 'conjug_manager', 'conjugation-ro.json')),}

PRE_TRAINED_MODEL_PATH = {
    'fr': '/'.join(('data', 'models', 'trained_model-fr-final.zip')),
    'it': '/'.join(('data', 'models', 'trained_model-it-final.zip')),
    'es': '/'.join(('data', 'models', 'trained_model-es-final.zip')),
    'en': '/'.join(('data', 'models', 'trained_model-en-final.zip')),
    'pt': '/'.join(('data', 'models', 'trained_model-pt-final.zip')),
    'ro': '/'.join(('data', 'models', 'trained_model-ro-final.zip')),
}

ABBREVS = ("1s", "2s", "3s", "1p", "2p", "3p")

PRONOUNS = {'fr': {'abbrev': ABBREVS,
                    'pronoun': ("je", "tu", "il (elle, on)", "nous", "vous", "ils (elles)")},
             'it': {'abbrev': ABBREVS,
                    'pronoun': ('io', 'tu', 'egli/ella', 'noi', 'voi', 'essi/esse')},
             'es': {'abbrev': ABBREVS,
                    'pronoun': ('yo', 'tú', 'él', 'nosotros', 'vosotros', 'ellos')},
             'en': {'abbrev': ABBREVS,
                    'pronoun': ('I', 'you', 'he/she/it', 'you', 'we', 'they')},
             'pt': {'abbrev': ABBREVS,
                    'pronoun': ('eu', 'tu', 'ele', 'nós', 'vós', 'eles')},
             'ro': {'abbrev': ABBREVS,
                    'pronoun': ('eu', 'tu', 'el/ea', 'noi', 'voi', 'ei/ele')}
             }

IMPERATIVE_PRONOUNS = {'fr': {'abbrev': ("2s", "1p", "2p"),
                               'pronoun': ("", "", "")},
                        'it': None,
                        'es': {'abbrev': ("2s", "3s", "1p", "2p", "3p"),
                               'pronoun': ('tú', 'él', 'nosotros', 'vosotros', 'ellos')},
                        'en': {'abbrev': ("2s", "1p", "2p"),
                               'pronoun': ("", "let's", "")},
                        'pt': None,
                        'ro': {'abbrev': ("2s", "2p"),
                               'pronoun': ("tu", "voi")},
                        }

AUXILIARIES = {'fr': None,
                'it': 'non',
                'es': 'no',
                'en': None,
                'pt': 'não',
                'ro': 'nu'}

GENDER = {'fr': {'abbrev': ("ms", "mp", "fs", "fp"),
                  'pronoun': ("masculin singulier", "masculin pluriel", "feminin singulier", "feminin pluriel")},
           'it': None,
           'es': None,
           'en': None,
           'pt': None,
           'ro': None}

NEGATION = {'fr': 'ne',
             'it': 'non',
             'es': 'no',
             'en': "don't",
             'pt': 'não',
             'ro': 'nu'}

ALPHABET = {'fr': {'vowels': 'aáàâeêéèiîïoôöœuûùy',
                    'consonants': 'bcçdfghjklmnpqrstvwxyz'},
             'en': {'vowels': 'aeiouy',
                    'consonants': 'bcdfghjklmnpqrstvwxyz'},
             'es': {'vowels': 'aáeiíoóuúy',
                    'consonants': 'bcdfghjklmnñpqrstvwxyz'},
             'it': {'vowels': 'aàeéèiìîoóòuùy',
                    'consonants': 'bcdfghjklmnpqrstvwxyz'},
             'pt': {'vowels': 'aàãááeêéiíoóõuúy',
                    'consonants': 'bcçdfghjklmnpqrstvwxyz'},
             'ro': {'vowels': 'aăâeiîouy',
                    'consonants': 'bcdfghjklmnpqrsșştțţvwxyz'},
             }

if __name__ == "__main__":
    pass

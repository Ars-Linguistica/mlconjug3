_RESOURCE_PACKAGE = 'mlconjug3'

_LANGUAGES = ('default', 'fr', 'en', 'es', 'it', 'pt', 'ro')

# Sets up the automatic translation of annotated strings displayed to the user.
_TRANSLATIONS_PATH = pkg_resources.resource_filename(_RESOURCE_PACKAGE, 'locale')

_SUPPORTED_LANGUAGES = ('default', 'en', 'es', 'fr', 'it', 'pt', 'ro')
_TRANSLATED_LANGUAGES = _SUPPORTED_LANGUAGES[2:]

_LANGUAGE_FULL = {'fr': 'Français',
                  'en': 'English',
                  'es': 'Español',
                  'it': 'Italiano',
                  'pt': 'Português',
                  'ro': 'Română',
                  }

_VERBS = {'fr': VerbFr,
          'en': VerbEn,
          'es': VerbEs,
          'it': VerbIt,
          'pt': VerbPt,
          'ro': VerbRo,
          }

_PRE_TRAINED_MODEL_PATH = {
    'fr': '/'.join(('data', 'models', 'trained_model-fr-final.zip')),
    'it': '/'.join(('data', 'models', 'trained_model-it-final.zip')),
    'es': '/'.join(('data', 'models', 'trained_model-es-final.zip')),
    'en': '/'.join(('data', 'models', 'trained_model-en-final.zip')),
    'pt': '/'.join(('data', 'models', 'trained_model-pt-final.zip')),
    'ro': '/'.join(('data', 'models', 'trained_model-ro-final.zip')),
}

_ALPHABET = {'fr': {'vowels': 'aáàâeêéèiîïoôöœuûùy',
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

_VERBS_RESOURCE_PATH = {'fr': '/'.join(('data', 'conjug_manager', 'verbs-fr.json')),
                        'it': '/'.join(('data', 'conjug_manager', 'verbs-it.json')),
                        'es': '/'.join(('data', 'conjug_manager', 'verbs-es.json')),
                        'en': '/'.join(('data', 'conjug_manager', 'verbs-en.json')),
                        'pt': '/'.join(('data', 'conjug_manager', 'verbs-pt.json')),
                        'ro': '/'.join(('data', 'conjug_manager', 'verbs-ro.json')),}

_CONJUGATIONS_RESOURCE_PATH = {'fr': '/'.join(('data', 'conjug_manager', 'conjugation-fr.json')),
                               'it': '/'.join(('data', 'conjug_manager', 'conjugation-it.json')),
                               'es': '/'.join(('data', 'conjug_manager', 'conjugation-es.json')),
                               'en': '/'.join(('data', 'conjug_manager', 'conjugation-en.json')),
                               'pt': '/'.join(('data', 'conjug_manager', 'conjugation-pt.json')),
                               'ro': '/'.join(('data', 'conjug_manager', 'conjugation-ro.json')),}

_ABBREVS = ("1s", "2s", "3s", "1p", "2p", "3p")

_PRONOUNS = {'fr': {'abbrev': _ABBREVS,
                    'pronoun': ("je", "tu", "il (elle, on)", "nous", "vous", "ils (elles)")},
             'it': {'abbrev': _ABBREVS,
                    'pronoun': ('io', 'tu', 'egli/ella', 'noi', 'voi', 'essi/esse')},
             'es': {'abbrev': _ABBREVS,
                    'pronoun': ('yo', 'tú', 'él', 'nosotros', 'vosotros', 'ellos')},
             'en': {'abbrev': _ABBREVS,
                    'pronoun': ('I', 'you', 'he/she/it', 'you', 'we', 'they')},
             'pt': {'abbrev': _ABBREVS,
                    'pronoun': ('eu', 'tu', 'ele', 'nós', 'vós', 'eles')},
             'ro': {'abbrev': _ABBREVS,
                    'pronoun': ('eu', 'tu', 'el/ea', 'noi', 'voi', 'ei/ele')}
             }

_IMPERATIVE_PRONOUNS = {'fr': {'abbrev': ("2s", "1p", "2p"),
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

_AUXILIARIES = {'fr': None,
                'it': 'non',
                'es': 'no',
                'en': None,
                'pt': 'não',
                'ro': 'nu'}

_GENDER = {'fr': {'abbrev': ("ms", "mp", "fs", "fp"),
                  'pronoun': ("masculin singulier", "masculin pluriel", "feminin singulier", "feminin pluriel")},
           'it': None,
           'es': None,
           'en': None,
           'pt': None,
           'ro': None}

_NEGATION = {'fr': 'ne',
             'it': 'non',
             'es': 'no',
             'en': "don't",
             'pt': 'não',
             'ro': 'nu'}
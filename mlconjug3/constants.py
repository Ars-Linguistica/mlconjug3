_RESOURCE_PACKAGE = 'mlconjug3'

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

import toml

def load_config(file_path):
    with open(file_path, 'r') as f:
        config = toml.load(f)
    return config

CONFIG_FILE = 'path/to/config.toml'
config = load_config(CONFIG_FILE)

LANGUAGES = config.get('LANGUAGES', ('default', 'fr', 'en', 'es', 'it', 'pt', 'ro'))

TRANSLATIONS_PATH = config.get('TRANSLATIONS_PATH', pkg_resources.resource_filename(RESOURCE_PACKAGE, 'locale'))

SUPPORTED_LANGUAGES = config.get('SUPPORTED_LANGUAGES', ('default', 'en', 'es', 'fr', 'it', 'pt', 'ro'))
TRANSLATED_LANGUAGES = config.get('TRANSLATED_LANGUAGES', SUPPORTED_LANGUAGES[2:])

LANGUAGE_FULL = config.get('LANGUAGE_FULL', {'fr': 'Français',
                  'en': 'English',
                  'es': 'Español',
                  'it': 'Italiano',
                  'pt': 'Português',
                  'ro': 'Română',
                  })

VERBS = config.get('VERBS', {'fr': VerbFr,
          'en': VerbEn,
          'es': VerbEs,
          'it': VerbIt,
          'pt': VerbPt,
          'ro': VerbRo,
          })

PRE_TRAINED_MODEL_PATH = config.get('PRE_TRAINED_MODEL_PATH', {
    'fr': '/'.join(('data', 'models', 'trained_model-fr-final.zip')),
    'it': '/'.join(('data', 'models', 'trained_model-it-final.zip')),
    'es': '/'.join(('data', 'models', 'trained_model-es-final.zip')),
    'en': '/'.join(('data', 'models', 'trained_model-en-final.zip')),
    'pt': '/'.join(('data', 'models', 'trained_model-pt-final.zip')),
    'ro': '/'.join(('data', 'models', 'trained_model-ro-final.zip')),
})

ALPHABET = config.get('ALPHABET', {'fr': {'vowels': 'aáàâeêéèiîïoôöœuûùy',
                    'consonants': 'bcçdfghjklmnpqrstvwxyz'},
             # continue
                                  })

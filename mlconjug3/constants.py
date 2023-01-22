from .verbs import *

RESOURCE_PACKAGE = 'mlconjug3'

LANGUAGE_FULL = {'fr': 'Français',
                  'en': 'English',
                  'es': 'Español',
                  'it': 'Italiano',
                  'pt': 'Português',
                  'ro': 'Română',
                  }

VERBS = {'fr': VerbFr,
          'en': VerbEn,
          'es': VerbEs,
          'it': VerbIt,
          'pt': VerbPt,
          'ro': VerbRo,
          }

PRE_TRAINED_MODEL_PATH = {
    'fr': '/'.join(('data', 'models', 'trained_model-fr-final.zip')),
    'it': '/'.join(('data', 'models', 'trained_model-it-final.zip')),
    'es': '/'.join(('data', 'models', 'trained_model-es-final.zip')),
    'en': '/'.join(('data', 'models', 'trained_model-en-final.zip')),
    'pt': '/'.join(('data', 'models', 'trained_model-pt-final.zip')),
    'ro': '/'.join(('data', 'models', 'trained_model-ro-final.zip')),
}

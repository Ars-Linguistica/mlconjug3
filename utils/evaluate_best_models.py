
import mlconjug3
import joblib

try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path


langs = ('ro', 'it', 'en', 'es', 'fr', 'pt')

results = {}

for lang in langs:
    my_file = Path('raw_data/models/reduced_search/best_model_{0}.pkl'.format(lang))
    if not my_file.exists():
        continue
    else:
        with open('raw_data/models/reduced_search/best_model_{0}.pkl'.format(lang), 'rb') as file:
            best_model = joblib.load(file)

        # Load best model parameters
        with open('raw_data/experiments/reduced_search/best_model_parameters_{0}.pkl'.format(lang),
                  'rb') as file:
            best_params = joblib.load(file)

        dataset = mlconjug3.DataSet(mlconjug3.Verbiste(language=lang).verbs)
        dataset.split_data(proportion=0.95)

        predicted = best_model.predict(dataset.test_input)
        predicted2 = best_model.predict(dataset.verbs_list)

        score = len([(a, b) for a, b in zip(predicted, dataset.test_labels) if a == b]) / len(predicted)
        misses = len([(a, b) for a, b in zip(predicted, dataset.test_labels) if a != b])
        entries = len(predicted)
        print('The score of the {0} best model is {1} on test set.'.format(lang, score))

        score2 = len([(a, b) for a, b in zip(predicted2, dataset.templates_list) if a == b]) / len(predicted2)
        misses2 = len([(a, b) for a, b in zip(predicted2, dataset.templates_list) if a != b])
        entries2 = len(predicted2)
        print('The score of the {0} best model is {1} on full dataset.\n'.format(lang, score2))
        results[lang] = (lang, best_model, best_params, (score, misses, entries), (score2, misses2, entries2))

print('ok')

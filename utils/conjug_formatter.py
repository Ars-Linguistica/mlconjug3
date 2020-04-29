import pickle
from os import listdir
from os.path import isfile, join
from collections import OrderedDict, defaultdict


def detect_root(verb, info_verb, language):
    if 'type' in info_verb:
        return None
    result = OrderedDict()
    verb_forms = [forms for key, forms in info_verb.items() if key != 'doubles']
    flat_verb_forms = []
    for tense in verb_forms:
        for form in tense:
            if '/' in form[-1]:
                if not language == 'it':
                    standard_form = form[-1][:form[-1].index('/')]
                else:
                    standard_form = form[-1][form[-1].index('/') +1:]
                if len(standard_form) > 0:
                    flat_verb_forms.append(standard_form.strip().split(' ')[-1])
                pass
            elif not form[-1] in ('' or '-'):
                standard_form = form[-1].strip().split(' ')[-1]
                if len(standard_form) > 0:
                    flat_verb_forms.append(standard_form)
    root = ''
    for i in range(1, len(verb)+1):
        prefix = verb[:i]
        if all([elmt.startswith(prefix) for elmt in flat_verb_forms]):
            root = prefix
        else:
            break
    suffix = verb[len(root):]
    return (root, suffix)


def construct_template(verb, info_verb, root_info, language, pronouns_dict):
    if 'type' in info_verb:
        return None
    result = OrderedDict()
    verb_roots = OrderedDict()
    verb_roots[verb] = root_info[0]
    for key, val in info_verb.items():
        if key != 'doubles':
            forms = []
            for form in val:
                if form[-1].startswith('('):
                    continue
                if not form[-1] in ('' or '-'):
                    forms.append(form[-1].strip().split(' ')[-1][len(root_info[0]):])
                if form[-1].strip().split(' ')[-1] == '-':
                    forms.append(form[-1].strip().split(' ')[-1])
                if len(form) > 1:
                    pronouns_dict[language].add(form[0])
            result[key] = tuple(forms)
    return result


def group_by_template(model_verbs_dict, all_verbs_dict, verb_roots):
    results = defaultdict(dict)
    for key, val in model_verbs_dict.items():
        if val:
            pattern = frozenset(val.items())
            results[pattern]['model_verb'] = key
            results[pattern]['members'] = [key, ]
            root = verb_roots[key]
            template = root + ':' + key[len(root):]
            results[pattern]['template'] = template
        pass
    for key, val in all_verbs_dict.items():
        if val:
            pattern = frozenset(val.items())
            if pattern in results:
                results[pattern]['members'].append(key)
                pass
            else:
                results[pattern]['model_verb'] = key
                results[pattern]['members'] = [key, ]
                root = verb_roots[key]
                template = root + ':' + key[len(root):]
                results[pattern]['template'] = template
                pass
            pass
    return results


def construct_verbs_dict(hastable, verb_roots):
    verb_dict = {}
    for val in hastable.values():
        root = verb_roots[val['model_verb']]
        template = root + ':' + val['model_verb'][len(root):]
        for verb in set(val['members']):
            verb_dict[verb] = template
            pass
        pass
    return verb_dict


def construct_conjug_dict(hastable, verb_roots, all_verbs_conjugation):
    conjug_dict = {}
    for val in hastable.values():
        root = verb_roots[val['model_verb']]
        template = root + ':' + val['model_verb'][len(root):]
        conjug = all_verbs_conjugation[val['model_verb']]
        conjug_dict[template] = conjug
        pass
    return conjug_dict


if __name__ == "__main__":
    path = 'C:/Users/SDiao/PycharmProjects/mlconjug3/utils/cooljugator'
    files = [join(path, f) for f in listdir(path) if isfile(join(path, f))]
    for file in files:
        conjugation = {}
        verbs = {}
        lang = file.split('-')[1].split('.')[0]
        with open(file, 'rb') as conjug_file:
            conjug_data = pickle.load(conjug_file)
            # Detect conjugation pattern by Identifying root and ending
            # Populate 'conjugation' and 'verbs' dict
            # Save data as json
            pass

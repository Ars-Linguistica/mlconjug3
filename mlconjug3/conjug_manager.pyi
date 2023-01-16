class ConjugManager:
    def __init__(self, extract_verb_features:callable, pre_trained_models=None, language:str='fr'):
        pass
    def _load_verbs(self, verbs_file:str):
        pass
    def _load_conjugations(self, conjugations_file:str):
        pass
    def _detect_allowed_endings(self)->set:
        pass
    def is_valid_verb(self, verb:str)->Union[str,bool]:
        pass

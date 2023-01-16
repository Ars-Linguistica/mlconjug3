class VerbFilter:
    def __init__(self):
        pass
        
    def filter_by_tense(self, verbs: list, tense: str):
        """
        Filters verbs by tense
        :param verbs: list
        :param tense: str
        :return: list
        """
        filtered_verbs = []
        for verb in verbs:
            if verb.conjug_info["tense"] == tense:
                filtered_verbs.append(verb)
        return filtered_verbs
    
    def filter_by_person(self, verbs: list, person: str):
        """
        Filters verbs by person
        :param verbs: list
        :param person: str
        :return: list
        """
        filtered_verbs = []
        for verb in verbs:
            if verb.conjug_info["person"] == person:
                filtered_verbs.append(verb)
        return filtered_verbs

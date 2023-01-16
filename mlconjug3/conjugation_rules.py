class ConjugationRule:
    def __init__(self, language, conjugation_class, rule):
        self.language = language
        self.conjugation_class = conjugation_class
        self.rule = rule

class ConjugationRuleFactory:
    def create_conjugation_rule(self, language, conjugation_class, rule):
        if language == 'fr':
            return ConjugationRuleFr(conjugation_class, rule)
        elif language == 'en':
            return ConjugationRuleEn(conjugation_class, rule)
        # add additional languages as needed

class ConjugationRuleFr(ConjugationRule):
    def __init__(self, conjugation_class, rule):
        super().__init__('fr', conjugation_class, rule)

class ConjugationRuleEn(ConjugationRule):
    def __init__(self, conjugation_class, rule):
        super().__init__('en', conjugation_class, rule)

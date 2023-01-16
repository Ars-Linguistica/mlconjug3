class VerbInfo:
    def __init__(self, infinitive:str, root:str, template:str):
        pass

    def __repr__(self):
        pass

    def __eq__(self, other):
        pass

class Verb:
    def __init__(self, verb_info:VerbInfo, conjug_info:OrderedDict, subject:str='abbrev', predicted:bool=False):
        pass
    def __repr__(self):
        pass
    def iterate(self)->List[Tuple]:
        pass
    def _load_conjug(self):
        pass

      
class VerbFr:
    def init(self, verb: str, subject: str):
        pass
      
    def conjugate(self, mood: str, tense: str, person: str) -> str:
        pass

    def conjugate_all(self) -> Dict[str, Dict[str, Union[str, Dict[str, str]]]]:
        pass

    def is_valid(self) -> bool:
        pass
      
      
class VerbEn:
    def init(self, verb: str, subject: str):
        pass
      
    def conjugate(self, mood: str, tense: str, person: str) -> str:
        pass

    def conjugate_all(self) -> Dict[str, Dict[str, Union[str, Dict[str, str]]]]:
        pass

    def is_valid(self) -> bool:
        pass
      
      
class VerbEs:
    def init(self, verb: str, subject: str):
        pass
      
    def conjugate(self, mood: str, tense: str, person: str) -> str:
        pass

    def conjugate_all(self) -> Dict[str, Dict[str, Union[str, Dict[str, str]]]]:
        pass

    def is_valid(self) -> bool:
        pass
      
      
class VerbIt:
    def init(self, verb: str, subject: str):
        pass
      
    def conjugate(self, mood: str, tense: str, person: str) -> str:
        pass

    def conjugate_all(self) -> Dict[str, Dict[str, Union[str, Dict[str, str]]]]:
        pass

    def is_valid(self) -> bool:
        pass
      
      
class VerbPt:
    def init(self, verb: str, subject: str):
        pass
      
    def conjugate(self, mood: str, tense: str, person: str) -> str:
        pass

    def conjugate_all(self) -> Dict[str, Dict[str, Union[str, Dict[str, str]]]]:
        pass

    def is_valid(self) -> bool:
        pass
      
      
class VerbRo:
    def init(self, verb: str, subject: str):
        pass
      
    def conjugate(self, mood: str, tense: str, person: str) -> str:
        pass

    def conjugate_all(self) -> Dict[str, Dict[str, Union[str, Dict[str, str]]]]:
        pass

    def is_valid(self) -> bool:
        pass
      

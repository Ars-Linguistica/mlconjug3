class History:
    """
    A class that keeps track of the previously conjugated verbs and allows the user to access them easily.
    """
    def __init__(self):
        self.history = []

    def add_to_history(self, verb):
        """
        Add a verb to the conjugation history.
        :param verb: str. The verb to add to the history.
        """
        self.history.append(verb)

    def get_history(self):
        """
        Retrieve the conjugation history.
        :return: list. A list of the previously conjugated verbs.
        """
        return self.history

    def clear_history(self):
        """
        Clear the conjugation history.
        """
        self.history = []

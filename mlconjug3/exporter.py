class ConjugationExporter:
    """
    A class that exports conjugated verbs in different formats such as CSV or JSON.
    """
    def __init__(self, filename, format='csv'):
        """
        :param filename: str. The name of the file to export the conjugated verbs to.
        :param format: str. The format to export the conjugated verbs in. Default is 'csv'.
        """
        self.filename = filename
        self.format = format

    def export(self, conjugated_verbs):
        """
        Export the conjugated verbs to the specified file in the specified format.
        :param conjugated_verbs: list. A list of conjugated verbs.
        """
        if self.format == 'csv':
            self._export_csv(conjugated_verbs)
        elif self.format == 'json':
            self._export_json(conjugated_verbs)
        else:
            raise ValueError(f'Invalid export format: {self.format}')

    def _export_csv(self, conjugated_verbs):
        """
        Export the conjugated verbs to a CSV file.
        :param conjugated_verbs: list. A list of conjugated verbs.
        """
        # Code to export the conjugated verbs to a CSV file
        pass

    def _export_json(self, conjugated_verbs):
        """
        Export the conjugated verbs to a JSON file.
        :param conjugated_verbs: list. A list of conjugated verbs.
        """
        # Code to export the conjugated verbs to a JSON file
        pass

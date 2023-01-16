class ConjugationImporter:
    """
    A class that imports verbs from external sources such as a spreadsheet.
    """
   
    def __init__(self, filename, format='csv'):
        """
        Initialize the ConjugationImporter with the file name and format of the external source.
        :param filename: str. The file name of the external source.
        :param format: str. The format of the external source. Default is 'csv'.
        """
        self.filename = filename
        self.format = format
        
    def import_data(self):
       """
       Imports the data from the external source and returns it as a DataFrame.
       :return: pandas DataFrame. The imported data.
       """
       if self.format == 'csv':
           return pd.read_csv(self.filename)
       elif self.format == 'json':
           return pd.read_json(self.filename)
       else:
           raise ValueError('Invalid file format')
        


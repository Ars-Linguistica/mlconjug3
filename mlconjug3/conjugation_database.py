class ConjugationDatabase:
    def __init__(self):
        self.database = {}
        
    def load_data(self, data: dict):
        """
        Loads data into the database
        :param data: dict
        """
        self.database = data
        
    def update_data(self, data: dict):
        """
        Updates the existing data in the database
        :param data: dict
        """
        self.database.update(data)
        
    def search_data(self, key: str):
        """
        Search for a key in the database
        :param key: str
        :return: dict
        """
        if key in self.database:
            return self.database[key]
        return None

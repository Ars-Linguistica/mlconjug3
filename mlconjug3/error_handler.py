class ErrorHandler:
    """
    This class handles errors and exceptions in the package.
    """
    def __init__(self):
        pass
    
    def handle_error(self, error: Exception):
        """
        Handles errors and exceptions in the package.
        :param error: Exception. The error or exception that occurred.
        """
        error_type = type(error).__name__
        error_message = str(error)
        
        # Log the error
        logger.error(f"{error_type}: {error_message}")
        
        # Handle specific error types
        if error_type == "InvalidLanguageError":
            self._handle_invalid_language_error(error)
        elif error_type == "InvalidVerbError":
            self._handle_invalid_verb_error(error)
        elif error_type == "ModelError":
            self._handle_model_error(error)
        elif error_type == "ConjugationRuleError":
            self._handle_conjugation_rule_error(error)
        else:
            self._handle_general_error(error)
    
    def _handle_invalid_language_error(self, error: InvalidLanguageError):
        """
        Handles InvalidLanguageError.
        :param error: InvalidLanguageError. The error that occurred.
        """
        error_message = f"Invalid language: {error.language}. Please use one of the following languages: {_LANGUAGES}."
        print(error_message)
    
    def _handle_invalid_verb_error(self, error: InvalidVerbError):
        """
        Handles InvalidVerbError.
        :param error: InvalidVerbError. The error that occurred.
        """
        error_message = f"Invalid verb: {error.verb}. Please enter a valid verb infinitive."
        print(error_message)
        
    def _handle_model_error(self, error: ModelError):
        """
        Handles ModelError.
        :param error: ModelError. The error that occurred.
        """
        error_message = f"Model error: {error.message}. Please try again later or contact the package maintainer for assistance."
        print(error_message)
    
    def _handle_conjugation_rule_error(self, error: ConjugationRuleError):
        """
        Handles ConjugationRuleError.
        :param error: ConjugationRuleError. The error that occurred.
        """
        error_message = f"Conjugation rule error: {error.message}. Please contact the package maintainer for assistance."
        print(error_message)
        
    def _handle_general_error(self, error: Exception):
        """
        Handles general errors.
        :param error: Exception. The error that occurred.
        """
        error_message = f"An error occurred: {error}. Please contact the package maintainer for assistance."
        print(error_message)

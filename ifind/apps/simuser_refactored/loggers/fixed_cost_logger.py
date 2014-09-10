from loggers.base_logger import BaseLogger

class FixedCostLogger(BaseLogger):
    """
    
    """
    def __init__(self, time_limit=300):
        """
        Instantiates the BaseLogger class and sets up additional instance variables for the FixedCostLogger.
        Note that this does not enforce the time limit...
        """
        super(FixedCostLogger, self).__init__()
        
        #  Series of costs (in seconds) for each interaction that the user can perform; these are fixed.
        self.__query_cost = 10
        self.__document_cost = 20
        self.__snippet_cost = 3
        self.__serp_results_cost = 5
        self.__mark_document_cost = 3
        
        self.__total_time = 0  # An elapsed counter of the number of seconds a user has been interacting for.
        self.__time_limit = time_limit  # The maximum time that a user can search for in a session.
    
    def is_finished(self):
        """
        Concrete implementation of the is_finished() method from the BaseLogger.
        Returns True if the user has reached their search "allowance".
        """
        # Include the super().is_finished() call to determine if there are any queries left to process.
        return (not (self.__total_time < self.__time_limit)) or super(FixedCostLogger, self).is_finished()
    
    def _report(self, action):
        """
        Re-implementation of the _report() method from BaseLogger.
        Includes additional details in the message such as the total elapsed time, and maximum time available to the user after the action has been processed.
        """
        base = super(FixedCostLogger, self)._report(action)
        print "{0}{1} {2}".format(base, self.__time_limit, self.__total_time)
    
    def _log_query(self, **kwargs):
        """
        Concrete implementation of the _log_query() method from the BaseLogger.
        Increments the __total_time counter with the cost of issuing a query.
        """
        self.__total_time = self.__total_time + self.__query_cost
        self._report('Q')
    
    def _log_serp(self, **kwargs):
        """
        Concrete implementation of the _log_serp() method from the BaseLogger.
        Increments the __total_time counter with the cost of examining a SERP.
        """
        self.__total_time = self.__total_time + self.__serp_results_cost
        self._report('R')
    
    def _log_snippet(self, **kwargs):
        """
        A concrete implementation of the log_snippet() method from the BaseLogger.
        Increments __total_time to reflect the cost of examining a snippet.
        """
        self.__total_time = self.__total_time + self.__snippet_cost
        self._report('S')
    
    def _log_assess(self, **kwargs):
        """
        Concrete implementation for assessing a document at a fixed cost.
        """
        self.__total_time = self.__total_time + self.__document_cost
        self._report('D')
    
    def _log_mark_document(self, **kwargs):
        """
        Concrete implementation for marking a document as relevant as a fixed cost.
        """
        self.__total_time = self.__total_time + self.__mark_document_cost
        self._report('M')
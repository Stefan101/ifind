from loggers import Actions
from decision_makers.base_decision_maker import BaseDecisionMaker

class TotalNonrelDecisionMaker(BaseDecisionMaker):
    """
    A concrete implementation of a decision maker.
    Returns True iif the depth at which a user is in a SERP is less than a predetermined value.
    """
    def __init__(self, search_context, nonrelevant_threshold=3):
        super(TotalNonrelDecisionMaker, self).__init__(search_context)

        self.__nonrelevant_threshold = nonrelevant_threshold  # The threshold; get to this point, we stop in the current SERP.
        self.__counter = 0  # The total number of nonrelevant snippets that have been seen.

    def decide(self):
        """
        If the user's current position in the current SERP is < the maximum depth, look at the next snippet in the SERP.
        Otherwise, a new query should be issued.
        """
        examined_snippets = self._search_context.get_examined_snippets()
        examined_snippets.reverse()

        for snippet in examined_snippets:
            judgment = snippet.judgment

            if judgment == 0:
                self.__counter = self.__counter + 1  # Found something nonrelevant; increment counter

                if self.__counter == self.__nonrelevant_threshold:
                    self.__counter = 0  # Reset counter for the next query.
                    return Actions.QUERY

        # If we get here, we are okay - so we examine the next snippet.
        return Actions.SNIPPET
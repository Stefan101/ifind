from ifind.common.query_ranker import QueryRanker
from ifind.common.query_generation import SingleQueryGeneration
from query_generators.smarter_generator import SmarterQueryGenerator

class AdditionalQueryGenerator(SmarterQueryGenerator):
    """
    Implementing strategies four and five from Heikki's 2009 paper.
    Given n fixed query terms, we then append query terms to the end of the fixed query m times.
    Fixed terms are derived from the topic title, appended terms from the topic description.
    """
    def generate_query_list(self, topic):
        """
        Given a Topic object, produces a list of query terms that could be issued by the simulated agent.
        """
        self.__title_stem_length = 2
        self.__description_cutoff = 0
        
        topic_title = topic.title
        topic_description = topic.content
        topic_language_model = self._generate_topic_language_model(topic)
        
        # Generate a series of query terms from the title, and then rank the generated terms.
        title_generator = SingleQueryGeneration(minlen=3, stopwordfile=self._stopword_file)
        title_query_list = title_generator.extract_queries_from_text(topic_title)
        title_query_list = self._rank_terms(title_query_list, topic_language_model=topic_language_model)
        
        # Produce the title query "stem"
        title_stem = self.__get_title_stem(topic_language_model, title_query_list)
        
        # Perform the same steps, but from the description of the topic.
        description_generator = SingleQueryGeneration(minlen=3, stopwordfile=self._stopword_file)
        description_query_list = description_generator.extract_queries_from_text(topic_description)
        description_query_list = self._rank_terms(description_query_list, topic_language_model=topic_language_model)
        
        return self.__generate_permutations(topic_language_model, title_stem, description_query_list)
    
    def _rank_terms(self, terms, **kwargs):
        """
        Ranks the query terms by their discriminatory power.
        The length of the list returned == list of initial terms supplied.
        """
        topic_language_model = kwargs.get('topic_language_model', None)
        
        ranker = QueryRanker(smoothed_language_model=topic_language_model)
        ranker.calculate_query_list_probabilities(terms)
        return ranker.get_top_queries(len(terms))
    
    def __get_title_stem(self, topic_language_model, title_query_list):
        """
        Returns a string of query terms of the length of self.__title_stem_length terms.
        If this value is longer than the number of ranked query terms for the title, then the maximum is returned.
        """
        return_str = ""
        
        for i in range(0, self.__title_stem_length):
            if i+1 > len(title_query_list):
                break
            
            return_str = "{0} {1}".format(return_str, title_query_list[i][0])
        
        return_str = return_str.strip()
        return return_str
    
    def __generate_permutations(self, topic_language_model, title_stem, description_query_list):
        """
        Returns a list of queries based on the title stem, the description query term list, and the cutoff value.
        If self.__description_cutoff < 0, all description terms will be used.
        """
        return_terms = []
        cutoff_counter = 0
        
        for description_term in description_query_list:
            if self.__description_cutoff > 0 and cutoff_counter == self.__description_cutoff:
                break
            
            return_terms.append(('{0} {1}'.format(title_stem, description_term[0]), 0))
            cutoff_counter = cutoff_counter + 1
        
        return return_terms
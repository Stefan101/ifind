import os
import string
from lxml import etree
from collections import defaultdict
from xml.etree import cElementTree
from component_factory import ComponentFactory

class ConfigReaderError(Exception):
    """
    A special Exception which is raised when something is incorrect with the configuration file.
    """
    pass

class ConfigReader(object):
    """
    The configuration reader class.
    Checks the configuration file to see if it exists, is well formed, and the values supplied are legitimate.
    """
    def __init__(self, config_filename=None):
        self.__config_filename = config_filename
        self.__dtd_filename = 'config_reader/simulation_config.dtd'
        
        if self.__config_filename is None:
            raise ConfigReaderError("No configuration file specified.")
        else:
            self.__config_file = etree.parse(self.__config_filename)
        
        self.__validate_against_dtd()
        self.__build_dictionary()
        self.__validate_config()
        
        self.__components = ComponentFactory(self.__config_dict)
    
    def get_components_dictionary(self):
        """
        Returns a reference to the components dictionary.
        """
        return self.__components.get_objects()
    
    def __validate_against_dtd(self):
        """
        Parses the configuration file and checks its validity compared to the DTD specification.
        """
        # Opens the DTD file and loads it into a lxml DTD object.
        dtd_file = open(self.__dtd_filename, 'r')
        dtd_object = etree.DTD(dtd_file)
        
        # .validate() checks if the config file complies to the schema. If it doesn't, this condition is entered.
        if not dtd_object.validate(self.__config_file):
            dtd_file.close()
            raise ConfigReaderError("DTD validation failed on {0}: {1}".format(self.__config_filename,
                                                                               dtd_object.error_log.filter_from_errors()[0]))
        
        # If we get here, the validation passed, so we can close the DTD file object.
        dtd_file.close()
        
    def __build_dictionary(self):
        """
        Turns the XML configuration file into a Python dictionary object.
        The nested function recursive_generation() is unsurprisingly recursive.
        """
        def recursive_generation(t):
            """
            Recursive solution from http://stackoverflow.com/a/10077069 (2013-01-19)
            """
            d = {t.tag: {} if t.attrib else None}
            children = list(t)
            
            if children:
                dd = defaultdict(list)
                
                for dc in map(recursive_generation, children):
                    for k, v in dc.iteritems():
                        dd[k].append(v)
                
                d = {t.tag: {k:v[0] if len(v) == 1 else v for k, v in dd.iteritems()}}
            
            if t.attrib:
                d[t.tag].update(('@' + k, v) for k, v in t.attrib.iteritems())
            
            if t.text:
                text = t.text.strip()
                
                if children or t.attrib:
                    if text:
                        d[t.tag]['#text'] = text
                else:
                    d[t.tag] = text
            
            return d
        
        string_repr = etree.tostring(self.__config_file, pretty_print=True)
        element_tree = cElementTree.XML(string_repr)
        
        self.__config_dict = recursive_generation(element_tree)
        self.__config_dict = self.__config_dict[self.__config_dict.keys()[0]]
    
    def __validate_config(self):
        """
        Validates the contents of the configuration file - under the assumption that it is well formed and conforms to the DTD.
        Checks aspects such as the types of attributes, for example.
        """
        filesystem_exists_check(self.__config_dict['topic']['@filename'])
        
        def check_types(val):
            """
            Checks the types for a given attribute dictionary.
            """
            attribute_type = val['@type']
            val['@is_argument'] = parse_boolean(val['@is_argument'])
            
            if attribute_type == 'boolean':
                val['@value'] = parse_boolean(val['@value'])
            elif attribute_type == 'int':
                val['@value'] = int(val['@value'])
            elif attribute_type == 'float':
                val['@value'] = float(val['@value'])
        
        def validate_attributes(input_dict):
            """
            A recursive method to iterate through the configuration dictionary, validating each attribute.
            If a value does not match the expected type, an exception is raised.
            """
            for k, v in input_dict.iteritems():
                if isinstance(v, dict):
                    if k == 'attribute':
                        check_types(v)
                    else:
                        validate_attributes(v)
                else:
                    if k == 'attribute':
                        for entry in v:
                            check_types(entry)
        
        validate_attributes(self.__config_dict)

def parse_boolean(boolean_value):
	"""
	Given a string (boolean_value), returns a boolean value representing the string contents.
	For example, a string with 'true', 't', 'y' or 'yes' will yield True.
	"""
	boolean_value = string.lower(boolean_value) in ('yes', 'y', 'true', 't', '1')
	return boolean_value

def empty_string_check(string, raise_exception = True):
	"""
	Simple check to see if the string provided by parameter string is empty. False indicates that the string is NOT empty.
	Parameter raise_exception determines if a ValueError exception should be raised if the string is empty. If raise_exception is False and the string is empty, True is returned.
	"""
	if string != '':
		return False

	if raise_exception:
		raise ValueError("Empty string detected!")

	return True

def filesystem_exists_check(path, raise_exception = True):
	"""
	Checks to see if the path, specified by parameter path, exists. Can be either a directory or file. If the path exists, True is returned. If the path does not exist, and raise_exception is set to True, an IOError is raised - else False is returned.
	"""
	if os.path.lexists(path):
		return True

	if raise_exception:
		raise IOError("Could not find the specified path, %s." % (path))

	return False
from rdflib import Graph, RDF
from collections import defaultdict
from error import ValidationError
from vocabulary import DcatApVocab
import sys


if len(sys.argv) > 1:
    CATALOG = sys.argv[1]
else:
    print "Please provide an RDF graph URI as an argument."
    exit();

print "Obtaining RDF graph...\n"

graph = Graph()
graph.parse(CATALOG, format="turtle")


"""
Checks whether the graph contains instances of a (mandatory)
class as specified in DCAT-AP v1.1.

Args:
    graph: The rdflib.Graph to check.
    klass: The URIRef (representing an RDFS class) to check.

Returns:
    A defaultdict (errors) that contains error codes mapped to the resources that are not valid
    according to the DCAT-AP spec. For example:

    {'1': ('dcat.Catalog')}

    The error code signifies the type of the validation error, for more see ValidationError class.

"""
def check_mandatory_class(graph, klass):
    errors = defaultdict(list)
    if (None, None, klass) in graph:
        instances = graph.subjects(predicate=RDF.type, object=klass)
        if not instances:
            errors[ValidationError.ERROR_MANDATORY_CLASS_MISSING].append(klass) # No instances of a mandatory "klass" found

    return errors

"""
Checks whether all instances of a class have the mandatory properties defined in DCAT-AP

Args:
    graph: The rdflib.Graph to check.
    klass: The URIRef (representing an RDFS class) to check the presence of mandatory properties
    associated with this class.

Returns:
    A defaultdict (errors) that contains error codes mapped to the resources that are not valid
    according to the DCAT-AP spec. For example:

    {'11': ('dcat.dataset', 'dcat.Catalog')}

    The error code signifies the type of the validation error, for more see ValidationError class.

"""
def check_mandatory_properties(graph, klass):
    errors = defaultdict(list)
    if (None, None, klass) in graph:
        instances = graph.subjects(predicate=RDF.type, object=klass)
        for instance in instances:
            predicates = graph.predicates(subject=instance, object=None) # obtain predicates for each instance of klass
            for predicate in DcatApVocab.MANDATORY_PROPERTIES_FOR_CLASSES[klass]:
                if predicate not in predicates: # check if all mandatory predicates are found in the graph
                    errors[ValidationError.ERROR_MANDATORY_PROPERTY_FOR_CLASS_MISSING].append((predicate, klass))

    return errors


"""
Checks whether the graph follows the DCAT-AP regarding
the mandatory classes and properties for a given class.

Args:
    graph: The rdflib.Graph to check.
    klass: The URIRef (representing an RDFS class) to check the presence of mandatory properties
    associated with this class.

Returns:
    A combined list of error message that show where the validity breaks.

"""
def check_class_validity(graph, klass):
    errorList = []
    error_class = check_mandatory_class(graph, klass)
    errorList.extend(get_error_messages(error_class))
    error_property = check_mandatory_properties(graph, klass)
    errorList.extend(get_error_messages(error_property))

    return errorList

"""
Converts an error dict to a human readable message.

Args:
    error: A dictionary of errors and the respective resources.

Returns:
    A human readable sentence that shows where the graph breaks a DCAT-AP constraint.
"""
def get_error_messages(errors):
    errorList = []
    error = ValidationError()
    for key in errors:
        for resourceList in errors[key]:
            error_message = error.to_human_readable(key, resourceList)
            errorList.append(error_message)

    return errorList

"""Check if some mandatory classes defined in DCAT-AP are valid with respect to the spec.

Prints error messages to show where the validity breaks.
"""
for klass in DcatApVocab.MANDATORY_CLASSES:
    errors = check_class_validity(graph, klass)
    for message in set(errors):
        print (message)


print "\nValidation completed."

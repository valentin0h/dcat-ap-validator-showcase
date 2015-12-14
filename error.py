class ValidationError:
    ERROR_MANDATORY_CLASS_MISSING = 100;
    ERROR_MANDATORY_PROPERTY_FOR_CLASS_MISSING = 101;

    """
    Converts an error code and list of resource to a human readable message.

    Args:
        code: A dictionary of errors and the respective resources.
        resourceList: A list of resources that are not valid with respet to DCAT-AP

    Returns:
        A human readable sentence that shows where the graph breaks a DCAT-AP constraint.
    """
    def to_human_readable(self, code, resourceList):
        if (code == ValidationError.ERROR_MANDATORY_CLASS_MISSING):
            return "The mandatory class : %s is missing from your DCAT graph." % resourceList[0]
        elif (code == ValidationError.ERROR_MANDATORY_PROPERTY_FOR_CLASS_MISSING):
            return "One or more instance(s) of the mandatory class : %s has a missing property : %s in your DCAT graph." % (resourceList[1], resourceList[0])
from rdflib import Namespace

class DcatApVocab:

    # Namespaces
    DCAT = Namespace("http://www.w3.org/ns/dcat#")
    DCT = Namespace("http://purl.org/dc/terms/")

    MANDATORY_CLASSES = (DCAT.Catalog, DCAT.Dataset)

    MANDATORY_PROPERTIES_FOR_CLASSES = {
        DCAT.Catalog: (DCAT.dataset, DCAT.description, DCT.publisher, DCT.title),
        DCAT.Dataset: (DCAT.description, DCT.title)
    }

from xml.dom.minidom import parseString

class ProcessXML:
    """Parse an XML RSS feed and return the object.
    """
    def __init__(self, xml: str):
        """Class constructor

        Args:
            xml (str): The XML string to be parsedinto an XML object.
        """
        self.xml = xml


    def parse(self) -> object:
        """Parse the XML file into an object

        Returns:
            object: xml.dom.minidom.Document Class.
        """
        return parseString(self.xml)

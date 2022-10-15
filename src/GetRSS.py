##
# Links:
#   https://realpython.com/python-xml-parser/
#   https://docs.python.org/3/library/xml.dom.minidom.html#dom-example

from xml.dom.minidom import Node

class GetRSS:
    """Get the podcast data, from a podcast's RSS XML URL.

    Author:
        Gareth Palmer <bravdthepally@gmail.com>
    """
    def __init__(self, url: str):
        """Class Constructor.

        Args:
            url (str): The url to the RSS XML URL
        """
        import urllib.request
        fp = urllib.request.urlopen(url)
        mybytes = fp.read()
        self.raw = mybytes.decode("utf8")
        fp.close()

        from src.ProcessXML import ProcessXML
        self.xml = ProcessXML(self.raw)
        self.parsed_data = {}

        self.podcast_title = ''
        self.podcast_image = ''


    def print_xml(self):
        """Print out the raw XML text gathered from the URL.
        """
        print(self.raw)


    def _kill(self):
        """Kill the script immediately.
        """
        import sys
        sys.exit()


    def parse(self, limit:int=None):
        """Parse the RSS feed XML and gather out all relevant data.

        Args:
            limit (int, optional): Limit the number of episodes to record. Defaults to None.
        """

        self.parsed_xml = self.xml.parse()
        self._parse_channel_info()
        self._parse_links(limit)


    def _parse_channel_info(self) -> None:
        """Parse the basic channel info from the XML file.
        """
        channel_info = self.parsed_xml.getElementsByTagName('channel')[0]
        for item in list(channel_info.childNodes):
            if item.nodeType != Node.ELEMENT_NODE:
                continue
            if item.tagName == 'title':
                self.podcast_title = item.childNodes[0].data
            elif item.tagName == 'image':
                for tag in list(item.childNodes):
                    if tag.nodeType != Node.ELEMENT_NODE:
                        continue
                    if tag.tagName == 'url':
                        self.podcast_image = tag.childNodes[0].data
                        break


    def _parse_links(self, limit:int=None) -> None:
        """Get the links from an RSS XML file.

        Args:
            limit (int, optional): Limit the number of episodes to record. Defaults to None.
        """
        links = self.parsed_xml.getElementsByTagName('item')
        i = 0
        for link in links:
            i += 1
            for element in list(link.childNodes):
                if element.nodeType != Node.ELEMENT_NODE:
                    continue
                if element.tagName == 'title':
                    title = element.childNodes[0].data
                elif element.tagName == 'enclosure':
                    audio = list(element.attributes.values())[0].firstChild.data
                    duration = list(element.attributes.values())[1].firstChild.data
                elif element.tagName == 'link':
                    siteURL = element.childNodes[0].data
                elif element.tagName == 'pubDate':
                    timestamp = element.childNodes[0].data
                elif element.tagName == 'guid':
                    guid = element.childNodes[0].data
                
                try:
                    self.parsed_data[guid] = {
                        'title': title.strip(),
                        'audioLink': audio.strip(),
                        'duration': duration.strip(),
                        'siteURL': siteURL.strip(),
                        'published': timestamp.strip(),
                    }
                except UnboundLocalError:
                    # print(element)
                    pass
            if limit is not None and i == limit:
                break

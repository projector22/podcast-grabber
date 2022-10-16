class JSON:
    @staticmethod
    def dump_to_file(data: dict|list, file_name: str = 'results', pretty_print: bool = False) -> None:
        """Export a specified dictionary or list to a JSON file.

        Args:
            data (dict | list): The data to write to the JSON file
            file_name (str, optional): The name of the file to export to. Extension can be left off. Defaults to 'results'.
            pretty_print (bool, optional): Format the JSON to be more readable. False will leave the JSON at it's most compact. Defaults to False.
        """
        import json
        if file_name[-5:] != '.json':
            file_name = str(file_name) + '.json'
        with open(file_name, "w") as file:
            if pretty_print:
                json.dump(data, file, indent=4)
            else:
                json.dump(data, file)
        file.close()
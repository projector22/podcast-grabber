class JSON:
    def __init__(self, data: dict) -> None:
        self.data = data


    def write_file(self, file_name: str = 'results', pretty_print: bool = False) -> object:
        """Export the completed map to a JSON file.
        Args:
            file_name (str, optional): The name of the file to export to. Extension can be left off. Defaults to 'data'.
            pretty_print (bool, optional): Format the JSON to be more readable. False will leave the JSON at it's most compact. Defaults to False.
        Returns:
            object: self - used for method chaining.
        """
        import json
        if file_name[-5:] != '.json':
            file_name = str(file_name) + '.json'
        with open(file_name, "w") as file:
            if pretty_print:
                json.dump(self.data, file, indent=4)
            else:
                json.dump(self.data, file)
        file.close()
        return self

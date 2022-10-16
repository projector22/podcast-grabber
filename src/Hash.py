def md5(string_text: str) -> str:
    """Generate an MD5 table id.

    Args:
        string_text (str): The podcast title out of which the hash will be created.

    Returns:
        str: MD5 hash
    """
    import hashlib
    return hashlib.md5(string_text.encode()).hexdigest()
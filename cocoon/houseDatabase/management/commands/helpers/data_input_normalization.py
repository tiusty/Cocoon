def normalize_street_address(address):
    """
    Makes sure that the street address for all the providers have commas and period removed
    :param address: (string) -> The address for the house
    :return: (string) -> The address that has elements removed
    """
    return address.replace(',', '').replace('.', '')

def from_string(message):
    return message
    
def from_list(message):
    return '\n'.join(message)

def from_keys(dct, filter):
    return from_list([key for key in dct if key not in filter])

def from_values(dct, key):
    return from_list(dct[key]) if key in dct else ''
    

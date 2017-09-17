def from_string(message):
    return message
    
def from_list(message):
    if len(message) > 0 and isinstance(message[0], list):
        return from_list(message[0])
    return '\n'.join(message)

def with_dct(fn):
    def wrapped(dct, filter):
        return from_list([fn(dct, key) for key in dct if filter(key)])
    return wrapped
    
@with_dct
def from_keys(dct, key):
    return key

@with_dct
def from_values(dct, key):
    return dct[key]
    
def not_empty(fn):
    def wrapped(*arguments):
        return [x for x in fn(*arguments) if x != ""]
    return wrapped
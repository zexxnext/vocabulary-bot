def to_string(message):
    if isinstance(message, str):
        return message
    if len(message) > 0 and isinstance(message[0], list):
        return to_string(message[0])
    print(message)
    return '\n'.join(message)

def from_string(lst):
    return lst.split('\n')
    
    
def with_dct(fn):
    def wrapped(dct, filter):
        return to_string([fn(dct, key) for key in dct if filter(key)])
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
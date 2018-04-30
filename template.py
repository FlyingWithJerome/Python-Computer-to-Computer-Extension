'''
template.py

This module includes a template class to expand the
parsed program
'''

class Template(object):

    get_from_eval = \
    '''
    [
        (tokenize.NAME    , "{variable_name}"),
        (tokenize.N_TOKENS, "="),
        (tokenize.NAME    , "self"),
        (tokenize.N_TOKENS, "."),
        (tokenize.NAME    , "getfrom"),
        (tokenize.N_TOKENS, "("),
        (tokenize.STRING  , '"{host_name}"'),
        (tokenize.N_TOKENS, ","),
        (tokenize.STRING  , '"{pool_name}"'),
        (tokenize.N_TOKENS, ")")
    ]
    '''

    send_to_eval = \
    '''
    [
        (tokenize.NAME    , "self"),
        (tokenize.N_TOKENS, "."),
        (tokenize.NAME    , "sendto"),
        (tokenize.N_TOKENS, "("),
        (tokenize.STRING  , '"{host_name}"'),
        (tokenize.N_TOKENS, ","),
        (tokenize.STRING  , '"{variable_name}"'),
        (tokenize.N_TOKENS, ","),
        (tokenize.NAME    , "{variable_name}")
        (tokenize.N_TOKENS, ")")
    ]
    '''
'''
parser.py

This code implements the parser
'''
import os.path
import re
import sys
import tokenize

from io import StringIO, BytesIO

import template

class Parser(object):

    def __init__(self, source_code_path:str):

        tokens    = []
        file_name = os.path.basename(source_code_path)
        with open(source_code_path, "r") as source_code:
            source_raw = source_code.read()
            source_code_copy_str  = StringIO(source_raw)
            source_code_copy_byte = BytesIO(source_raw.encode("UTF-8"))

        source_code_iter = tokenize.tokenize(source_code_copy_byte.readline)

        for token_type, token_val, *_ in source_code_iter:
            if token_type == tokenize.COMMENT:
                temp_token_val = token_val[1:]
                res = Parser.parse_and_expand_instruction(temp_token_val)
                tokens.extend(res)
            else:
                tokens.append((token_type, token_val))

        source = tokenize.untokenize(tokens)

        with open("{}_parsed.py".format(file_name), "wb") as s:
            s.write(source)   

    @staticmethod
    def parse_and_expand_instruction(string_value) -> [(int, str)]:
        try:
            # parse getfrom
            if string_value.startswith("getfrom"):
                host_name, pool_name, var_name = Parser.parse_get_from(string_value)
                new_instruction = template.Template.get_from_eval
                new_instruction = new_instruction.format(host_name=host_name, pool_name=pool_name, variable_name=var_name)
                return eval(new_instruction.strip())
            
            # parse sendto
            elif string_value.startswith("sendto"):
                host, var = Parser.parse_send_to(string_value)
                new_instruction = template.Template.send_to_eval
                new_instruction = new_instruction.format(host_name=host, variable_name=var)
                return eval(new_instruction.strip())

            # parse broadcast
            elif string_value.startswith("broadcast"):
                host, var = Parser.parse_broadcast(string_value)
                new_instruction = template.Template.broadcast_eval
                new_instruction = new_instruction.format(variable_name=var)
                return eval(new_instruction.strip())

            # parse synchronize
            elif string_value.startswith("synchronize"):
                host, ser = Parser.parse_synchronize(string_value)
                new_instruction = template.Template.synchronize_eval
                new_instruction = new_instruction.format(host_name=host, serial_num=ser)
                return eval(new_instruction.strip())

            # parse getfrom_nonblock
            elif string_value.startswith("getfrom_nonblock"):
                host, ser = Parser.parse_synchronize(string_value)
                new_instruction = template.Template.getfrom_nonblock_eval
                new_instruction = new_instruction.format(host_name=host, serial_num=ser)
                return eval(new_instruction.strip())

            else:
                return [(tokenize.COMMENT, string_value),]

        except:
            return [(tokenize.COMMENT, string_value),]

    @staticmethod
    def parse_get_from(string):
        arguments =\
        string[len("getfrom("):-len(")")]

        [host, pool_name, variable_name] = arguments.split(",")
        return host.strip(), pool_name.strip(), variable_name.strip()

    @staticmethod
    def parse_get_from_nonblock(string):
        arguments =\
        string[len("getfrom("):-len(")")]

        [host, pool_name, variable_name] = arguments.split(",")
        return host.strip(), pool_name.strip(), variable_name.strip()
        
    @staticmethod
    def parse_send_to(string):
        arguments =\
        string[len("sendto("):-len(")")]

        [host, variable_name] = arguments.split(",")
        return host.strip(), variable_name.strip()
    
    @staticmethod
    def parse_synchronize(string):
        arguments =\
        string[len("syncrhonize("):-len(")")]

        [host, serial] = arguments.split(",")
        return host.strip(), serials.strip()

    @staticmethod
    def parse_broadcast(string):
        arguments =\
        string[len("broadcast("):-len(")")]

        [variable_name] = arguments.split(",")
        return variable_name.strip()
    
        

if __name__ == "__main__":
    p = Parser(sys.argv[1])
        


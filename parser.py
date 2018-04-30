'''
parser.py

This code implements the parser
'''
import re
import tokenize

from io import StringIO, BytesIO

import template

class Parser(object):

    def __init__(self, source_code_path:str):

        tokens = []
        with open(source_code_path, "r") as source_code:
            source_raw = source_code.read()
            source_code_copy_str  = StringIO(source_raw)
            source_code_copy_byte = BytesIO(source_raw.encode("UTF-8"))

        source_code_iter = tokenize.tokenize(source_code_copy_byte.readline)

        for token_type, token_val, *_ in source_code_iter:
            if token_type == tokenize.COMMENT:
                temp_token_val = token_val[1:]
                if temp_token_val.startswith("getfrom"):
                    print("extending")
                    res = Parser.parse_and_expand_instruction(temp_token_val)
                    tokens.extend(res)
            else:
                tokens.append((token_type, token_val))

        source = tokenize.untokenize(tokens)

        with open("parsed.py", "wb") as s:
            s.write(source)   

    #     expansion_info = []
    #     for (message), (start_row, start_col) in tokens:
    #         if message.startswith("getfrom"):
    #             host, variable = Parser.parse_get_from(message)
    #             expansion_info.append((message, start_row, start_col, host, variable))
    #         elif message.startswith("sendto"):
    #             host, variable = Parser.parse_send_to(message)
    #             expansion_info.append((message, start_row, start_col, host, variable))

    #     self.__expander(expansion_info)

    # def __expander(self, expansion_information):
    #     for exp in expansion_information:
    #         self.__expand_single_instruction(*exp)

    # def __expand_single_instruction(self, *expansion_info):
    #     assert len(expansion_info) > 3

    #     message, start_row, start_col, *metavar = expansion_info

    #     print(message)

    @staticmethod
    def parse_and_expand_instruction(string_value) -> [(int, str)]:
        try:
            if string_value.startswith("getfrom"):
                host_name, pool_name, var_name = Parser.parse_get_from(string_value)
                new_instruction = template.Template.get_from_eval
                new_instruction = new_instruction.format(host_name=host_name, pool_name=pool_name, variable_name=var_name)
                return eval(new_instruction.strip())
            
            elif string_value.startswith("sendto"):
                host, var = Parser.parse_send_to(string_value)
                new_instruction = template.Template.send_to_eval
                new_instruction = new_instruction.format(host_name=host, variable_name=var)
                return eval(new_instruction.strip())

        except AttributeError as e:
            print(e)
            return [string_value]

    @staticmethod
    def parse_get_from(string):
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
    def parse_block_until(string):
        raise NotImplementedError("waited to be implemented")
        

if __name__ == "__main__":
    p = Parser("sample_code.py")
        


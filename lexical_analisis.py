# Lexical analisis of the language "Psicoder" by using a state machine
import sys


class StringIs:
    def __init__(self, input_string):
        self.string = input_string
        self.real_row = row_counter - (len(buffer) - 1)

    def is_reserved_word(self):
        if self.string in reserved_words:
            print("<{},{},{}>".format(self.string, line_counter, self.real_row))

    def is_operator(self):
        if self.string in operator_tokens:
            print("<{},{},{}>".format(operator_tokens[self.string],
                                      line_counter, self.real_row))

    def is_identifier(self):
            print("<id,{},{},{}>".format(self.string, line_counter,
                                     self.real_row))

    def is_digit(self, digit_type):
        print("<tk_{},{},{},{}>".format(digit_type, self.string, line_counter,
                                     self.real_row))

    def is_error(self):
        print("Error lexico (linea: {}, posicion: {})".format(line_counter,
                                                              self.real_row))


class CharIs:
    def __init__(self, input_char):
        self.input_char = input_char

    @staticmethod
    def is_digit(input_char):
        if input_char.isdigit():
            return True
        else:
            return False

    @staticmethod
    def is_symbol(input_char):
        if input_char in operator_tokens:
            return True
        else:
            return False

    @staticmethod
    def is_empty(input_char):
        if input_char == "":
            return True
        else:
            return False

    @staticmethod
    def is_letter(input_char):
        if input_char.isalpha():
            return True
        else:
            return False

    @staticmethod
    def is_space(input_char):
        if input_char == " ":
            return True
        else:
            return False

    @staticmethod
    def is_endline(input_char):
        if input_char == "\n":
            return True
        else:
            return False

    def input_type(self):
        if self.is_endline(self.input_char):
            return "endline"
        elif self.is_digit(self.input_char):
            return "digit"
        elif self.is_empty(self.input_char):
            return "empty"
        elif self.is_letter(self.input_char):
            return "letter"
        elif self.input_char == "_":
            return "letter"
        elif self.is_symbol(self.input_char):
            return "symbol"
        elif self.is_space(self.input_char):
            return "space"
        elif self.input_char == "&" or self.input_char == "|":
            return "symbol"


class StateMachine:
    def __init__(self, input_char):
        global buffer
        self.char = input_char
        buffer += self.char
        self.char_type = CharIs(self.char).input_type()
        print(actual_state)
        if self.char_type is None:
            self.error_state()

    def go_to_actual_state(self):
        # go to the actual state
        if actual_state == "initial_state":
            self.initial_state()
        elif actual_state == "ignore_line_state":
            self.ignore_line_state()
        elif actual_state == "ignore_all_state":
            self.ignore_all_state()
        elif actual_state == "symbol_state":
            self.symbol_state()
        elif actual_state == "digit_state":
            self.digit_state()
        elif actual_state == "real_state":
            self.real_state()
        elif actual_state == "reserved_identifier_state":
            self.reserved_identifier_state()

    def initial_state(self):
        global actual_state
        if self.char_type == "digit":
            self.digit_state()
        elif self.char_type == "letter":
            self.reserved_identifier_state()
        elif self.char_type == "symbol":
            self.symbol_state()
        elif self.char_type == "space":
            self.ignore_state()
        elif self.char_type == "endline":
            if CharIs(buffer[0]).input_type() == "symbol":
                self.symbol_state()
            elif CharIs(buffer[0]).input_type() == "letter":
                self.reserved_identifier_state()
            elif CharIs(buffer[0]).input_type() == "digit":
                self.digit_state()
            elif actual_state == "real_state":
                self.real_state()
        else:
            self.error_state()

    # lots of repeated code, refactor please
    def symbol_state(self):
        global actual_state, buffer, row_counter

        if self.char_type == "space" and buffer[:-1] in operator_tokens:
            row_counter -= 1
            self.ignore_state()
            StringIs(buffer).is_operator()
            row_counter += 1
            actual_state = "initial_state"
            buffer = ""

        elif buffer in operator_tokens and len(buffer) > 1:
            StringIs(buffer).is_operator()
            actual_state = "initial_state"
            buffer = ""

        elif "//" in buffer:
            actual_state = "ignore_line_state"
        elif "/*" in buffer:
            actual_state = "ignore_all_state"

        elif "\n" in buffer:
            buffer = buffer.replace("\n", "")
            row_counter -= 1
            if "//" in buffer:
                actual_state = "ignore_line_state"
            elif "/*" in buffer:
                actual_state = "ignore_all_state"
            elif buffer in operator_tokens:
                StringIs(buffer).is_operator()
                actual_state = "initial_state"
                buffer = ""
            elif self.char_type == "space" and buffer[:-1] in operator_tokens:
                row_counter -= 1
                self.ignore_state()
                StringIs(buffer).is_operator()
                row_counter += 1
                actual_state = "initial_state"
                buffer = ""
            elif self.char_type == "letter":
                StringIs(buffer[:-1]).is_operator()
                actual_state = "reserved_identifier_state"
                buffer = buffer[-1]
            else:
                self.error_state()

        elif self.char_type == "letter":
            StringIs(buffer[:-1]).is_operator()
            actual_state = "reserved_identifier_state"
            buffer = buffer[-1]

        elif self.char_type == "digit":
            StringIs(buffer[:-1]).is_operator()
            actual_state = "digit_state"
            buffer = buffer[-1]
        elif self.char_type == "symbol":
            StringIs(buffer[:-1]).is_operator()
            actual_state = "symbol_state"
            buffer = buffer[-1]
        elif buffer not in operator_tokens:
            self.error_state()
        else:
            actual_state = "symbol_state"

    def reserved_identifier_state(self):
        global actual_state, buffer, row_counter

        if self.char_type == "space" and buffer[:-1] in reserved_words:
            row_counter -= 1
            self.ignore_state()
            StringIs(buffer).is_reserved_word()
            row_counter += 1
            buffer = ""
            actual_state = "initial_state"

        elif self.char_type == "space" and buffer[:-1] not in reserved_words:
            row_counter -= 1
            self.ignore_state()
            StringIs(buffer).is_identifier()
            row_counter += 1
            buffer = ""
            actual_state = "initial_state"

        elif "\n" in buffer:
            buffer = buffer.replace("\n", "")
            row_counter -= 1
            if buffer in reserved_words:
                StringIs(buffer).is_reserved_word()
                buffer = ""
                actual_state = "initial_state"
            elif self.char_type == "space" and buffer[:-1] in reserved_words:
                row_counter -= 1
                self.ignore_state()
                StringIs(buffer).is_reserved_word()
                row_counter += 1
                actual_state = "initial_state"
                buffer = ""
            else:
                StringIs(buffer).is_identifier()
                buffer = ""
                actual_state = "initial_state"

        elif self.char_type == "symbol":
            if buffer[:-1] in reserved_words:
                StringIs(buffer[:-1]).is_reserved_word()
                buffer = buffer[-1]
                actual_state = "symbol_state"
            else:
                StringIs(buffer[:-1]).is_identifier()
                buffer = buffer[-1]
                actual_state = "symbol_state"
        else:
            actual_state = "reserved_identifier_state"

    def digit_state(self):
        global actual_state, buffer, row_counter
        if self.char_type == "space":
            row_counter -= 1
            self.ignore_state()
            StringIs(buffer).is_digit("entero")
            row_counter += 1
            buffer = ""
            actual_state = "initial_state"

        elif "\n" in buffer:
            buffer = buffer.replace("\n", "")
            row_counter -= 1
            StringIs(buffer).is_digit("entero")
            buffer = ""
            actual_state = "initial_state"

        elif self.char_type == "symbol":
            if "." in buffer:
                actual_state = "real_state"
            else:
                StringIs(buffer[:-1]).is_digit("entero")
                buffer = buffer[-1]
                actual_state = "symbol_state"

        elif self.char_type == "letter":
            StringIs(buffer[:-1]).is_digit("entero")
            buffer = buffer[-1]
            actual_state = "reserved_identifier_state"

        else:
            actual_state = "digit_state"

    def real_state(self):
        global buffer, actual_state, row_counter

        if self.char_type == "space":
            row_counter -= 1
            self.ignore_state()
            if buffer[-1] == ".":
                StringIs(buffer[:-1]).is_digit("entero")
                row_counter += 1
                buffer = buffer[-1]
                actual_state = "symbol_state"
            if CharIs(buffer[-1]).input_type() == "digit":
                StringIs(buffer).is_digit("real")
                actual_state = "initial_state"
                buffer = ""

        elif "\n" in buffer:
            buffer = buffer.replace("\n", "")
            row_counter -= 1
            if CharIs(buffer[-1]).input_type() == "digit":
                StringIs(buffer).is_digit("real")
                actual_state = "initial_state"
                buffer = ""
            elif buffer[-1] == ".":
                StringIs(buffer[:-1]).is_digit("entero")
                buffer = buffer[-1]+"\n"
                self.symbol_state()

        elif self.char_type == "letter":
            if CharIs(buffer[-2]).input_type() == "digit":
                StringIs(buffer[:-1]).is_digit("real")
                buffer = buffer[-1]
            elif buffer[-2] == ".":
                StringIs(buffer[:-2]).is_digit("entero")
                StringIs(buffer[-2]).is_operator()
                buffer = buffer[-1]
            actual_state = "reserved_identifier_state"

        elif self.char_type == "symbol":
            if CharIs(buffer[-2]).input_type() == "digit":
                StringIs(buffer[:-1]).is_digit("real")
                buffer = buffer[-1]
            elif buffer[-2] == ".":
                StringIs(buffer[:-2]).is_digit("entero")
                StringIs(buffer[-2]).is_operator()
                buffer = buffer[-1]
            actual_state = "symbol_state"

        else:
            actual_state = "real_state"

    @staticmethod
    def ignore_state():
        global buffer, actual_state, row_counter
        buffer = buffer.replace(" ", "")

    def ignore_line_state(self):
        global actual_state, buffer
        buffer = ""
        actual_state = "ignore_line_state"
        if self.char_type == "endline":
            actual_state = "initial_state"

    @staticmethod
    def ignore_all_state():
        global actual_state, buffer
        if "*/" in buffer:
            buffer = ""
            actual_state = "initial_state"

    @staticmethod
    def error_state():
        global actual_state, buffer
        actual_state = "initial_state"
        StringIs(buffer).is_error()
        sys.exit()


actual_state = "initial_state"
buffer = ""
reserved_words = [
            "funcion_principal", "fin_principal", "booleano", "caracter",
            "entero", "real", "cadena", "leer", "imprimir", "si", "entonces",
            "fin_si", "si_no", "mientras", "hacer", "fin_mientras", "para",
            "hacer", "fin_para", "seleccionar", "entre", "caso", "romper",
            "defecto", "fin_seleccionar", "estructura", "fin_estructura",
            "funcion", "retornar", "fin_funcion", "falso", "verdadero"
        ]
operator_tokens = {
            "+": "tk_mas",
            "-": "tk_menos",
            "*": "tk_mult",
            "/": "tk_div",
            "%": "tk_mod",
            "=": "tk_asig",
            "<": "tk_menor",
            ">": "tk_mayor",
            "<=": "tk_menor_igual",
            ">=": "tk_mayor_igual",
            "==": "tk_igual",
            "&&": "tk_y",
            "||": "tk_o",
            "!=": "tk_dif",
            "!": "tk_neg",
            ":": "tk_dosp",
            ";": "tk_pyc",
            ",": "tk_coma",
            ".": "tk_punto",
            "(": "tk_par_izq",
            ")": "tk_par_der",
            "'": "tk_comilla_sen",
            '"': "tk_comilla_dob",
        }

if __name__ == "__main__":
    line_counter = 1
    row_counter = 0
    while True:
        if actual_state == "ignore_all_state":
            actual_state = "ignore_all_state"
        char = sys.stdin.readline(1)
        if char == "":
            break
        row_counter += 1
        #print(buffer, actual_state)
        if char == "ñ" or char == "Ñ":
            StateMachine(char).error_state()
        else:
            StateMachine(char).go_to_actual_state()
        if char == "\n":
            line_counter += 1
            row_counter = 0
            buffer = ""



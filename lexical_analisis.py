# Lexical analisis of the language "Psicoder" by using a state machine

# class StartsLetterNumOperator:
class StringIs:
    def __init__(self, input_buffer):

        self.buffer = input_buffer

        self.reserved_words = [
            "funcion_principal", "fin_principal", "booleano", "caracter",
            "entero", "real", "cadena", "leer", "imprimir", "si", "entonces",
            "fin_si", "si_no", "mientras", "hacer", "fin_mientras", "para",
            "hacer", "fin_para", "seleccionar", "entre", "caso", "romper",
            "defecto", "fin_seleccionar", "estructura", "fin_estructura",
            "funcion", "retornar", "fin_funcion", "falso", "verdadero"
        ]

        self.operator_tokens = {
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
        }

    def is_reserved_word(self):
        if self.buffer in self.reserved_words:
            return 1, self.buffer
        else:
            return 0

    def is_operator(self):
        if self.buffer in self.operator_tokens:
            return 1, self.operator_tokens[self.buffer]
        else:
            return 0
'''
class AnalysisStates:
    def __init__(self):
        #
    def state_machine(self):
'''
if __name__ == "__main__":
    buffer = "falso"
    buffer_obj = StringIs(buffer)
    print(buffer_obj.is_reserved_word())
    print(buffer_obj.is_operator())


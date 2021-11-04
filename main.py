# coding=utf-8
import io

# Terminals
METKI = "метки"
SEMICOLON = ";"
DIGITS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

dump = []


def is_digit(token):
    return token in DIGITS


def is_int(token):
    for elem in token:
        if not (is_digit(elem)):
            return False
    return True


def is_float(tokens):
    if len(tokens) != 3:
        return False
    if not (is_int(tokens[0]) and is_int(tokens[2])):
        return False
    return True


def definition(tokens):
    print(tokens[0])
    if tokens[0] == METKI:
        dump.append(tokens.remove("метки"))
    else:
        raise Exception("Определение должно начинаться с ")
    while True:
        float_token = tokens[:3]
        dump.append(float_token)
        tokens[:3] = []
        if is_float(float_token) is False:
            err_token = "".join(float_token)
            err_msg = "Ошибка в " + err_token + " . После 'метки' должны быть вещественные числа"
            raise Exception(err_msg)




def operator(tokens):
    pass


def _set(tokens):
    pass


if __name__ == "__main__":
    user_input = io.open(file="syntax.txt", mode="r", encoding="utf-8").readline().encode("utf-8").split()

    definition(user_input)
    operator(user_input)
    _set(user_input)

# coding=utf-8
import io
import sys

global right_hand

# Terminals
EQUALS = "="
MINUS = "-"
PLUS = "+"
LEFT_ROUND_BRACKET = "("
RIGHT_ROUND_BRACKET = ")"
LEFT_SQUARE_BRACKET = "["
RIGHT_SQUARE_BRACKET = "]"
DEGREE = "^"
MULT = "*"
DIV = "/"

METKI = "метки"
SEMICOLON = ";"
COLON = ":"
DIGITS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"]
LITERALS = ["А", "Б", "В", "Г", "Д", "Е", "Ё", "Ж", "З", "И", "Й", "К", "Л", "М", "Н", "О", "П", "Р", "С", "Т", "У", "Ф", "Х", "Ц", "Ч", "Ш", "Щ", "Ъ", "Ы", "Ь", "Э", "Ю", "Я", "а", "б", "в", "г", "д", "е", "ё", "ж", "з", "и", "й", "к", "л", "м", "н", "о", "п", "р", "с", "т", "у", "ф", "х", "ц", "ч", "ш", "щ", "ъ", "ы", "ь", "э", "ю", "я"]

dump = []


def get_next_token(tokens, number):
    if number == 1:
        try:
            result = tokens.pop(0)
        except IndexError:
            print("<конец строки>")
            return None
        dump.append(result)
    else:
        result = tokens[:number]
        dump.append(result)
        tokens[:number] = []
    return result


def is_letter(token):
    return token in LITERALS


def is_var(token):
    for i in range(0, len(token)):
        current = token[i]
        if i == 0 and (is_letter(current) is False):
            err_msg = "Ошибка при обработке Оператора. " + current + ". Переменная должна начинаться с буквы"
            return False
            # raise Exception(err_msg)
        elif (is_letter(current) or is_digit(current)) is False:
            err_msg = "Ошибка при обработке Оператора. " + current + ". Переменная должна содержать или рус. буквы, или 16-тиричные цифры"
            return False
            # raise Exception(err_msg)
    return True


def is_digit(token):
    return token in DIGITS


def is_int(token):
    for elem in token:
        if not (is_digit(elem)):
            return False
    return True


def is_float(token):
    token = token.split('.')
    if (len(token) != 2) or (is_int(token[0]) is False) or (is_int(token[1]) is False):
        return False
    return True


def definition(tokens):
    next_token = get_next_token(tokens, 1)
    if next_token != METKI:
        raise Exception("Ошибка при обработке Определения. " + next_token + " . Определение должно начинаться с " + METKI)
    while True:
        next_token = get_next_token(tokens, 1)
        if is_float(next_token) is False:
            err_token = "".join(next_token)
            err_msg = "Ошибка при обработке Определения. " + err_token + " . После 'метки' должны быть вещественные числа"
            raise Exception(err_msg)
        next_token = get_next_token(tokens, 1)
        if next_token != SEMICOLON:
            tokens.insert(0, next_token)
            break


def operator(tokens):
    next_token = get_next_token(tokens, 1)
    is_metka = False
    if is_int(next_token) is True:
        is_metka = True
        next_token = get_next_token(tokens, 1)
        if next_token != COLON:
            err_msg = "Ошибка при обработке Оператора. " + next_token + " . После Метки ожидался символ \'" + COLON + "\'"
            raise Exception(err_msg)
        next_token = get_next_token(tokens, 1)
    if is_var(next_token) is False:
        if is_metka is True:
            raise Exception("Ошибка при обработке Оператора. " + next_token + " . После метки \":\" ожидалась переменная")
        else:
            raise Exception("Ошибка при обработке Оператора. Получен \'" + next_token + "\' . Ожидалась переменная")
    next_token = get_next_token(tokens, 1)
    if next_token != EQUALS:
        err_msg = "Ошибка при обработке Оператора. После переменной ожидалось \'=\'"
        raise Exception(err_msg)
    return get_next_token(tokens, 1)


def block_3(tokens, next_token):
    if next_token is None:
        err_msg = "Ошибка при обработке Правой части. После операнда отсутствует оператор."
        raise Exception(err_msg)
    elif is_var(next_token):
        return get_next_token(tokens, 1)
    elif is_float(next_token):
        return get_next_token(tokens, 1)
    elif next_token == LEFT_ROUND_BRACKET:
        pass
    elif next_token == LEFT_SQUARE_BRACKET:
        pass
    else:
        raise Exception("Ошибка при обработке Правой части.")


def block_2(tokens, next_token):
    next_token = block_3(tokens, next_token)
    while True:
        if next_token != DEGREE:
            return next_token
        next_token = get_next_token(tokens, 1)
        next_token = block_3(tokens, next_token)


def block_1(tokens, next_token):
    next_token = block_2(tokens, next_token)
    while True:
        if next_token != MULT and next_token != DIV:
            return next_token
        next_token = get_next_token(tokens, 1)
        next_token = block_2(tokens, next_token)


def right_part(tokens, next_token):
    if next_token == MINUS:
        next_token = get_next_token(tokens, 1)
    while True:
        next_token = block_1(tokens, next_token)
        if next_token is None:
            return
        elif next_token != PLUS and next_token != MINUS:
            raise Exception
        next_token = get_next_token(tokens, 1)


def _set(tokens):
    pass


if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('utf-8')

    s = "метки 5.67 ; 1.22 567 : А13121 = 5.1 + 2.1 * 1.0 [ ( 4.1 * 1.1 ) ]"
    user_input = s.decode().split()

    definition(user_input)
    a = operator(user_input)
    right_part(user_input, a)
    _set(user_input)

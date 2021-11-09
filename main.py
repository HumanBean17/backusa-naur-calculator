# coding=utf-8
import io
import sys

# Terminals
METKI = "метки"
SEMICOLON = ";"
COLON = ":"
DIGITS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"]
LITERALS = ["А", "Б", "В", "Г", "Д", "Е", "Ё", "Ж", "З", "И", "Й", "К", "Л", "М", "Н", "О", "П", "Р", "С", "Т", "У", "Ф", "Х", "Ц", "Ч", "Ш", "Щ", "Ъ", "Ы", "Ь", "Э", "Ю", "Я", "а", "б", "в", "г", "д", "е", "ё", "ж", "з", "и", "й", "к", "л", "м", "н", "о", "п", "р", "с", "т", "у", "ф", "х", "ц", "ч", "ш", "щ", "ъ", "ы", "ь", "э", "ю", "я"]

dump = []


def get_next_token(tokens, number):
    if number == 1:
        result = tokens.pop(0)
        dump.append(result)
    else:
        result = tokens[:number]
        dump.append(result)
        tokens[:number] = []
    return result


def is_letter(token):
    return token in LITERALS


def is_var(token):
    result = False
    for i in range(0, len(token)):
        current = token[i]
        if i == 0 and (is_letter(current) is False):
            err_msg = "Ошибка при обработке Оператора. " + current + ". Переменная должна начинаться с буквы"
            raise Exception(err_msg)
        elif (is_letter(current) or is_digit(current)) is False:
            err_msg = "Ошибка при обработке Оператора. " + current + ". Переменная должна содержать или рус. буквы, или 16-тиричные цифры"
            raise Exception(err_msg)
        result = True
    return result


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


def _set(tokens):
    pass


if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('utf-8')

    s = "метки 5.67 ; 1.22 567 : А13121 = 5.1 + 2.1 * [ ( 4.1 * 1.1 ) ]"
    user_input = s.decode().split()

    definition(user_input)
    operator(user_input)
    _set(user_input)

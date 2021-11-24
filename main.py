# coding=utf-8
import Tkinter as tk
from tkinter import font as tkFont
import sys


global k
k = 1


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

METKI = "\"Метки\""
ANALIZ = "\"Анализ\""

SEMICOLON = ";"
COLON = ":"
COMMA = ","

DIGITS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"]
LITERALS = ["А", "Б", "В", "Г", "Д", "Е", "Ё", "Ж", "З", "И", "Й", "К", "Л", "М", "Н", "О", "П", "Р", "С", "Т", "У", "Ф", "Х", "Ц", "Ч", "Ш", "Щ", "Ъ", "Ы", "Ь", "Э", "Ю", "Я", "а", "б", "в", "г", "д", "е", "ё", "ж", "з", "и", "й", "к", "л", "м", "н", "о", "п", "р", "с", "т", "у", "ф", "х", "ц", "ч", "ш", "щ", "ъ", "ы", "ь", "э", "ю", "я"]

dump = []


def get_next_token(tokens, number):
    if number == 1:
        try:
            result = tokens.pop(0)
        except IndexError:
            err_msg = "<конец строки>"
            raise Exception(err_msg)
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

######################################################


def definition(tokens):
    next_token = get_next_token(tokens, 1)
    while True:
        if next_token != METKI:
            err_msg = "Ошибка при обработке Определения. Получено \'" + next_token + "\' . Определение должно начинаться с \'" + METKI + "\'"
            raise Exception(err_msg)
        while True:
            next_token = get_next_token(tokens, 1)
            if is_float(next_token) is False:
                err_msg = "Ошибка при обработке Определения. Получено \'" + next_token + "\' . Ожидалось \'" + METKI + "\'"
                raise Exception(err_msg)
            next_token = get_next_token(tokens, 1)
            if next_token != SEMICOLON:
                break
        if next_token != METKI:
            return next_token

######################################################


def operator(tokens, next_token):
    while True:
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
                err_msg = "Ошибка при обработке Оператора. После Метки \':\' ожидалась переменная. Получено: \'" + next_token + "\'"
                raise Exception(err_msg)
            else:
                err_msg = "Ошибка при обработке Оператора. Ожидалась переменная. Получено \'" + next_token + "\'"
                raise Exception(err_msg)
        next_token = get_next_token(tokens, 1)
        if next_token != EQUALS:
            err_msg = "Ошибка при обработке Оператора. После переменной ожидалось \'=\'"
            raise Exception(err_msg)
        next_token = right_part(tokens, get_next_token(tokens, 1))
        if next_token == ANALIZ:
            return next_token


def block_3(tokens, next_token):
    global k
    if next_token is None:
        err_msg = "Ошибка при обработке Правой части. После операнда отсутствует оператор."
        raise Exception(err_msg)
    elif is_var(next_token):
        return get_next_token(tokens, 1)
    elif is_float(next_token):
        return get_next_token(tokens, 1)
    elif next_token == LEFT_ROUND_BRACKET:
        next_token = get_next_token(tokens, 1)
        next_token = right_part(tokens, next_token)
        if next_token != RIGHT_ROUND_BRACKET:
            err_msg = "Ошибка при обработке правой части. Отсутствует " + "\')\'" + ". Получено \'" + str(next_token) + "\'"
            raise Exception(err_msg)
        return get_next_token(tokens, 1)
    elif next_token == LEFT_SQUARE_BRACKET:
        if k > 2:
            err_msg = "Ошибка при обработке правой части. Получена глубина вложенности квадратных скобок > 2."
            raise Exception(err_msg)
        k += 1
        next_token = get_next_token(tokens, 1)
        next_token = right_part(tokens, next_token)
        k = 1
        if next_token != RIGHT_SQUARE_BRACKET:
            err_msg = "Ошибка при обработке правой части. Отсутствует " + "\']\'" + ". Получено \'" + str(next_token) + "\'"
            raise Exception(err_msg)
        return get_next_token(tokens, 1)
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
            return next_token
        next_token = get_next_token(tokens, 1)

######################################################


def _set(tokens, next_token):
    while True:
        if next_token != ANALIZ:
            err_msg = "Ошибка при обработке Множества. Получено \'" + next_token + "\'. Ожидалось \'" + ANALIZ + "\'"
            raise Exception(err_msg)
        next_token = get_next_token(tokens, 1)
        while True:
            if is_int(next_token) is False:
                err_msg = "Ошибка при обработке Множества. Получено \'" + next_token + "\'. Ожидалось целое число"
                raise Exception(err_msg)
            next_token = get_next_token(tokens, 1)
            if next_token != COMMA and next_token != ANALIZ:
                err_msg = "Ошибка при обработке Множества. Получено \'" + next_token + "\'. Ожидался символ \'" + COMMA + "\' или <конец строки>"
                raise Exception(err_msg)
            elif next_token == ANALIZ:
                break
            next_token = get_next_token(tokens, 1)


def start_parse():
    user_input = text_edit.get(0.1, tk.END).decode().split()
    try:
        nt = definition(user_input)
        nt = operator(user_input, nt)
        _set(user_input, nt)
    except Exception as e:
        print(e.message)
        output.configure(state=tk.NORMAL)
        output.delete(0.1, tk.END)
        output.insert(0.1, e.message)
        output.configure(state=tk.DISABLED)
        # v.set(e.message)
        return e.message


if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('utf-8')

    root = tk.Tk()
    root.resizable(False, False)
    root.title("BNF")
    root.geometry("1200x700")

    helv36 = tkFont.Font(family='Courier New', size=14)
    text_edit = tk.Text(root, borderwidth=0.5, wrap=tk.WORD, relief=tk.SOLID)
    text_edit['font'] = helv36
    text_edit.place(relx=0.26, rely=0.37, anchor="c", height=500, width=600, bordermode=tk.OUTSIDE)

    bnf = "Язык = Определение … Определение Опер … Опер Множество … Множество\n" \
          "Определение = «Метки» Вещ “;” … Вещ\n" \
          "Опер = </ Метка “:”/> Перемен. “=” Прав. Часть\n" \
          "Множество = «Анализ» Цел “,” … Цел\n" \
          "Прав_Часть = </“-“/> Блок_1 Знак_1 … Блок_1\n" \
          "Знак_1 = “+” ! “-“\n" \
          "Блок_1 = Блок_2 Знак_2 … Блок_2\n" \
          "Знак_2 = “*” ! “/”\n" \
          "Блок_2 = Блок_3 “^” … Блок_3\n" \
          "Блок_3 = Перемен. ! Вещ. ! “(“ Прав_Часть “)” ! “[“ Прав_Часть “]” вложенность = 2\n" \
          "Метка = Цел\n" \
          "Перемен. = Буква </ Буква!Цифра … Буква!Цифра/>\n" \
          "Вещ. = Цел “.” Цел\n" \
          "Цел = Цифра…Цифра\n" \
          "Буква = “А” ! “Б” ! … “Я”\n" \
          "Цифра = “0” ! “!” … “F”"
    label = tk.Label(root, text=bnf, font="14", justify=tk.LEFT)
    label.place(relx=0.53, rely=0.039)

    btn = tk.Button(root, text="Run", command=start_parse)
    btn.place(relx=0.7, rely=0.5, width=200)

    # v = tk.StringVar()
    output = tk.Text(root, borderwidth=0.5, state=tk.DISABLED, relief=tk.SOLID)
    output.place(relx=0.013, rely=0.8, height=100, width=1150, bordermode=tk.OUTSIDE)

    root.mainloop()

    # инфо о русских буквах



# coding=utf-8
import Tkinter as tk
import re
import sys

from tkinter import font as tkFont

SKIP_PATTERNS = [
    ur"^\n+",
    ur"^ ",
    ur"^\t+"
]

PATTERNS = [
    ur"^EXPR",
    ur"^Метки",
    ur"^Анализ",
    ur"^\d+\.\d+",
    ur"^\d+",
    ur"^[а-яА-ЯеЁ](\d+|[а-яА-ЯеЁ]+)*",
    ur"^\+",
    ur"^\-",
    ur"^\*",
    ur"^\/",
    ur"^\=",
    ur"^\,",
    ur"^\;",
    ur"^\:",
    ur"^\[",
    ur"^\]",
    ur"^\(",
    ur"^\)"
]

global prev_token, current_token, idx, variables, k, err_code, global_input

is_error = True
current_token = None
idx = 0
global_input = []
err_code = ""
k = 1
variables = dict()

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

METKI = "Метки"
ANALIZ = "Анализ"

SEMICOLON = ";"
COLON = ":"
COMMA = ","

DIGITS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"]
LITERALS = ["А", "Б", "В", "Г", "Д", "Е", "Ё", "Ж", "З", "И", "Й", "К", "Л", "М", "Н", "О", "П", "Р", "С", "Т", "У", "Ф", "Х", "Ц", "Ч", "Ш", "Щ", "Ъ", "Ы", "Ь", "Э", "Ю", "Я", "а", "б", "в", "г", "д", "е", "ё", "ж", "з", "и", "й", "к", "л", "м", "н", "о", "п", "р", "с", "т", "у", "ф", "х", "ц", "ч", "ш", "щ", "ъ", "ы", "ь", "э", "ю", "я"]

TOKENS = [EQUALS, MINUS, PLUS, LEFT_ROUND_BRACKET, RIGHT_ROUND_BRACKET, LEFT_ROUND_BRACKET, RIGHT_SQUARE_BRACKET, DEGREE, MULT, DIV, METKI, SEMICOLON, COLON, COMMA] + DIGITS + LITERALS

dump = []


def get_next_token(tokens, number):
    global is_error, current_token, idx, variables

    if number == 1:
        try:
            result = tokens.pop(0)
            current_token = result
            idx += 1
        except IndexError:
            err_msg = ""
            lst = []
            for var in variables:
                lst.append(var + " = " + str(variables[var]))
            lst.reverse()
            for elem in lst:
                err_msg += elem + "\n"
            is_error = False
            raise Exception(err_msg)
        dump.append(result)
    else:
        result = tokens[:number]
        dump.append(result)
        tokens[:number] = []
    return result


def is_letter(token):
    global err_code
    if token not in LITERALS:
        err_code = "Содержит символы не из русского алфавита."
        return False
    return True


def is_var(token):
    global err_code
    if token == METKI or token == ANALIZ:
        return False
    for i in range(0, len(token)):
        current = token[i]
        if i == 0 and (is_letter(current) is False):
            err_code = "Переменная должна начинаться с буквы рус. алфавита."
            return False
            # raise Exception(err_msg)
        elif (is_letter(current) or is_digit(current)) is False:
            err_code = "Переменная должна содержать или рус. буквы, или 16-тиричные цифры."
            return False
            # raise Exception(err_msg)
    return True


def is_digit(token):
    global err_code
    if token not in DIGITS:
        err_code = "Язык поддерживает только цифры 16-тиричной арифметики."
        return False
    return True


def is_int(token):
    global err_code
    for elem in token:
        if not (is_digit(elem)):
            err_code = "Целое число должно состоять из 16-тиричных цифр."
            return False
    return True


def is_float(token):
    global err_code
    token = token.split('.')
    if (len(token) != 2) or (is_int(token[0]) is False) or (is_int(token[1]) is False):
        err_code = "Вещественное число должно состоять из целых чисел разделенных точкой."
        return False
    return True

######################################################


def definition(tokens):
    global err_code
    next_token = get_next_token(tokens, 1)
    while True:
        if next_token != METKI:
            err_msg = "Ошибка при обработке Определения . Определение должно начинаться с \'" + METKI + "\'. Получено \'" + next_token + "\'. "
            raise Exception(err_msg)
        while True:
            next_token = get_next_token(tokens, 1)
            if is_float(next_token) is False:
                if is_int(next_token) is True:
                    err_msg = "Ошибка при обработке Определения. Ожидалось вещественное число. Получено целое число \'" + next_token + "\'. " + err_code
                    raise Exception(err_msg)
                elif is_var(next_token) is True:
                    err_msg = "Ошибка при обработке Определения. Ожидалось вещественное число. Получена переменная \'" + next_token + "\'. " + err_code
                    raise Exception(err_msg)
                else:
                    err_msg = "Ошибка при обработке Определения. Ожидалось вещественное число. Получено \'" + next_token + "\'. " + err_code
                    raise Exception(err_msg)
            next_token = get_next_token(tokens, 1)
            if next_token != SEMICOLON:
                break
        if next_token != METKI and is_float(next_token) is True:
            err_msg = "Ошибка при обработке определения. Пропущен разделитель \'" + SEMICOLON + "\'"
            raise Exception(err_msg)
        elif next_token != METKI:
            return next_token

######################################################


def operator(tokens, next_token):
    global variables, err_code

    first_iter = True
    while True:
        is_metka = False
        if not first_iter:
            if is_float(next_token):
                err_msg = "Ошибка при обработке правой части. Пропущен знак действия."
                raise Exception(err_msg)
        if is_int(next_token) is True:
            is_metka = True
            next_token = get_next_token(tokens, 1)
            if next_token != COLON:
                err_msg = "Ошибка при обработке Оператора. После Метки ожидалось \'" + COLON + "\'. Получено " + next_token + ". "
                raise Exception(err_msg)
            next_token = get_next_token(tokens, 1)
        if is_var(next_token) is False:
            if is_metka is True:
                err_msg = "Ошибка при обработке Оператора. После Метки \':\' ожидалась Переменная. Получено: \'" + next_token + "\'. " + err_code
                raise Exception(err_msg)
            else:
                err_msg = "Ошибка при обработке Оператора. Ожидалась Переменная или Метка. Получено \'" + next_token + "\'. " + err_code
                raise Exception(err_msg)
        current_var = next_token
        variables[current_var] = None
        next_token = get_next_token(tokens, 1)
        if next_token != EQUALS:
            err_msg = "Ошибка при обработке Оператора. После переменной ожидалось \'=\'. "
            raise Exception(err_msg)
        next_token, rp = right_part(tokens, get_next_token(tokens, 1))
        first_iter = False
        variables[current_var] = rp
        if next_token == ANALIZ:
            return next_token


def block_3(tokens, next_token):
    global k, variables, err_code, prev_token

    if next_token is None:
        err_msg = "Ошибка при обработке Правой Части. После операнда отсутствует оператор. " + err_code
        raise Exception(err_msg)
    elif is_var(next_token):
        if next_token not in variables:
            err_msg = "Ошибка при обработке Правой Части. Переменная \'" + next_token + "\' не определена"
            raise Exception(err_msg)
        b3 = float(variables[next_token])
        return get_next_token(tokens, 1), b3
    elif is_float(next_token):
        b3 = float(next_token)
        return get_next_token(tokens, 1), b3
    elif next_token == LEFT_ROUND_BRACKET:
        next_token = get_next_token(tokens, 1)
        next_token, rp = right_part(tokens, next_token)
        if next_token != RIGHT_ROUND_BRACKET:
            err_msg = "Ошибка при обработке Правой Части. Отсутствует " + "\')\'" + ". Получено \'" + str(next_token) + "\'"
            raise Exception(err_msg)
        return get_next_token(tokens, 1), rp
    elif next_token == LEFT_SQUARE_BRACKET:
        if k > 2:
            err_msg = "Ошибка при обработке Правой Части. Получена глубина вложенности квадратных скобок > 2."
            raise Exception(err_msg)
        k += 1
        next_token = get_next_token(tokens, 1)
        next_token, rp = right_part(tokens, next_token)
        k = 1
        if next_token != RIGHT_SQUARE_BRACKET:
            err_msg = "Ошибка при обработке Правой Части. Отсутствует " + "\']\'" + ". Получено \'" + str(next_token) + "\'"
            raise Exception(err_msg)
        return get_next_token(tokens, 1), rp
    elif is_int(next_token):
        err_msg = "Ошибка при обработке Правой Части. Ожидалось вещественное число, переменная или круглая/квадратная скобка. Получено целое число \'" + str(next_token) + "\'. " + err_code
        raise Exception(err_msg)
    else:
        err_msg = "Ошибка при обработке Правой Части."
        if next_token in [MINUS, PLUS, DIV, MULT, DEGREE]:
            err_msg += " Два знака действия подряд."
        # elif next_token
        err_msg += " Ожидалось вещественное число или скобка. Получено \'" + str(next_token) + "\'. " + err_code
        raise Exception(err_msg)


def block_2(tokens, next_token):
    # global b2, b3
    next_token, b3 = block_3(tokens, next_token)
    b2 = b3
    while True:
        if next_token != DEGREE:
            return next_token, b2
        next_token, b3 = block_3(tokens, get_next_token(tokens, 1))
        b2 = b2 ** b3


def block_1(tokens, next_token):
    global current_token
    next_token, b2 = block_2(tokens, next_token)
    b1 = b2
    while True:
        if next_token != MULT and next_token != DIV:
            return next_token, b1
        sign = next_token
        next_token, b2 = block_2(tokens, get_next_token(tokens, 1))
        if sign == MULT:
            b1 *= b2
        elif sign == DIV:
            if b2 != 0.0:
                b1 /= b2
            else:
                current_token = str(b2)
                err_msg = "Ошибка при обработке правой части. Деление на \'0\'"
                raise Exception(err_msg)


def right_part(tokens, next_token):
    # global rp, b1
    is_minus = False
    if next_token == MINUS:
        next_token = get_next_token(tokens, 1)
        is_minus = True
    rp = 0
    prev_token = None
    while True:
        next_token, b1 = block_1(tokens, next_token)
        if is_minus:
            b1 = -b1
            is_minus = False

        if prev_token == PLUS:
            rp += b1
        elif prev_token == MINUS:
            rp -= b1
        else:
            rp += b1

        if next_token is None:
            return
        elif next_token != PLUS and next_token != MINUS:
            return next_token, rp
        prev_token = next_token
        next_token = get_next_token(tokens, 1)

######################################################


def _set(tokens, next_token):
    global err_code
    while True:
        if next_token != ANALIZ:
            err_msg = "Ошибка при обработке Множества. Ожидалось \'" + ANALIZ + "\'. Получено \'" + next_token + "\'. "
            raise Exception(err_msg)
        next_token = get_next_token(tokens, 1)
        while True:
            if is_int(next_token) is False:
                err_msg = "Ошибка при обработке Множества. Ожидалось целое число. Получено \'" + next_token + "\'. " + err_code
                raise Exception(err_msg)
            next_token = get_next_token(tokens, 1)
            if next_token != COMMA and next_token != ANALIZ:
                err_msg = "Ошибка при обработке Множества. Пропущен разделитель \'" + COMMA + "\'" #Ожидался символ \'" + COMMA + "\' или <конец строки>. Получено \'" + next_token + "\'. "
                raise Exception(err_msg)
            elif next_token == ANALIZ:
                break
            next_token = get_next_token(tokens, 1)


def split_tokens(str):
    result = []
    index = 0
    while index < len(str):
        flag = False
        curr_str = str[index:]
        for pattern in PATTERNS:
            match = re.match(pattern, curr_str)
            if match:
                flag = True
                value = match.group(0)
                result.append(value)
                index += len(value)
                break
        if flag is False:
            for pattern in SKIP_PATTERNS:
                match = re.match(pattern, curr_str)
                if match:
                    flag = True
                    value = match.group(0)
                    result.append(value)
                    index += len(value)
                    break
        if flag is False:
            result.append(str[index])
            index += 1
    return result


def start_parse():
    global is_error, current_token, idx, err_code, global_input
    err_code = ""
    idx = 0
    current_token = None
    is_error = True
    variables.clear()
    user_input = text_edit.get(0.1, tk.END).decode()
    user_input = split_tokens(user_input)
    global_input = user_input[:]
    if global_input[-1] == "\n":
        global_input.pop(-1)
    i = 0
    while i < len(user_input):
        if user_input[i] == " " or user_input[i] == "\t" or user_input[i] == "\n":
            user_input.pop(i)
        i += 1
    print(user_input)
    try:
        nt = definition(user_input)
        nt = operator(user_input, nt)
        _set(user_input, nt)
    except Exception as e:
        print(e.message)
        text_edit.delete(0.1, tk.END)
        # idx -= 2
        while global_input[idx] != current_token:
            idx += 1
        text_edit.insert(tk.END, "".join(global_input[:idx]))
        tmp = global_input[idx:]
        tmp = tmp[0]
        if is_error:
            text_edit.insert(tk.END, tmp, "warning")
        else:
            text_edit.insert(tk.END, "".join(tmp))
        try:
            text_edit.insert(tk.END, "".join(global_input[idx + 1:]))
        except Exception as e:
            text_edit.insert(tk.END, "".join(global_input[idx:]))
        output.configure(state=tk.NORMAL)
        output.delete(0.1, tk.END)
        output.insert(0.1, e.message)
        output.configure(state=tk.DISABLED)
        return e.message


def add_spaces(lst):
    tmp = lst[:]
    i = 0
    while True:
        if i % 2 == 0:
            tmp.insert(i + 1, " ")
        i += 1
        if i == len(tmp):
            break
    i = 0
    while True:
        if tmp[i] == "\n":
            tmp.pop(i + 1)
        i += 1
        if i == len(tmp):
            break
    return tmp


if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('utf-8')

    root = tk.Tk()
    root.resizable(False, False)
    root.title("BNF")
    root.geometry("1200x700")

    helv36 = tkFont.Font(family='Courier New', size=14)
    text_edit = tk.Text(root, borderwidth=0.5, wrap=tk.WORD, relief=tk.SOLID)
    text_edit.tag_config('warning', background="red", foreground="white")
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
          "Цифра = “0” ! “1” … “F”"
    label = tk.Label(root, text=bnf, font="14", justify=tk.LEFT)
    label.place(relx=0.53, rely=0.039)

    btn = tk.Button(root, text="Run", command=start_parse)
    btn.place(relx=0.7, rely=0.5, width=200)

    # v = tk.StringVar()
    output = tk.Text(root, borderwidth=0.5, wrap=tk.WORD, state=tk.DISABLED, relief=tk.SOLID)
    output.place(relx=0.013, rely=0.8, height=100, width=1150, bordermode=tk.OUTSIDE)

    root.mainloop()

    # инфо о русских буквах



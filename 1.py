# coding=utf-8
import tkinter
from tkinter import *
from tkinter import messagebox

root = Tk()
text = Text()
s = list()
oldText = list  ()
errorindex = -1
dump = list()
peremennaya = ""
deep = 0
d = {}
terminals = ["Программа", "Ввод", "Конец", "=", "*", "[","/","+","-","]", ":", ";", "0", "1", "2", "3", "4", "5", "6", "7", "а", "б", "в", "г", "д", "е", "ё", "ж", "з", "и", "й", "к", "л", "м", "н", "о", "п", "р", "с", "т", "у", "ф", "х", "ц", "ч", "ш", "щ", "э", "ю", "я", "А", "Б", "В", "Г", "Д", "Е", "Ё", "Ж", "З", "И", "Й", "К", "Л", "М", "Н", "О", "П", "Р", "С", "Т", "У", "Ф", "Х", "Ц", "Ч", "Ш", "Щ", "Э", "Ю", "Я"]
letter = ["а", "б", "в", "г", "д", "е", "ё", "ж", "з", "и", "й", "к", "л", "м", "н", "о", "п", "р", "с", "т", "у", "ф", "х", "ц", "ч", "ш", "щ", "э", "ю", "я", "А", "Б", "В", "Г", "Д", "Е", "Ё", "Ж", "З", "И", "Й", "К", "Л", "М", "Н", "О", "П", "Р", "С", "Т", "У", "Ф", "Х", "Ц", "Ч", "Ш", "Щ", "Э", "Ю", "Я"]
number = ["0", "1", "2", "3", "4", "5", "6", "7"]
blockednumber = ["8", "9"]

def SplitString(s):
    return [char for char in s]

def PrintError(dump, s, error):
    global newText
    global errorindex
    text1['state'] = 'normal'
    fullerror = error
    fullerror += '\n'+ "Встречено: " + str(s[0])
    text1.delete(1.0, END)
    global errorindex

    textforshowing = ''
    errorpos = 0
    firstext = ''
    errorelem = ''
    secondtext = ''
    for i in range(len(oldText)):
        if(oldText[i].find('\n') != -1)or(i + 1 == len(oldText)):
            addstr = ''
        else:
            addstr = ' '
        if (i < errorindex):
            firstext += oldText[i]+addstr
        else:
            if(i == errorindex):
                errorelem += oldText[i]+addstr
            else:
                secondtext += oldText[i]+addstr

    text.delete(1.0, END)
    strpos = 0
    linepos = 1
    f = list(firstext)
    for ff in f:
        text.insert(tkinter.END, ff)
        if(ff == '\n'):
            linepos += 1
            strpos = 0
        else:
            strpos += 1
    if(list(errorelem)[0]=='\n'):
        linepos += 1
        strpos = 0
    text['state'] = 'normal'
    text1['state'] = 'normal'
    text1.delete(1.0, END)
    text1.delete(1.0, END)
    text1.insert(tkinter.END, fullerror)
    text1['state'] = 'disabled'
    if(secondtext!=''):
        tmps = errorelem + secondtext
        text.insert(tkinter.END, tmps)
    else:
        text.insert(tkinter.END, errorelem)
    text.tag_add("error", f"{linepos}.{strpos}", f"{linepos}.{strpos+len(errorelem)-1}")
    #text.tag_add("error", 5.1, END)
    text.tag_config("error", background="red", foreground="white")


def ParceNumber(s):
    checkNumber = True
    tmp = list(s.rstrip('\n'))
    for c in tmp:
        if (c not in number):
            checkNumber = False
    return checkNumber

def ParceString():
    text.tag_config("error", background="white", foreground="black")
    global d
    global s
    global oldText
    global errorindex
    errorindex = 0
    text1['state'] = 'normal'
    dump.clear()
    text1.delete(1.0, END)
    string = str(text.get(1.0, END))
    oldText.clear()
    s.clear()
    oldText = string.split('\n')
    oldText = [x for x in oldText if x]
    oldText[len(oldText) - 1] = oldText[len(oldText) - 1].rstrip("\n")
    for i in range(len(oldText)):
        oldText[i] = oldText[i].rstrip(' ')
    newList = list()
    for i in range(len(oldText)-1):
        oldText[i] = oldText[i]+'\n'
    for substr in oldText:
        a = substr.split(' ')
        for ss in a:
            newList.append(ss)
    for i in range(len(newList)):
        s.append(newList[i].strip('\n'))
    oldText = newList

    Yazik()
    
    #вывод результата
    if(len(s) == 0):
        for x in d:
            if(str(d[x])=="True"):
                trmpstr = "Значение переменной " + str(x) + " = " + '1' + "\n"
            else:
                if(str(d[x])=="False"):
                    trmpstr = "Значение переменной " + str(x) + " = " + '0' + "\n"
                else:
                    trmpstr = "Значение переменной " + str(x) + " = " + str(d[x]) + "\n"
            text1.insert(INSERT, trmpstr)
        text1['state'] = 'disabled'
    else:
        PrintError(dump, s, "Обнаружены символы после \"Конец\"")

def Yazik():
    global d
    d = {}
    global errorindex
    global s
    if(s[0]=="Программа"):
        dump.append(s[0])
        del s[0]
        errorindex += 1
    else:
        PrintError(dump, s, "Язык должен начинаться со слова \"Программа\"")
        raise Exception()
    Zveno()
    return s

def Zveno():
    global errorindex
    global s
    if (s[0] == "Ввод"):
        dump.append(s[0])
        del s[0]
        errorindex += 1
    else:
        PrintError(dump, s, "Звено должно начинаться со слова \"Ввод\"")
        raise Exception()
    while(ParceNumber(s[0])):
        Slovo()
    if (s[0] == ";"):
        dump.append(s[0])
        del s[0]
        errorindex += 1
        Zveno()
    else:
        if (s[0] == "Конец"):
            dump.append(s[0])
            del s[0]
            errorindex += 1
        else:
            PrintError(dump, s, "После Слова должно идти новое Слово, либо \";\", либо \"Конец\"")
            raise Exception()
    return s

def Slovo():
    global errorindex
    global s
    global d
    global deep
    global peremennaya
    deep = 0
    if (not ParceNumber(s[0])):
        PrintError(dump, s, "Слово должно начинаться с метки")
        raise Exception()
    else:
        dump.append(s[0])
        del s[0]
        errorindex += 1
    if (s[0] != ":"):
        PrintError(dump, s, "После метки должен идти символ \":\"")
        raise Exception()
    else:
        dump.append(s[0])
        del s[0]
        errorindex += 1
    peremennaya = s[0]
    a = list(s[0])
    if(a[0] not in letter):
        PrintError(dump, s, "В переменной на 1 позиции должна стоять буква")
        raise Exception()
    for i in range(3):
        if (not ParceNumber(a[i+1])):
            string_arg = "В переменной на " + str(i + 2) + " позиции должна стоять цифра"
            PrintError(dump, s, string_arg)
            raise Exception()
    dump.append(s[0])
    del s[0]
    errorindex += 1
    if (s[0] == "="):
        dump.append(s[0])
        del s[0]
        errorindex += 1
    else:
        PrintError(dump, s, "После переменной должно идти \"=\"")
        raise Exception()
    d[peremennaya] = PravayaChast()
    if (d[peremennaya] == 'False'):
        d[peremennaya] == '0'
    if (d[peremennaya] == 'True'):
        d[peremennaya] == '1'
    if(deep != 2):#ИЗМЕНИТЬ ГЛУБИНУ       ИЗМЕНИТЬ ГЛУБИНУ        ИЗМЕНИТЬ ГЛУБИНУ     ИЗМЕНИТЬ ГЛУБИНУ
        s.reverse()
        s.append(dump[len(dump)-1])
        s.reverse()
        del(dump[len(dump)-1])
        errorindex -= 1
        PrintError(dump, s, "Допустимая глубина вложенности квадратных скобок - 2")
        raise Exception()
    return s

def PravayaChast():
    global errorindex
    global s
    global pravayachastint
    if (s[0] == "-"):
        dump.append(s[0])
        del s[0]
        errorindex += 1
        pravayachastint = 0 - Block1()
    else:
        pravayachastint = Block1();
    while (s[0] == "+") or (s[0] == "-"):
        if(s[0]=="+"):
            dump.append(s[0])
            del s[0]
            errorindex += 1
            pravayachastint = pravayachastint+Block1()
        else:
            dump.append(s[0])
            del s[0]
            errorindex += 1
            pravayachastint = pravayachastint - Block1()
    return pravayachastint

def Block1():
    global errorindex
    global s
    block1int = Block2()
    while (s[0] == "*") or (s[0] == "/"):
        if(s[0]=="*"):
            dump.append(s[0])
            del s[0]
            errorindex += 1
            block1int = block1int * Block2()
        else:
            dump.append(s[0])
            del s[0]
            errorindex += 1
            try:
                block1int = block1int / Block2()
            except ZeroDivisionError:
                s.reverse()
                s.append(dump[len(dump) - 1])
                s.reverse()
                del (dump[len(dump) - 1])
                errorindex -= 1
                PrintError(dump, s, "Дeление на 0 невозможно")
                raise Exception()
    return block1int

def Block2 ():
    global errorindex
    block2int = Block3()
    while (s[0] == "&") or (s[0] == "|"):
        if (s[0] == "&"):
            dump.append(s[0])
            del s[0]
            errorindex += 1
            tmp = Block3()
            block2int = block2int and tmp
        else:
            dump.append(s[0])
            del s[0]
            errorindex += 1
            tmp = Block3()
            block2int = block2int or tmp
    return block2int

def Block3 ():
    global errorindex
    global pravayachastint
    if (s[0] == "!"):
        dump.append(s[0])
        del s[0]
        errorindex += 1
        block3int  = not Block4()
    else:
        block3int = Block4()
    return block3int

def Block4 ():
    global errorindex
    peremennaya = s[0]
    a = list(s[0])
    if (a[0] in letter)and(len(a)==4):
        for i in range(3):
            if (not ParceNumber(a[i+1])):
                PrintError(dump, s, "В правой части должны стоять целое или переменная. ")
                raise Exception()
        if (d.get(s[0]) == None):
            PrintError(dump, s,'Неизвестно значение переменной ' + s[0])
            raise Exception()
        else:
            pravayachastint = d.get(s[0])
        dump.append(s[0])
        del s[0]
        errorindex += 1
    else:
        global deep
        if (not ParceNumber(s[0])):
            if(s[0] == "(")or(s[0] == "["):
                if(s[0] == "("):
                    dump.append(s[0])
                    del s[0]
                    errorindex += 1
                    pravayachastint = PravayaChast()
                    if(s[0] != ")"):
                        PrintError(dump, s, "Ожидался символ \")\"")
                        raise Exception()
                    else:
                        dump.append(s[0])
                        del s[0]
                        errorindex += 1
                else:
                    if(deep < 2):
                        deep += 1
                        dump.append(s[0])
                        del s[0]
                        errorindex += 1
                        pravayachastint = PravayaChast()
                        if (s[0] != "]"):
                            PrintError(dump, s, "Ожидался символ \"]\"")
                            raise Exception()
                        else:
                            dump.append(s[0])
                            del s[0]
                            errorindex += 1
                    else:
                        PrintError(dump, s, "Допустимая глубина вложенности квадратных скобок - 2")
                        raise Exception()
            else:
                PrintError(dump, s, "В правой части должны быть Переменная либо Целое")
                raise Exception()
        else:
            pravayachastint = int(s[0])
            dump.append(s[0])
            del s[0]
            errorindex += 1
    return pravayachastint


root.title('Транслирующее средство')
root.geometry('900x600')
root.resizable(width=False, height=False)

text = Text(width = 55, height = 20, font = 100)
text.configure(font=("Courier", 14))
text.grid(row = 0, column = 0)

text.insert(INSERT, "Программа \nВвод \n11 : о512 = 5 * [ 1 + 7 ] - ( 14 + 3 ) \n11 : о511 = 5 * ( 1 + о512 ) / 1 - 7  \nКонец")

text2 = Text(width = 55, height = 20, font = 100)
text2.configure(font=("Courier", 14))
text2.grid(row = 0, column = 1)
text2.insert(INSERT, "Язык = “Программа” Звено”;”… Звено “Конец” \nЗвено = “Ввод” Слово … Слово \nСлово = Метка “:” Переменная “=” Правая часть \n \nПравая часть = </“-”/> Блок1 Знак1 … Блок1 \nЗнак1 = “+” ! “-” \nБлок1 =  Блок2 Знак2 … Блок2 \nЗнак2 = “*” ! “/” \nБлок2 =  Блок3 Знак3 … Блок3 \nЗнак3 = “&” ! “|” \nБлок3 = </“ ¬ ”/> Блок4 \nБлок4 = Переменная ! Целое ! “(”  Правая часть “)” \n! “[” Правая часть “]” вложенность <=2 \n\nПеременная = Буква Цифра Цифра Цифра \nМетка = Целое  \nЦелое = Цифра … Цифра  \nЦифра = “0” ! “1” !…! “7” \nБуква = “А” ! “Б” !…! “я”" )
text2['state'] = 'disabled'

text1 = Text(width = 110, height = 20, font = 100)
text1.configure(font=("Courier", 14))
text1.place(x = 0, y = 320)
text1['state'] = 'disabled'
btn = Button(text="Проверить", command = ParceString)
btn.place(x = 400, y= 289)


root.mainloop()
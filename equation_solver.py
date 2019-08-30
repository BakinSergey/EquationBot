import math
import sys, os
import re
import subprocess
from collections import namedtuple
import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


from GDriveFunc import GDriveUploadFile, GDriveCreateFolder

sin = r'\sin'
cos = r'\cos'
tan = r'\tan'
cot = r'\cot'
arcsin = r'\arcsin'
arccos = r'\arccos'
arctan = r'\arctan'
arccot = r'\arccot'
sinh = r'\sinh'
cosh = r'\cosh'
tanh = r'\tanh'
coth = r'\coth'
sec = r'\sec'
csc = r'\csc'

document = r'\documentclass{style}{doctype}'
doc_coding = r'\usepackage{coding}{module}'
doc_lang = r'\usepackage{lang}{module}'

# словарь переменная:значение (со скобками для отрицательных: A:'(-3)', B:'2')
vv = dict()

# folder id on GDrive
Solutions_folder = '1xXnqTir21XIEA3TTr8Tz94IS8xLFkq-p'
folder_prefix = 'https://drive.google.com/drive/folders/{}'
file_prefix = 'https://drive.google.com/open?id={}'


def writeline(f, line):
    f.write(line)
    f.write('\n')


def getlanguage(data):
    lang = data.lang
    module = data.module
    return doc_lang.format(lang=lang, module=module)


def getcoding(data):
    coding = data.coding
    module = data.module
    return doc_coding.format(coding=coding, module=module)


def getheader(data):
    d_type = data.doctype
    f_size = data.fsize

    return document.format(style=f_size, doctype=d_type)


def equation(a=0, b=0, c=0, et=''):
    if et == 'full':
        return 'квадратное уравнение: \n' \
               r'$$ {A}\cdot x^2{B:+}\cdot x{C:+}=0$$'.format(A=a, B=b, C=c)

    if et == 'trim_c':
        return 'квадратное уравнение: \n' \
               r'$$ {A}\cdot x^2{B:+}\cdot x=0$$'.format(A=a, B=b)

    if et == 'trim_b':
        return 'квадратное уравнение: \n' \
               r'$$ {A}\cdot x^2{C:+}=0$$'.format(A=a, C=c)

    if et == 'trim_bc':
        return 'квадратное уравнение: \n' \
               r'$$ {A}\cdot x^2=0$$'.format(A=a)


def set_parenthesis(a):
    if a < 0:
        # vv[a] = '('+str(a)+')'
        return '(' + str(a) + ')'
    else:
        # vv[a] = str(a)
        return str(a)


def trim_bc_colution(a):
    sol = []
    sol += ['является неполным, коэффициенты b,c равны нулю,',
            'уравнение имеет единственный корень:',
            r'$$ x = 0 $$']
    return sol


def trim_b_colution(a, c):
    sol = []

    sol += ['является неполным, коэффициент b равен нулю, перенесем с в правую часть и разделим обе части на а:']

    if c < 0:
        cc = int_plz(math.fabs(c))
        sol += [r'$$ x^2 = \frac{{{C}}}{{{A}}} $$'.format(A=a, C=cc)]
    else:
        sol += [r'$$ x^2 = \frac{{-{C}}}{{{A}}} $$'.format(A=a, C=c)]

    if a * c < 0:
        x1 = math.sqrt(-c / a)
        x2 = -math.sqrt(-c / a)
        x1, x2 = map(int_plz, [x1, x2])
        # меняем числа на строки и формируем строки вычислений
        a, c = tuple(map(set_parenthesis, [a, c]))
        a = a.translate({ord(l): None for l in '(-)'})
        c = c.translate({ord(l): None for l in '(-)'})

        sol += [
            r'уравнение имеет два корня:',
            r'$$ x_1 = \sqrt {{\frac{{{C}}}{{{A}}} }} = {X1} $$'.format(A=a, C=c, X1=x1),
            r'$$ x_2 = -\sqrt {{\frac{{{C}}}{{{A}}} }} = {X2} $$'.format(A=a, C=c, X2=x2)]

    else:
        sol += ['правая часть отрицательна, действительных корней уравнение не имеет']

    return sol


def trim_c_colution(a, b):
    div_sign = '+' if (b / a) > 0 else '-'
    x1 = 0
    x2 = -b / a
    x2 = int_plz(x2)
    # меняем числа на строки и формируем строки вычислений
    a, b = tuple(map(set_parenthesis, [a, b]))
    return ['является неполным, свободный член равен нулю, разложим его на множители:',
            r'$$ {A} \cdot x \cdot \left(x {ds} \frac{{{B}}}{{{A}}}\right)=0$$'.format(A=a, B=b, ds=div_sign),
            r'приравнивая каждый из множителей к нулю, получаем корни уравнения:',
            r'$$ x_1 = {X1} $$'.format(X1=x1),
            r'$$ x_2 = -\frac{{b}}{{a}} = -\frac{{{B}}}{{{A}}} = {X2}$$'.format(A=a, B=b, X2=x2),
            ]


def full_solution(a, b, c):
    d = round(b * b - 4 * a * c, 3)
    if d > 0:
        x1 = (-b + math.sqrt(d)) / (2 * a)
        x2 = (-b - math.sqrt(d)) / (2 * a)
        x1, x2 = map(int_plz, [x1, x2])
    if d == 0:
        x1 = (-b) / (2 * a)
        x1 = int_plz(x1)

    # меняем числа на строки и формируем строки вычислений
    a, b, c = tuple(map(set_parenthesis, [a, b, c]))

    sol = ['является полным, вычисляем дискриминант:',
           r'$$ d=b^2-4\cdot a \cdot c = {B}^2-4\cdot {A}\cdot{C} = {D}$$'.format(A=a, B=b, C=c, D=d)]

    if d > 0:
        sol += ['дискриминант положительный(d>0), поэтому уравнение имеет два корня:',
                r'$$ x_1 = \frac{{-b + \sqrt{{d}}}}{{2\cdot a}} = \frac{{-{B}+\sqrt{{{D}}}}}{{2\cdot {A}}} = {X1}$$'.format(
                    A=a, B=b, C=c, D=d, X1=x1),
                r'$$ x_2 = \frac{{-b - \sqrt{{d}}}}{{2\cdot a}} = \frac{{-{B}-\sqrt{{{D}}}}}{{2\cdot {A}}} = {X2}$$'.format(
                    A=a, B=b, C=c, D=d, X2=x2)]
    elif d < 0:
        sol += ['дискриминант отрицательный(d<0),',
                'поэтому уравнение не имеет действительных корней']
    elif d == 0:
        sol += ['дискриминант равен нулю(d=0), поэтому уравнение имеет один корень:',
                r'$$ x_1 = \frac{{-b}}{{2\cdot a}}=\frac{{-{B}}}{{2\cdot {A}}} = {X1}$$'.format(A=a, B=b, X1=x1)]
    return sol


def int_plz(el):
    return int(el) if el - int(el) == 0 else round(el, 4)


def getEQ():
    print('ax2 + bx + c = 0')
    a, b, c = map(float, input('Ввод a,b,c(через пробел):').split())
    a, b, c = map(int_plz, [a, b, c])

    return [a, b, c]


def Solve_Square_Eq(aa, bb, cc, debug_mode=False):
    # aa, bb, cc = getEQ()
    eq_type = 'тип квадратного уравнения'

    if aa != 0 and bb != 0 and cc != 0:
        eq_type = 'full'

    elif aa == 0:
        print('это не квадратное уравнение')
        exit()

    elif bb == 0 and cc == 0:
        eq_type = 'trim_bc'

    elif bb == 0:
        eq_type = 'trim_b'

    elif cc == 0:
        eq_type = 'trim_c'

    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    tex_out = '{aa}x2{bb:+}x{cc:+}'.format(aa=aa, bb=bb, cc=cc)
    file = open(r'{}.tex'.format(tex_out), 'wt', encoding="utf-8")

    header = namedtuple('header', 'fsize doctype')
    coding = namedtuple('coding', 'coding module')
    language = namedtuple('language', 'lang module')

    # create tex document

    # \documentclass{article}
    writeline(file, getheader(header(r'[12pt]', '{article}')))

    # \usepackage[utf8]{inputenc}
    writeline(file, getcoding(coding(r'[utf8]', '{inputenc}')))

    # \usepackage[russian]{babel}
    writeline(file, getlanguage(language(r'[english,russian]', '{babel}')))

    # body start
    writeline(file, r'\begin{document}')
    writeline(file, r'\begin{flushleft}')

    # user_Text
    writeline(file, equation(aa, bb, cc, et=eq_type))

    if eq_type == 'full':
        for l in full_solution(aa, bb, cc):
            writeline(file, l)

    elif eq_type == 'trim_c':
        for l in trim_c_colution(aa, bb):
            writeline(file, l)

    elif eq_type == 'trim_b':
        for l in trim_b_colution(aa, cc):
            writeline(file, l)

    elif eq_type == 'trim_bc':
        for l in trim_bc_colution(aa):
            writeline(file, l)

    # body end
    writeline(file, r'\end{flushleft}')
    writeline(file, r'\end{document}')

    file.close()

    mode = ''
    if not debug_mode:
        mode = '-interaction=batchmode'
        priv = '--admin'

    os.chdir(r'latex')

    return_value = subprocess.call(['pdflatex', ''.join(mode), os.path.abspath(tex_out)], shell=False)

    logger.warning('pdflatex return: %s', str(return_value))

    mime_type = 'application/pdf'
    filename = r'latex/{}.pdf'.format(tex_out)
    description = 'squared equation solution'
    parent_id = Solutions_folder

    f = GDriveUploadFile(filename=filename,
                         description=description,
                         mime_type=mime_type,
                         parent_id=parent_id)

    return file_prefix.format(f['id'])

# print(prefix.format(GDriveCreateFolder(name='folder', parent_id='1xXnqTir21XIEA3TTr8Tz94IS8xLFkq-p')))

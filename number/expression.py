from inspect import signature


def is_number(char):
    try:
        if str(char).endswith('x'):
            char = char.removesuffix('x')
            if char == '-' or char == '':
                char += '1'
        float(char)
        return True
    except ValueError:
        return False


def priority(operator):
    operators = {
        '*': 2,
        '/': 2,
        '//': 2,
        '/-': 2,
        '/+': 2,
        '-': 1,
        '+': 1,
    }
    try:
        return operators[operator]
    except KeyError:
        try:
            test = globals()[operator]
            return 3
        except Exception:
            raise SyntaxError(f"L'operateur ou la fonction '{operator}' n'existe pas!")


def clean(expression):
    expression = verify(expression)
    clean_exp = []
    temp = ""
    previous_type = ""
    for x in expression:
        if x.isspace():
            continue

        if x == 'x':
            current_type = "x"
        elif x.isalpha():
            current_type = "alpha"
        elif is_number(x) or x == '.':
            current_type = "number"
        elif x == '(' or x == ')':
            current_type = "pr"
        else:
            current_type = "operator"

        if current_type == 'pr' and previous_type == 'pr':
            clean_exp.append(x)
            temp = ""

        if current_type == 'x':
            temp += x
        elif current_type == previous_type or previous_type == '':
            temp += x
        else:
            if (temp == '-' or temp == '+') \
                    and ((len(clean_exp) > 0 and clean_exp[-1] != ')' and not is_number(clean_exp[-1]))
                         or len(clean_exp) == 0):
                clean_exp.append('0')
            if len(temp) > 0:
                clean_exp.append(temp)
            temp = x
        previous_type = current_type
    if len(temp) > 0:
        clean_exp.append(str(temp))

    return clean_exp


def verify(expression):
    count_p = 0
    i_last_p = 0

    for i, x in enumerate(expression):
        if x == '(':
            i_last_p = i
            count_p += 1
        elif x == ')':
            count_p -= 1

        if count_p < 0:
            error = f"Cette parenthèse n'a pas été ouverte!\n{expression}\n" + ("-" * i) + '^'
            raise SyntaxError(error)

    if count_p > 0:
        error = f"Il y {count_p} parenthèse(s) non-fermée(s)!\n{expression}\n" + ("-" * i_last_p) + '^'
        raise SyntaxError(error)
    return expression


def convert(expression):
    expression = clean(expression)
    pile = []
    output = []
    for elem in expression:
        if is_number(elem):
            output.append(elem)
        elif elem == ',':
            while pile[0] != '(':
                output.append(pile.pop(0))
        elif elem == '(':
            pile.insert(0, elem)
        elif elem == ')':
            while pile[0] != '(':
                output.append(pile.pop(0))
            pile.pop(0)
        else:
            while len(pile) > 0 and pile[0] != '(' and priority(elem) <= priority(pile[0]):
                output.append(pile[0])
                pile.pop(0)
            pile.insert(0, elem)
    if len(pile) > 0:
        output.extend(pile)
    return output


def pre_operation(a, b):
    nbs = []
    if not is_number(str(a)):
        nbs.extend(a)
    else:
        nbs.append(a)
    if not is_number(str(b)):
        nbs.extend(b)
    else:
        nbs.append(b)
    return nbs


def plus(a, b):
    nbs = pre_operation(a, b)
    exp_x = []
    exp_c = []
    for nb in nbs:
        if str(nb).endswith('x'):
            t = str(nb).removesuffix('x')
            if t == '' or t == '-':
                t += '1'
            exp_x.append(float(t))
        else:
            exp_c.append(float(nb))
    s_exp_x = sum(exp_x)
    s_exp_c = sum(exp_c)
    if s_exp_x != 0 and s_exp_c != 0:
        return [str(s_exp_x) + 'x', s_exp_c]
    if s_exp_x == 0:
        return str(s_exp_c)
    return str(s_exp_x) + 'x'


def minus(a, b):
    if not is_number(str(b)):
        new_b = []
        for elem in b:
            if str(elem).startswith('-'):
                new_b.append(str(elem).removeprefix('-'))
            else:
                new_b.append('-' + str(elem))
    else:
        new_b = '-' + str(b)
    return plus(a, new_b)


def multiply(a, b):
    a = [a] if is_number(str(a)) else a
    b = [b] if is_number(str(b)) else b
    res = []
    for elem_a in a:
        for elem_b in b:
            if str(elem_a).endswith('x') and str(elem_b).endswith('x'):
                if str(elem_a).removesuffix('x') == '0' or str(elem_b).removesuffix('x') == '0':
                    res.append('0')
                else:
                    raise SyntaxError(f"Ne supporte pas la multiplication de deux variables! {elem_a} * {elem_b}")
            elif str(elem_a).endswith('x') and not str(elem_b).endswith('x'):
                if str(elem_a).removesuffix('x') == '':
                    res.append(str(elem_b) + 'x')
                else:
                    res.append(str(float(str(elem_a).removesuffix('x')) * float(str(elem_b))) + 'x')
            elif not str(elem_a).endswith('x') and str(elem_b).endswith('x'):
                if str(elem_b).removesuffix('x') == '':
                    res.append(str(elem_a) + 'x')
                else:
                    res.append(str(float(str(elem_b).removesuffix('x')) * float(str(elem_a))) + 'x')
            else:
                res.append(float(elem_a) * float(elem_b))
    return res


def divide(a, b):
    a = [a] if is_number(str(a)) else a
    b = [b] if is_number(str(b)) else b
    res = []
    for elem_a in a:
        for elem_b in b:
            if str(elem_a).endswith('x') and str(elem_b).endswith('x'):
                if str(elem_b).removesuffix('x') == '0':
                    raise ZeroDivisionError(f"Impossible de diviser par 0! {elem_a} / {elem_b}")
                res.append(str(float(str(elem_a).removesuffix('x')) / float(str(elem_b).removesuffix('x'))))
            elif str(elem_a).endswith('x') and not str(elem_b).endswith('x'):
                if str(elem_a).removesuffix('x') == '':
                    res.append(str(elem_b) + 'x')
                else:
                    res.append(str(float(str(elem_a).removesuffix('x')) / float(str(elem_b))) + 'x')
            elif not str(elem_a).endswith('x') and str(elem_b).endswith('x'):
                if str(elem_b).removesuffix('x') == '':
                    res.append(str(elem_a) + 'x')
                else:
                    res.append(str(float(str(elem_a)) / float(str(elem_b).removesuffix('x'))) + 'x')
            else:
                res.append(float(elem_a) / float(elem_b))
    return res


def calculate(expression):
    try:
        expression = convert(expression)
    except Exception:
        raise SyntaxError('Il y a une erreur dans votre expression!')
    pile = []
    for elem in expression:
        if is_number(elem):
            pile.insert(0, elem)
        else:
            temp = 0
            operations = {'+': lambda x, y: plus(x, y),
                          '-': lambda x, y: minus(x, y),
                          '*': lambda x, y: multiply(x, y),
                          '/': lambda x, y: divide(x, y),
                          '/-': lambda x, y: divide(x, '-' + str(y)),
                          '/+': lambda x, y: divide(x, y),
                          }
            if elem in operations:
                op = operations[elem]
                temp = op(pile[1], pile[0])
                pile.pop(0)
                pile.pop(0)
            elif elem.isalpha():
                function = globals()[elem]
                try:
                    sign = signature(function)
                    r_pile = pile[::-1]
                    temp = function(*[float(x) for x in r_pile[len(r_pile) - len(sign.parameters):]])
                    for i in range(len(sign.parameters)):
                        pile.pop(0)
                except Exception:
                    if is_number(function):
                        temp = function
                    else:
                        raise SyntaxError(f"La fonction '{elem}' n'existe pas!")
            pile.insert(0, temp)
    if isinstance(pile[0], list):
        print(pile[0])
        return result(pile[0])
    else:
        print(pile)
        return result(pile)


def result(res):
    if is_number(str(res)):
        return res
    r = []
    for elem in res:
        if str(elem).startswith('-'):
            r.append(str(elem))
        else:
            r.append('+ ' + str(elem))
    return ' '.join(r).strip()


def est_nombre(nombre):
    try:
        float(nombre)
        return True
    except Exception:
        return False


def est_operateur(valeur):
    op = ['+', '-', '*', '/']
    return valeur in op


def formater(equation):
    res = ""
    for i, x in enumerate(equation):
        if x == " ":
            if (est_nombre(res[-1]) and (est_nombre(equation[i + 1]) or equation[i + 1] == "x")) \
                    or est_operateur(res[-1]):
                continue
        res += x
    return res


def inverser(valeur):
    if str(valeur).startswith('+'):
        return '-' + valeur[1:]
    if str(valeur).startswith('-'):
        return '+' + valeur[1:]
    if str(valeur).startswith('*'):
        return '/' + valeur[1:]
    if str(valeur).startswith('/'):
        return '*' + valeur[1:]


def regler_signe(list_valeur):
    res = []
    for x in list_valeur:
        if not est_operateur(x[:1]):
            res.append("+" + str(x))
        else:
            res.append(x)
    return res


def separation(equation, sep):
    equation = formater(equation)
    x = []
    c = []
    apres_egal = False
    for i, elem in enumerate(str(equation).split(" ")):
        if elem == sep:
            apres_egal = True
            continue
        if str(elem).endswith('x'):
            if apres_egal:
                x.append(inverser(elem))
            else:
                x.append(elem)
        else:
            if apres_egal:
                c.append(elem)
            else:
                c.append(inverser(elem))
    return f"{' '.join(regler_signe(x))} {sep} {' '.join(regler_signe(c))}"

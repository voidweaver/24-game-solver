#!/usr/bin/env python3

from decimal import Decimal
import time
import argparse
import sys


def longer_indent_formatter(prog):
    return argparse.RawTextHelpFormatter(prog, max_help_position=32)


if len(sys.argv) > 1:
    parser = argparse.ArgumentParser(
        description='Find a solution to construct the target number using the given numbers',
        formatter_class=longer_indent_formatter)
    parser.add_argument('numbers', metavar='N', type=float, nargs=4,
                        help="numbers to construct from", default=[None])
    parser.add_argument('-t', '--target', metavar='target', type=float, nargs=1,
                        help="target number to achieve (default: %(default)s)", default=[24])
    parser.add_argument('-n', '--limit', metavar='limit', type=int, nargs=1,
                        help="number of solutions to show (default: all)", default=[None])
    arguments = parser.parse_args()

OPS = [' + ', ' - ', ' * ', ' / ']


def is_duplicate(*vars):
    history = []
    for var in vars:
        if var in history:
            return True
        else:
            history.append(var)
    return False


def generate_expressions(digits):
    expressions = []
    for a in range(4):
        for b in range(4):
            if is_duplicate(a, b):
                continue
            for c in range(4):
                if is_duplicate(a, b, c):
                    continue
                for d in range(4):
                    if is_duplicate(a, b, c, d):
                        continue
                    for x in range(4):
                        for y in range(4):
                            for z in range(4):
                                # ---------------------------------------------- Single Parenthesis ----------------------------------------------
                                expressions.append(
                                    '( ' + str(digits[a]) + OPS[x] + str(digits[b]) + ' )' + OPS[y] + str(digits[c]) + OPS[z] + str(digits[d]))
                                expressions.append(
                                    str(digits[a]) + OPS[x] + '( ' + str(digits[b]) + OPS[y] + str(digits[c]) + ' )' + OPS[z] + str(digits[d]))
                                expressions.append(
                                    str(digits[a]) + OPS[x] + str(digits[b]) + OPS[y] + '( ' + str(digits[c]) + OPS[z] + str(digits[d]) + ' )')
                                expressions.append(
                                    '( ' + str(digits[a]) + OPS[x] + str(digits[b]) + ' )' + OPS[y] + '( ' + str(digits[c]) + OPS[z] + str(digits[d]) + ' )')
                                # ---------------------------------------------- Double Parenthesis ----------------------------------------------
                                expressions.append(
                                    '( ' + '( ' + str(digits[a]) + OPS[x] + str(digits[b]) + ' )' + OPS[y] + str(digits[c]) + ' )' + OPS[z] + str(digits[d]))
                                expressions.append(
                                    '( ' + str(digits[a]) + OPS[x] + '( ' + str(digits[b]) + OPS[y] + str(digits[c]) + ' )' + ' )' + OPS[z] + str(digits[d]))
                                expressions.append(
                                    str(digits[a]) + OPS[x] + '( ' + '( ' + str(digits[b]) + OPS[y] + str(digits[c]) + ' )' + OPS[z] + str(digits[d]) + ' )')
                                expressions.append(
                                    str(digits[a]) + OPS[x] + '( ' + str(digits[b]) + OPS[y] + '( ' + str(digits[c]) + OPS[z] + str(digits[d]) + ' )' + ' )')
    return expressions


def get_indices(list, target):
    indices = []
    for i, elem in enumerate(list):
        if elem == target:
            indices.append(i)
    return indices


def eval(expression):
    expression = expand_negative(expression)
    tokens = expression.split(' ')
    for token in tokens:
        if token is None:
            return None

    if '(' in tokens:
        open_indices = get_indices(tokens, '(')
        close_indices = get_indices(tokens, ')')
        if len(open_indices) != len(close_indices):
            raise Exception("Unbalanced parenthesis")
        else:
            while '(' in tokens:
                for i in range(0, len(tokens)):
                    j = len(tokens) - 1 - i
                    if tokens[j] == '(':
                        open_index = j
                        break
                for i in range(open_index, len(tokens)):
                    if tokens[i] == ')':
                        close_index = i
                        break

                evaled = eval(' '.join(tokens[open_index + 1:close_index]))
                if evaled is None:
                    return None

                del tokens[open_index:close_index + 1]
                tokens.insert(open_index, str(evaled))

    if '(' not in tokens:
        while '*' in tokens or '/' in tokens:
            if '*' in tokens and '/' in tokens:
                mult_index = tokens.index('*')
                div_index = tokens.index('/')
                if mult_index < div_index:
                    index = mult_index
                    is_multiply = True
                else:
                    index = div_index
                    is_multiply = False
            else:
                if '*' in tokens:
                    index = tokens.index('*')
                    is_multiply = True
                else:
                    index = tokens.index('/')
                    is_multiply = False
            if is_multiply:
                result = Decimal(tokens[index - 1]) * \
                    Decimal(tokens[index + 1])
            else:
                if Decimal(tokens[index + 1]) == 0:
                    return None
                result = Decimal(tokens[index - 1]) / \
                    Decimal(tokens[index + 1])

            del tokens[index - 1:index + 2]
            tokens.insert(index - 1, str(result))

        while '+' in tokens:
            index = tokens.index('+')
            sum = Decimal(tokens[index - 1]) + Decimal(tokens[index + 1])
            del tokens[index - 1: index + 2]
            tokens.insert(index - 1, str(sum))

        if len(tokens) == 1:
            return tokens[0]


def expand_negative(expression):
    tokens = expression.split(' ')
    while '-' in tokens:
        index = tokens.index('-')
        if tokens[index + 1] != '(':
            tokens[index] = '+'
            if tokens[index + 1][0] == '-':
                tokens[index + 1] = '+' + tokens[index + 1][1:]
            elif tokens[index + 1][0] == '+':
                tokens[index + 1] = '-' + tokens[index + 1][1:]
            else:
                tokens[index + 1] = '-' + tokens[index + 1]\

        else:
            tokens[index] = '+'
            already = False
            for i in range(index + 1, len(tokens)):
                if tokens[i] == '*' or tokens[i] == '/':
                    already = True
                if tokens[i] == ')':
                    break
                else:
                    try:
                        int(tokens[i])
                    except ValueError:
                        None
                    else:
                        if not already:
                            if tokens[i][0] == '-':
                                tokens[i] = '+' + tokens[i][1:]
                            else:
                                tokens[i] = '-' + tokens[i]

    return ' '.join(tokens)


def abs(n):
    return n if n >= 0 else -n


def main():
    try:
        arguments
    except NameError:
        user_input = input("Enter numbers: ").split(' ')
        target = input("Number to construct (default: 24): ")
        if target == '':
            target = 24
        else:
            target = Decimal(target)
        output_limit = input("Solutions to show (default: all): ")
        if output_limit == '':
            output_limit = None
        else:
            output_limit = int(output_limit)
        pause = True
    else:
        args = vars(arguments)

        user_input = args['numbers']
        output_limit = args['limit'][0]
        target = Decimal(args['target'][0])

        pause = False

    for i in range(len(user_input)):
        user_input[i] = Decimal(user_input[i])

    digits = user_input
    exs = generate_expressions(digits)

    has_no_solutions = True

    answers = 0

    for ex in exs:
        res = eval(ex)
        if res is not None:
            dec = Decimal(res)
        else:
            continue

        if abs(dec - Decimal(target)) < 0.00000000000001:
            print(str(ex) + " = " + str(round(dec)))
            has_no_solutions = False
            answers += 1

        if output_limit is not None and answers >= output_limit:
            break

    if has_no_solutions:
        print("No solutions found")

    print("Time taken: " + str(time.process_time()))

    if pause:
        input("Press enter to continue...")


main()

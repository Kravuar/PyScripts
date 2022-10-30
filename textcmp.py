#!/usr/bin/env python3
from colorama import Fore, Style
from recordclass import dataobject
from itertools import islice
from argparse import ArgumentParser, RawDescriptionHelpFormatter


class Difference(dataobject):
    start: int
    end: int


infoPrimary = Fore.GREEN + Style.DIM + '{}' + Style.RESET_ALL
infoSecondary = Fore.CYAN + Style.BRIGHT + '{}' + Style.RESET_ALL
difference = Fore.RED + Style.BRIGHT + '{}' + Style.RESET_ALL
match = Fore.GREEN + Style.NORMAL + '{}' + Style.RESET_ALL
error = Fore.RED + Style.BRIGHT + '{}' + Style.RESET_ALL


err_invalid_file = error.format("Invalid file: {}\n")


def file_valid(parser, file):
    try:
        return open(file)
    except IOError:
        parser.error(err_invalid_file.format(file))


def find_difs(lines):  # *lines
    difs = []
    zipped = enumerate(zip(*lines))
    for idx, chars in zipped:
        if len(set(chars)) != 1:
            dif = Difference(idx, idx + 1)
            while pair := next(zipped, False):
                _, nextChars = pair
                if len(set(nextChars)) == 1:
                    break
                dif.end += 1
            difs.append(dif)

    sortedLines = sorted(lines, key=len)
    if (sortedLines[0] != sortedLines[-1]):
        difs.append(Difference(len(sortedLines[0]), len(sortedLines[-1])))
    return difs


def print_styled(s, difs):
    prev = 0
    if (len(difs) == 0):
        print(match.format(s), end='')
    else:
        for dif in difs:
            print(match.format(s[prev:dif.start]), end='')
            print(difference.format(s[dif.start:dif.end]), end='')
            prev = dif.end
    print()


def print_difs(difs, lines=None, files=None):  # Eh
    print(difs)


def print_lines(difs, lines, files):
    for file, line in enumerate(lines):
        print(infoSecondary.format('*' + files[file].name + '*'))
        print_styled(line, difs)


def print_full(difs, lines, files):
    print_lines(difs, lines, files)
    print_difs(difs)


def main(args):
    printer = (print_difs
                if args.only_difs
                else (print_full
                        if args.difs
                        else print_lines))

    for idx, lines in islice(enumerate(zip(*args.files)), args.start, args.until):
        print(infoPrimary.format("--------------Line #{}--------------".format(idx)))
        printer(find_difs(lines), lines, args.files)


if __name__ == "__main__":
    parser = ArgumentParser(
        prog='TextCMP',
        formatter_class=RawDescriptionHelpFormatter,
        description='''
---------------------------------------------------------------
    Script which finds differences between text files.
    Comparing files line by line (hence it compares until
    shortest file is exhausted), highlighting differences.
---------------------------------------------------------------
        ''')
    parser._positionals.title = "Required"
    parser._optionals.title = "Optional"
    parser.add_argument("files", help="input files to compare", metavar="FILES",
                        nargs='+', type=lambda x: file_valid(parser, x))
    parser.add_argument("-d", "--difs", action="store_true",
                        help="output differences list")
    parser.add_argument("-D", "--only-difs", action="store_true",
                        help="output only differences list")
    parser.add_argument("-s", "--start", type=int,
                        help="from nth line")
    parser.add_argument("-u", "--until", type=int,
                        help="until nth line")
    args = parser.parse_args()
    main(args)

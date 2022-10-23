#!/usr/bin/env python3
from colorama import Fore, Style
from recordclass import dataobject
from argparse import ArgumentParser


class Difference(dataobject):
    start: int
    end: int


infoPrimary = Fore.GREEN + Style.DIM + '{}' + Style.RESET_ALL
infoSecondary = Fore.CYAN + Style.BRIGHT + '{}' + Style.RESET_ALL
difference = Fore.RED + Style.BRIGHT + '{}' + Style.RESET_ALL
match = Fore.GREEN + Style.NORMAL + '{}' + Style.RESET_ALL
error = Fore.RED + Style.BRIGHT + '{}' + Style.RESET_ALL


err_invalid_arg_amount = error.format("Expected exactly 2 arguments: 2 files to compare.\n")
err_invalid_file = error.format("Invalid file: {}\n")


def file_len(filename):
    with open(filename) as f:
        for i, _ in enumerate(f):
            pass
    return i + 1


def file_valid(parser, file):
    try:
        return open(file)
    except IOError:
        parser.error(err_invalid_file.format(file))


def find_difs(*lines):
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
    for dif in difs:
        print(match.format(s[prev:dif.start]), end='')
        print(difference.format(s[dif.start:dif.end]), end='')
        prev = dif.end
    print()


def main(files):
    for idx, lines in enumerate(zip(*files)):
        difs = find_difs(*lines)
        print(infoPrimary.format("--------------Line #{}--------------".format(idx)))
        for file, line in enumerate(lines):
            print(infoSecondary.format('*' + files[file].name + '*'))
            print_styled(line, difs)


if __name__ == "__main__":
    parser = ArgumentParser(description='Script which finds differencies between text files.')
    parser.add_argument("-f", dest="files", required=True,
                        help="input files to compare", metavar="FILE",
                        nargs='+', type=lambda x: file_valid(parser, x))
    args = parser.parse_args()
    main(args.files)
    # compare string not files
    # compare arbitrary amount of strings/files
    # argument -f to compare files instead of strings followed by arbitrary amount of files
    # argument -o output difs list
    # argument -O output only difs list

    # else:
    #     print(err_invalid_arg_amount)
    #     parser.print_help()

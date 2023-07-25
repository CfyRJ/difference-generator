#!/usr/bin/env python3


import argparse


from gendiff.gendiff import generate_diff


TEXT_HELP = '''Compares two configuration files and shows a difference.
Available formats: stylish, plain, json.'''


def main():
    res = generate_diff(args.path_file1, args.path_file2, args.format)
    print(res)


parser = argparse.ArgumentParser(description=TEXT_HELP)

parser.add_argument('path_file1',
                    type=str,
                    help='Path to the first (old) file.')
parser.add_argument('path_file2',
                    type=str,
                    help='Path to the second (new) file.')
parser.add_argument('-f', '--format',
                    dest='format',
                    default='stylish',
                    type=str,
                    help='Result output format.')

args = parser.parse_args()


if __name__ == '__main__':
    main()

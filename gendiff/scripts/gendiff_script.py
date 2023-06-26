#!/usr/bin/env python3

import argparse


parser = argparse.ArgumentParser(
    prog='gendiff',
    description='Compares two configuration files and shows a difference.'
    )
parser.add_argument('first_file')
parser.add_argument('second_file')
parser.add_argument(
    '-f FORMAT',
    metavar='--format FORMAT',
    help='set format of output'
    )
parser.print_help()


def main():
    print('Hello world!')


if __name__ == '__main__':
    main()

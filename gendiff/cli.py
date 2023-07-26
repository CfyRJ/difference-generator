import argparse


TEXT_HELP = '''Compares two configuration files and shows a difference.
Available formats: stylish, plain, json.'''


def make_parser():
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

    return parser

"""
These helpers are external to setup.py to allow them to be debugged
and tested without running a setup.py
"""
import os
import subprocess

def get_version():
    version = '0.0.1'
    if os.path.isdir('.git'):
        version = subprocess.check_output(['git', 'describe']).strip().decode('utf-8')
        with open('VERSION.txt', 'w') as f:
            f.write('%s\n' % version)
    elif os.path.isfile('VERSION.txt'):
        with open('VERSION.txt', 'r') as f:
            version = f.read().strip()
    return version


def filter_dependencies(lines):
    """
    Remove lines that are empty, for comments, imports or options,
    and parse the package name.
    :param lines: a list of lines
    :return: a list of package names
    """
    non_empty_lines = filter(lambda l: len(l) > 0, lines)
    non_comment_lines = filter(lambda l: not l.startswith('#'), non_empty_lines)
    package_lines = filter(lambda l: not l.startswith('-'), non_comment_lines)

    def package_name_from(line):
        matches = [line.index(c) for c in '><=,' if c in line]
        if len(matches) > 0:
            line = line[:min(matches)]
        return line

    packages = [package_name_from(line) for line in package_lines]
    return packages


def get_dependencies(path):
    """
    Parse requirements files using pip internals and return only the name of the requirement
    """
    lines = []
    with open(path, 'r') as f:
        lines = [l.strip() for l in f]
    return filter_dependencies(lines)


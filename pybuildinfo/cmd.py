# -*- coding: UTF-8 -*-
"""
Python Build Info Tool
Starter
"""
import os
import sys
import argparse
import json
import logging
import pybuildinfo
import pybuildinfo.vcs as vcs
from pybuildinfo.run import run
from pybuildinfo import resource


def arg_path(arg):
    arg = os.path.abspath(arg)
    if not os.path.isdir(arg):
        raise argparse.ArgumentError()
    return arg


def cmd(argv):
    vcs_all = []
    for x in vcs.all_vcs():
        vcs_all.extend(x(void=True).alias)
    vcs_all = [x.lower() for x in vcs_all]

    parser = argparse.ArgumentParser()
    parser.add_argument('-o',
                        type=argparse.FileType('wb'),
                        default=sys.stdout.buffer,
                        dest='output'
                        )
    parser.add_argument('-vcs',
                        type=arg_path,
                        default=os.getcwd(),
                        dest='vcs_dir'
                        )
    parser.add_argument('-vcs-force',
                        type=str,
                        dest='vcs_force',
                        choices=vcs_all
                        )
    parser.add_argument('-dict',
                        type=str,
                        default='{}'
                        )
    parser.add_argument('-template',
                        type=argparse.FileType('r'),
                        default=resource.r_find('default.hpp')
                        )
    parser.add_argument('-verbose',
                        action='store_true'
                        )
    parser.add_argument('-version',
                        action='store_true'
                        )
    parser.add_argument('-version-regex',
                        type=str
                        )
    parser.add_argument('-quiet',
                        action='store_true'
                        )
    args = parser.parse_args(argv)

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)

    if args.version:
        print(pybuildinfo.version())
        return 0

    return run(
        usr_dict=json.loads(args.dict),
        vcs_root=args.vcs_dir,
        vcs_force=args.vcs_force,
        output=args.output,
        template=args.template,
        version_regex=args.version_regex,
        quiet=args.quiet,
    )


def main():
    cmd(sys.argv[1:])


if __name__ == '__main__':
    main()

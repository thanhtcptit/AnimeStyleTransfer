import os
import sys
import pkgutil
import argparse
import importlib


def import_submodules(package_name):
    importlib.invalidate_caches()

    sys.path.append('.')

    module = importlib.import_module(package_name)
    path = getattr(module, '__path__', [])
    path_string = '' if not path else path[0]

    # walk_packages only finds immediate children, so need to recurse.
    for module_finder, name, _ in pkgutil.walk_packages(path):
        # Sometimes when you import third-party libraries that are on your path
        # `pkgutil.walk_packages` returns those too, so we need to skip them.
        if path_string and module_finder.path != path_string:
            continue
        subpackage = f'{package_name}.{name}''
        import_submodules(subpackage)


import_submodules('src')
from src.utils import load_json


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    subcommands = {
        'preprocess': Preprocess(),
        'train': Train(),
        'experiments': Experiments(),
    }
    for name, subcommand in subcommands.items():
        subparser = subcommand.add_subparser(name, subparsers)

    args = parser.parse_args()
    if 'func' in dir(args):
        args.func(args)
    else:
        parser.print_help()


class Preprocess:
    def add_subparser(self, name, parser):
        description = '''Preprocess the specified dataset.'''
        subparser = parser.add_parser(name, description=description)

        subparser.add_argument(
            'param_path', type=str,
            help='path to parameter file describing the model to be trained')
        subparser.add_argument(
            '-f', '--force', action='store_true', required=False,
            help='overwrite the output directory if it exists')

        subparser.set_defaults(func=preprocess)
        return subparser


def preprocess(args):
    params = load_json(args.param_path)
    return func(params, args.force)


class Train(Subcommand):
    def add_subparser(self, name, parser):
        description = '''Train the specified model on the specified dataset.'''
        subparser = parser.add_parser(
            name, description=description, help='Train a model.')

        subparser.add_argument(
            'param_path', type=str,
            help='path to parameter file describing the model to be trained')
        subparser.add_argument(
            '-s', '--serialization-dir', type=str,
            help='directory in which to save the model and its logs')
        subparser.add_argument(
            '-r', '--recover', action='store_true', default=False,
            help='recover training from the state in serialization_dir')
        subparser.add_argument(
            '-f', '--force', action='store_true', required=False,
            help='overwrite the output directory if it exists')

        subparser.set_defaults(func=train_model)
        return subparser


def train_model(args):
    params = load_json(args.param_path)
    serialization_dir = args.serialization_dir
    if not serialization_dir:
        param_filename = os.path.splitext(os.path.split(args.param_path)[1])[0]
        serialization_dir = os.path.join('checkpoints', param_filename)
    return func(params, serialization_dir, args.recover,
                args.force)


class Experiments(Subcommand):
    def add_subparser(self, name, subparsers):
        description = 'Run multi experiments.'
        subparser = subparsers.add_parser(name, description=description)

        subparser.add_argument(
            'experiments_dir', type=str,
            help='path to directory contains config files')
        subparser.add_argument(
            'log_dir', type=str,
            help=('directory in which to save the model and its logs.'))
        subparser.add_argument(
            '-r', '--recover', action='store_true',
            help='recover training from the state in serialization_dir')
        subparser.add_argument(
            '-f', '--force', action='store_true',
            help='force override serialization dir')
        subparser.add_argument(
            '-d', '--display_logs', action='store_true',
            help='Options to display logs in shell')

        subparser.set_defaults(func=run_multi_experiments)
        return subparser


def run_multi_experiments(args):
    from src.run_experiments import main as run_experiments
    return run_experiments(args.experiments_dir, args.log_dir, args.recover,
                           args.force, args.display_logs)


def run():
    main()


if __name__ == "__main__":
    run()

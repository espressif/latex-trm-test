import argparse
import subprocess
import glob
from timeit import default_timer as timer


def build_all(chip_series, module_names, languages):

    processing_times = {}

    for target in chip_series:
        for module in module_names:
            for language in languages:
                clean_output(target, module, language)
                document = glob.glob(f"{target}/*{module}__{language}.tex")[0]
                print(f'Building PDF for {document}')
                start = timer()
                build_cmd = [
                    'python',
                    'build-pdf.py',
                    '-c', target,
                    '-m', module,
                    '-l', language
                ]
                subprocess.run(build_cmd)
                processing_times[document] = timer() - start

    print('Build time(s) in seconds:')
    for document, build_time in processing_times.items():
        print(document, f' {build_time:.0f}')

def clean_all(chip_series, module_names, languages):

    for target in chip_series:
        for module in module_names:
            for language in languages:
                clean_output(target, module, language)

def clean_output(target, module, language):

    document = glob.glob(f"{target}/*{module}__{language}.tex")[0]
    print(f'Cleaning build artifacts of {document}')
    clean_cmd = [
        'latexmk',
        '-m',
        '-output-directory=out'
    ]
    subprocess.run(clean_cmd, cwd=target)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Build PDFs from LaTeX sources'
    )
    parser.add_argument(
        '-ca', '--clean_all',
        action='store_true',
        help='Clean all existing build artifacts only, do not build.'
    )
    parser.add_argument(
        'chip_series',
        nargs='+',
        help='Chip series to build PDFs for'
    )
    parser.add_argument(
        'module_names',
        nargs='+',
        help='Module names to build PDFs for'
    )
    parser.add_argument(
        'languages',
        nargs='+',
        help='Languages to build PDFs in'
    )

    args = parser.parse_args()

    if args.clean_all:
        clean_all(args.chip_series, args.module_names, args.languages)
    else:
        build_all(args.chip_series, args.module_names, args.languages)

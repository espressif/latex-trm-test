import argparse
import subprocess
import os.path
import os
import glob


def build_pdf(chip_series, module_names, languages):

    build_cmd = [
        'latexmk',
        '-pdf',
        # When ``-f`` is used, latexmk will continue building
        # if it encounters errors. We still receive a failure exit code
        # in this case, but the correct steps should run.
        '-f',
        '-dvi-',    # dont generate dvi
        '-ps-',     # dont generate ps
        '-interaction=nonstopmode',
        '-quiet',
        '-output-directory=out',
        '-cd',      # change to the directory where the build file is located
    ]

    # Extract module name from the last part of the file name before splitting by '__'
    module_name = module_names.split('__')[-1]
    file_path_tex = glob.glob(f"{chip_series}/*{module_names}__{languages}.tex")[0]
    file_path_pdf = file_path_tex.replace(chip_series, f"{chip_series}/out", 1) \
                            .replace('.tex', '.pdf')

    # Export DOCUMENT_PATH as an environment variable
    with open("doc_path.env", "w") as env_file:
        env_file.write(f"DOCUMENT_PATH={file_path_pdf}")

    print(f'Building PDF from {file_path_tex}')
    if os.path.exists(file_path_tex) == False:
        print(f'Input file {file_path_tex} does not exist!')
        exit(1)
    subprocess.run(build_cmd + [file_path_tex], cwd='.')
    if os.path.exists(file_path_pdf) == False:
        print(f'Output file {file_path_pdf} has not been built!')
        exit(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Build PDFs')
    parser.add_argument('-c', '--chip_series', type=str, help='Chip series')
    parser.add_argument('-m', '--module_names', type=str, help='Module names')
    parser.add_argument('-l', '--languages',    type=str, help='Languages')

    args = parser.parse_args()

    if args.chip_series and args.module_names and args.languages:
        build_pdf(args.chip_series, args.module_names, args.languages)

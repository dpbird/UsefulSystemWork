import os
import subprocess
import shutil
import csv
from glob import glob
from tqdm import tqdm
import argparse
import multiprocessing


def run_silently(args):
    p = subprocess.run(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if p.returncode != 0:
        print(p.stdout.decode('utf-8'))
        raise subprocess.CalledProcessError(p.returncode, ' '.join(args))


def helper(row):
    andrew_id = row['Andrew ID']
    first = row['Preferred/First Name']
    last = row['Last Name']
    room = row['Room']
    seat = row['Seat']
    num = row['Exam Number']

    # Hacky seat number fix ('A1' to 'A01')
    seat = seat.strip()
    if len(seat) == 2:
        seat = seat[0] + '0' + seat[1]
    else:
        assert len(seat) == 3
    # Exam number fix ('1' to '001')
    num = int(num)
    num = '%03d' % (num)
    # Replace '/' in seat number (e.g. 'N/A' to 'NA')
    seat = seat.replace('/', '')

    # Dictionary of (old string --> new string) replacements
    replace_dict = {'\\toreplace{fullName}' : first + ' ' + last,
                   '\\toreplace{andrewID}' : andrew_id,
                   '\\toreplace{roomNumber}' : room,
                   '\\toreplace{seatNumber}' : seat,
                   '\\toreplace{examNumber}' : num}

    # For each .tex file in the latex_src directory, create a copy
    # of it in latex_copy with the string replacements made
    tmp_local = os.path.join(args.temp_dir, multiprocessing.current_process().name)
    if not os.path.exists(tmp_local):
        shutil.copytree(args.in_dir, tmp_local)
        files_to_copy = [args.main_file.replace('.tex', '.aux'),
                         args.main_file.replace('.tex', '.out')]
        if args.precompile:
            files_to_copy.append(args.main_file.replace('.tex', '.fmt'))
        for f in files_to_copy:
            shutil.copyfile(os.path.join(args.temp_dir, f), os.path.join(tmp_local, f))

    for tex_file in changing_files:
        with open(os.path.join(args.in_dir, tex_file)) as f:
            main_str = f.read()

        for k, v in replace_dict.items():
            main_str = main_str.replace(k, v)

        if args.precompile:
            if tex_file == args.main_file:
                tail = main_str[main_str.find("\\begin{document}"):]
                main_str = f"%&{args.main_file.replace('.tex', '')}" + os.linesep + tail

        with open(os.path.join(tmp_local, tex_file), 'w') as f:
            f.write(main_str)

    # Run latex to create the student-specific output PDF in latex_src_copy
    os.chdir(tmp_local)
    run_silently([args.latex_cmd, '-halt-on-error', args.main_file])

    # Move the student-specific PDF to the output directory
    main_pdf = args.main_file.replace('.tex', '.pdf')
    out_pdf = os.path.join('..', '..', args.out_dir, '{}-{}-{}-{}.pdf'.format(num, room, seat, andrew_id))
    shutil.copyfile(main_pdf, out_pdf)
    os.chdir('..')
    os.chdir('..')


def set_globals(args_in, changing_files_in):
    global args
    global changing_files
    args = args_in
    changing_files = changing_files_in


def main(args):
    
    assert os.path.exists(args.in_dir)

    # Make latex_src_copy directory
    if os.path.exists(args.temp_dir):
        shutil.rmtree(args.temp_dir)
    shutil.copytree(args.in_dir, args.temp_dir)

    # Make pdfs directory
    if not os.path.exists(args.out_dir):
        os.mkdir(args.out_dir)

    # Halt option depends on latex_cmd:
    halt_option = '-halt-on-error' if args.latex_cmd == 'pdflatex' else '--halt-on-error'

    # Test that compile succeeds with no changes
    os.chdir(args.temp_dir)
    cmd = [args.latex_cmd, halt_option, args.main_file]
    print('Running cmd: ', ' '.join(cmd))
    run_silently(cmd)

    # precompile fmt if necessary
    if args.precompile:
        if args.latex_cmd != "pdflatex":
            raise ValueError("Can only run precompilation with pdflatex")
        cmd = ['pdflatex', '-shell-escape', '-ini', f'-jobname="{args.main_file.replace(".tex", "")}"', '"&pdflatex"', 'mylatexformat.ltx', args.main_file]
        print('Running cmd: ', ' '.join(cmd))
        run_silently(cmd)
    os.chdir('..')

    with open(args.seating_chart_csv, 'r') as chart:
        reader = csv.DictReader(chart)
        rows = list(reader)

    changing_files = set()
    for tex_path in glob(os.path.join(args.in_dir, '*.tex')):
        with open(tex_path) as f:
            main_str = f.read()
            if "toreplace" in main_str:
                changing_files.add(os.path.basename(tex_path))

    # loop over students
    with multiprocessing.Pool(args.num_threads, initializer=set_globals, initargs=(args, changing_files)) as p:
        _ = list(tqdm(p.imap_unordered(helper, rows), total=len(rows)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create student-specific PDFs of the exam via string replacement in .te files.')
    parser.add_argument('--main_file', default='main.tex', help='Filename of main file for compiling with latex')
    parser.add_argument('--seating_chart_csv', default='seating_chart.csv', help='Filename of main file for compiling with latex')
    parser.add_argument('--in_dir', default='latex_src', help='Input directory containing latex source')
    parser.add_argument('--temp_dir', default='latex_src_copy', help='Temporary directory')
    parser.add_argument('--out_dir', default='pdfs', help='Output directory containin PDFs')
    parser.add_argument('--latex_cmd', default='pdflatex', help='Latex compiler binary')
    parser.add_argument('--num_threads', default=12, type=int, help='Number of threads to use')
    parser.add_argument('--precompile', default=False, type=bool,
        help="""Whether to precompile header. TeX header (not pdf header) must 
        be entirely static, all toreplace commands should be moved into 
        document environment. PDF header definition can be moved into main 
        right under definition of toreplace.""")
    args = parser.parse_args()
    # main(args)

    print("Overleaf files found:")
    for dir in os.listdir(args.in_dir):
        print(dir)
    print("Which file do you want to generate:")
    
    genFile = input()

    if genFile in os.listdir(args.in_dir):
        #DO THE THING
        args.in_dir = os.path.join(args.in_dir, genFile)
        print(args.in_dir)
        main(args)
    else:
        print("You must select a file from the list presented! Closing down.")

# TODO: this can potentially be further optimized by use of latexmk pvc and repeated edits/copies

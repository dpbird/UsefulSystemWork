import os
import subprocess
import shlex
import shutil
import csv
from glob import glob
from tqdm import tqdm
import argparse

# def run_silently(args):
#     p = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
#     print(f"p: {p}")
#     if p.returncode != 0:
#         print(p.stdout.decode('utf-8'))
#         raise subprocess.CalledProcessError(p.returncode, ' '.join(args))

def run_silently(args):
    p = subprocess.run(' '.join(args), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    # print(f"p: {p}\n\n\n")
    if p.returncode != 0:
        # print("ERROR\nERROR\nERROR")
        # print("Decode:")
        print(p.stdout.decode('utf-8'))
        raise subprocess.CalledProcessError(p.returncode, ' '.join(args))


'''
This function merges all the tex files specified by \input{} in the main tex file
It is capable of handling input files specified by a relative path
It also handles nested \input{} commands
It does not copy over the input files when the \input{} command is commented out
It raises a runtime error when there is a parsing problem
'''
def collect_inputs(path):
    merged_tex = []
    input_command = "\\input{"
    line_number = 0
    with open(path, "r") as f:
        for line in f:
            line_number += 1
            # check if the \input{} command exists
            input_command_index = line.find(input_command)
            if input_command_index != -1:
                # the \input{} command is in this line
                comment_index = line.find("%")
                # check if the \input{} command is commented out
                if comment_index == -1 or comment_index > input_command_index:
                    # in this case it's not commented out, replace it
                    input_command_end_index = line[input_command_index:].find("}")
                    if input_command_end_index == -1:
                        # if we can't find the end curly brace, raise an error
                        error_message = ("Cannot find matching end brace"
                            + " for \\input command in file {} on line {}.\n"
                            + " Problematic line: {}").format(path, line_number, line)
                        raise RuntimeError(error_message)
                    #print(f"input_command_index: {input_command_index}\nlen(input_command): {len(input_command)}\ninput_command_end_index: {input_command_end_index}")
                    replace_path = line[input_command_index + len(input_command):\
                        input_command_index+input_command_end_index].strip()
                    #print("DEBUG: replace_path = " + replace_path)
                    absolute_replace_path = os.path.join(os.path.dirname(path), replace_path)
                    #print(f"Current path:{path}\nabsolute_replace_path: {absolute_replace_path}\nLine: {line}")
                    merged_tex += collect_inputs(absolute_replace_path)
                else:
                    # it's commented out
                    merged_tex.append(line)
            else:
                # it's just a normal line
                merged_tex.append(line)
                pass
    return merged_tex

    
def main(args):
    
    assert os.path.exists(args.in_dir)

    # Make latex_src_copy directory
    if os.path.exists(args.temp_dir):
        shutil.rmtree(args.temp_dir)
    shutil.copytree(args.in_dir, args.temp_dir)

    # Make pdfs directory
    #if os.path.exists(args.out_dir):
    #    shutil.rmtree(args.out_dir)
    if not os.path.exists(args.out_dir):
        os.mkdir(args.out_dir)

    with open(args.seating_chart_csv, 'r') as chart:
        reader = csv.DictReader(chart)

        # Halt option depends on latex_cmd:
        halt_option = '-halt-on-error' if args.latex_cmd == 'pdflatex' else '--halt-on-error'
        
        # Test that compile succeeds with no changes
        os.chdir(args.temp_dir)
        cmd = [args.latex_cmd, halt_option, args.main_file]
        print('Running cmd: ', ' '.join(cmd))
        run_silently(cmd)
        os.chdir('..')

        # Read each line of the SeatingChart.csv
        for row in tqdm(list(reader)):
            print(f"Currently Processing: {row}")
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

            # Gather all the .tex input one string (including \inputs{})
            main_lines = collect_inputs(os.path.join(args.in_dir, args.main_file))
            main_str = ''.join(main_lines)
            # Create a copy of it in args.temp_dir with the string replacements made
            for k, v in replace_dict.items():
                main_str = main_str.replace(k, v)

            with open(os.path.join(args.temp_dir, args.main_file), 'w') as f:
                f.write(main_str)
                print(f)
                
            # For each .tex file in the latex_src directory, create a copy
            # of it in latex_copy with the string replacements made
            # for tex_path in glob(os.path.join(args.in_dir, '*.tex')):
            #     tex_file = os.path.basename(tex_path)
            #     with open(os.path.join(args.in_dir, tex_file)) as f:
            #         main_str = f.read()

            #     for k, v in replace_dict.items():
            #         main_str = main_str.replace(k, v)

            #     with open(os.path.join(args.temp_dir, tex_file), 'w') as f:
            #         f.write(main_str)

            # Run latex to create the student-specific output PDF in latex_src_copy
            os.chdir(args.temp_dir)
            run_silently([args.latex_cmd, halt_option, args.main_file])

            # Move the student-specific PDF to the output directory
            main_pdf = args.main_file.replace('.tex', '.pdf')
            print(f"main_pdf: {main_pdf}")
            out_pdf = os.path.join('..', args.out_dir, '{}-{}-{}-{}.pdf'.format(num, room, seat, andrew_id))
            shutil.copyfile(main_pdf, out_pdf)
            os.chdir('..')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create student-specific PDFs of the exam via string replacement in .te files.')
    parser.add_argument('--main_file', default='main.tex', help='Filename of main file for compiling with latex')
    parser.add_argument('--seating_chart_csv', default='seating_chart.csv', help='Filename of main file for compiling with latex')
    parser.add_argument('--in_dir', default='latex_src', help='Input directory containing latex source')
    parser.add_argument('--temp_dir', default='latex_src_copy', help='Temporary directory')
    parser.add_argument('--out_dir', default='pdfs', help='Output directory containin PDFs')
    parser.add_argument('--latex_cmd', default='pdflatex', help='Latex compiler binary')

    args = parser.parse_args()

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

    

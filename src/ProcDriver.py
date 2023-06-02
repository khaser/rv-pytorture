import os
import subprocess

def clean():
    clean_results()
    clean_tmp()

def clean_results():
    _run("make rm_results -s")

def clean_tmp():
    _run("make rm_tmp -s")

def get_rank():
    return _parse_rank("make get_rank")

def get_coverage():
    return _run("make get_coverage")

def get_total_rank():
    return sum(map(lambda x : x[2], _parse_rank("make get_total_rank")))

def run_test(name, text):
    filename = os.path.join(_get_tmp_dirname(), f"{name}.S")
    print(text, file=open(filename, "w+"))

    proc = subprocess.run(f"make PROG={name} run", shell = True)
    if proc.returncode != 0:
        print(f"Signatures differ, test name: {name}")
        exit(0)

def _parse_rank(cmd):
    output = _run(cmd)
    for test_line in output.strip().split('\n'):
        covered, rank, unique, test_name = test_line.split()
        yield int(covered), int(rank), int(unique), test_name

def _get_tmp_dirname():
    return _run("make get_tmp").strip()

def _run(cmd):
    proc = subprocess.run(cmd, shell = True, stdout = subprocess.PIPE)
    return proc.stdout.decode("utf-8")

#!/usr/bin/env python
'''
* Brett Slatkin, 2014, "effective Python"
* Brett Slatkin's example code([GitHub](https://github.com/bslatkin/effectivepython))
* I modified the example code a bit to confirm my understanding.
* item36.py is written in Python 3.6

Use subprocess to manage child processes
'''
import subprocess
from time import sleep, time
import os

def run_sleep(period):
    proc = subprocess.Popen(['sleep', str(period)])
    return proc

def run_openssl(data):
    """
    Use the openssl command-line tool to encrypt some data
    """
    env = os.environ.copy()
    env['password'] = b'\xe24U\n\xd0Ql3S\x11'
    proc = subprocess.Popen(
        ['openssl', 'enc', '-des3', '-pass', 'env:password'],
        env=env,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE)
    proc.stdin.write(data)
    proc.stdin.flush()  # Ensure the child gets input
    return proc

def run_md5(input_stdin):
    """
    Starts a child process that will cause the md5 commnad-line tool to consume
    an input stream
    """
    proc = subprocess.Popen(
        ['md5'],
        stdin=input_stdin,
        stdout=subprocess.PIPE)
    return proc

if __name__=="__main__":
    # Popen constructor starts the process
    # communicate() method reads the child process's output
    proc = subprocess.Popen(
        ['echo', 'Hello from the child!'], stdout=subprocess.PIPE
        )
    out, err = proc.communicate()
    print(out.decode('utf-8'))
    print("")

    # Child processes will run independently from their parent
    proc = subprocess.Popen(['sleep', '0.3'])
    while proc.poll() is None:
        print('Working...')
        # Some time consuming work here
        sleep(0.2)
    print('Exit status', proc.poll()) # Exit status 0
    print("")

    # start all the child process together upfront
    start = time()
    procs = []
    for _ in range(10):
        proc = run_sleep(0.1)
        procs.append(proc)
    print(procs)
    print("")

    # terminate with the communicate method
    for proc in procs:
        proc.communicate()
    end = time()
    print('Finished in %.3f seconds' % (end - start))
    print("If these processes ran in sequence, the total delay == 1 second not 0.1")
    print("")

    # Pipe data from Python program into a subprocess
    # and retrieve its output
    import os
    procs = []
    for _ in range(3):
        data = os.urandom(10) # in practice, e.g. user input, file handle, ...
        proc = run_openssl(data)
        procs.append(proc)

    # terminate with the communicate method
    # chile processes run in prallel and consume their input
    for proc in procs:
        out, err = proc.communicate()
        print(out[-10:])
    print("")
    # create chains of parallel processes just like UNIX pipes
    # kick off a set of openssl processes to encrypt some data
    # and another set of processes to md5 hash the encrypted output
    input_procs = []
    hash_procs = []
    for _ in range(3):
        data = os.urandom(10) # in practice, e.g. user input, file handle, ...
        proc = run_openssl(data)
        input_procs.append(proc)
        hash_proc = run_md5(proc.stdout)
        hash_procs.append(hash_proc)

    for proc in input_procs:
        proc.communicate()
    for proc in hash_procs:
        out, err = proc.communicate()
        print(out.strip())
    print("")

    # Be sure to pass the timeout parameter
    proc = run_sleep(10)
    try:
        proc.communicate(timeout=0.1)
    except subprocess.TimeoutExpired:
        proc.terminate()
        proc.wait()
    print('Exit status', proc.poll())
    

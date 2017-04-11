#!/usr/bin/env python

"""
Tool for confirming the output of a program piped into stdin is a permutation
of the file passed in as a command line argument
"""

import sys, json

import os 
dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)
inputdir = os.path.join(dir_path, "input")
solutiondir = os.path.join(dir_path, "solutions")

def unique(s):
    if "sortkeys" not in sys.argv:
        return s.rstrip("\n")
    def sortList(l):
        for i in range(len(l)):
            if type(l[i]) == list:
                l[i] = sortList(l[i])
        try:
            return sorted(l)
        except TypeError:
            return l
    try:
        j = json.loads(s)
        if type(j) == list:
            j = sortList(j)

        return json.dumps(j, sort_keys=True)
    except ValueError:
        return s

def read_stdin():
    lines = set()
    get_input = (raw_input if (sys.version_info[0] < 3) else input)
    try:
        while True:
            lines.add(unique(get_input()))
    except EOFError:
        pass #This means STDIN was closed
    return lines

def hashlines(filename):
    lines = set()
    for line in open(filename, 'r').readlines():
        lines.add(unique(line))
    return lines

if __name__ == '__main__':
    if os.path.exists("./MapReduce.py") and os.getcwd() != dir_path:
        os.rename("./MapReduce.py", "./MapReduce_student.py")
    run_all = True if (len(sys.argv) == 2 and sys.argv[1] == "all") else False
    if len(sys.argv) <= 1 or run_all:
        self_path = sys.argv[0]
        import subprocess
        print ("\n\033[1m\033[4mChecking inverted_index.py\033[0m")
        if subprocess.call("PYTHONPATH=$PYTHONPATH%s python inverted_index.py %s/books.json | python %s %s/inverted_index.json 3 sortkeys" % (dir_path, inputdir, self_path, solutiondir), shell=True) > 0 and not run_all:
            exit(-1)

        print ("\n\033[1m\033[4mChecking join.py\033[0m")
        if subprocess.call("PYTHONPATH=$PYTHONPATH:%s python join.py %s/records.json | python %s %s/join.json 3" % (dir_path, inputdir, self_path, solutiondir), shell=True) > 0 and not run_all:
            exit(-1)

        print ("\n\033[1m\033[4mChecking friend_count.py\033[0m")
        if subprocess.call("PYTHONPATH=$PYTHONPATH:%s python friend_count.py %s/friends.json | python %s %s/friend_count.json 3 " % (dir_path, inputdir, self_path, solutiondir), shell=True) > 0 and not run_all:
            exit(-1)

        print ("\n\033[1m\033[4mChecking unique_trims.py\033[0m")
        if subprocess.call("PYTHONPATH=$PYTHONPATH:%s python unique_trims.py %s/dna.json | python %s %s/unique_trims.json 3" % (dir_path, inputdir, self_path, solutiondir), shell=True) > 0 and not run_all:
            exit(-1)

        print ("\n\033[1m\033[4mChecking multiply.py\033[0m")
        if subprocess.call("PYTHONPATH=$PYTHONPATH:%s python multiply.py %s/matrix.json | sed 's/\"//g' | python %s %s/multiply.json 3" % (dir_path, inputdir, self_path, solutiondir), shell=True) > 0 and not run_all:
            exit(-1)

        if not run_all:
            print(u"\n\t\U0001F60E\t\n")

        exit(0)

    else:
        ref_data = hashlines(sys.argv[1])
        out_data = read_stdin()

        indent = 0
        if len(sys.argv) >= 3:
            indent = int(sys.argv[2])

        missing = 0
        wrong = 0

        for i in out_data:
            if i not in ref_data:
                if wrong == 0:
                    print ("\n%s\033[1m\033[91m%s\033[0m" % (" "*indent, "Incorrect lines:")) #\033[91m makes it green, \033[0m makes it white
                wrong += 1
                i = i.replace("\n", "\\n")
                if len(i) > 120:
                    i = i[:50]+("...(%i chars)..."%(len(i) - 100))+i[-50:]
                print ("%s\033[91m%s\033[0m" % (" "*indent, i)) #\033[91m makes it red, \033[0m makes it white

        for i in ref_data:
            if i not in out_data:
                if missing == 0:
                    print ("\n%s\033[1m\033[92m%s\033[0m" % (" "*indent, "Missing lines:")) #\033[91m makes it green, \033[0m makes it white
                missing += 1
                i = i.replace("\n", "\\n")
                if len(i) > 120:
                    i = i[:50]+("...(%i chars)..."%(len(i) - 100))+i[-50:]
                print ("%s\033[92m%s\033[0m" % (" "*indent, i)) #\033[91m makes it green, \033[0m makes it white

        if missing == 0 and wrong == 0:
            print (u"%s\033[0mNice work \U0001F44D" % (" "*indent))
        else:
            print ("\033[0m")
        if wrong:
            print ("%sOutput contains %i lines that are not in the reference file." % (" "*indent, wrong))
        if missing:
            print("%sReference contains %i lines that should have been outputed but were not" % (" "*indent, missing))
        if len(ref_data) != len(out_data):
            print("%sReference contains %i lines but output had %i\n" % (" "*indent, len(ref_data), len(out_data)))

        exit(missing+wrong)

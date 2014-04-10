#!/usr/bin/env python

import os, sys, shutil, subprocess, argparse

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(THIS_DIR, "src", "PyroLibrary"))
sys.path.append(os.path.join(THIS_DIR, "doc"))

def main():
    run_doc_gen()

def run_doc_gen():
    import generate
    print
    generate.main()

if __name__ == '__main__':
    main()
#!/usr/bin/env python3
# The above tells bash or zah or whatever shell program you are using 
# to use python3 to execute this.

import os
import random
import argparse 

def read_filenames():
    # use the args object to get the directory
    # the command below should load in all of the filenames 
    # in this directory, but the syntax might be off (e.g., listdir might be under os.path.listdir?)
    files = os.listdir(args.directory)
    return files

def select_files(filelist):
    # randomly shuffle files
    random.shuffle(filelist)
    # return the first num_samples filenames
    return filelist[:args.num_samples]

def write_selected_files(filelist):
    with open(file("samples.txt"), "w") as f:
        for warc in filelist:
            f.write(warc+"\n")

if __name__ == "__main__":
    # use argparse package to load in variables 
    # right now, just load in number of samples
    parser = argparse.ArgumentParser()
    # look at the documentation to see how to specify that the 
    # number of samples is a number
    parser.add_argument("num_samples")
    # directory is whereever or whatever lists each of the warc files
    parser.add_argument("directory")

    args = parser.parse_args()
    print("Namespace object", args)
    print("Access elements of the namespace object", args.num_samples)

    files = read_filenames()
    print("read in {} files".format(len(files)))
    selected = select_files(files)
    assert len(selected) == args.num_samples
    print("selected {} files".format(len(selected)))
    write_selected_files(selected)

    print("you should now have a list of {} files in samples.txt".format(len(selected)))
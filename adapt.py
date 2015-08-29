import os
import fileinput
import sys

from tempfile import mkstemp
from shutil import move
from os import remove, close
import sys

root = "clang/"

def replace_includes(source_file_path):
    fh, target_file_path = mkstemp()
    target_file= open(target_file_path, 'w')
    source_file= open(source_file_path, 'r')
    for line in source_file:
    #check only the lines with includes
        if line.startswith("#include"):
        #replacing text
            for key in define_equivalence:
                line = line.replace(key, define_equivalence[key])
            for key in config_equivalence:
                line = line.replace(key, config_equivalence[key])
            for key in flatten_includes:
                line = line.replace(key, flatten_includes[key])
        target_file.write(line)
    target_file.close()
    close(fh)
    source_file.close()

    #move(target_file_path, "%s_out.txt"%source_file_path)
    remove(source_file_path)
    move(target_file_path, source_file_path)

def process_files(src_dir):
    for folder, subs, files in os.walk(src_dir):
        for filename in files:
            if filename.endswith(('.c','.h')):
                replace_includes(os.path.join(folder, filename))

def flattenIncludes(src_dir):
    include_dir = src_dir + "/include"
    for folder, subs, files in os.walk(src_dir):
        for filename in files:
            if filename.endswith(('.h')):
                source_path = os.path.join(folder, filename)
                target_path = os.path.join(include_dir, filename)
                move(source_file_path, target_path)
                print("move " + source_file_path + " to " + target_path)

def replace_in_file(source_file_path, search_string, replace_string):
    fh, target_file_path = mkstemp()
    target_file= open(target_file_path, 'w')
    source_file= open(source_file_path, 'r')
    file_data = source_file.read()
    new_data = file_data.replace(search_string,replace_string)
    target_file.write(new_data)
    target_file.close()
    close(fh)
    source_file.close()
    remove(source_file_path)
    move(target_file_path, source_file_path)

def process_includes():
    replace_in_file(root + "include/llvm/Support/Host.h",
    "#if defined(__linux__)",
    "#if defined(__linux__) || defined(__EMSCRIPTEN__) // XXX EMSCRIPTEN")

if __name__ == '__main__':
    process_includes()
    print("ADAPTATION DONE!")

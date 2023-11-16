import os
import shutil
from os.path import isdir

os.system("mdbook build")
os.system("cd stdlib && mdbook build & cd ..")
os.system("cd book && mkdir stdlib & cd ..")
    
source_dir = './stdlib/book'
target_dir = './book/stdlib'
    
file_names = os.listdir(source_dir)

for file_name in file_names:
    shutil.move(os.path.join(source_dir, file_name), target_dir)

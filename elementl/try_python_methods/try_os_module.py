import os
# print absolute path of the file
print(os.path.abspath('config.py'))

# create the target directory and its parent directories if not existing
# target_dir = "advanced"
# parent_dir = "/Users/a16502/dyc/elementl/tutorials"
target_dir = "python_methods"
parent_dir = "/Users/a16502/dyc/elementl/"  # end of the str "/" doesn't matter
path = os.path.join(parent_dir, target_dir)
os.makedirs(path, exist_ok=True)
# if exist_ok use default value false, when running again, it wil raise
# FileExistsError: [Errno 17] File exists: /Users/a16502/dyc/elementl/tutorials/advanced'
print("Direcotry '%s' created" % target_dir)

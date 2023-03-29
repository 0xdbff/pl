# my_lib.py

def slurp(filename):
    with open(filename, "r") as fh:
        contents = fh.read()
    return contents

#   fh = open(filename, "r")
#   contents = fh.read()
#   fh.close()
#   return contents
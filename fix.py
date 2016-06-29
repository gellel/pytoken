file_str = ""

with open("fixed.txt") as f:
    file_str = f.read()

print type(file_str)
#
file_str = "".join(file_str.split())

#
with open("fixed.txt", 'w') as f:
    f.write(file_str)
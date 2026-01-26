a = input()
a =  a.replace("em", "__TEMP__").replace("anh", "em").replace("__TEMP__", "anh")
print(a)
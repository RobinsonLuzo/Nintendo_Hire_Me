# Redundant now, as implemented in solution.py
byte_array = bytearray(b'7U\xd6\xfa\xb2>RY\xef\x95v\xba\x07\xbf4\xae\x0c\x1e7\x9e(\t\r\xd7r\xfb\xc9\x07\x18\x0788')

input_arr = [hex(i) for i in byte_array]

f = open("input_arr_solution.txt", "a")
f.write(repr(input_arr)+"\n") # Don't forget to remove ''
f.close()

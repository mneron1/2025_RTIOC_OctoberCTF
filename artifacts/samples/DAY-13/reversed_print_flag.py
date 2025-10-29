# inp = input("Flag: ")

FLAG = [114, 120, 109, 115, 135, 127, 61, 121, 124, 120, 113, 107, 111, 76, 113, 127, 76, 126, 137]

flag = ''.join(chr(x - 12) for x in FLAG)
print("The flag is : " + flag)

#if len(inp) != len(FLAG):
#    print("Wrong!")
#    quit()
#
#for i in range(len(FLAG)):
#    if ord(inp[i])+12 != FLAG[i]:
#        print("Wrong!")
#        quit()
    
print("Success!")
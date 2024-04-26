def fOpen(md):
    return open("BestRecords.txt", md)
f = fOpen("r")
l = [i.split(chr(9)) for i in f]
print(l)
f = fOpen("a")
f.write("NewKing" + chr(9) + "600" + chr(10))
f = fOpen("r")
l = [i.split(chr(9)) for i in f]
print(l)
for i in range(len(l) - 1):
    for j in range(i + 1, len(l)):
        if l[j][-1] > l[i][-1]:
            c = l[j]
            l[j] = l[i]
            l[i] = c
print(l)
f = fOpen("w")
for i in l:
    f.write(chr(9).join(i))
f = fOpen("r")
l = [i.split(chr(9)) for i in f]
print(l)
print(l[0][-1] > l[1][-1])
input("0123456789"[:-2])
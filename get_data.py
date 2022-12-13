import csv as c

genre = input("Genre: ")
year = int(input("Year: "))

    
with open("data.csv", "r") as f:
    data = c.reader(f)
    for i in  data:
        x = [i for i in data if genre in i[3] and int(i[-1])>50 and int(i[4]) in range(year, year+11)]
    
yd, ya = [],[]

for i in x:
    if int(i[7]) > int(i[-3]):
        yd.append([i[1]+" by "+i[2], int(i[6])//2 + (int(i[7])+int(i[9]))//2])
    elif int(i[-3]) > int(i[7]):
        ya.append((i[1]+" by "+i[2], int(i[6])//2 + (int(i[-3])+int(i[9]))//2))



user = input("Mood: ")

if user=='a':
    ya1 = [i[1] for i in ya]
    ya2 = [i[0] for i in ya]
    print(ya2[ya1.index(max(ya1))])
elif user=='d':
    yd1 = [i[1] for i in yd]
    yd2 = [i[0] for i in yd]
    print(yd2[yd1.index(max(yd1))])


#points = (Energy//2 + (Dancebility or Accousticness + Liveness)//2)
number = int(input())
degree = 0

while number % 2 == 0:
    degree += 1
    number //= 2

if degree > 1:
    print(degree)
else:
    print('НЕТ')
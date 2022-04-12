import random
import math
S1 = []
P1 = []
s = []
p = []
t = []
k = []
d = []
for i in range(10):
    S = random.randint(0, 10)
    P = random.randint(1, 11)
    S1.append(S)
    P1.append(P)

    if(S1[i]>=P1[i]):
        s.append(S1[i])
        p.append(P1[i])
        q = math.sqrt(S1[i]*S1[i]-P1[i]*P1[i])
        k.append(q)
        d.append(S1[i])
    else:
        t.append(S1[i])
print("S > P dan bo'lgandagi to'la quvvat natijalari:")
print('k = ', k)
print('\n')
print('Bu qiymatlar S katta bo\'lgan qiymatlar va hisoblash')
print("d = ", d)
print('\n')
print('Bu qiymatlar S dan kichik qiymatlar')
print("t = ", t)
print('\n')
print("Ixtiyoriy to'ldirilgan massiv elemetlari")
print('S = ', S1)
print('P =', P1)
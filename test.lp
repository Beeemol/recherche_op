\Problem name: ULS

Minimize
OBJROW: 300 y(1) + 300 y(2) + 300 y(3) + 300 y(4) + 300 y(5) + 300 y(6) + 300 y(7) + 5 x(1) + 3 x(2) + 4 x(3)
 + 5 x(4) + 6 x(5) + 3 x(6) + 4 x(7) + 2 s(1) + 2 s(2) + 2 s(3) + 2 s(4) + 2 s(5) + 2 s(6)
 + 2 s(7)
Subject To
constr(0):  s(0) = 0
constr(1):  -176 y(1) + x(1) <= -0
constr(2):  x(1) + s(0) >= 30
constr(3):  - x(1) - s(0) + s(1) = -30
constr(4):  s(0) = 0
constr(5):  -146 y(2) + x(2) <= -0
constr(6):  x(2) + s(1) >= 25
constr(7):  - x(2) - s(1) + s(2) = -25
constr(8):  s(0) = 0
constr(9):  -121 y(3) + x(3) <= -0
constr(10):  x(3) + s(2) >= 15
constr(11):  - x(3) - s(2) + s(3) = -15
constr(12):  s(0) = 0
constr(13):  -106 y(4) + x(4) <= -0
constr(14):  x(4) + s(3) >= 47
constr(15):  - x(4) - s(3) + s(4) = -47
constr(16):  s(0) = 0
constr(17):  -59 y(5) + x(5) <= -0
constr(18):  x(5) + s(4) >= 34
constr(19):  - x(5) - s(4) + s(5) = -34
constr(20):  s(0) = 0
constr(21):  -25 y(6) + x(6) <= -0
constr(22):  x(6) + s(5) >= 10
constr(23):  - x(6) - s(5) + s(6) = -10
constr(24):  s(0) = 0
constr(25):  -15 y(7) + x(7) <= -0
constr(26):  x(7) + s(6) >= 15
constr(27):  - x(7) - s(6) + s(7) = -15
Bounds
 0 <= y(0) <= 1
 0 <= y(1) <= 1
 0 <= y(2) <= 1
 0 <= y(3) <= 1
 0 <= y(4) <= 1
 0 <= y(5) <= 1
 0 <= y(6) <= 1
 0 <= y(7) <= 1
Integers
y(0) y(1) y(2) y(3) y(4) y(5) y(6) y(7) x(0) x(1) 
x(2) x(3) x(4) x(5) x(6) x(7) s(0) s(1) s(2) s(3) 
s(4) s(5) s(6) s(7) 
End

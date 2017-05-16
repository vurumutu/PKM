clear;
clc;
% Przypisanie wyznaczonych parametrów z pomiarów (K, T1, T2)
p1f = [36.51798116653935, 1.1223668468425692, 1.122306279293305]; % pierwszy poci¹g do przodu
p1b = [36.034737540826754, 1.1874373694891351, 1.1874855650530429]; % pierwszy poci¹g do ty³u
p2f = [27.058461561109851, 0.26965749323699495, 0.26925471524293587]; % drugi poci¹g do przodu
p2b = [26.764122761035111, 0.2484366865516302, 0.22432088646832404]; % drugi poci¹g do ty³u
p5 = [31.402555847205193, 0.74975242907425443, 0.74817549760812452]; % pi¹ty poci¹g
p6 = [16.490824834771217, 0.93619272651362073, 0.92267930676506804]; % szósty poci¹g

% Stworzenie transmitancji na podstawie parametrów
t1f = tf(p1f(1), [p1f(2)*p1f(3), (p1f(2)+p1f(3)), 1]);
t1b = tf(p1b(1), [p1b(2)*p1b(3), (p1b(2)+p1b(3)), 1]);
t2f = tf(p2f(1), [p2f(2)*p2f(3), (p2f(2)+p2f(3)), 1]);
t2b = tf(p2b(1), [p2b(2)*p2b(3), (p2b(2)+p2b(3)), 1]);
t5 = tf(p5(1), [p5(2)*p5(3), (p5(2)+p5(3)), 1]);
t6 = tf(p6(1), [p6(2)*p6(3), (p6(2)+p6(3)), 1]);

% Wyznaczenie równañ stanu
sys1f = ss(t1f);
sys1b = ss(t1b);
sys2f = ss(t2f);
sys2b = ss(t2b);
sys5 = ss(t5);
sys6 = ss(t6);
import numpy as np

#基板原点座標
x = 61.8
y = 38.5

#fmark_and_markcell原点
x_1 = x-8
y_1 = y+8

#fmark_1
x_2 = x_1
y_2 = y_1+1.325

#fmark_2
x_3 = x_1
y_3 = y_1-1.325

#mark_1
x_4 = x_1
y_4 = y_1+1.025

#mark_2
x_5 = x_1
y_5 = y_1-1.025

c=0.3 #chipsize(mm)
d=0.15 #chip間隔(mm)

#chip
s_1 = x_1-c-d
t_1 = y_1+1.5*c+1.5*d

s_2 = x_1
t_2 =y_1+1.5*c+1.5*d

s_3 =x_1+c+d
t_3 =y_1+1.5*c+1.5*d

s_4 =x_1-c-d
t_4 =y_1+0.5*c+0.5*d

s_5 =x_1
t_5 =y_1+0.5*c+0.5*d

s_6 =x_1+c+d
t_6 =y_1+0.5*c+0.5*d

s_7 =x_1-c-d
t_7 =y_1-0.5*c-0.5*d

s_8 =x_1
t_8 =y_1-0.5*c-0.5*d

s_9 =x_1+c+d
t_9 =y_1-0.5*c-0.5*d

s_10 =x_1-c-d
t_10 =y_1-1.5*c-1.5*d

s_11 =x_1
t_11 =y_1-1.5*c-1.5*d

s_12 =x_1+c+d
t_12 =y_1-1.5*c-1.5*d

print('mark_cell origin',round(x_1,5),round(y_1,5))

print('fmark_1',x_2,round(y_2,5))

print('fmark_2',x_3,round(y_3,5))

print('mark_1',x_4,round(y_4,5))

print('mark_2',x_5,round(y_5,5))

# s_1 ~ s_12 と t_1 ~ t_12 をリストに格納
s_list = [s_1, s_2, s_3, s_4, s_5, s_6, s_7, s_8, s_9, s_10, s_11, s_12]
t_list = [t_1, t_2, t_3, t_4, t_5, t_6, t_7, t_8, t_9, t_10, t_11, t_12]

# for文でリストを使用
for i in range(12):
    x = round(s_list[i],5)
    y = round(t_list[i],5)
    print('chip', i + 1, x, y)

arr_1d = np.array([1, 2, 3, 4, 5])
print("1次元配列:", arr_1d)
# 基板座標
x = 10
y = 10

# 描画ファイル原点座標
x_0 = x - 8
y_0 = y + 8

# 各x,y座標

x_1 = x_0 - 0.3
x_2 = x_0 - 0.1
x_3 = x_0 + 0.1
x_4 = x_0 + 0.3

y_1 = y_0 - 0.2
y_2 = y_0 - 0.1
y_3 = y_0 + 0.1
y_4 = y_0 + 0.3

# chip の場所

print(f"chip_1:({x_1}, {y_1})")
print(f"chip_2:({x_2}, {y_1})")
print(f"chip_3:({x_3}, {y_1})")
print(f"chip_4:({x_4}, {y_1})")
print(f"chip_5:({x_1}, {y_2})")
print(f"chip_6:({x_2}, {y_2})")
print(f"chip_7:({x_3}, {y_2})")
print(f"chip_8:({x_4}, {y_2})")
print(f"chip_9:({x_1}, {y_3})")
print(f"chip_10:({x_2}, {y_3})")
print(f"chip_11:({x_3}, {y_3})")
print(f"chip_12:({x_4}, {y_3})")
print(f"chip_13:({x_1}, {y_4})")
print(f"chip_14:({x_2}, {y_4})")
print(f"chip_15:({x_3}, {y_4})")
print(f"chip_16:({x_4}, {y_4})")
print(f"origin:({x_0}, {y_0})")
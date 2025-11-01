# 基板座標
x = 61.1
y = 38.0

# 描画ファイル原点座標
x_0 = x - 8
y_0 = y + 8

# 各x,y座標


x_1 = x_0 - 0.2
x_2 = x_0 + 0.2



y_1 = y_0 - 0.2
y_2 = y_0 + 0.2


# chip の場所

print(f"chip_1:({x_1}, {y_1})")
print(f"chip_2:({x_2}, {y_1})")
print(f"chip_3:({x_1}, {y_2})")
print(f"chip_4:({x_2}, {y_2})")

print(f"origin:({x_0}, {y_0})")
import matplotlib.pyplot as plt
import numpy as np

file_name = '06_#83_4_90.txt' #''が絶対必要
f = np.loadtxt(file_name,delimiter='\t',) #なぜか区切り文字が'\t'、tab区切りを意味するらしい

a = np.array(f)

a_split = np.hsplit(a,6) #列方向(縦方向)に1列ごとに分割 分割数に注意
 
b_1 = a_split[0] #磁場　#それぞれ1対1対応のデータ
b_2 = a_split[1] #抵抗値
b_3 = a_split[2] #経過時間
b_4 = a_split[3] #電圧
b_5 = a_split[4] #電流
#b_6 = a_split[5] #現在時間(タイムスタンプ)

sorted_b_2 = np.sort(b_2,axis=0) #昇順に並べ替え,列ごとに並べ替え
b_2_ave = np.mean(sorted_b_2[:10]) #最低値から10点の平均
b_2_ratio=b_2/b_2_ave #MR比に直す


x = b_1
y = (b_2_ratio-1)*100

print(b_2_ave)
#print(b_2)
#print(b_2_ratio)

#ここからorigin用データ作成エリア
output_file_name = "up_mr_for_o.txt"

# b_1とsorted_b_2を列方向に結合
output_data = np.hstack((b_1, y))

# ファイルに保存
np.savetxt(output_file_name, output_data, delimiter='\t')

print(f"データを {output_file_name} に保存しました。")

######ここからグラフ作成エリア


plt.scatter(x, y, s=20, c='blue', alpha=1, edgecolors='None') #散布図の作成
plt.xlabel(r'Magnetic Field $\mu_0 H$ (mT)',fontsize=20) #texで斜体で打ちたい
plt.ylabel(r'Resistance $R$(%)',fontsize=20)
plt.tick_params(direction="in") # 目盛りの方向を内向きに設定
plt.xticks(np.arange(-200, 210, 50),fontsize=15)  # X軸の目盛りを -150から150まで50刻みに設定
plt.yticks(np.arange(-0.2, 1.9, 0.2),fontsize=15)  # Y軸の目盛りを 0から6まで1刻みに設定
plt.plot(x, y, marker='none', linestyle='-',c='blue',label='') #隣の点同士を線で結ぶ
plt.xlim(-200,200)
plt.ylim(-0.2,1.8)
plt.legend(title=b_2_ave, fontsize=12, loc="upper right")  # 左上に配置
plt.tight_layout() #余白の調整
plt.savefig( '#83_4.png' , format= 'jpeg' , dpi=300) 
plt.show()


########ここまで

#print(b_2_ave)
#print(y)



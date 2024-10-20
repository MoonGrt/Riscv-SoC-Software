my_dict = {"CH1": [], "CH2": [], "CH3": [], "CH4": []}

# 判断字典的状态
if all(not value for value in my_dict.values()):
    print("字典是全空的")
elif all(value for value in my_dict.values()):
    print("字典是全满的")
else:
    print("字典是半满的")

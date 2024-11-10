from PIL import Image

# 打开图片
image = Image.open("icons/gowin_logo.png")  # 确保图像是 RGBA 格式（包含透明度）

# 如果图像是 RGB 格式（没有透明度），先转换为 RGBA
if image.mode != 'RGBA':
    image = image.convert('RGBA')

# 设置缩放的尺寸
new_width = 700
new_height = 250
resized_image = image.resize((new_width, new_height), Image.LANCZOS)  # 使用 LANCZOS 代替 ANTIALIAS

# 获取裁剪后的图像的像素数据
data = resized_image.getdata()

# 设置透明度（alpha 通道）
new_data = []
for item in data:
    # item 是 (r, g, b, a) 格式
    r, g, b, a = item
    # 设置新的透明度值，0 表示完全透明，255 表示完全不透明
    new_a = int(a * 0.1)  # 设置透明度为原来的 50%
    new_data.append((r, g, b, new_a))

# 更新裁剪后的图像的像素数据
resized_image.putdata(new_data)

# 保存裁剪并修改透明度后的图像
resized_image.save("new.png")

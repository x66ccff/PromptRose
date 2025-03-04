from PIL import Image, ImageDraw

# 创建一个简单的图标
img = Image.new('RGBA', (128, 128), color=(0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# 绘制一个简单的圆形图标
draw.ellipse((10, 10, 118, 118), fill=(30, 120, 200, 255))
draw.ellipse((30, 30, 98, 98), fill=(200, 200, 200, 255))

# 保存为png文件
img.save("icon.png")

# 也保存为ico文件 (Windows图标格式)
img.save("icon.ico", format="ICO")

print("图标文件已创建: icon.png 和 icon.ico")
from PIL import Image

image = Image.open('./assets/duck.png')
image.thumbnail((640,640),Image.Resampling.LANCZOS)

# 裁剪出 [119, 45, 392, 288]
image = image.crop((119, 45, 392, 288)) # x1 y1 x2 y2

# 显示图片
image.show()

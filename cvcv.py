from PIL import Image, ImageDraw, ImageFont, ImageFilter
import colorsys
import  codecs
import os
import time
"识别色例对应rgb"
def get_dominant_color(image):
#颜色模式转换，以便输出rgb颜色值
    image = image.convert('RGBA')
#生成缩略图，减少计算量，减小cpu压力
    image.thumbnail((200, 200))
    max_score = 0
    dominant_color = None
    for count, (r, g, b, a) in image.getcolors(image.size[0] * image.size[1]):
        # 跳过纯黑色
        # if a == 0:
        #     continue
        saturation = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)[1]
        y = min(abs(r * 2104 + g * 4130 + b * 802 + 4096 + 131072) >> 13, 235)
        y = (y - 16.0) / (235 - 16)
        # 忽略高亮色
        # if y > 0.9:
        #     continue
        # Calculate the score, preferring highly saturated colors.
        # Add 0.1 to the saturation so we don't completely ignore grayscale
        # colors by multiplying the count by zero, but still give them a low
        # weight.
        score = (saturation + 0.1) * count
        if score > max_score:
            max_score = score
            dominant_color = (r, g, b)
    return dominant_color

def to_hsv( color ):
    """ converts color tuples to floats and then to hsv """
    return colorsys.rgb_to_hsv(*[x/255.0 for x in color]) #rgb_to_hsv wants floats!

def color_dist( c1, c2):
    """ returns the squared euklidian distance between two color vectors in hsv space """
    return sum( (a-b)**2 for a,b in zip(to_hsv(c1),to_hsv(c2)) )

def min_color_diff( color_to_match, colors):
    """ returns the `(distance, color_name)` with the minimal distance to `colors`"""
    return min( # overal best is the best match to any color:
        (color_dist(color_to_match, test), test) # (distance to `test` color, color name)
        for test in colors)

def write_txt(color,txt_name):

    outfile = open("txt/" + txt_name, 'a', encoding='utf-8')
    color_str = ",".join([str(c) for c in color])
    outfile.writelines(color_str+"\n")

def write_txt1(color,txt_name,path):#写入的扩充RGB,写入的色例RGB,写入的目录

    outfile = open(path+"//" + txt_name, 'a', encoding='utf-8')
    color_str = ",".join([str(c) for c in color])
    outfile.writelines(color_str+"\n")

def draw_pic1(color,path):
    imageSize = (100, 100)
    image = Image.new("RGB", imageSize, color)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("ARIAL.ttf", 15)
    color_str = ",".join([str(c) for c  in color])
    draw.text((10, 50),color_str , font=font)
    # image.show()
    image.save(path+'\\'+color_str+".jpg")

#    draw_pic((255, 205, 0))
def draw_pic(color):
    imageSize = (100, 100)
    image = Image.new("RGB", imageSize, color)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("ARIAL.ttf", 15)
    color_str = ",".join([str(c) for c  in color])
    draw.text((10, 50),color_str , font=font)
    # image.show()
    image.save('pics\\'+color_str+".jpg")

# def handle_pic_main(filename):
#     color = get_dominant_color(Image.open(filename))  # 识别色例对应的rgb
#     color_str = ",".join([str(c) for c in color])
#     print("图片颜色")
#     print(color)
#     result = []  # 内容格式为((r.g,b),与色例的距离）
#     for r in range(0, 256, 5):  # 三个for用于穷举所有rgb跟色例rgb算两点间距离
#         for g in range(0, 256, 5):
#             for b in range(0, 256, 5):
#                 dist = color_dist((r, g, b), color)  # 两点间距离
#                 # pec = r / g if g != 0 else 0
#                 # print(str(pec))
#                 # if pec > 0.9 and pec < 1.1:  # 这个判断可选 如果是绿色系的话规定g的值最大保证色系不变
#                 if max(r,g,b) ==b:
#                 # if r<70 and b<70 and g<70:
#                     result.append(((r, g, b), dist))  # 加入到result数组
#                     # draw_pic((r,g,b))
#     result_sort = sorted(result, key=lambda x: x[1])  # 将结果集根据距离顺序排序
#     # print(result_sort)
#     os.mkdir(color_str)
#     for pic in result_sort[:200]:  # 排名前200的作为扩展色例
#         draw_pic(pic[0])
#         write_txt(pic[0], color_str)

def handle_pic_main1(filename,store_path):
    try:
        print("开始处理" + filename)
        color = get_dominant_color(Image.open(filename))  # 识别色例对应的rgb
        color_str = ",".join([str(c) for c in color])
        print("图片颜色")
        print(color)
        result = []  # 内容格式为((r.g,b),与色例的距离）
        for r in range(0, 256, 5):  # 三个for用于穷举所有rgb跟色例rgb算两点间距离
            for g in range(0, 256, 5):
                for b in range(0, 256, 5):
                    dist = color_dist((r, g, b), color)  # 两点间距离
                    pec = r / g if g != 0 else 0
                    # print(str(pec))
                    # if pec > 0.9 and pec < 1.1:  # 这个判断可选 如果是绿色系的话规定g的值最大保证色系不变
                    if max(r,g,b) ==b:
                    # if r<70 and g <70 and b<70:
                        result.append(((r, g, b), dist))  # 加入到result数组
                    # draw_pic((r,g,b))
        result_sort = sorted(result, key=lambda x: x[1])  # 将结果集根据距离顺序排序
        # print(result_sort)
        path = os.path.join(store_path, color_str)
        print(path)
        os.makedirs(path)
        for pic in result_sort[:600]:  # 排名前200的作为扩展色例
            draw_pic1(pic[0], path)
            write_txt1(pic[0], color_str, path)
    except BaseException:
        print(BaseException)



def main():
    root_path = "C:\\Users\\Silence\Desktop\倪老师数据\肤色\肤色\\"
    color_1 = ["\Purple","\Green","\Orange"] #条件无限制
    color_2 = ["\Black"]
    for i in range(1,7):
        for color in color_2:
            path = root_path+str(i)+color#获取色例的目录
            if os.path.exists(path):
                print("===========fileList========")
                fileList = os.listdir(path)
                storePath = "test\\"+str(i)+color
                # os.makedirs(storePath)#扩充色例以后存的文件夹
                for filename in fileList:
                    pic_path = os.path.join(path, filename)
                    handle_pic_main1(pic_path,storePath)

def main_sytle():
    root_path = "C:\\Users\\Silence\Desktop\倪老师数据\风格\\"
    color_1 = ["\Purple","\Green","\Orange","\Brown","\White"] #条件无限制
    color_2 = ["\Blue"]
    for i in range(1,7):
        for j in range(1,8):
            for color in color_2:
                path = root_path+str(i)+"\\"+str(j)+color#获取色例的目录
                if os.path.exists(path):
                    print(path)
                    fileList = os.listdir(path)
                    storePath = "test300_5_PIC\\"+str(i)+"\\"+str(j)+color
                     # os.makedirs(storePath)#扩充色例以后存的文件夹
                    for filename in fileList:
                        pic_path = os.path.join(path, filename)
                        handle_pic_main1(pic_path,storePath)

if __name__ == '__main__':
    # a = [0.5, 1, 0.5]
    #
    # print(colorsys.rgb_to_hsv(*a))

    # colors = dict((
    #     ((196, 2, 51), "RED"),
    #     ((255, 165, 0), "ORANGE"),
    #     ((255, 205, 0), "YELLOW"),
    #     ((0, 128, 0), "GREEN"),
    #     ((0, 0, 255), "BLUE"),
    #     ((127, 0, 255), "VIOLET"),
    #     ((0, 0, 0), "BLACK"),
    #     ((255, 255, 255), "WHITE"),))
    # color_to_match = (255, 255, 0)
    # dist,col = min_color_diff(color_to_match, colors)
    # handle_pic_main1("C:\\Users\\Silence\Desktop\倪老师数据\肤色\肤色\\1\Green\\1.jpg","test1\\1\Green")
    # main()
    # a=get_dominant_color(Image.open("C:\\Users\Silence\Desktop\倪老师数据\肤色\肤色\\1\Green\\3.jpg"))
    # print(a)
    # handle_pic_main("1.jpg")
    main_sytle()










import os
import shutil
from PIL import Image
path = os.getcwd() + "/"
x = 1304 
y = 809 
total_pixels = x * y

def move_diff_90(range_l, range_h):
    for i in range (range_l, range_h):
        i2p = path + "i2p/" + str(i) + "i2p.png" 
        pub = path + "pub/" + str(i) + "pub.png"

        im_i2p = Image.open(i2p) 
        pix_i2p = im_i2p.load()

        im_pub = Image.open(pub) 
        pix_pub = im_pub.load()

        identical_pixels = 0
        for i_x in range(0, x):
            for i_y in range(0, y):
                if pix_i2p[i_x, i_y] == pix_pub[i_x, i_y]:
                    identical_pixels += 1
        
        p = identical_pixels * 100 / total_pixels
        print(p)
        if p >= 90:
            shutil.move(i2p, path+"same")
            shutil.move(pub, path+"same")


move_diff_90(0, 100)

# def move():
#     for i in range (0, 100):
#         # i2p = path + "diff/" + str(i//2) + "i2p.png" 
#         pub = path + "diff/" + str(i) + "pub.png"
#         if i %2 !=0:
#             shutil.move(pub, path+"pub")
#             # shutil.move(pub, path+"diff")

# move()
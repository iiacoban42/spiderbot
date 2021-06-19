"""Filter images with phash"""
from PIL import Image
import imagehash
import os
import shutil

folder_path = os.getcwd() + "/i2p/i2p/scraper/"
screenshot_pub = folder_path + "screenshots/pub/"
screenshot_i2p = folder_path + "screenshots/i2p/"

images_pub = os.listdir(screenshot_pub)
images_pub.sort()
images_i2p = os.listdir(screenshot_i2p)
images_i2p.sort()

n = len(images_pub)
print(n)

def move_same():
    for i in range(n):
        i2p_img = screenshot_i2p + images_i2p[i]
        pub_img = screenshot_pub + images_pub[i]
        hash_i2p = imagehash.average_hash(Image.open(i2p_img))
        hash_pub = imagehash.average_hash(Image.open(pub_img))
        hash_diff = abs(hash_i2p-hash_pub)
        if hash_diff == 0:
            shutil.move(i2p_img, folder_path + "screenshots/not_blocked/")
            shutil.move(pub_img, folder_path + "screenshots/not_blocked/")

move_same()



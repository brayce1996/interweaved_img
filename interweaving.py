from PIL import Image
import random
im = Image.open('origin.png')
pixelMap = im.load()

img = Image.new( im.mode, im.size)
pixelsNew = img.load()

HEAD_NO_SHIFT = img.size[1] // 3
TAIL_NO_SHIFT = HEAD_NO_SHIFT + img.size[1] // 3

SHIFT_HIGH_MAX = 30
SHIFT_HIGH_MIN = 20
SHIFT_WID_RANGE = 30

print (img.size[1], img.size[0])
shift_high = -1
shift_wid = 0
for i in range(img.size[1]):

    if(shift_high <= 0):
        shift_high = random.randint(SHIFT_HIGH_MIN, SHIFT_HIGH_MAX)
        if shift_wid > 0:
            shift_wid = random.randint(-SHIFT_WID_RANGE, 0)
        elif shift_wid <0:
            shift_wid = random.randint(0, SHIFT_WID_RANGE)
        else:
            shift_wid = random.randint(-SHIFT_WID_RANGE, SHIFT_WID_RANGE)

        print (shift_high, shift_wid)
    else:
        shift_high -= 1
    for j in range(img.size[0]):
        if i < HEAD_NO_SHIFT or i > TAIL_NO_SHIFT or shift_wid == 0:
            pixelsNew[j,i] = pixelMap[j,i]

        elif shift_wid > 0:
            if shift_wid+j >= img.size[0]:
                break
            if j < shift_wid:
                pixelsNew[j*2,i] = pixelMap[j,i]
                pixelsNew[j*2+1,i] = pixelMap[j,i]
            else:
                pixelsNew[shift_wid + j,i] = pixelMap[j,i]
        elif shift_wid < 0:
            j_re = img.size[0] - j - 1
            if j_re + shift_wid < 0:
                break
            if j_re >= img.size[0] + shift_wid:
                pixelsNew[j_re - j,i] = pixelMap[j_re,i]
                pixelsNew[j_re - j - 1,i] = pixelMap[j_re,i]
            else:
                pixelsNew[j_re + shift_wid,i] = pixelMap[j_re,i]
img.show()

from PIL import Image
import random

def generate_shift_arr(h_size, w_size):
    # no shift area
    HEAD_NO_SHIFT = h_size // 3
    TAIL_NO_SHIFT = HEAD_NO_SHIFT + h_size // 3

    # shift pixel range, hight should be positive, and width could be positive or negative.
    SHIFT_HIGH_MAX = 30
    SHIFT_HIGH_MIN = 20
    SHIFT_WID_RANGE = 30

    shift_wid = 0
    sum_high = 0
    shift_high_arr = []
    shift_wid_arr = []
    while (sum_high <= h_size):
        shift_high = random.randint(SHIFT_HIGH_MIN, SHIFT_HIGH_MAX)
        sum_high += shift_high
        shift_high_arr.append(shift_high)

        if sum_high < HEAD_NO_SHIFT or sum_high > TAIL_NO_SHIFT:
            shift_wid = 0
        elif shift_wid > 0:
            shift_wid = random.randint(-SHIFT_WID_RANGE, 0)
        elif shift_wid < 0:
            shift_wid = random.randint(0, SHIFT_WID_RANGE)
        else:
            shift_wid = random.randint(-SHIFT_WID_RANGE, SHIFT_WID_RANGE)
        shift_wid_arr.append(shift_wid)

        print (shift_high, shift_wid)

    return shift_high_arr, shift_wid_arr

def interweaving(origin_img, output_name, shift_high_arr, shift_wid_arr):
    pixelMap = origin_img.load()

    img = Image.new( origin_img.mode, origin_img.size)
    pixelsNew = img.load()
    
    idx = 0
    shift_high = shift_high_arr[0]
    shift_wid = shift_wid_arr[0]
    for i in range(img.size[1]):
        if shift_high < 0:
            idx += 1
            shift_high = shift_high_arr[idx]    # take next hight
            shift_wid = shift_wid_arr[idx]
        else:
            shift_high -= 1                     # decrease by one after finish shifting a pixel row

        for j in range(img.size[0]):
            if shift_wid == 0:
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
    img.save(output_name)

def single_animating(origin_img, shift_high_arr, shift_wid_arr):
    STEPS = 10
    shift_wid_max = shift_wid_arr
    for i in range(STEPS*2):
        output_name = "pic/out_"+str(i)+".png"
        if i < STEPS:   # shift out
            shift_wid_arr = [ (x//STEPS)*i for x in shift_wid_max ]
        else:           # shift back
            shift_wid_arr = [ (x//STEPS)*(STEPS*2 - i) for x in shift_wid_max ]

        interweaving(origin_img, output_name, shift_high_arr, shift_wid_arr)


origin_img = Image.open('origin.png')

shift_high_arr, shift_wid_arr = generate_shift_arr(origin_img.size[1], origin_img.size[0])
#interweaving(origin_img,"test.png",shift_high_arr, shift_wid_arr)
single_animating(origin_img, shift_high_arr, shift_wid_arr)



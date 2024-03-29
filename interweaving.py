from PIL import Image
import random
import os

'''
Variables that you can tune:
    SHIFT_HIGH_MAX/MIN
    SHIFT_WID_MAX/MIN
    
    STEPS

    HEAD_SHIFT_HIGH
    TAIL_SHIFT_HIGH

    the calling structure(at bottom)
'''


def insert_origin_img(src_path, num):
    global pic_num
    for i in range(num):
        os.system("cp " + src_path + " pic/out_" + str(pic_num)+".png")
        pic_num += 1

def generate_shift_arr(h_size, w_size, pre_shift_high=[], pre_shift_wid=[]):
    # no shift area
    HEAD_SHIFT_HIGH = h_size // 3
    TAIL_SHIFT_HIGH = HEAD_SHIFT_HIGH + h_size // 3

    # shift pixel range, hight should be positive, and width could be positive or negative.
    SHIFT_HIGH_MAX = 25
    SHIFT_HIGH_MIN = 15
    SHIFT_WID_MAX = 100
    SHIFT_WID_MIN = 30
    

    # if previous shift array is given
    if len(pre_shift_high) > 0:
        shift_high_arr = pre_shift_high
    else:
        shift_high_arr = []
        sum_high = 0
        while (sum_high <= h_size):
            shift_high = random.randint(SHIFT_HIGH_MIN, SHIFT_HIGH_MAX)
            sum_high += shift_high
            shift_high_arr.append(shift_high)
    
    if len(pre_shift_wid) > 0:
        shift_wid_arr = []
        for shift_wid in pre_shift_wid:     # shift toward another direction and lower intensity
            if shift_wid == 0:
                #shift_wid = random.randint(-SHIFT_WID_RANGE, SHIFT_WID_RANGE)
                shift_wid = 0
            else:
                shift_wid = int(shift_wid * (-1) * random.uniform(0.5,0.8))
            shift_wid_arr.append(shift_wid)
    else:
        shift_wid_arr = []
        sum_high = 0
        shift_wid = 0
        for shift_high in shift_high_arr:
            sum_high += shift_high

            if sum_high < HEAD_SHIFT_HIGH or sum_high > TAIL_SHIFT_HIGH:
                if shift_wid > 0:
                    shift_wid = random.randint(-SHIFT_WID_MAX//5, -SHIFT_WID_MIN//5)
                elif shift_wid < 0:
                    shift_wid = random.randint(SHIFT_WID_MIN//5, SHIFT_WID_MAX//5)
                else:
                    shift_wid = random.randint(-SHIFT_WID_MAX//5, SHIFT_WID_MAX//5)
            else:
                if shift_wid > 0:
                    shift_wid = random.randint(-SHIFT_WID_MAX, -SHIFT_WID_MIN)
                elif shift_wid < 0:
                    shift_wid = random.randint(SHIFT_WID_MIN, SHIFT_WID_MAX)
                else:
                    shift_wid = random.randint(-SHIFT_WID_MAX, SHIFT_WID_MAX)
            shift_wid_arr.append(shift_wid)

    print (shift_high_arr)
    print (shift_wid_arr)
    return shift_high_arr, shift_wid_arr
'''
The concept of shifting:
suppose the following sequence of number is a row of pixels with value from 0~9
and the '|' indicate the border of the image.
|01234567890123456789|

if I want to shift this row by 4 pixels to the right, the result would be:
|    0123456789012345|6789

the space at the left would become black if the that pixels are not assigned value,
and the 6789 would not be displayed.

Thus, the problem here is that which value should be used to fill the space.

The solution here is scrach the left most pixels:
|00112233456789012345|6789

On the other hand, shift left by 4 pixels would be:
0123|4567890123456789    |

and the solution:
0123|45678901234566778899|
'''
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
    global pic_num
    STEPS = 1
    shift_wid_max = shift_wid_arr
    for i in range(STEPS*2):
        output_name = "pic/out_"+str(pic_num)+".png"
        pic_num += 1
        if i < STEPS:   # shift out
            shift_wid_arr = [ (x//STEPS)*i for x in shift_wid_max ]
        else:           # shift back
            shift_wid_arr = [ (x//STEPS)*(STEPS*2 - i) for x in shift_wid_max ]

        interweaving(origin_img, output_name, shift_high_arr, shift_wid_arr)


pic_num = 0 # the sequencial number of output pictures.
ori_img_path = 'demo.png'
ori_img_path2 = 'demo2.png'
origin_img = Image.open(ori_img_path)
os.system("rm -fr pic/*.png")

insert_origin_img(ori_img_path, 30)

shift_high_arr, shift_wid_arr = generate_shift_arr(origin_img.size[1], origin_img.size[0])
single_animating(origin_img, shift_high_arr, shift_wid_arr)

shift_high_arr, shift_wid_arr = generate_shift_arr(origin_img.size[1], origin_img.size[0], shift_high_arr, shift_wid_arr)
single_animating(origin_img, shift_high_arr, shift_wid_arr)

shift_high_arr, shift_wid_arr = generate_shift_arr(origin_img.size[1], origin_img.size[0], shift_high_arr, shift_wid_arr)
single_animating(origin_img, shift_high_arr, shift_wid_arr)

insert_origin_img(ori_img_path2, 30)

shift_high_arr, shift_wid_arr = generate_shift_arr(origin_img.size[1], origin_img.size[0], shift_high_arr)
single_animating(origin_img, shift_high_arr, shift_wid_arr)

shift_high_arr, shift_wid_arr = generate_shift_arr(origin_img.size[1], origin_img.size[0], shift_high_arr, shift_wid_arr)
single_animating(origin_img, shift_high_arr, shift_wid_arr)

shift_high_arr, shift_wid_arr = generate_shift_arr(origin_img.size[1], origin_img.size[0], shift_high_arr, shift_wid_arr)
single_animating(origin_img, shift_high_arr, shift_wid_arr)


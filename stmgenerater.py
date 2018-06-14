# stmfile generator
from PIL import Image
import numpy as np
import cv2
from itertools import product

# meta settings
NOCONVERT = False
NOMOVIE = True
filepath = "./10square_stripe.stm"
# settings
width = 10
height = 10
frame = 100
fps = 10
total_time = frame / fps
current_max = 10
# making arrays
## light
stim_array = np.zeros((width, height, frame))
light_bar = np.full((1,10),current_max)
for t in range(frame):
    for w in range(width):
        barexist = (w - t) % width
        if barexist >= 0 and barexist < 3:
            stim_array[w,:,t] = np.copy(light_bar)


# comvert array to stmfile
if NOCONVERT is False:
    stm_list = []
    for w in range(width):
        for h in range(height):
            stimseq = np.copy(stim_array[w,h,:])
            stimlist = stimseq.tolist()
            stm_start = 0
            stm_dur = 0
            stim_past = 0
            stim_now = 0
            for i, stim_item in enumerate(stimlist):
                if i == 0:
                    stim_past = 0
                else:
                    stim_past = stim_now
                stim_now = stim_item
                if stim_now != 0:
                    if stim_now == stim_past:
                        stm_dur += 1.0 / fps * 1000
                        if i == len(stimlist):
                            stm_list.append([w,h,stm_start,stm_dur,stim_now])
                    else:
                        if stim_past != 0:
                            stm_list.append([w,h,stm_start,stm_dur,stim_past])
                        stm_start = i * (1.0 / fps) * 1000
                        stm_dur = 1.0 / fps * 1000
                        if i == len(stimlist):
                            stm_list.append([w,h,stm_start,stm_dur,stim_now])

                else:
                    if stim_past != 0:
                        stm_list.append([w,h,stm_start,stm_dur,stim_past])
                        stm_start = 0
                        stm_dur = 0
    print(stm_list)
    f = open(filepath, 'w')
    for st in stm_list:
        f.write(str(st[0] + width * st[1])+','+str(st[2])+','+str(st[3])+','+str(st[4])+'\n')
    f.close()

# generate movie
if NOMOVIE is False:
    fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    out = cv2.VideoWriter('./output.mp4',fourcc,fps,(width*30,height*30))
    for t in range(frame):
        img = Image.new('L',(width*30,height*30))
        img_pix = img.load()
        for x,y in product(range(width),range(height)):
            for dx,dy in product(range(30),range(30)):
                img_pix[x*30+dx,y*30+dy] = int(255 * stim_array[x,y,t] / current_max)
        OpenCV_data = np.asarray(img)
        out.write(OpenCV_data)
    out.release()

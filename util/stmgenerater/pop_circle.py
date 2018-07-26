# stmfile generator
from PIL import Image
import numpy as np
import cv2
from itertools import product
import copy

# meta settings
NOCONVERT = False
NOMOVIE = False
filepath = "./pop_circle_bgliht.stm"
# settings
width = 10
height = 10
frame = 300
fps = 30
total_time = frame / fps
current_min = 0.01
current_max = 0.5
# making arrays
## light
stim_array = np.full((width, height, frame),current_min)

light_circle = np.zeros((width,height))
if width%2 ==1:
    w_center = int(width / 2) +1
else:
    w_center = int(width / 2) +0.5
if height%2 ==1:
    h_center = int(height / 2) +1
else:
    h_center = int(height / 2) +0.5
r = min(w_center,h_center) * 0.6
for h in range(height):
    for w in range(width):
        if pow(w -w_center,2) + pow(h -h_center,2) < pow(r,2):
            light_circle[w,h] = current_max

for t in range(int(frame/2),frame):
    stim_array[:,:,t] = copy.deepcopy(light_circle)

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
                if stim_now > 0.0001:
                    if pow(stim_now - stim_past,2) > 0.00001 :
                        stm_dur += 1.0 / fps * 1000
                        if i == len(stimlist):
                            stm_list.append([w,h,stm_start,stm_dur,stim_now])
                    else:
                        if stim_past > 0.0001:
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
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('./output.avi',fourcc,fps,(width,height),False)
    for t in range(frame):
        im_gray = np.zeros((height,width), dtype = 'uint8')
        for x,y in product(range(width),range(height)):
            im_gray[y,x] = int(255 * stim_array[x,y,t] / current_max)
        out.write(im_gray)
    out.release()

from email.policy import default
import easyocr

import cv2
import time
import sys



def Translate(img_src):
    text = ''
    img_gray = cv2.cvtColor(img_src, cv2.COLOR_BGR2GRAY)
    a,img_black = cv2.threshold(img_gray,120,255,cv2.THRESH_BINARY)

    pos_x_0 = 370
    pos_x_1 = 1620
    dis_1 = (pos_x_1 - pos_x_0)/12
    width = 60

    pos_y_0 = 300
    pos_y_1 = 1450
    stage = 0
    for i in range(0,13):
        y0 = 0
        y1 = 0
        # print("new line",i)
        j = pos_y_0
        pos_x = pos_x_1 - dis_1*i
        for jj in range(pos_y_0, pos_y_1):
            j = j + 1
            if j > pos_y_1:
                break

            if j == pos_x_0 + 50 and y0 == 0:
                text += "\n"

            if (img_black[ j , int(pos_x - width/2):int(pos_x + width/2)] == 255).all():
                stage = 1
            elif stage == 1:
                y0 = j
                for k in range(y0+52, y0, -1):
                    if (img_black[ k , int(pos_x - width/2):int(pos_x + width/2)] == 255).all():
                        
                        stage = 2
                    elif stage == 2:
                        last_y1 = y1
                        y1 = k
                        if k > pos_y_1:
                            break
                        if y1-y0<25:
                            img_box = img_black[last_y1:y1+25, int(pos_x - width/2):int(pos_x + width/2)]
                        else:
                            img_box = img_black[y0-3:y1+3, int(pos_x - width/2):int(pos_x + width/2)]
                        # cv2.imshow("temp",img_box)
                        # cv2.waitKey()
                        content = reader.recognize(img_box, detail=0)
                        if content != []:
                            for k in range(len(content)):
                                if content[k] == "〉" or content[k] == " 〉":
                                    content[k] = ","
                                text += content[k]
                            # print(content[0])
                        break
                stage = 0
                j = y1
            
    # print(text)

    pos_y_0 = 1495
    pos_y_1 = 2675
    stage = 0
    for i in range(0,13):
        y0 = pos_y_0
        y1 = pos_y_0
        # print("new line",i)
        j = pos_y_0
        pos_x = pos_x_1 - dis_1*i
        for jj in range(pos_y_0, pos_y_1):
            j = j + 1
            if j > pos_y_1:
                break

            if j == pos_x_0 + 50 and y0 == 0:
                text += "\n"

            if (img_black[ j , int(pos_x - width/2):int(pos_x + width/2)] == 255).all():
                stage = 1
            elif stage == 1:
                y0 = j
                for k in range(y0+52, y0, -1):
                    if (img_black[ k , int(pos_x - width/2):int(pos_x + width/2)] == 255).all():
                        
                        stage = 2
                    elif stage == 2:
                        last_y1 = y1
                        y1 = k
                        if k > pos_y_1:
                            break
                        if y1-y0<25:
                            img_box = img_black[last_y1:y1+25, int(pos_x - width/2):int(pos_x + width/2)]
                        else:
                            img_box = img_black[y0-3:y1+3, int(pos_x - width/2):int(pos_x + width/2)]

                        content = reader.recognize(img_box, detail=0)
                        if content != []:
                            for k in range(len(content)):
                                if content[k] == "〉" or content[k] == " 〉":
                                    content[k] = ","
                                text += content[k]
                        break
                stage = 0
                j = y1
    return text




PATH = ".\\"

T0 = time.time()
T1 = T0
reader = easyocr.Reader(['ch_sim','en'])
content = ''
for i in range(17,176):
    if i == 27:
        continue
    img_src = cv2.imread(PATH + str(i) + ".jpg")
    if type(img_src) == None:
        continue
    print(PATH + str(i) + ".jpg")
    content += Translate(img_src)
    print(time.time() - T1, "s")
    T1 = time.time()
    if i %10 == 0:
        with open(PATH + "output" +str(i) + ".txt", 'w+', encoding='ANSI') as file:
            file.write(content)

# print(content)


with open(PATH + "output.txt", 'w', encoding='ANSI') as file:
    file.write(content)
print("finish")



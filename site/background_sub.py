import numpy

import cv2

import time

import matplotlib

#loads video
cap = cv2.VideoCapture('newseat1.mp4')

#subtract background of video
back_sub = cv2.createBackgroundSubtractorMOG2(detectShadows=True)

#open close kernels for erosion and dialation
kernelOpen = numpy.ones((3,3), numpy.uint8)
kernelClose = numpy.ones((11, 11), numpy.uint8)

area_thresh = 40000

status = "unoccupied"



while(cap.isOpened()):
    ret, vid = cap.read()

    vid = cv2.line(vid, (430, 0), (430,1200), (255, 0, 0), 3)
    vid = cv2.circle(vid,(430,720),50,(255,0,0),-1)

    back_sub_mask = back_sub.apply(vid)

    try:
        #binarize video
        ret, imBin = cv2.threshold(back_sub_mask, 200, 255, cv2.THRESH_BINARY)

        mask = cv2.morphologyEx(imBin, cv2.MORPH_OPEN, kernelOpen)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernelClose)

        #cv2.imshow('Test Video', cv2.resize(vid,(800,600)))
        #cv2.imshow('BackSub', cv2.resize(back_sub_mask,(800,600)))


    except:
        print ("End of video")
        break



    _, contours0, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    for cnt in contours0:
        cv2.drawContours(vid,cnt, -1,(0,255,0),3,8)
        area = cv2.contourArea(cnt)
        #print (area)
        if area > area_thresh:
            M = cv2.moments(cnt)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01'] / M['m00'])
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.circle(vid, (cx, cy), 5, (0, 0, 255), -1)
            centerx = cx
            centery =cy
            img = cv2.rectangle(vid, (x, y), (x + w, y + h), (0,0,255), 2)

            if centerx >= 300 and centerx <= 500:

                if centery >= 600 and centery <= 800:
                    status = "occupied"

    print(status)






    cv2.imshow('test', cv2.resize(vid,(1000,800)))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
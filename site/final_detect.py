import numpy

import cv2

import time

import matplotlib

import json

#loads video
cap = cv2.VideoCapture('seat.mp4')


#subtract background of video
back_sub = cv2.createBackgroundSubtractorMOG2(detectShadows=True)

#open close kernels for erosion and dialation
kernelOpen = numpy.ones((3,3), numpy.uint8)
kernelClose = numpy.ones((11,11), numpy.uint8)

area_thresh = 600

seat1_status = "false"
seat2_status = "false"
seat1_value = 0
seat2_value = 0

# Update the text file\
counter = 0
with open('test.json', 'w') as file:
    json_dict = {'seat1': seat1_status, 'seat2': seat2_status}
    file.write(json.dumps(json_dict))


while True:
    while(cap.isOpened()):
        ret, vid = cap.read()

        counter += 1

        if (counter % 56 == 0):
            seat1_status = "false"
            seat1_value = 0
            seat2_status = "false"
            seat2_value = 0

        #BILL
        vid = cv2.circle(vid,(170,150),10,(255,0,0),-1)


        #MARY
        vid = cv2.circle(vid,(400,150),10,(255,0,0),-1)

        back_sub_mask = back_sub.apply(vid)

        try:
            #binarize video
            ret, imBin = cv2.threshold(back_sub_mask, 240, 200, cv2.THRESH_BINARY)

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

                if centerx > 100 and centerx <= 300 and centery <= 300:
                    seat1_status = "true"
                    seat1_value = 1

                    #vid = cv2.circle(vid,(50,300),20,(0,0,255), -1)
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    vid = cv2.putText(vid, 'OCCUPIED', (50, 300), font, 1, (0, 0, 255), 2, cv2.LINE_AA)

                if centerx >= 350 and centerx <= 450 and centery <= 450:
                    seat2_status = "true"
                    seat2_value = 1

                    #vid = cv2.circle(vid, (500, 300), 20, (0, 0, 255), -1)
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    vid = cv2.putText(vid, 'OCCUPIED', (350, 300), font, 1, (0, 0, 255), 2, cv2.LINE_AA)

                value_array = [seat1_value,seat2_value]


        #print("SEAT1: ",seat1_status)
        #print("SEAT2: ",seat2_status)
        #print(value_array)

        # Update the text file
        with open('test.json', 'w') as file:
            json_dict = {'seat1': seat1_status, 'seat2': seat2_status}
            file.write(json.dumps(json_dict))

        cv2.imshow('test', cv2.resize(vid,(1000,800)))
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    # Update the text file
    with open('test.json', 'w') as file:
        json_dict = {'seat1': "false", 'seat2': "false"}
        file.write(json.dumps(json_dict))
    cap = cv2.VideoCapture('seat.mp4')

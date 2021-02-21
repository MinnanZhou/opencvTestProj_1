import cv2
import os


# import numpy as np


def getgreyimage(inputimage):
    framemidded = cv2.medianBlur(inputimage, 3)
    # edges = cv2.Canny(framemidded, 100, 200)
    imagegrayed = cv2.cvtColor(framemidded, cv2.COLOR_BGR2GRAY)
    return inputimage, imagegrayed


def generatecontours_circle(oimage, gimage, thresvalue, minimumradius, outimagetype, heattype):
    if outimagetype == 0:
        outimage = oimage
    else:
        outimage = gimage
    if heattype == 'whiteheat':
        ret, thresh1 = cv2.threshold(gimage, thresvalue, 255, cv2.THRESH_BINARY)
    else:
        ret, thresh1 = cv2.threshold(gimage, thresvalue, 255, cv2.THRESH_BINARY_INV)
    contours, cnt = cv2.findContours(thresh1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # outimage = oimage
    for i in range(len(contours)):
        (x, y), radius = cv2.minEnclosingCircle(contours[i])
        print(x, y)
        center = (int(x), int(y))
        outcenter = '(' + '%d' % x + ',' + '%d' % y + ')'
        radius = int(radius)
        if radius >= minimumradius:
            if outimagetype == 0:
                outimage = cv2.circle(oimage, center, radius, (0, 255, 0), 1)
                outimage = cv2.putText(outimage, outcenter, (int(x), int(y)), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 0.7,
                                       (0, 255, 0), 1)
            else:
                outimage = cv2.circle(gimage, center, radius, (0, 255, 0), 1)
                outimage = cv2.putText(outimage, outcenter, (int(x), int(y)), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 0.7,
                                       (0, 255, 0), 1)
    # cv2.drawContours(oimage, contours, -1, (0, 0, 255), 3)
    return outimage


def generatecontours_rec(oimage, gimage, thresvalue, minimumwidth, minimumheight, outimagetype, heattype):
    if outimagetype == 0:
        outimage = oimage
    else:
        outimage = gimage
    if heattype == 'whiteheat':
        ret, thresh1 = cv2.threshold(gimage, thresvalue, 255, cv2.THRESH_BINARY)
    else:
        ret, thresh1 = cv2.threshold(gimage, thresvalue, 255, cv2.THRESH_BINARY_INV)
    contours, cnt = cv2.findContours(thresh1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # outimage = oimage
    for i in range(len(contours)):
        x, y, w, h = cv2.boundingRect(contours[i])
        print(x, y)
        center = (int(x + 0.5*w), int(y + 0.5*h))
        outcenter = '(' + '%d' % center[1] + ',' + '%d' % center[2] + ')'
        pt1 = (int(x), int(y))
        pt2 = (int(x + w), int(y + h))
        if w >= minimumwidth & h >= minimumheight:
            if outimagetype == 0:
                outimage = cv2.rectangle(oimage, pt1, pt2, (0, 255, 0), 1)
                outimage = cv2.putText(outimage, outcenter, pt2, cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 0.7,
                                       (0, 255, 0), 1)
            else:
                outimage = cv2.rectangle(gimage, pt1, pt2, (0, 255, 0), 1)
                outimage = cv2.putText(outimage, outcenter, pt2, cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 0.7,
                                       (0, 255, 0), 1)
    # cv2.drawContours(oimage, contours, -1, (0, 0, 255), 3)
    return outimage


def getcontourfromvideos(inputpath, outputpath):
    cap = cv2.VideoCapture(inputpath)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')  # 保存视频的编码
    out = cv2.VideoWriter(outputpath, fourcc, 25.0, (1280, 976))
    while 1:
        back, getnframes = cap.read()
        originalimage, grayimage = getgreyimage(getnframes)
        image = generatecontours_circle(originalimage, grayimage, 20, 2, 0, 'blackheat')  # 'blackheat' or 'whiteheat'
        # image = generatecontours_rec(originalimage, grayimage, 20, 2, 2, 0, 'blackheat')  # 'blackheat' or 'whiteheat'
        cv2.imshow("output", originalimage)
        out.write(image)
        if cv2.waitKey(20) & 0xff == ord('q'):
            break
    cap.release()
    out.release()
    cv2.destroyAllWindows()


def getcontourfromimages(inputpath, outputpath):
    imagescount = 0
    oimage = []
    gimage = []
    filelist = os.listdir(inputpath)
    for imgname in filelist:
        if imgname.endswith(".jpg") or imgname.endswith(".bmp") or imgname.endswith(".jpeg") or imgname.endswith(
                ".png"):
            originalimage, grayimage = getgreyimage(cv2.imread(inputpath + imgname))
            oimage.append(originalimage)
            gimage.append(grayimage)
            imagescount = imagescount + 1
            # resultimg = generatecontours_circle(originalimage, grayimage, 124, 2, 0, 'blackheat') # 'blackheat' or 'whiteheat'
            resultimg = generatecontours_rec(originalimage, grayimage, 50, 10, 10, 0, 'whiteheat')  # 'blackheat' or 'whiteheat'
            cv2.imshow('processed', resultimg)
            if cv2.waitKey(1000) & 0xff == ord('q'):
                break
            cv2.imwrite(outputpath + 'output_' + imgname, resultimg)
            print(imagescount)


# getcontourfromimages('/home/joe/Pictures/testimages/', '/home/joe/Pictures/outputtestimages/')
getcontourfromvideos('/home/joe/Videos/testVideo2.mp4', '/home/joe/Videos/output2.avi')

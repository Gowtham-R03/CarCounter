import cv2
import numpy as np
import stack

cap = cv2.VideoCapture('drone.mp4')
frame_width = 640
frame_height = 480

# minimum
min_width_rect = 80
min_height_rect = 80

# Count line position
count_line_position = 300

# INITIALIZE Substracts
algo = cv2.createBackgroundSubtractorMOG2()

# saving video
result = cv2.VideoWriter('filename.avi',
                         cv2.VideoWriter_fourcc(*'MJPG'),
                         30, (640, 480))

def center_handle(x, y, w, h):
    x1 = int(w / 2)
    y1 = int(h / 2)
    cx = x + x1
    cy = y + y1
    return cx, cy


detect = []
offset = 6
counter = 0

while True:
    sucess, img = cap.read()
    img = cv2.resize(img, (frame_width, frame_height))
    imgContour = img.copy()
    imgContour = imgContour[60:480, :]
    imgGray = cv2.cvtColor(img[60:480, :], cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 5)
    imgEdge = cv2.Canny(imgGray, 100, 100)
    contours, hierarchy = cv2.findContours(imgEdge, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)


    # # applying on each frame
    # imgSub = algo.apply(imgBlur)
    #
    # imgDilate = cv2.dilate(imgSub, np.ones((5, 5)))
    # kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    # dilate = cv2.morphologyEx(imgDilate, cv2.MORPH_CLOSE, kernel)
    # dilate = cv2.morphologyEx(dilate, cv2.MORPH_CLOSE, kernel)
    # imgContour, h = cv2.findContours(dilate, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #
    # line
    cv2.line(img, (25, count_line_position), (600, count_line_position), (255, 255, 0), 1)

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 490:
            # cv2.drawContours(imgContour, cnt, -1, (255, 0, 255), 2)  # 7width of boundary
            # to get corner points of our shape object
            para = cv2.arcLength(cnt, True)  # true for closed contours
            # to approximate the points to get what shape is this
            approx = cv2.approxPolyDP(cnt, 0.02 * para, True)  # 0.02*para = resolution
            print(len(approx))  # here we get ex:4 it indicates it is square or rectangle
            objCor = len(approx)
            x, y, w, h = cv2.boundingRect(approx)
            cv2.rectangle(img[60:480, :], (x, y), (x + w, y + h), (0, 90, 255), 1)
            center = center_handle(x, y, w, h)
            detect.append(center)
            cv2.circle(img[60:480, :], center, 4, (0, 0, 255), -1)

            for (x, y) in detect:
                if y<(count_line_position + offset) and y>(count_line_position - offset):
                    counter += 1
                cv2.line(imgContour, (25, count_line_position), (600, count_line_position), (0, 255, 255), 2)
                detect.remove((x, y))
                print("Vechile Count: ", str(counter))
                cv2.putText(img, str(counter), (x-30, y + 30), cv2.FONT_HERSHEY_PLAIN, 1, (204, 153, 255), 2)

    cv2.putText(img,  str(counter), (550, 50), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 100, 255), 2)
    cv2.putText(img,  'Gowtham R', (280, 40), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 100, 255), 2)

    result.write(img)
    # cv2.imshow("Image", imgContour)
    cv2.imshow("CarCounter", img)
    # imgStack = stack.stackImages(([img], [imgContour]), 0.3)

    if cv2.waitKey(30) and 0xFF == ord('q'):
            break

cap.release()
result.release()
cv2.destroyAllWindows()


import cv2
import numpy as np
import utils


#########################################################
path = "Resources/2.jpg"
widthImg = 600
heightImg = 600
questions=5
choices=5
ans = [1,2,0,3,4]
img = cv2.imread(path)
#########################################################



##### 1. PREPARE THE IMAGE 

img = cv2.resize(img, (widthImg, heightImg))
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
imgBlur = cv2.GaussianBlur(imgGray, (5,5), 1)
imgCanny = cv2.Canny(imgBlur, 10, 50)



##### 2. FINDING CONTOURS

imgContours = img.copy()
imgBiggestContours = img.copy()
contours, hierarchy = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
cv2.drawContours(imgContours, contours, -1, (0,255,0), 10)

# Finding biggest and second biggest rectangle
rectCon = utils.rectContour(contours)
biggestContour = utils.getCornerPoints(rectCon[0])
gradePoints = utils.getCornerPoints(rectCon[1])
# print(biggestContour, gradePoints)



##### 3. WARP PERSPECTIVE

if biggestContour.size != 0 and gradePoints.size != 0:
    
    cv2.drawContours(imgBiggestContours, biggestContour, -1, (0,255,0), 20)
    cv2.drawContours(imgBiggestContours, gradePoints, -1, (255,0,0), 20)

    biggestContour = utils.reorder(biggestContour)
    gradePoints = utils.reorder(gradePoints)

    ## FOR BIGGEST RECTANGLE
    pt1 = np.float32(biggestContour)
    pt2 = np.float32([[0,0], [widthImg,0], [0,heightImg], [widthImg,heightImg]])
    matrix = cv2.getPerspectiveTransform(pt1,pt2)
    imgWarpColored = cv2.warpPerspective(img, matrix, (widthImg,heightImg))
    
    ## FOR SECOND BIGGEST RECTANGLE
    ptG1 = np.float32(gradePoints)
    ptG2 = np.float32([[0,0], [300,0], [0,150], [300,150]])
    matrixG = cv2.getPerspectiveTransform(ptG1,ptG2)
    imgGradeDisplay = cv2.warpPerspective(img, matrixG, (300,150))
    # cv2.imshow("Grade", imgGradeDisplay)



    ##### 4. APPLY THRESHOLD

    imgWarpGray = cv2.cvtColor(imgWarpColored, cv2.COLOR_BGR2GRAY)
    imgThresh = cv2.threshold(imgWarpGray, 170, 255, cv2.THRESH_BINARY_INV)[1]

    ## GET INDIVIDUAL BOXES & THREIR NON-ZERO PIXEL VALUES
    boxes = utils.splitBoxes(imgThresh)
    # cv2.imshow("Test", boxes[2])

    myPixelVal = np.zeros((questions, choices))
    countC, countR = 0, 0

    for image in boxes:
        totalPixels = cv2.countNonZero(image)
        myPixelVal[countR][countC] = totalPixels
        countC += 1
        if countC == choices:
            countR += 1
            countC = 0
    # print(myPixelVal)



    ##### 5. FIND BUBBLE MARKS AND COMPARE WITH ANSWERS

    myIndex = []
    answers = []
    for x in range(0, questions):
        p = myPixelVal[x]
        maxVal = np.amax(p)
        myIndexVal = np.where(p==np.amax(p))
        myIndex.append(myIndexVal[0][0])
        if maxVal > 6000:
            answers.append(myIndexVal[0][0])
        else:
            answers.append(-1)
        
    # print(myIndex)
    # print(answers)


    grading = []
    for x in range(0, questions):
        if ans[x] == answers[x]:
            grading.append(1)
        else:
            grading.append(0)
    # print(grading)
    # Calculate Score
    score = (sum(grading)/questions)*100
    print(score)



    ##### 6. DISPLAY SCORE IN ORIGINAL SHEET
    
    imgResult = imgWarpColored.copy()
    imgResult = utils.showAnswers(imgResult, myIndex, grading, ans, answers, questions, choices)

    imgRawDrawing = np.zeros_like(imgWarpColored)
    imgRawDrawing = utils.showAnswers(imgRawDrawing, myIndex, grading, ans, answers, questions, choices)
    
    ## INVERSE PERSPECTIVE

    # Part 1: Answers
    invMatrix = cv2.getPerspectiveTransform(pt2,pt1)
    imgInvWarp = cv2.warpPerspective(imgRawDrawing, invMatrix, (widthImg,heightImg))

    imgFinal = img.copy()

    # Part 2: Grade
    imgRawGrade = np.zeros_like(imgGradeDisplay)
    cv2.putText(imgRawGrade, str(int(score))+"%", (50,100), cv2.FONT_HERSHEY_COMPLEX, 3, (0,255,255), 3)
    cv2.imshow("Grade", imgRawGrade)
    invMatrixG = cv2.getPerspectiveTransform(ptG2,ptG1)
    imgInvGrade = cv2.warpPerspective(imgRawGrade, invMatrixG, (widthImg,heightImg))

    
    imgFinal = cv2.addWeighted(imgFinal, 1, imgInvWarp, 1, 0)
    imgFinal = cv2.addWeighted(imgFinal, 1, imgInvGrade, 1, 0)




imgBlank = np.zeros_like(img)
imgArray = ([img, imgGray, imgBlur, imgCanny],
            [imgContours, imgBiggestContours, imgWarpColored, imgThresh], 
            [imgResult, imgRawDrawing, imgInvWarp, imgFinal])

'''lables = [["Original", "Gray", "Blur", "Canny"],
            ["Contours", "Biggest Cont.", " Warp", "Threshold"],
            ["Result", "Raw Drawing", "Inverse", "Final"]]'''
imgStacked = utils.stackImages(imgArray, 0.3)

cv2.imshow("Final Sheet", imgFinal)
cv2.imshow("Stacked Images", imgStacked)
cv2.waitKey(0)

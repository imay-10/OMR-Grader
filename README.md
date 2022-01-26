# Optical Mark Recognition - Grader

Optical Mark Recognition Grading System using Computer Vision (Python + OpenCV)

<img src="https://github.com/imay-10/OMR-Grader/blob/master/Outputs/out_1.png" width="640" height="520"/>

## Installations

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install opencv and numpy

```bash
pip install numpy
pip install opencv-python
```

## Workflow

### 1. Image Processing
*This is the initial stage, where we have converted the original image to GrayScale, added Gaussian Blur to it, and used the Canny Edge Detector to detect the edges.*

### 2. Finding the Contours
*In this step, we have detected the contours present in the image. The biggest contour corresponds to the marking area, and the 2nd biggest corresponds to the grading area.*

### 3. Warp Perspective
*Here, we use the transformation matrix to get the bird's eye view of the marking area and the grading area.*

### 4. Applying Threshold
*Thresholding simply means segmenting of image. We create a binary form of our image in this case.* 
*We count the total no. of questions and the no. of choices each question has. We multiply them to know in how many parts are we going to split our image. For eg., if we have five questions and four choices for each question, then the image is split into 5 x 4 = 20 parts.*

### 5. Finding Bubble Marks
*We iterate through each row, and the index where the maximum pixel count occurs, we consider it for answer. 
Now, if the maximum pixel count fails to be above a certain value, the bubbling is considered improper, and no marks is alloted in such cases. The considered answers are now compared to the correct answers, and the grades are calculated.*

### 6. Displaying the Score
*Now, just like we got the warp perspective before, we get the inverse warp perspective in this stage to display the score back in the original sheet.*


## Final Output

<img src="https://github.com/imay-10/OMR-Grader/blob/master/Outputs/out_2.png" width="640"/>

## Credits
[Murtaza's Workshop - Robotics and AI](https://www.murtazahassan.com/)

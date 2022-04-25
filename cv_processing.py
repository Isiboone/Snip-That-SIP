# Isis Boone AI contest, AI Processing pictures and turning into code
# Last Tested:March 25th 2022 11:37PM
# This is the librarys for the CV processing for the snippings
import cv2
import numpy as np

# This is the class for processing the image when the snipping tool grabs the text or code
class CV_Processing:
    # get grayscale image
    @staticmethod
    def get_grayscale(image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # noise removal
    @staticmethod
    def remove_noise(image):
        return cv2.medianBlur(image, 5)

    # thresholding
    @staticmethod
    def thresholding(image):
        return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    # dilation
    @staticmethod
    def dilate(image):
        kernel = np.ones((5, 5), np.uint8)
        return cv2.dilate(image, kernel, iterations=1)

    # erosion
    @staticmethod
    def erode(image):
        kernel = np.ones((5, 5), np.uint8)
        return cv2.erode(image, kernel, iterations=1)

    # opening - erosion followed by dilation
    @staticmethod
    def opening(image):
        kernel = np.ones((5, 5), np.uint8)
        return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

    # canny edge detection
    @staticmethod
    def canny(image):
        return cv2.Canny(image, 100, 200)

    # skew correction
    @staticmethod
    def deskew(image):
        coords = np.column_stack(np.where(image > 0))
        angle = cv2.minAreaRect(coords)[-1]
        if angle < -45:
            angle = -(90 + angle)

        else:
            angle = -angle
            (h, w) = image.shape[:2]
            center = (w // 2, h // 2)
            M = cv2.getRotationMatrix2D(center, angle, 1.0)
            rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
            return rotated

    # template matching
    @staticmethod
    def match_template(image, template):
        return cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)

    @staticmethod
    def unsharp_mask(image, kernel_size=(5, 5), sigma=1.0, amount=1.0, threshold=0):
        """Return a sharpened version of the image, using an unsharp mask."""
        blurred = cv2.GaussianBlur(image, kernel_size, sigma)
        sharpened = float(amount + 1) * image - float(amount) * blurred
        sharpened = np.maximum(sharpened, np.zeros(sharpened.shape))
        sharpened = np.minimum(sharpened, 255 * np.ones(sharpened.shape))
        sharpened = sharpened.round().astype(np.uint8)
        if threshold > 0:
            low_contrast_mask = np.absolute(image - blurred) < threshold
            np.copyto(sharpened, image, where=low_contrast_mask)
        return sharpened

import cv2
import pytesseract

"""
Install Tesseract OCR Download the official installer from UB Mannheim’s Tesseract page.
Set the path in your Python script Add this line before calling image_to_string():
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
"""


class ImageSearcher:

    @staticmethod
    def sub_image_search(main_image, template, debugging_enabled: bool):
        # Convert both to grayscale for better matching
        main_gray = cv2.cvtColor(main_image, cv2.COLOR_BGR2GRAY)
        template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

        # Improving contrast and reducing noise can help a lot.
        template_eq = cv2.equalizeHist(template_gray)
        main_eq = cv2.equalizeHist(main_gray)
        template_edges = cv2.Canny(template_eq, 50, 150)
        main_edges = cv2.Canny(main_eq, 50, 150)
        result = cv2.matchTemplate(main_edges, template_edges, cv2.TM_CCOEFF_NORMED)

        # Find the best match location
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        top_left = max_loc
        h, w = template_gray.shape
        bottom_right = (top_left[0] + w, top_left[1] + h)
        center = (top_left[0] + w / 2, top_left[1] + h / 2)

        if debugging_enabled:
            print(f"{min_val=}")
            print(f"{max_val=}")
            print(f"{top_left=}")
            print(f"{bottom_right=}")
            print(f"{center=}")

            cv2.rectangle(main_image, top_left, bottom_right, (0, 0, 0), 6)
            # Create a resizable window
            cv2.namedWindow("CustomWindow", cv2.WINDOW_NORMAL)
            # Resize the window to your desired dimensions
            cv2.resizeWindow("CustomWindow", 600, 900)
            # Show the image in the resized window
            cv2.imshow("CustomWindow", main_image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        return min_val, max_val, top_left, bottom_right, center

    @staticmethod
    def search_with_text(image: str, template1: str, template2: str, search_for_text: str = "", debugging_enabled: bool = False):
        main_image = cv2.imread(image, cv2.IMREAD_COLOR)
        template1_image = cv2.imread(template1, cv2.IMREAD_COLOR)
        min_val, max_val, top_left, bottom_right, center1 = ImageSearcher.sub_image_search(main_image,
                                                                                           template1_image,
                                                                                           debugging_enabled)

        a, b, c, d = int(top_left[1]), int(bottom_right[1]), int(top_left[0]), int(bottom_right[0])
        cropped = main_image[a:b, c:d]
        if debugging_enabled:
            cv2.imshow("CustomWindow", cropped)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        template2_image = cv2.imread(template2, cv2.IMREAD_COLOR)
        min_val, max_val, top_left, bottom_right, center2 = ImageSearcher.sub_image_search(cropped,
                                                                                           template2_image,
                                                                                           debugging_enabled)

        a, b, c, d = int(top_left[1]), int(bottom_right[1]), int(top_left[0]), int(bottom_right[0])
        cropped_final = cropped[a:b, c:d]
        if debugging_enabled:
            cv2.imshow("CustomWindow", cropped_final)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        if search_for_text:
            # Convert to grayscale
            gray = cv2.cvtColor(cropped_final, cv2.COLOR_BGR2GRAY)
            # Optional: Apply thresholding or denoising
            gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

            if debugging_enabled:
                cv2.imshow("CustomWindow", gray)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

            # Extract text
            extracted_text = pytesseract.image_to_string(gray)
            print(f"Extracted {extracted_text=}")
            return (search_for_text in extracted_text), center2

        return False, None

    @staticmethod
    def search(image: str, template: str, debugging_enabled: bool = False):
        # Load the main image and the template
        main_image = cv2.imread(image, cv2.IMREAD_COLOR)
        template_image = cv2.imread(template, cv2.IMREAD_COLOR)
        min_val, max_val, top_left, bottom_right, center = ImageSearcher.sub_image_search(main_image,
                                                                                          template_image,
                                                                                          debugging_enabled)
        return center

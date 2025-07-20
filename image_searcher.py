import cv2


class ImageSearcher:

    @staticmethod
    def search(image: str, template: str, debugging_enabled: bool = False):
        # Load the main image and the template
        main_image = cv2.imread(image, cv2.IMREAD_COLOR)
        template = cv2.imread(template, cv2.IMREAD_COLOR)

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

        return center

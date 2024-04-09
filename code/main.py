import pytesseract
import os
import cv2

def process_image(image):

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    #_, binary_image = cv2.threshold(gray_image, 150, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    _, binary_image = cv2.threshold(gray_image, 100, 255, cv2.THRESH_BINARY)
    
    resized_image = cv2.resize(binary_image, (binary_image.shape[1]*2, binary_image.shape[0]*2), interpolation=cv2.INTER_CUBIC)

    return resized_image


def ocr_image(file_path):

    image = cv2.imread(file_path)

    processed = process_image(image)

    custom_config = r'--psm 7 --oem 3 -c tessedit_char_whitelist=0123456789. '
    text = pytesseract.image_to_string(processed, config=custom_config)
    
    return text

def main():

    current_dir = os.getcwd()

    folder_path = os.path.join(current_dir, '../data/')

    output_file = open("../output.txt", "w")

    filenames = os.listdir(folder_path)

    # Sort the filenames based on the numbers at the end
    sorted_filenames = sorted(filenames, key=lambda x: int(x.split("_")[-1].split(".png")[0]))


    for filename in sorted_filenames:

        image_path = os.path.join(folder_path, filename)

        output = ocr_image(image_path)


        output_file.write(filename + ': ' + output)
        

    output_file.close()

    print('done')






if __name__ == '__main__':

    main()

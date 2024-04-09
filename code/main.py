import pytesseract
import os
import cv2

def process_image(image):
    '''
    This function handles image pre-processing, I was experimenting with a few different
    ideas but found this setup with just a grayscale and manual binary thresholding to 
    be good enough for me. I also included an image resizing step, I found that by widening 
    the image and using the interpolation to blur the edges a little I could improve
    recognition marginally. This could definitely be improved through further experimentation. 
    '''

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary_image = cv2.threshold(gray_image, 200, 255, cv2.THRESH_BINARY)
    resized_image = cv2.resize(binary_image, (binary_image.shape[1]*3, binary_image.shape[0]*2), interpolation=cv2.INTER_CUBIC)
   
    return resized_image


def ocr_image(file_path):
    '''
    This function calls the image pre-processing function and performs the OCR on
    it using Tesseracts LSTM neural network OCR engine. I set up a custom config to exlude 
    common non-digit characters. Then we just use pytesseract's built-in image_to_string
    to get a string from the image.
    '''

    image = cv2.imread(file_path)
    processed = process_image(image)

    custom_config = r'--psm 7 --oem 1 -c tessedit_char_blacklist=abcdefghijklmnopqrstuvwxyz!@#$%&*()'
    text = pytesseract.image_to_string(processed, config=custom_config)
    
    return text

def main():
    # This is set up so that your current working directory is the code folder
    current_dir = os.getcwd()
    folder_path = os.path.join(current_dir, '../data/')
    output_file = open("../output.txt", "w")
    
    # Here we collect the filenames from the folder and sort them by image number.
    filenames = os.listdir(folder_path)
    sorted_filenames = sorted(filenames, key=lambda x: int(x.split("_")[-1].split(".png")[0]))

    # Now we loop through our filenames, perform OCR, 
    # and add the output to the output.txt file. 
    for filename in sorted_filenames:

        image_path = os.path.join(folder_path, filename)

        output = ocr_image(image_path)

        output_file.write(filename + ': ' + output)

    output_file.close()
    print('done')


if __name__ == '__main__':

    main()

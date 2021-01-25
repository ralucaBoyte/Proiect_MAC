import cv2
import numpy as np


class LSB:
    def __init__(self):
        self.original_image_path = "pictures/beach.png"
        self.stego_image_path = "pictures/beach_encoded.png"

    @staticmethod
    def messageToBinary(message):
        if type(message) == str:
            return ''.join([format(ord(i), '08b') for i in message])
        elif type(message) == bytes or type(message) == np.ndarray:
            return [format(i, '08b') for i in message]
        elif type(message) == int or type(message) == np.uint8:
            return format(message, '08b')
        else:
            raise TypeError("Input type not supported")

    @staticmethod
    def LSB_encoding_method(image, secret_message):
        n_bytes = image.shape[0] * image.shape[1] * 3 // 8
        if len(secret_message) > n_bytes:
            raise ValueError("Too many bytes to be encoded!!! You need a bigger image or less data to encode!!")

        secret_message += "*****"
        data_index = 0
        binary_secret_msg = LSB.messageToBinary(secret_message)

        data_len = len(binary_secret_msg)  # Find the length of data that needs to be hidden
        for values in image:
            for pixel in values:

                red, green, blue = LSB.messageToBinary(pixel)

                # We encode our message in the LSB of each RGB binary value
                if data_index < data_len:
                    pixel[0] = int(red[:-1] + binary_secret_msg[data_index], 2)
                    data_index += 1

                if data_index < data_len:
                    pixel[1] = int(green[:-1] + binary_secret_msg[data_index], 2)
                    data_index += 1

                if data_index < data_len:
                    pixel[2] = int(blue[:-1] + binary_secret_msg[data_index], 2)
                    data_index += 1

                if data_index >= data_len:
                    break

        return image

    @staticmethod
    def LSB_decoding_method(image):
        binary_data = ""
        for values in image:
            for pixel in values:
                red, green, blue = LSB.messageToBinary(pixel)

                #WE STORE THE LAST BIT OF EVERY RGB VALUE IN binary_data
                binary_data += red[-1]
                binary_data += green[-1]
                binary_data += blue[-1]

        #WE SPLIT THE binary_data INTO GROUPS OF BYTES (8 BITS)
        all_bytes = [binary_data[i: i + 8] for i in range(0, len(binary_data), 8)]

        decoded_data = ""
        for byte in all_bytes:
            decoded_data += chr(int(byte, 2))
            # WE CHECK IF THE LAST 5 CHARACTERS ARE *****, THEN WE HAVE REACHED OUR DELIMITER
            if decoded_data[-5:] == "*****":
                break
        return decoded_data[:-5]

    def encode_our_message(self):
        image_name = self.original_image_path
        image = cv2.imread(image_name)
        data = input("Enter data to be encoded: ")
        if len(data) == 0:
            raise ValueError('Data is empty')

        encoded_image = LSB.LSB_encoding_method(image, data)
        cv2.imwrite(self.stego_image_path, encoded_image)

    def decode_our_message(self):
        # REDING THE STEGO IMAGE
        image = cv2.imread(self.stego_image_path)
        text = LSB.LSB_decoding_method(image)
        return text

# Image Steganography
from LSB_steganography.Utils import Utils


class Steganography:

    @staticmethod
    def LSB_Steganography():
        a = input("Image Steganography \n 1. Encode the data \n 2. Decode the data \n Your input is: ")
        userinput = int(a)

        if (userinput == 1):
            print("\nEncoding....")
            Utils.encode_text()

        elif (userinput == 2):
            print("\nDecoding....")
            print("Decoded message is " + Utils.decode_text())
        else:
            raise Exception("Enter correct input")


Steganography.LSB_Steganography()  # encode image

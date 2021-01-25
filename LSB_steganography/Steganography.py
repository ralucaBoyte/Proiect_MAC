# Image Steganography
from LSB_steganography.LSB import LSB


class Steganography:

    @staticmethod
    def LSB_Steganography():
        a = input("Image Steganography using the LSB algorithm \nPress: \n1. To encode the data \n2. To decode the data \nYour choice: ")
        userInput = int(a)
        lsb_steganography = LSB()

        if userInput == 1:
            print("\nEncoding....")
            lsb_steganography.encode_our_message()

        elif userInput == 2:
            print("\nDecoding....")
            print("Decoded message is " + lsb_steganography.decode_our_message())
        else:
            raise Exception("Enter correct input")


Steganography.LSB_Steganography()

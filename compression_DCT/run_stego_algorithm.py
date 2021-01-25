import cv2
import bitstring
import numpy  as np
import compression_DCT.zigzag as zz
import compression_DCT.image_preparation as img
import compression_DCT.data_embedding as stego

original_image_path = "../pictures/corgis.jpg"
stego_image_path = "../pictures/corgis_encoded.jpg"
secret_message = "OUR SECRET MESSAGES RIGHT HERE"

original_image = cv2.imread(original_image_path, flags=cv2.IMREAD_COLOR)
height, width = original_image.shape[:2]

# PREPARE IMAGE HEIGHT AND WIDTH TO BE DIVIDED INTO 8x8 BLOCKS
while height % 8:
    height += 1
while width % 8:
    width += 1

dimensions = (width, height)
resized_image = cv2.resize(original_image, dimensions)
original_image_f32 = np.float32(resized_image)

# WE CONVERT COLOUR SPACE FROM RGB TO YCbCr
# Y - luminance
# Cb - Blue difference chroma component
# Cr - Red difference chroma component
original_image_YCbCr = cv2.cvtColor(original_image_f32, cv2.COLOR_BGR2YCrCb)

# WE CREATE AN YCrCb CLASS WITH height, width and channels attributes AND STORE THE RED, GREEN AND BLUE VALUES FOR OUR PICTURE IN THE channels ATTRIBUTE
original_image_YCC = img.YCbCr_Image(original_image_YCbCr)

# WE WILL STORE OUR STEGO IMAGE IN stego_image
stego_image = np.empty_like(original_image_f32)

for index in range(3):
    # FORWARD DCT STAGE
    dct_blocks = [cv2.dct(block) for block in original_image_YCC.channels[index]]

    # QUANTIZATION STAGE
    dct_quants = [np.around(np.divide(item, img.standard_quantization_table)) for item in dct_blocks]

    # SORT DCT COEFFICIENTS BT FREQUENCY
    sorted_coefficients = [zz.zigzag(block) for block in dct_quants]

    # EMBED DATA INTO LUMINANCE LAYER
    if index == 0:
        # DATA INSERTION STAGE
        secret_data = ""
        for char in secret_message.encode('ascii'):
            secret_data += bitstring.pack('uint:8', char)
        embedded_dct_blocks = stego.embed_encoded_data_into_DCT(secret_data, sorted_coefficients)
        desorted_coefficients = [zz.inverse_zigzag(block, vmax=8, hmax=8) for block in embedded_dct_blocks]
    else:
        # REORDER COEFFIECIENT TO HOW THE ORIGINALLY WERE
        desorted_coefficients = [zz.inverse_zigzag(block, vmax=8, hmax=8) for block in sorted_coefficients]

    # DEQUANTIZATION STAGE
    dct_dequants = [np.multiply(data, img.standard_quantization_table) for data in desorted_coefficients]

    # WE APPLY INVERSE DCT
    idct_blocks = [cv2.idct(block) for block in dct_dequants]

    # WE REBUILD FULL IMAGE CHANNEL
    current_channel_blocks = img.stitch_8x8_blocks_back_together(original_image_YCC.width, idct_blocks)
    stego_image[:, :, index] = np.asarray(current_channel_blocks)

# CONVERT IMAGE BACK TO RBG (BGR) COLOURSPACE
stego_image_BGR = cv2.cvtColor(stego_image, cv2.COLOR_YCR_CB2BGR)

# WE PLACE VALUES FROM OUR stego_image_BGR TO VALUES IN THE [0 - 255] INTERVAL
final_stego_image = np.uint8(np.clip(stego_image_BGR, 0, 255))

# WRITE STEGO IMAGE
cv2.imwrite(stego_image_path, final_stego_image)

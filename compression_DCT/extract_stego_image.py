import cv2
import struct
import numpy  as np
import compression_DCT.zigzag as zz
import compression_DCT.data_embedding as stego
import compression_DCT.run_stego_algorithm as src
import compression_DCT.image_preparation   as img


stego_image = cv2.imread(src.stego_image_path, flags=cv2.IMREAD_COLOR)
stego_image_f32 = np.float32(stego_image)
stego_image_YCC = img.YCbCr_Image(cv2.cvtColor(stego_image_f32, cv2.COLOR_BGR2YCrCb))

# FORWARD DCT STAGE
dct_blocks = [cv2.dct(block) for block in stego_image_YCC.channels[0]]  # WE ONLY TAKE THE LUMINANACE LAYER

# QUANTIZATION STAGE
dct_quants = [np.around(np.divide(item, img.standard_quantization_table)) for item in dct_blocks]

# Sort DCT coefficients by frequency
sorted_coefficients = [zz.zigzag(block) for block in dct_quants]

# DATA EXTRACTION STAGE
recovered_data = stego.extract_encoded_data_from_DCT(sorted_coefficients)

# Determine length of secret message
data_len = int(recovered_data.read('uint:32') / 8)

# Extract secret message from DCT coefficients
extracted_data = bytes()
for _ in range(data_len):
    extracted_data += struct.pack('>B', recovered_data.read('uint:8'))

# Print secret message back to the user
print(extracted_data.decode('ascii'))
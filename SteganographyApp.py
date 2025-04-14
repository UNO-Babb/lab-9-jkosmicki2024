from PIL import Image
import os

def encode(img, msg):
    pixels = img.load()
    width, height = img.size
    msg_length = len(msg)
    red, green, blue = pixels[0, 0]
    pixels[0, 0] = (msg_length, green, blue)
    letter_index = 0
    pixel_count = 0
    binary_letter = ""

    for i in range(msg_length * 3):
        x = i % width
        y = i // width
        red, green, blue = pixels[x, y]
        red_binary = format(red, '08b')
        green_binary = format(green, '08b')
        blue_binary = format(blue, '08b')

        if pixel_count % 3 == 0:
            binary_letter = format(ord(msg[letter_index]), '08b')
            green_binary = green_binary[:-1] + binary_letter[0]
            blue_binary = blue_binary[:-1] + binary_letter[1]
        elif pixel_count % 3 == 1:
            red_binary = red_binary[:-1] + binary_letter[2]
            green_binary = green_binary[:-1] + binary_letter[3]
            blue_binary = blue_binary[:-1] + binary_letter[4]
        else:
            red_binary = red_binary[:-1] + binary_letter[5]
            green_binary = green_binary[:-1] + binary_letter[6]
            blue_binary = blue_binary[:-1] + binary_letter[7]
            letter_index += 1

        pixels[x, y] = (int(red_binary, 2), int(green_binary, 2), int(blue_binary, 2))
        pixel_count += 1

    img.save("encoded_image.png", 'PNG')


def decode(img):
    msg = ""
    pixels = img.load()
    width, height = img.size
    red, green, blue = pixels[0, 0]
    msg_length = red
    pixel_count = 0
    binary_letter = ""
    
    for i in range(msg_length * 3):
        x = i % width
        y = i // width
        red, green, blue = pixels[x, y]
        red_binary = format(red, '08b')
        green_binary = format(green, '08b')
        blue_binary = format(blue, '08b')

        if pixel_count % 3 == 0:
            binary_letter = green_binary[-1] + blue_binary[-1]
        elif pixel_count % 3 == 1:
            binary_letter += red_binary[-1] + green_binary[-1] + blue_binary[-1]
        else:
            binary_letter += red_binary[-1] + green_binary[-1] + blue_binary[-1]
            msg += chr(int(binary_letter, 2))

        pixel_count += 1

        if len(msg) >= msg_length:
            break
    
    return msg


def main():
    choice = input("Would you like to encode or decode a message? (encode/decode): ").strip().lower()
    if choice == "encode":
        img_path = input("Enter the path of the image: ").strip()
        msg = input("Enter the message you want to encode: ").strip()
        try:
            img = Image.open(img_path)
            encode(img, msg)
            print("Message successfully encoded into 'encoded_image.png'.")
        except Exception as e:
            print(f"Error: {e}")
    elif choice == "decode":
        img_path = input("Enter the path of the encoded image: ").strip()
        try:
            img = Image.open(img_path)
            decoded_message = decode(img)
            print(f"Decoded Message: {decoded_message}")
        except Exception as e:
            print(f"Error: {e}")
    else:
        print("Invalid choice! Please choose 'encode' or 'decode'.")

if __name__ == '__main__':
    main()

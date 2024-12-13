from PIL import Image


def can_encode_message(image, message):
    width, height = image.size

    max_capacity = (width * height) // 8
    print(f'длина сообщения {len(message.encode("utf-8"))} вместимость {max_capacity}')
    return len(message) <= max_capacity


def encode_image(image_path, message, output_path):
    image = Image.open(image_path)
    if not can_encode_message(image, message):
        raise ValueError("Сообщение слишком длинное для этого изображения.")

    encoded_image = image.copy()

    binary_message = ''.join(format(ord(char), '08b') for char in message) + '1111111111111110'
    data_index = 0

    for y in range(encoded_image.height):
        for x in range(encoded_image.width):
            if data_index < len(binary_message):
                pixel = list(encoded_image.getpixel((x, y)))

                pixel[0] = (pixel[0] & ~1) | int(binary_message[data_index])
                encoded_image.putpixel((x, y), tuple(pixel))

                data_index += 1

            if data_index >= len(binary_message):
                break
        if data_index >= len(binary_message):
            break

    encoded_image.save(output_path)
    print(f"Encoded image saved as {output_path}")


def decode_image(image_path):
    image = Image.open(image_path)
    binary_message = ''

    for y in range(image.height):
        for x in range(image.width):

            pixel = image.getpixel((x, y))
            binary_message += str(pixel[0] & 1)

            if binary_message.endswith('1111111111111110'):
                break
        else:
            continue
        break
    message = ''.join(chr(int(binary_message[i:i + 8], 2)) for i in range(0, len(binary_message) - 16, 8))
    return message


# Пример использования
if __name__ == "__main__":
    with open('data/input_message.txt', 'r', encoding='utf-8') as input_file:
        message = input_file.read()

    encode_image('data/input_image.png', message, 'data/output_image.png')
    secret_message = decode_image('data/output_image.png')

    with open('data/output_message.txt', 'w', encoding='utf-8') as output_file:
        output_file.write(secret_message)

    print('Decoded message:', secret_message)

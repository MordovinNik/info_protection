import cv2
def encode_message_in_video(input_video_path: str, output_video_path: str, message: bytearray):
    size = len(message) * 8
    msg_bits = [(size >> i) & 1 for i in range(4 * 8)]
    for c in message:
        msg_bits += [(c >> i) & 1 for i in range(8)]

    binary_index = 0

    cap = cv2.VideoCapture(input_video_path)

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*'FFV1')
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        for i in range(frame_height):
            for j in range(frame_width):
                if binary_index < len(msg_bits):
                    frame[i, j, 0] = (frame[i, j, 0] & 254) | msg_bits[binary_index]
                    binary_index += 1
                else:
                    break

            if binary_index >= len(msg_bits):
                break

        out.write(frame)
    cap.release()
    out.release()
    cv2.destroyAllWindows()


def decode_message_from_video(video_path: str) -> bytearray:
    cap = cv2.VideoCapture(video_path)
    msg_bits = []
    size_bits = []
    msg_size = 0

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        for i in range(frame_height):
            for j in range(frame_width):
                if len(size_bits) < 4 * 8:
                    size_bits.append(frame[i, j, 0] % 2)
                    if len(size_bits) == 4 * 8:
                        msg_size = 0
                        for j, size_bit in enumerate(size_bits):
                            msg_size |= (int(size_bit) << j)
                elif len(msg_bits) < msg_size:
                    msg_bits.append(frame[i, j, 0] % 2)
                else:
                    cap.release()
                    cv2.destroyAllWindows()
                    message = bytearray()
                    value = 0

                    for j, bit in enumerate(msg_bits):
                        if j % 8 == 0 and j != 0:
                            message.append(value)
                            value = 0
                        value |= (bit << (j % 8))

                    return message


if __name__ == "__main__":
    with open('data/input_message.txt', 'rb') as input_file:
        message = bytearray(input_file.read())

    encode_message_in_video('data/input_video.avi', 'data/output_video.avi', message)
    message = decode_message_from_video('data/output_video.avi')
    with open('data/output_message.txt', mode='wb') as msg_file:
        msg_file.write(message)

import wave


def encode_audio(message: bytearray, audio_data: bytearray, sampwidth) -> bytearray:
    res = audio_data
    size = len(message)
    msg_bits = [(size >> i) & 1 for i in range(4 * 8)]
    for c in message:
        msg_bits += [(c >> i) & 1 for i in range(8)]
    j = 0
    for i in range(0, len(audio_data), sampwidth):
        if audio_data[i] % 2 != msg_bits[j]:
            s = 1
            if audio_data[i] == 255:
                s = -1
            res[i] += s
        j += 1
        if j >= len(msg_bits):
            break
    return res


def decode_audio(audio_data: bytearray) -> bytearray:
    message = bytearray()
    size_bits = []
    for i in range(0, 4 * 2 * 8, 2):
        size_bits.append(audio_data[i] % 2)
    msg_size = 0
    for j, size_bit in enumerate(size_bits):
        msg_size |= (size_bit << j)
    bits = []
    for i in range(4 * 2 * 8, (4 + msg_size + 1) * 2 * 8, 2):
        bits.append(audio_data[i] % 2)
    value = 0

    for j, bit in enumerate(bits):
        if j % 8 == 0 and j != 0:
            message.append(value)
            value = 0
        value |= (bit << (j % 8))

    return message


# Пример использования
if __name__ == "__main__":
    with wave.open('data/input_audio.wav', mode='rb') as wav:
        frames = bytearray(wav.readframes(wav.getnframes()))
        params = wav.getparams()

    with open('data/input_message.txt', 'rb') as input_file:
        message = bytearray(input_file.read())

    data = encode_audio(message, frames, params.sampwidth)

    with wave.open('data/output_audio.wav', 'wb') as wav:
        wav.setparams(params)
        wav.writeframes(bytes(data))

    with wave.open('data/output_audio.wav', mode='rb') as wav:
        frames = bytearray(wav.readframes(wav.getnframes()))
        params = wav.getparams()

    message = decode_audio(frames)
    with open('data/output_message.txt', mode='wb') as msg_file:
        msg_file.write(message)

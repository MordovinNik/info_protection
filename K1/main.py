import re
import matplotlib.pyplot as plt
from collections import Counter


def shift_text(text, numbers):
    """Функция шифрования"""
    alphabet = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
    shifted_text = []
    numbers_length = len(numbers)
    i = 0
    for j, char in enumerate(text):
        if char in alphabet:
            # Получаем код символа
            char_code = alphabet.find(char)
            shift_value = numbers[i % numbers_length]
            char_code -= shift_value
            char_code = char_code % len(alphabet)
            new_char = alphabet[char_code]
            # Добавляем новый символ в список
            shifted_text.append(new_char)
            i += 1
        else:
            shifted_text.append(char)

    # Объединяем символы в строку
    return ''.join(shifted_text)


with open('encrypted.txt', 'r', encoding='utf-8') as file:
    encrypted_text = file.read()

cleaned_text = re.sub(r'[^а-яА-ЯёЁ]', '', encrypted_text)

with open('war_and_peace.ru.txt', encoding='utf-8') as file:
    text = file.read()

cleaned_war_and_peace = re.sub(r'[^а-яА-ЯёЁ]', '', text.upper())

char_count = Counter(cleaned_war_and_peace)
char_count = dict(sorted(char_count.items(), key=lambda item: item[1], reverse=True))
chars = list(char_count.keys())
counts = list(char_count.values())

# визуально анализируем частоты символов в "Война и мир"
plt.figure(figsize=(10, 6))
plt.bar(chars, counts, color='skyblue')
plt.xlabel('Символы')
plt.ylabel('Количество вхождений')
plt.title(f'Количество вхождений символов в тексте Война и мир')
plt.xticks(rotation=45)
plt.show()

# Ищем длину ключа, перебирая шаг. И выбирая элементы с периодичностью в шаг
step = 0
n = 8
print(f'отношение первых {n} по частоте символов к {n} последним: {sum(counts[:n]) / sum(counts[-n:])}')
# порог, во сколько раз первые n самых частых символа будут перевешивать последние n
# возьмем вдвое меньше, чем в "Война и мир"
threshold = sum(counts[:n]) / sum(counts[-n:]) / 2

for i in range(1, 200):
    text = cleaned_text[0::i]
    char_count = Counter(text)
    char_count = dict(sorted(char_count.items(), key=lambda item: item[1], reverse=True))
    chars = list(char_count.keys())
    counts = list(char_count.values())

    print(f'step = {i}, {sum(counts[:n]) / sum(counts[-n:])}, n = {n}')

    # проверяем, что нашли именно длину ключа, а не повторяющиеся символы в ключе, проверяя символы в других позициях
    if sum(counts[:n]) / sum(counts[-n:]) > threshold:
        is_valid_length = True
        for j in range(1, i):
            text = cleaned_text[j::i]
            char_count = Counter(text)
            char_count = dict(sorted(char_count.items(), key=lambda item: item[1], reverse=True))
            chars = list(char_count.keys())
            counts = list(char_count.values())
            if sum(counts[:n]) / sum(counts[-n:]) < threshold:
                is_valid_length = False
                break
        if is_valid_length:
            step = i
            break

password = []
# Ищем пароль перебирая алфавит, пока частоты самых распространенных символов не встанут на первые места
for i in range(step):
    for j in range(33):
        text = cleaned_text[i::step]
        text = shift_text(text, [j])
        char_count = Counter(text)

        char_count = dict(sorted(char_count.items(), key=lambda item: item[1], reverse=True))

        chars = list(char_count.keys())
        counts = list(char_count.values())
        # Пробовал сюда еще добавлять проверку редких символов, но они слишком нестабильны
        # Распространенных оказалось достаточно
        if 'О' in chars[:2] and 'А' in chars[:5] and 'Е' in chars[:5]:
            plt.figure(figsize=(10, 6))
            plt.bar(chars, counts, color='skyblue')
            plt.xlabel('Символы')
            plt.ylabel('Количество вхождений')
            plt.title(f'Количество вхождений символов в строке {i + 1}, {j}')
            plt.xticks(rotation=45)
            # plt.show() # проверям, что все в порядке
            password.append(j)

# password = [16, 15, 17, 14, 13, 32, 0, 20, 32, 31, 32]

# Расшифровываем текст с помощью пароля
test = shift_text(encrypted_text, password)
alphabet = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"

# это же отрывок из "Преступление и наказание"
print(test)
with open('decrypted.txt', "w", encoding="utf-8") as file:
    file.write(test)

print(password)
for i in password:
    print(alphabet[i])

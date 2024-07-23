import numpy as np
import hashlib


# 평문에서 키 추출(혹은 개인에 따라 지정해도 됨) -> 아스키코드 합 사용
def extract_key(text):
    ascii_sum = sum(ord(char) for char in text)
    return ascii_sum % (2 * np.pi)  # 키를 0과 2π 사이로 정규화


# 암호화
def encrypt(text):
    key = extract_key(text)  # 평문에서 키를 추출
    numbers = [ord(char) for char in text]
    # 0과 2π 사이로 정규화
    normalized_numbers = [(num / 255.0) * 2 * np.pi for num in numbers]
    # 키를 사용하여 변환
    encrypted_numbers = [np.exp(1j * (num + key)) for num in normalized_numbers]

    # 암호화된 복소수들을 문자열로 변환
    encrypted_strings = [
        f"{num.real:.2f} + {num.imag:.2f}j" for num in encrypted_numbers
    ]

    # 문자열을 하나로 합침
    combined_string = ", ".join(encrypted_strings)

    # 문자열을 해싱
    hashed_value = hashlib.sha256(combined_string.encode()).hexdigest()

    return combined_string, hashed_value


# 복호화
def decrypt(encrypted_string, text):
    key = extract_key(text)  # 평문에서 키를 추출

    # 암호화된 문자열을 복소수로 변환
    encrypted_strings = encrypted_string.split(", ")
    encrypted_numbers = [
        complex(num.replace("j", "j").replace(" + ", "+").replace(" ", ""))
        for num in encrypted_strings
    ]

    decrypted_angles = [np.angle(num) - key for num in encrypted_numbers]
    decrypted_angles = [(angle + 2 * np.pi) % (2 * np.pi) for angle in decrypted_angles]
    decrypted_numbers = [(angle / (2 * np.pi)) * 255.0 for angle in decrypted_angles]
    decrypted_numbers = [int(round(num)) for num in decrypted_numbers]
    decrypted_numbers = [min(max(num, 0), 255) for num in decrypted_numbers]

    return "".join(chr(num) for num in decrypted_numbers)


# 테스트
original_text = "I LOVE U TEACHER S2"
print(f"Original Text: {original_text}")

# 암호화
encrypted_string, hashed_value = encrypt(original_text)
print(f"Encrypted String: {encrypted_string}")
print(f"Hashed Encrypted Value: {hashed_value}")

# 복호화
decrypted_text = decrypt(encrypted_string, original_text)
print(f"Decrypted Text: {decrypted_text}")

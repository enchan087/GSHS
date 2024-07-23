import numpy as np

# SU(2) 행렬 생성 함수
def su2_matrix(theta, phi, psi):
    alpha = np.cos(theta / 2) * np.exp(1j * (phi + psi) / 2)
    beta = np.sin(theta / 2) * np.exp(1j * (phi - psi) / 2)
    return np.array([[alpha, beta], [-np.conj(beta), np.conj(alpha)]])

# 뫼비우스 변환 함수
def mobius_transform(z, U):
    a, b = U[0, 0], U[0, 1]
    c, d = U[1, 0], U[1, 1]
    return (a * z + b) / (c * z + d)

# 뫼비우스 변환 역함수
def inverse_mobius_transform(w, U):
    a, b = U[0, 0], U[0, 1]
    c, d = U[1, 0], U[1, 1]
    det_inv = 1 / (a * d - b * c)
    return det_inv * (d * w - b) / (a - c * w)

# 평문에서 각도 추출
def extract_angles(text):
    angles = []
    for char in text:
        ascii_val = ord(char)
        theta = (ascii_val % 180) * (np.pi / 180)
        phi = (ascii_val % 360) * (np.pi / 180)
        psi = (ascii_val % 90) * (np.pi / 180)
        angles.append((theta, phi, psi))
    return angles

# 평문을 복소수로 변환
def text_to_complex(text):
    complex_numbers = []
    for char in text:
        ascii_val = ord(char)
        z = complex(ascii_val, 0)
        complex_numbers.append(z)
    return complex_numbers

# 복소수에서 문자로 변환
def complex_to_text(complex_numbers):
    text = ''
    for z in complex_numbers:
        ascii_val = round(z.real)
        if 0 <= ascii_val <= 255:
            text += chr(ascii_val)
        else:
            text += '?'
    return text

# 평문
message = "HELLOW"

# 개인키
private_theta, private_phi, private_psi = np.pi / 4, np.pi / 3, np.pi / 6

# 공개키 생성
public_key_U = su2_matrix(private_theta, private_phi, private_psi)

# 각도 추출
angles = extract_angles(message)

# 평문을 복소수로 변환
complex_numbers = text_to_complex(message)

# 암호화 과정
encrypted_numbers = []
for z, (theta, phi, psi) in zip(complex_numbers, angles):
    U = su2_matrix(theta, phi, psi)
    encrypted_numbers.append(mobius_transform(z, public_key_U))

# 암호화된 복소수를 좌표쌍으로 저장
encrypted_coordinates = [(z.real, z.imag) for z in encrypted_numbers]

print("평문 >", message)
print("암호화된 좌표쌍 >", encrypted_coordinates)

# 복호화 과정
decrypted_numbers = []
for (x, y), (theta, phi, psi) in zip(encrypted_coordinates, angles):
    w = complex(x, y)
    U = su2_matrix(theta, phi, psi)
    decrypted_numbers.append(inverse_mobius_transform(w, public_key_U))

# 복호화된 메시지 확인
decrypted_message = complex_to_text(decrypted_numbers)

print("복호화된 메시지 >", decrypted_message)

from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
import zlib

def calculate_entropy(text):
    counter = Counter(text)
    length = len(text)
    return -sum((count / length) * np.log2(count / length) for count in counter.values())

def frequency_analysis(text):
    counter = Counter(text)
    length = len(text)
    return {char: count / length for char, count in counter.items()}

def dynamic_max_lag(text_length):
    return min(text_length - 1, int(10 * np.log10(text_length)))

def autocorrelation(text, max_lag=None):
    text_length = len(text)
    if max_lag is None:
        max_lag = dynamic_max_lag(text_length)
    
    text_numeric = np.array([ord(c) for c in text])
    mean = np.mean(text_numeric)
    var = np.var(text_numeric)

    if text_length < 2:
        return [1.0]
    
    def r(h):
        return np.correlate(text_numeric - mean, np.roll(text_numeric - mean, h))[0] / (text_length * var)
    
    return [r(lag) for lag in range(min(max_lag, text_length))]

def compression_ratio(text):
    compressed = zlib.compress(text.encode())
    return len(compressed) / len(text)

def index_of_coincidence(text):
    counter = Counter(text)
    length = len(text)
    return sum(count * (count - 1) for count in counter.values()) / (length * (length - 1))

def analyze_encryption(ciphertext):
    entropy = calculate_entropy(ciphertext)
    max_entropy = np.log2(len(set(ciphertext)))
    print(f"Entropy: {entropy} (Max: {max_entropy})")

    freq = frequency_analysis(ciphertext)
    plt.figure(figsize=(12, 3))
    
    plt.subplot(141)
    plt.bar(freq.keys(), freq.values())
    plt.title('Character Frequency Distribution')
    plt.xlabel('Characters')
    plt.ylabel('Frequency')

    max_lag = dynamic_max_lag(len(ciphertext))
    autocorr = autocorrelation(ciphertext, max_lag)
    plt.subplot(142)
    plt.plot(range(len(autocorr)), autocorr)
    plt.title('Autocorrelation')
    plt.xlabel('Lag')
    plt.ylabel('Autocorrelation')

    ratio = compression_ratio(ciphertext)
    print(f"Compression ratio: {ratio}")

    plt.subplot(143)
    plt.bar(['Original', 'Compressed'], [1, ratio])
    plt.title('Compression Ratio')
    plt.ylabel('Relative Size')
    
    ioc = index_of_coincidence(ciphertext)
    print(f"Index of Coincidence: {ioc}")

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    ciphertext = input("||Input Ciphertext: ")
    analyze_encryption(ciphertext)

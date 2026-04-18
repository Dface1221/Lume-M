import cv2
import numpy as np
import matplotlib.pyplot as plt

VIDEO_PATH = "test7.1.mp4"

cap = cv2.VideoCapture(VIDEO_PATH)
brightness = []

while True:
    ret, frame = cap.read()
    if not ret:
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    brightness.append(np.mean(gray))

cap.release()

brightness = np.array(brightness)

# Smooth a bit
smooth = np.convolve(brightness, np.ones(5)/5, mode='same')

# -------- Find baseline --------
base_level = np.median(smooth)
threshold = base_level + 10

# -------- Find pulse regions --------
pulses = []
inside = False
start = 0

for i, val in enumerate(smooth):
    if val > threshold and not inside:
        inside = True
        start = i
    elif val <= threshold and inside:
        inside = False
        end = i
        height = np.mean(smooth[start:end])
        pulses.append((start, end, height))

print(f"[+] Pulses found: {len(pulses)}")

# -------- Classify dot/dash --------
heights = np.array([h for _,_,h in pulses])
split = (heights.min() + heights.max()) / 2

symbols = []
for start, end, h in pulses:
    if h < split:
        symbols.append((start, '.'))
    else:
        symbols.append((start, '-'))

print("Symbols:", ''.join([s for _, s in symbols]))

# -------- Gap analysis --------
letters = []
current = ""

for i in range(len(symbols)):
    current += symbols[i][1]

    if i < len(symbols) - 1:
        gap = symbols[i+1][0] - symbols[i][0]

        if gap > 50:
            letters.append(current)
            letters.append(" ")
            current = ""
        elif gap > 25:
            letters.append(current)
            current = ""

letters.append(current)

print("Morse groups:", letters)

# Morse decode
MORSE = {
    ".-": "A","-...": "B","-.-.": "C","-..": "D",".": "E",
    "..-.": "F","--.": "G","....": "H","..": "I",".---": "J",
    "-.-": "K",".-..": "L","--": "M","-.": "N","---": "O",
    ".--.": "P","--.-": "Q",".-.": "R","...": "S","-": "T",
    "..-": "U","...-": "V",".--": "W","-..-": "X","-.--": "Y","--..": "Z"
}

decoded = ""
for code in letters:
    if code == " ":
        decoded += " "
    else:
        decoded += MORSE.get(code, '?')

print("\n✅ DECODED:", decoded)

# Plot
plt.figure(figsize=(12,6))
plt.plot(smooth)
plt.axhline(threshold, color='r')
plt.title("Pulse Regions Detection")
plt.show()

import cv2
import numpy as np
import matplotlib.pyplot as plt

VIDEO_PATH = "test7.mp4"

cap = cv2.VideoCapture(VIDEO_PATH)

# Read first frame
ret, first_frame = cap.read()
if not ret:
    print("Error: Could not open video.")
    exit()

# -----------------------------
# 🔥 FIX: Resize for ROI display
# -----------------------------
display_width = 800  # adjust if needed
scale = display_width / first_frame.shape[1]

resized_frame = cv2.resize(first_frame, None, fx=scale, fy=scale)

print("Select the LED area with your mouse and press ENTER/SPACE")

roi = cv2.selectROI("Select LED", resized_frame, fromCenter=False, showCrosshair=True)
cv2.destroyWindow("Select LED")

# Scale ROI back to original size
x = int(roi[0] / scale)
y = int(roi[1] / scale)
w = int(roi[2] / scale)
h = int(roi[3] / scale)

# -----------------------------
# Continue your original code
# -----------------------------
brightness_history = []
frame_count = 0

print("Processing video...")

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    led_zone = frame[y:y+h, x:x+w]
    
    gray = cv2.cvtColor(led_zone, cv2.COLOR_BGR2GRAY)
    
    avg_brightness = np.mean(gray)
    brightness_history.append(avg_brightness)
    
    frame_count += 1

cap.release()

brightness_history = np.array(brightness_history)

# -----------------------------
# Smoothing
# -----------------------------
window_size = 3 
smooth_brightness = np.convolve(
    brightness_history,
    np.ones(window_size)/window_size,
    mode='same'
)

# -----------------------------
# Pulse Detection
# -----------------------------
base_level = np.median(smooth_brightness)
threshold = base_level + 10

pulses = []
inside = False
start = 0

for i, val in enumerate(smooth_brightness):
    if val > threshold and not inside:
        inside = True
        start = i
    elif val <= threshold and inside:
        inside = False
        end = i
        height = np.mean(smooth_brightness[start:end])
        pulses.append((start, end, height))

print(f"[+] Pulses found: {len(pulses)}")

# -----------------------------
# Dot/Dash Classification
# -----------------------------
heights = np.array([h for _, _, h in pulses])

if len(heights) == 0:
    print("No pulses detected.")
    exit()

split = (heights.min() + heights.max()) / 2

symbols = []
for start, end, h in pulses:
    if h < split:
        symbols.append((start, '.'))
    else:
        symbols.append((start, '-'))

print("Symbols:", ''.join([s for _, s in symbols]))

# -----------------------------
# Gap Analysis
# -----------------------------
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

# -----------------------------
# Morse Decode
# -----------------------------
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

# -----------------------------
# Plot
# -----------------------------
plt.figure(figsize=(15, 6))
plt.plot(smooth_brightness, label='LED Brightness')

plt.title(f"LED Intensity Over Time ({VIDEO_PATH})")
plt.xlabel("Frame Number")
plt.ylabel("Brightness")
plt.grid(True, alpha=0.3)
plt.legend()

plt.axhline(y=np.min(smooth_brightness), linestyle='--', label='Min')
plt.axhline(y=np.max(smooth_brightness), linestyle='--', label='Max')

plt.tight_layout()
plt.show()
import cv2
import numpy as np
import matplotlib.pyplot as plt

VIDEO_PATH = "test9.mp4"

cap = cv2.VideoCapture(VIDEO_PATH)

# Read the first frame to select the LED area
ret, first_frame = cap.read()
if not ret:
    print("Error: Could not open video.")
    exit()

print("Select the LED area with your mouse and press ENTER/SPACE")
roi = cv2.selectROI("Select LED", first_frame, fromCenter=False, showCrosshair=True)
cv2.destroyWindow("Select LED")

x, y, w, h = int(roi[0]), int(roi[1]), int(roi[2]), int(roi[3])

brightness_history = []
frame_count = 0

print("Processing video...")

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # 1. Crop to the LED only
    led_zone = frame[y:y+h, x:x+w]
    
    # 2. Convert to Grayscale
    gray = cv2.cvtColor(led_zone, cv2.COLOR_BGR2GRAY)
    
    # 3. Get the average brightness of just that spot
    avg_brightness = np.mean(gray)
    brightness_history.append(avg_brightness)
    
    frame_count += 1

cap.release()

# Convert to numpy array for plotting
brightness_history = np.array(brightness_history)

# Optional: Slight smoothing to remove sensor flicker
# Higher number = smoother graph (but hides fast transitions)
window_size = 3 
smooth_brightness = np.convolve(brightness_history, np.ones(window_size)/window_size, mode='same')


# -------- Detect Pulses --------
base_level = np.median(smooth_brightness)
threshold = base_level + 10   # you can tweak this if needed

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

# -------- Classify Dot / Dash --------
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

# -------- Gap Analysis (group into letters) --------
letters = []
current = ""

for i in range(len(symbols)):
    current += symbols[i][1]

    if i < len(symbols) - 1:
        gap = symbols[i+1][0] - symbols[i][0]

        if gap > 50:   # word gap
            letters.append(current)
            letters.append(" ")
            current = ""
        elif gap > 25: # letter gap
            letters.append(current)
            current = ""

letters.append(current)

print("Morse groups:", letters)

# -------- Morse Dictionary --------
MORSE = {
    ".-": "A","-...": "B","-.-.": "C","-..": "D",".": "E",
    "..-.": "F","--.": "G","....": "H","..": "I",".---": "J",
    "-.-": "K",".-..": "L","--": "M","-.": "N","---": "O",
    ".--.": "P","--.-": "Q",".-.": "R","...": "S","-": "T",
    "..-": "U","...-": "V",".--": "W","-..-": "X","-.--": "Y","--..": "Z"
}

# -------- Decode --------
decoded = ""

for code in letters:
    if code == " ":
        decoded += " "
    else:
        decoded += MORSE.get(code, '?')

print("\n DECODED:", decoded)


# -------- Plotting --------
plt.figure(figsize=(15, 6))
plt.plot(smooth_brightness, color='blue', linewidth=1.5, label='LED Brightness')

# Formatting the graph
plt.title(f"LED Intensity Over Time (Source: {VIDEO_PATH})")
plt.xlabel("Frame Number")
plt.ylabel("Brightness (0-255)")
plt.grid(True, alpha=0.3)
plt.legend()

# Show the 'Base' level to see the breathing floor
plt.axhline(y=np.min(smooth_brightness), color='red', linestyle='--', label='Min Breath')
plt.axhline(y=np.max(smooth_brightness), color='green', linestyle='--', label='Max Peak')

plt.tight_layout()
plt.show()
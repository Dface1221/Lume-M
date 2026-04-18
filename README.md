# Lume-M
---
# Steganographic LED Morse Communication (ESP32 + Computer Vision)

A covert communication system that encodes Morse code into **subtle brightness variations** of an LED using an ESP32, and decodes it from video using Python + OpenCV.

Instead of obvious blinking, this project hides information inside **smooth light intensity changes**, making it appear like normal ambient lighting to the human eye while remaining machine-decodable.

---

## Features

*  **Stealth Communication** — No visible blinking, only smooth brightness modulation
*  **ESP32-based Encoder** — Real-time LED signal generation using FastLED
*  **Camera-based Decoder** — Extracts hidden data from recorded video
*  **Adjustable Signal Parameters** — Control brightness, speed, and smoothness
*  **Scene System** — Structured phases for calibration, idle, and transmission
*  **Full Morse Support** — A–Z, 0–9, and spaces

---

## How It Works

### Encoding (ESP32)

The LED never turns fully off. Instead:

```
Final Brightness = BASE_LEVEL + Pulse Signal
```

* **BASE_LEVEL** → constant ambient light (stealth layer)
* **DOT / DASH** → small and large brightness increases
* **Smoothing** → gradual rise/fall to avoid sharp transitions

This creates a signal that looks like natural lighting but carries data.

---

### Decoding (Python + OpenCV)

1. Select LED region in video
2. Extract brightness per frame
3. Smooth signal
4. Apply threshold detection
5. Convert pulses → Morse → text

---

## Hardware Setup

* ESP32
* WS2812B LED strip (or single LED)
* Camera (phone or webcam)

---

## Software Requirements

### ESP32

* Arduino IDE
* FastLED library

### Python

```bash
pip install opencv-python numpy matplotlib
```

---

## Configuration (Encoder)

You can control the behavior using these parameters:

```cpp
#define BASE_LEVEL 30.0   // Ambient brightness
#define DOT_BOOST  60.0   // Dot intensity
#define DASH_BOOST 140.0  // Dash intensity

#define RISE_SPEED 0.02   // Speed of brightness increase
#define FALL_SPEED 0.04   // Speed of brightness decrease
```

---

## Parameter Guide

| Parameter    | Description                                    |
| ------------ | ---------------------------------------------- |
| `BASE_LEVEL` | Background light level (higher = more stealth) |
| `DOT_BOOST`  | Brightness increase for dot                    |
| `DASH_BOOST` | Brightness increase for dash                   |
| `RISE_SPEED` | How fast light rises                           |
| `FALL_SPEED` | How fast light falls                           |

---

## Stealth vs Reliability

| Mode             | Settings                    |
| ---------------- | --------------------------- |
| **Easy Decode**  | High boosts, faster speeds  |
| **Balanced**     | Medium boosts and smoothing |
| **Stealth Mode** | Low boosts, slow smoothing  |

---

## Example Output

* Raw signal appears as smooth light variation
* Decoder reconstructs Morse sequence
* Final output:

```
WORLD
```

---

## Limitations

* Very low brightness differences may fail detection
* Camera FPS affects decoding accuracy
* Strong ambient lighting can introduce noise

---

## Currently work under controlled environment

* It is still under development so error can occur
* Work in controlled environment, outside use can produce undesired result
* Need some adjustments before deployment and the environment must be known to user and tested multiple time at different angles

---

## Future Improvements

* Adaptive thresholding in decoder
* Real-time decoding (live camera feed)
* Frequency/phase-based encoding
* Multi-LED parallel communication

---

## Project Structure

```
/esp32
  └── led_morse.ino

/python
  └── decoder.py

/videos
  └── sample.mp4
```

---

## Contributing

Feel free to fork, experiment, and improve decoding robustness or stealth techniques.

---

## License

MIT License

---

## Acknowledgments

* Inspired by covert optical communication techniques
* Built using FastLED and OpenCV

---

## Summary

This project demonstrates how:

> **Information can be hidden in plain sight using light.**

A normal-looking LED becomes a covert communication channel.

---

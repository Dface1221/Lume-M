#include <FastLED.h>

#define LED_PIN    2
#define NUM_LEDS   8

CRGB leds[NUM_LEDS];

// --- Morse Settings ---
String message = "HELLO WORLD I AM DFACE";
int messageIdx = 0;
int symbolIdx = 0;
bool isGapActive = false;
bool messageFinished = false;

// --- CALIBRATION (YOU CONTROL EVERYTHING HERE) ---
#define BASE_LEVEL    30.0   // ambient constant light
#define DOT_BOOST     60.0   // dot brightness above base
#define DASH_BOOST    140.0  // dash brightness above base

#define RISE_SPEED    0.02   // faster = sharper
#define FALL_SPEED    0.04   // faster = quicker drop

float pulseTarget = 0;
float pulseCurrent = 0;

int currentScene = 0;
unsigned long sceneStartTime = 0;

void setup() {
  delay(2000);
  FastLED.addLeds<WS2812B, LED_PIN, GRB>(leds, NUM_LEDS);
  sceneStartTime = millis();
}

String getMorse(char c) {
  switch (toupper(c)) {
    // Letters
    case 'A': return ".-";
    case 'B': return "-...";
    case 'C': return "-.-.";
    case 'D': return "-..";
    case 'E': return ".";
    case 'F': return "..-.";
    case 'G': return "--.";
    case 'H': return "....";
    case 'I': return "..";
    case 'J': return ".---";
    case 'K': return "-.-";
    case 'L': return ".-..";
    case 'M': return "--";
    case 'N': return "-.";
    case 'O': return "---";
    case 'P': return ".--.";
    case 'Q': return "--.-";
    case 'R': return ".-.";
    case 'S': return "...";
    case 'T': return "-";
    case 'U': return "..-";
    case 'V': return "...-";
    case 'W': return ".--";
    case 'X': return "-..-";
    case 'Y': return "-.--";
    case 'Z': return "--..";

    // Numbers
    case '0': return "-----";
    case '1': return ".----";
    case '2': return "..---";
    case '3': return "...--";
    case '4': return "....-";
    case '5': return ".....";
    case '6': return "-....";
    case '7': return "--...";
    case '8': return "---..";
    case '9': return "----.";

    // Space (word gap)
    case ' ': return " ";

    default: return ""; // unknown character
  }
}

void loop() {
  unsigned long now = millis();
  float masterMultiplier = 0.0;

  if (currentScene == 0) { 
    masterMultiplier = 1.0;
    if (now - sceneStartTime > 3000) { currentScene = 1; sceneStartTime = now; }
  } 
  else if (currentScene == 1) { 
    masterMultiplier = 0.0;
    if (now - sceneStartTime > 3000) { currentScene = 2; sceneStartTime = now; }
  } 
  else if (currentScene == 2) { 
    masterMultiplier = 1.0;
    if (now - sceneStartTime > 3000) { currentScene = 3; messageIdx = 0; messageFinished = false; }
  } 
  else if (currentScene == 3) { 
    masterMultiplier = 1.0;
    handleAbsoluteMorse(); 
    if (messageFinished) { currentScene = 4; sceneStartTime = now; }
  } 
  else if (currentScene == 4) { 
    masterMultiplier = 1.0;
    pulseTarget = 0;
    if (now - sceneStartTime > 3000) { currentScene = 5; sceneStartTime = now; }
  } 
  else if (currentScene == 5) { 
    masterMultiplier = 0.0;
    if (now - sceneStartTime > 2000) { currentScene = 0; sceneStartTime = now; }
  }

  float speed = (pulseTarget > pulseCurrent) ? RISE_SPEED : FALL_SPEED;
  pulseCurrent += (pulseTarget - pulseCurrent) * speed;


  float finalValue = (BASE_LEVEL + pulseCurrent) * masterMultiplier;

  int outputLevel = (int)constrain(finalValue, 0, 255);

  fill_solid(leds, NUM_LEDS, CRGB(outputLevel, outputLevel, outputLevel));
  FastLED.show();
  delay(10);
}

void handleAbsoluteMorse() {
  bool reachedTarget = abs(pulseTarget - pulseCurrent) < 0.5;

  if (reachedTarget) {
    String currentCode = getMorse(message[messageIdx]);

    if (!isGapActive) {
      if (symbolIdx < currentCode.length()) {
        char s = currentCode[symbolIdx];

        if (s == '.') pulseTarget = DOT_BOOST;
        else if (s == '-') pulseTarget = DASH_BOOST;
        else if (s == ' ') pulseTarget = 0;

        symbolIdx++;
        isGapActive = true;
      } else {
        messageIdx++;
        symbolIdx = 0;
        if (messageIdx >= message.length()) messageFinished = true;
      }
    } else {
      pulseTarget = 0;
      isGapActive = false;
    }
  }
}
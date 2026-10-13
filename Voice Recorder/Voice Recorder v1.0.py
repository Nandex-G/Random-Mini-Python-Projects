import sounddevice as sd
import wavio as wav


freq = 44100
duration = 5

recording = sd.rec(int(freq * duration), samplerate=freq, channels=1)

sd.wait()

wav.write("Audio.wav", recording, freq, sampwidth=1)
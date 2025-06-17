#Importamos las librerías necesarias
import numpy as np
import matplotlib.pyplot as plt
#import librosa
#import librosa.display
import soundfile as sf
from IPython.display import Audio, display
import matplotlib.pyplot as plt
from scipy.signal import spectrogram

# %% (Acá se carga y se muestra la información básica del audio.)
archivo = 'AnalisisTextos.wav'
audio, sr = sf.read('AnalisisTextos.wav')

# Información solicitada del audio (por consignas).
print("Vector de la señal segmentada:", audio)
print("Cantidad total de elementos en la muestra:", len(audio))
print("Frecuencia de Muestreo (Medida en MegaHerzios):", sr)
duracion = len(audio) / sr
print("Duración del audio:", duracion)

# %% Se reproduce el audio original.
print("Audio original (Sin modificaciones):")
display(Audio(audio, rate=sr))

# %% Se imprime el gráfico de la señal sonora del audio original.
plt.figure(figsize=(10, 4))
plt.plot(audio, color='red')
plt.title("Espectograma del audio:")
plt.xlabel("Muestras")
plt.ylabel("Amplitud")
plt.tight_layout()
plt.show()

# %% Aceleramos el audio al X2 (Duplicamos la velocidad).
print("Audio acelerado (velocidad duplicada / al X2):")
display(Audio(audio, rate=sr * 2))

print("Espectrograma del audio acelerado (velocidad duplicada / al X2):")
f_fast, t_fast, Sxx_fast = spectrogram(audio, fs=sr * 2)
plt.figure(figsize=(10, 4))
plt.pcolormesh(t_fast, f_fast, 10 * np.log10(Sxx_fast), shading='gouraud', cmap='magma')
plt.title("Espectrograma - Audio acelerado (x2)")
plt.ylabel('Frecuencia [Hz]')
plt.xlabel('Tiempo [s]')
plt.colorbar(label='Intensidad [dB]')
plt.tight_layout()
plt.show()

# %% Ralentizamos el audio (Bajamos su velocidad al 0.5 haciendo uso de "//2").
print("Audio ralentizado (velocidad reducida a la mitad):")
display(Audio(audio, rate=sr // 2))

# Espectrograma de audio ralentizado
print("Espectrograma del audio ralentizado (velocidad reducida a la mitad):")
f_slow, t_slow, Sxx_slow = spectrogram(audio, fs=sr // 2)
plt.figure(figsize=(10, 4))
plt.pcolormesh(t_slow, f_slow, 10 * np.log10(Sxx_slow), shading='gouraud', cmap='magma')
plt.title("Espectrograma - Audio ralentizado (x0.5)")
plt.ylabel('Frecuencia [Hz]')
plt.xlabel('Tiempo [s]')
plt.colorbar(label='Intensidad [dB]')
plt.tight_layout()
plt.show()

# %% Se baja la calidad del audio.
audio_baja_calidad = (audio * 2**3).astype(np.int8)
print("Audio con menor calidad (se reducen la cantidad de bits):")
display(Audio(audio_baja_calidad, rate=sr))

# %% Guardamos el audio con las siguientes lineas de codigo: 
"""sf.write('AnalisisTexto2.wav', audio, samplerate=sr)
print("Archivo guardado como 'AnalisisTextos2.wav'")"""
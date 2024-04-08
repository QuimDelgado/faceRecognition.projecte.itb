#!/usr/bin/env python3
"""
Envia una foto de la cara quan en reconeix alguna. Versió descartada per ser massa lenta.
"""
import subprocess
import time
import cv2
import face_recognition
from send import sendToServerPIC
from i2c import OledDisplay, drawText


def take_pic(nom_foto="foto_capturada.jpg"):
    video_capture = cv2.VideoCapture('/dev/video0')

    print("MIRA A LA CAMARA :D")
    
    cara_detectada = False
    num_frames = 0
    start_time = time.time()  # Marca de tiempo al inicio

    while not cara_detectada:
        ret, frame = video_capture.read()
        if ret:
            num_frames += 1  # Incrementa el contador de cuadros

            # Reducir la resolución del frame para la detección de caras
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = small_frame[:, :, ::-1]

            ubicacions_caras = face_recognition.face_locations(rgb_small_frame)
            if ubicacions_caras:
                cv2.imwrite(nom_foto, frame)
                cara_detectada = True
                break

    end_time = time.time()  # Marca de tiempo al final
    elapsed_time = end_time - start_time  # Calcula el tiempo transcurrido
    fps = num_frames / elapsed_time  # Calcula los FPS

    print(f"FPS: {fps:.2f}")  # Muestra los FPS

    video_capture.release()

    respostaServerPIC = "Quim"   #sendToServerPIC(nom_foto)
    if respostaServerPIC != "false":
        drawText(f"Usuari {respostaServerPIC} validat. Benvingut")
    else:
        drawText("Accés denegat")

    return respostaServerPIC

if __name__ == "__main__":
    take_pic()


"""
Captura una imatge i la envia al servidor
(modificar url)
"""

import face_recognition
import cv2
import platform
import requests

def mostra_camara(nom_arxiu, video_capture):
    """Funció per mostrar la càmera i capturar una imatge quan detecta una cara."""
    cara_detectada = False
    while not cara_detectada:
        ret, frame = video_capture.read()
        if ret:
            # Aquí es fa servir face_recognition per detectar les ubicacions de les cares
            ubicacions_caras = face_recognition.face_locations(frame)
            for top, right, bottom, left in ubicacions_caras:
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cara_detectada = True

            cv2.imshow('Vídeo', frame)

            if cv2.waitKey(1) & 0xFF == ord('q') or cara_detectada:
                break
    cv2.imwrite(nom_arxiu, frame)

def captura_imatge_camara(nom_arxiu="foto_capturada.jpg"):
    """Captura una imatge des de la càmera i la guarda només quan detecta una cara."""
    video_capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    print("Iniciant càmera...")

    if platform.system() == 'Windows':
        mostra_camara(nom_arxiu, video_capture)
    else:
        while True:
            ret, frame = video_capture.read()
            if ret:
                # Aquí també s'usa face_recognition per detectar les cares
                ubicacions_caras = face_recognition.face_locations(frame)
                if ubicacions_caras:
                    cv2.imwrite(nom_arxiu, frame)
                    break

    video_capture.release()
    cv2.destroyAllWindows()

    envia_imatge_servidor(nom_arxiu)

def envia_imatge_servidor(nom_arxiu):
    """Envia la imatge al servidor."""
    url = "http://localhost:8080/upload"
    with open(nom_arxiu, 'rb') as f:
        files = {'file': (nom_arxiu, f)}
        response = requests.post(url, files=files)
        print("Resposta del servidor:", response.text)

if __name__ == "__main__":
    captura_imatge_camara()

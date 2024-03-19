"""
Fa una foto i si no coincideix amb cap cara ja guardada al directori genera un nou directori i guarda a l'usuari

newUser.py
Quim Delgado
"""

import face_recognition
import cv2
import os

def captura_imagen_camara():
    """Captura una imagen desde la cámara automáticamente cuando detecta una cara."""
    video_capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    print("Iniciando cámara para captura de usuario nuevo...")
    cara_detectada = False
    frame_capturado = None

    while not cara_detectada:
        ret, frame = video_capture.read()
        if not ret:
            print("Error al capturar imagen. Intente nuevamente.")
            continue
        
        # Busca caras en el frame actual.
        ubicaciones_caras = face_recognition.face_locations(frame)
        if ubicaciones_caras:
            # Si encuentra al menos una cara, guarda el frame.
            cara_detectada = True
            frame_capturado = frame
            print("Cara detectada, capturando imagen...")
            break

        cv2.imshow('Previsualización', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):  # Permitir salida con 'q' como precaución
            break

    video_capture.release()
    cv2.destroyAllWindows()
    return frame_capturado

def comprobar_usuario_existente(imagen):
    """Comprueba si la cara en la imagen ya está registrada."""
    for root, dirs, _ in os.walk("./fotos"):
        for subdir in dirs:
            path = os.path.join(root, subdir)
            for foto in os.listdir(path):
                imagen_referencia = face_recognition.load_image_file(os.path.join(path, foto))
                codificacion_referencia = face_recognition.face_encodings(imagen_referencia)
                codificacion_actual = face_recognition.face_encodings(imagen)
                if codificacion_actual and codificacion_referencia:
                    resultado = face_recognition.compare_faces(codificacion_referencia, codificacion_actual[0])
                    if True in resultado:
                        return True
    return False

def registrar_usuario(imagen):
    """Registra al usuario guardando su foto en el directorio correspondiente."""
    nombre = input("Ingrese su nombre: ").strip()
    directorio_usuario = f"./fotos/{nombre}"
    if not os.path.exists(directorio_usuario):
        os.makedirs(directorio_usuario)
    cv2.imwrite(f"{directorio_usuario}/{nombre}.jpg", imagen)
    print(f"Usuario {nombre} registrado exitosamente.")

def main():
    while True:
        imagen = captura_imagen_camara()
        if comprobar_usuario_existente(imagen):
            print("Usuario coincidente, tiene que ser un usuario nuevo.")
            break  # Salir si el usuario ya existe

        cv2.imshow("Confirmar foto", imagen)
        cv2.waitKey(1)  # Pequeña espera para que la imagen se muestre correctamente
        respuesta = input("¿Desea repetir la foto? [S/n]: ").upper()
        cv2.destroyAllWindows()

        if respuesta != 'S':
            registrar_usuario(imagen)
            break

main()

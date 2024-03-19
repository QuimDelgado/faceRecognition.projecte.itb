"""
Verifica l'usuari i mira si la cara de la imatge enviada es correspon a una dins dels directoris dins de fotos.

verificaUsuari.py
Quim Delgado
"""
import face_recognition
import os

def troba_caras(imagen):
    """Troba les codificacions de cares en una imatge."""
    codificacions = face_recognition.face_encodings(imagen)
    return codificacions

def compara_caras(directori, codificacio_desconeguda):
    """Compara una cara desconeguda amb totes les cares en un directori."""
    for root, dirs, files in os.walk(directori):
        for subdir in dirs:
            path = os.path.join(root, subdir)
            for foto in os.listdir(path):
                try:
                    imatge_referencia = face_recognition.load_image_file(os.path.join(path, foto))
                    codificacio_referencia = troba_caras(imatge_referencia)
                    if codificacio_referencia:
                        resultat = face_recognition.compare_faces(codificacio_referencia, codificacio_desconeguda[0])
                        if True in resultat:
                            return subdir
                except Exception as e:
                    print(f"Error al processar {foto} en {subdir}: {e}")
    return None

def identificar_usuari():
    usuari_identificat = False
    imatge_capturada = r".\rebedor\foto_capturada.jpg"
    
    print("Verificant usuari...")
    try:
        imatge_desconeguda = face_recognition.load_image_file(imatge_capturada)
        codificacio_desconeguda = troba_caras(imatge_desconeguda)
        if codificacio_desconeguda:
            resultat = compara_caras(".\\fotos", codificacio_desconeguda)
            if resultat:
                print(f"Usuari identificat, benvingut {resultat}")
                usuari_identificat = True
                return usuari_identificat 
            else:
                print("Usuari no identificat.")
                return False
        else:
            print("No s'ha trobat cap cara a la imatge.")
    except FileNotFoundError:
        print("No s'ha trobat la imatge 'foto_capturada.jpg'.")

if __name__ == "__main__":
    identificar_usuari()

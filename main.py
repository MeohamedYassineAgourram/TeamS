# Vérification de la question 7 sur l'exemple de la section 1.7
from outils import EcrivainBits, LecteurBits


def lecture(fichier_bin):
    with open(fichier_bin, 'rb') as fichier:
        contenu = fichier.read()
    bits = "".join(f"{octet:08b}" for octet in contenu)
    print(bits)
    return bits


codes = [97, 98, 256, 256, 256, 97, 258, 97]
largeurs = [8, 8, 9, 9, 9, 9, 9, 9]

# Écriture des codes
with open("test_q7.bin", "wb") as f:
    ecrivain = EcrivainBits(f)
    for i in range(len(codes)):
        ecrivain.ecrire_code(codes[i], largeurs[i])
    ecrivain.fermer()

# Vérification avec la fonction lecture
attendu = ("01100001" "01100010" "100000000" "100000000" "100000000"
           "001100001" "100000010" "001100001" "00")
bits = lecture("test_q7.bin")
print("bits identiques à la section 1.7 :", bits == attendu)

# Relecture avec lire_code
with open("test_q7.bin", "rb") as f:
    lecteur = LecteurBits(f)
    relus = [lecteur.lire_code(w) for w in largeurs]
print("codes relus :", relus, "->", relus == codes)
print("bits restants (bourrage) :", lecteur.bits_restants())

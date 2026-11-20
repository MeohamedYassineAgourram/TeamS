import outils

# Question 7

codes    = [97, 98, 256, 256, 256, 97, 258, 97]
largeurs = [8,  8,  9,   9,   9,   9,  9,   9]

# Test d'écriture
with open("test_q7.lzmw", "wb") as f:
    f.write(bytes([24]))  # En-tête b = 24
    
    outils.fichier_bin = f
    outils.buffer = 0
    outils.nb_bits = 0
    
    for c, w in zip(codes, largeurs):
        outils.ecrire_code(c, w)
        
    # Bourrage final : s'il reste des bits dans le tampon, on complète avec des 0 à droite
    if outils.nb_bits > 0:
        octet_final = (outils.buffer << (8 - outils.nb_bits)) & 0xFF
        f.write(bytes([octet_final]))

# Vérification avec la fonction lecture
outils.lecture("test_q7.lzmw")

# Test de relecture avec la fonction lire_code
with open("test_q7.lzmw", "rb") as f:
    b = f.read(1)[0]
    
    outils.fichier_bin = f
    outils.buffer = 0
    outils.nb_bits = 0
    
    codes_lus = [outils.lire_code(w) for w in largeurs]
    print("b =", b, "| Codes relus :", codes_lus)
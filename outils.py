# Question 5
# Fonction permettant la lecture du contenu du fichier et son affichage à l’écran sous forme d’une chaîne de bits
def lecture(fichier_bin):
    # Ouverture du fichier en mode lecture binaire
    with open(fichier_bin, 'rb') as fichier:
        contenu = fichier.read()

    # Conversion du contenu binaire en une chaîne de bits et affichage à l'écran
    bits = "".join(f"{octet:08b}" for octet in contenu)
    print(bits)


# Question 6
# Fonction produisant en sortie un fichier binaire nommé fichier.bin encodant le texte fichier_chaine.txt sous forme de fichier binaire
def ecriture(fichier_chaine, fichier_bin) :
    # Ouverture du fichier texte en mode lecture
    with open(fichier_chaine, 'r') as fichier :
        contenu = fichier.read().strip() # .strip() pour enlever '\n' à la fin du fichier

    # Bourrage à droite avec des '0' pour atteindre un multiple de 8 bits
    while (len(contenu) % 8 != 0) :
        contenu += '0'

    # Découpe du contenu en blocs de 8 bits et conversion en octets
    octets = bytearray()
    for i in range(0, len(contenu), 8):
        tranche = contenu[i:i+8]
        octets.append(int(tranche, 2))

    # Ecriture du contenu binaire dans le fichier binaire (en respectant la forme )
    with open(fichier_bin, 'wb') as fichier :
        fichier.write(octets)


# Question 7

# Variables globales pour mémoriser le fichier et l'état du tampon entre deux appels
fichier_bin = None
buffer = 0
nb_bits = 0

# Fonction permettant d'écrire (resp. lire) un entier c sur w bits dans un fichier binaire ouvert, sans écrire ni lire les bits un par un sur le disque (utiliser un tampon)
def ecrire_code(c, w):
    global buffer, nb_bits
    
    # Ajout des w bits du code dans le tampon
    buffer = (buffer << w) | c
    nb_bits += w
    
    # Écriture des octets complets dans le fichier
    while nb_bits >= 8:
        nb_bits -= 8
        octet = (buffer >> nb_bits) & 0xFF
        fichier_bin.write(bytes([octet]))
        
    # Nettoyage des bits déjà écrits
    buffer &= (1 << nb_bits) - 1


def lire_code(w):
    global buffer, nb_bits
    
    # Remplissage du tampon jusqu'à avoir au moins w bits
    while nb_bits < w:
        octet = fichier_bin.read(1)
        if not octet:
            return None
        buffer = (buffer << 8) | octet[0]
        nb_bits += 8
        
    # Extraction du code sur w bits et mise à jour du tampon
    nb_bits -= w
    code = (buffer >> nb_bits) & ((1 << w) - 1)
    buffer &= (1 << nb_bits) - 1
    return code
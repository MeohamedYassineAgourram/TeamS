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
# Écriture et lecture de codes de w bits dans un fichier binaire ouvert,
# en passant par un tampon (on n'écrit / lit jamais bit par bit sur le disque).

import os

TAILLE_BLOC = 4096  # nombre d'octets écrits ou lus sur le disque en une seule fois


class EcrivainBits:
    def __init__(self, fichier):
        self.fichier = fichier   # fichier déjà ouvert en mode 'wb'
        self.tampon = ""         # bits en attente, sous forme de '0' et '1'

    def ecrire_code(self, c, w):
        # On ajoute le code c, écrit sur exactement w bits, à la fin du tampon
        self.tampon += format(c, f"0{w}b")

        # Quand le tampon contient assez de bits, on écrit sur le disque
        # tous les octets complets, et on garde le reste (moins de 8 bits)
        if len(self.tampon) >= 8 * TAILLE_BLOC:
            self._vider_octets_complets()

    def _vider_octets_complets(self):
        nb_complets = len(self.tampon) // 8 * 8       # nombre de bits formant des octets entiers
        octets = bytearray()
        for i in range(0, nb_complets, 8):
            octets.append(int(self.tampon[i:i+8], 2))
        self.fichier.write(octets)
        self.tampon = self.tampon[nb_complets:]       # il reste au plus 7 bits

    def fermer(self):
        # Bourrage : on complète le dernier octet avec des '0'
        while len(self.tampon) % 8 != 0:
            self.tampon += "0"
        self._vider_octets_complets()


class LecteurBits:
    def __init__(self, fichier):
        self.fichier = fichier   # fichier déjà ouvert en mode 'rb'
        self.tampon = ""         # bits déjà lus sur le disque mais pas encore utilisés
        self.pos = 0             # position du prochain bit à lire dans le tampon
        # nombre de bits qu'il reste à lire dans le fichier (codes + bourrage)
        taille = os.path.getsize(fichier.name)
        self.restants = 8 * (taille - fichier.tell())

    def bits_restants(self):
        return self.restants

    def lire_code(self, w):
        if w > self.restants:
            raise EOFError("plus assez de bits dans le fichier")

        # S'il n'y a pas assez de bits dans le tampon, on lit un nouveau bloc
        # d'octets sur le disque et on le convertit en bits
        while len(self.tampon) - self.pos < w:
            bloc = self.fichier.read(TAILLE_BLOC)
            self.tampon = self.tampon[self.pos:] + "".join(f"{o:08b}" for o in bloc)
            self.pos = 0

        # On prend les w bits suivants et on les convertit en entier
        bits = self.tampon[self.pos:self.pos + w]
        self.pos += w
        self.restants -= w
        return int(bits, 2)

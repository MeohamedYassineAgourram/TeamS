# Compression LZMW

## 2 Questions théoriques

### Question 1 : algorithme de décompression LZMW
#### Notations
* F est le fichier compressé, de taille T octets (T ≥ 1, car il contient au moins l’en-tête).
* D est le dictionnaire. Le décompresseur l’utilise de deux façons :
    - **par code** : D[c] désigne le mot de code c ;
    - **par mot** : le test « u ∈ D » dit si le mot u est déjà une entrée (nécessaire pour détecter les doublons).
* |D| est le nombre d’entrées de D.
* R est le nombre de bits **encore non lus** dans F (en-tête exclu).
* lire(w) lit les w bits suivants de F (bit de poids fort en premier) et renvoie l’entier qu’ils représentent. On a alors R ← R − w.

#### Algorithme
**Algorithme 2 :** Décompression LZMW
**Entrée :** un fichier compressé `F`  
**Sortie :** le texte `t`

```text
 1: b ← premier octet de F                            # en-tête
 2: R ← 8 × (T − 1)                                   # nombre de bits après l'en-tête
 3: D ← les 256 octets, l'octet v ayant le code v     # |D| = 256
 4: P ← ε                                             # phrase précédente
 5: t ← ε                                             # texte reconstruit
 6: w ← ⌈log2 |D|⌉                                    # largeur du prochain code (= 8)
 7: tant que R ≥ w faire
 8:     c ← lire(w)                                   # R ← R − w
 9:     si c ≥ |D| alors erreur « fichier corrompu »  # n'arrive jamais (question 2)
10:     M ← D[c]
11:     t ← t · M                                     # écrire M
12:     si P ≠ ε et |D| < 2^b et P·M ∉ D alors
13:         ajouter P·M à D avec le code |D|
14:     fin si
15:     P ← M
16:     w ← ⌈log2 |D|⌉                                # largeur du code suivant
17: fin tant que
18: retourner t                                       # les R < w bits restants sont du bourrage
```

#### Déroulé sur la suite 0 1 2 2 2 0 4 0
On reprend l'exemple de la section 1.3 : alphabet {a, b} avec `code(a) = 0` et `code(b) = 1`, nouvelles entrées numérotées 2, 3, …, sans limite de taille. On part de la suite de codes déjà extraite (la lecture bit à bit est traitée juste après sur le vrai format).

**Dictionnaire initial :** D = {a:0, b:1}, \|D\| = 2, P = ε, t = ε.

| Étape | Code lu `c` | \|D\| avant | Phrase décodée `M = D[c]` | `P` (précédente) | `P·M` | Entrée ajoutée | Texte reconstruit `t` |
|:-----:|:-----------:|:-----------:|:-------------------------:|:----------------:|:-----:|:---------------|:----------------------|
| 1 | 0 | 2 | a    | ε    | —     | aucune (P = ε)                | a |
| 2 | 1 | 2 | b    | a    | ab    | ab : 2                        | ab |
| 3 | 2 | 3 | ab   | b    | bab   | bab : 3                       | abab |
| 4 | 2 | 4 | ab   | ab   | abab  | abab : 4                      | ababab |
| 5 | 2 | 5 | ab   | ab   | abab  | aucune (doublon : abab ∈ D)   | abababab |
| 6 | 0 | 5 | a    | ab   | aba   | aba : 5                       | ababababa |
| 7 | 4 | 6 | abab | a    | aabab | aabab : 6                     | ababababaabab |
| 8 | 0 | 7 | a    | abab | ababa | ababa : 7                     | ababababaababa |

**Résultat :** `t = ababababaababa` (14 caractères), soit le texte d'origine.
**Dictionnaire final :** {a:0, b:1, ab:2, bab:3, abab:4, aba:5, aabab:6, ababa:7}, identique à celui du compresseur (section 1.3).

#### Observations
- **Étape 5 :** le doublon est détecté, donc aucun code n'est consommé, et l'entrée suivante (aba, étape 6) reçoit bien le code 5, comme chez le compresseur.
- **Étape 7 :** le code 4 est lu alors que \|D\| = 6, donc 4 < \|D\| et l'entrée existe déjà (ajoutée à l'étape 4). À chaque étape, on vérifie que c < \|D\| : la ligne 9 n'est jamais déclenchée. C'est ce que la question 2 demande de démontrer en général.


### Question 02:

#### Partie 1 : le code lu figure toujours dans le dictionnaire

##### Notations
On note **Dⱼ** le dictionnaire du compresseur **au moment où il émet le j-ème code** (avant l’ajout éventuel de l’étape j), et **D′ⱼ** le dictionnaire du décompresseur **au moment où il lit le j-ème code**. On note `cⱼ = code(Mⱼ)` le **j-ème code**.

##### Deux remarques préliminaires
**(R1) Les codes d’un dictionnaire sont exactement 0, 1, …, |D| − 1**. Au départ, les codes sont 0 à 255 et |D| = 256. Ensuite, chaque ajout donne le code |D| à la nouvelle entrée, puis |D| augmente de 1. Un doublon ou un dictionnaire gelé ne crée aucune entrée et ne consomme aucun code. Les codes restent donc consécutifs, sans trou. Par conséquent, **« l’entrée de code c existe dans D » équivaut à « c < |D| »**.

**(R2) Le compresseur n’émet que des codes d’entrées existantes**. À la ligne 5, Mⱼ est choisi **parmi les entrées de Dⱼ**. Ce choix est toujours possible, puisque Dⱼ contient les 256 octets. Et l’émission (ligne 6) a lieu avant l’ajout (ligne 8). Donc Mⱼ ∈ Dⱼ, c’est-à-dire cⱼ < |Dⱼ|.

#### Énoncé à démontrer
```text
Propriété Q(j) : D′ⱼ = Dⱼ (mêmes mots avec les mêmes codes), et pour j ≥ 2, la phrase précédente P du décompresseur vaut Mⱼ₋₁.
```
Si Q(j) est vraie, alors d’après (R2), cⱼ est le code d’une entrée de Dⱼ = D′ⱼ. L’entrée de code cⱼ figure donc dans le dictionnaire du décompresseur, et c’est bien Mⱼ.

##### Preuve par récurrence sur j
**Initialisation (j = 1)**. D₁ et D′₁ contiennent tous les deux les 256 octets, l’octet v ayant le code v. Il n’y a pas de phrase précédente. Q(1) est vraie.

**Hérédité**. Supposons Q(j) vraie.
1. D’après (R2), cⱼ est le code de Mⱼ dans Dⱼ = D′ⱼ. Le décompresseur décode donc **la même phrase Mⱼ**.
2. Les deux algorithmes évaluent ensuite la **même condition** sur les **mêmes données** : P = Mⱼ₋₁ (ou ε si j = 1), M = Mⱼ et le même dictionnaire. La condition est « P ≠ ε et |D| < 2ᵇ et P·M ∉ D », avec la même valeur de b, que le décompresseur a lue dans l’en-tête.
    - Si elle est vraie, les deux ajoutent Mⱼ₋₁·Mⱼ avec le **même code |Dⱼ|** ;
    - sinon (première étape, doublon, ou dictionnaire gelé), **aucun des deux n’ajoute rien**.
3. Les deux font ensuite P ← Mⱼ.

Donc Dⱼ₊₁ = D′ⱼ₊₁, et la phrase précédente du décompresseur vaut Mⱼ : Q(j + 1) est vraie.

**Conclusion**. Q(j) est vraie pour tout j = 1, …, k. À chaque lecture, l’entrée de code c lue figure déjà dans le dictionnaire du décompresseur.

##### Cas du dictionnaire gelé
La preuve le couvre déjà : quand |D| = 2ᵇ, la condition |D| < 2ᵇ est fausse **des deux côtés**, donc aucun des deux ne modifie son dictionnaire. On a toujours Dⱼ = D′ⱼ, et comme Mⱼ est choisi dans ce dictionnaire gelé (R2), son code y figure.

L’entrée ajoutée à l’étape j, **Mⱼ₋₁·Mⱼ**, ne dépend **que des phrases déjà émise**s**. Le décompresseur la connaît donc entièrement **dès qu’il a décodé cⱼ**, et il peut faire l’ajout **à la même étape** que le compresseur. Son dictionnaire n’est **jamais en retard**.

##### Le cas de chevauchement de LZW.
En LZW, le compresseur ajoute wᵢ·x, où x est le caractère qui suit wᵢ, c’est-à-dire la première lettre de wᵢ₊₁. Le décompresseur ne connaît pas encore wᵢ₊₁ quand il lit le code i : il fait donc cet ajout avec une étape de retard.

Le problème arrive quand le compresseur utilise tout de suite l’entrée qu’il vient de créer : wᵢ = wᵢ₋₁·x. Le décompresseur reçoit alors un code qu’il n’a pas encore. Dans ce cas, x est aussi la première lettre de wᵢ₋₁. On a donc **wᵢ₋₁ = bw** et **wᵢ = bwb**, et le décompresseur reconstruit wᵢ = wᵢ₋₁ · première(wᵢ₋₁). Par exemple, dans l’exemple du cours (`T = ababcbababaaaaaa`), le code 8 arrive juste après `ba`, et on reconstruit `bab`.

##### Pourquoi LZMW n’a pas ce problème.
En LZW, l’entrée ajoutée dépend de la **phrase suivante**, pas encore lue par le décompresseur. En LZMW, l’entrée ajoutée Mⱼ₋₁·Mⱼ ne dépend que de **deux phrases déjà décodées**. Le décompresseur peut donc faire l’ajout à la même étape que le compresseur, sans retard. Le compresseur ne peut jamais émettre une entrée que le décompresseur ne connaît pas encore.

### Question 3
**Au départ**, le trie contient la racine et ses 256 fils (un par octet), soit **257 nœuds**.

**Les nœuds ne sont créés que lors des ajouts.** La recherche de la plus longue phrase ne fait que descendre dans le trie, sans rien créer. Un ajout consiste à descendre le long de P·M en créant les nœuds manquants.

**Ce qui se passe lors de l'ajout de P·M** (à l'étape j, avec P = Mⱼ₋₁ et M = Mⱼ) : P est une entrée du dictionnaire, puisqu'il a été lu comme phrase à l'étape précédente. Son nœud existe donc déjà dans le trie, et avec lui tout le chemin de la racine jusqu'à P. En descendant le long de P·M, les |P| premiers nœuds existent déjà, et seuls les nœuds correspondant aux lettres de M peuvent être nouveaux. **Un ajout crée donc au plus |Mⱼ| nœuds.**

Il n'y a pas d'ajout à la première étape, ni en cas de doublon ou de dictionnaire gelé. Le nombre total de nœuds créés est donc au plus :
|M₂| + |M₃| + ⋯ + |Mₖ| ≤ |M₁| + |M₂| + ⋯ + |Mₖ| = n
car les phrases découpent exactement le texte.

**Conclusion** : à la fin de la compression, le trie a au plus **n + 257 nœuds**, racine comprise.
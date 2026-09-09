# Deep Learning — TP ESPCI

Sept travaux pratiques de deep learning en PyTorch, réalisés à l'ESPCI Paris,
allant de la régression linéaire à la main jusqu'aux *neural operators* pour la
résolution d'EDP. Les notebooks ont été complétés, corrigés et commentés après
les séances : chaque section porte les résultats obtenus et leur interprétation.

---

## Les TP

| # | Notebook | Sujet | Notions clés |
|---|---|---|---|
| 01 | [Introduction à PyTorch](notebooks/01_intro_pytorch.py) | Tenseurs, autograd, régression linéaire et logistique | `backward()`, `Optimizer`, `Module`, BCE, mode batch vs stochastique |
| 02 | [MLP sur Fashion-MNIST](notebooks/02_mlp_fashion_mnist.py) | Réseaux feed-forward, classification d'images | Activations, momentum, BatchNorm, Dropout, overfitting, découpage train/valid/test |
| 03 | [CNN et convolutions 2D](notebooks/03_cnn_conv2d.py) | Classification d'images par convolutions | `Conv2d`, padding, MaxPool, champ receptif, VGG-16, data augmentation |
| 04 | [U-Net et segmentation](notebooks/04_unet_segmentation.py) | Segmentation de noyaux cellulaires | Encodeur/décodeur, `ConvTranspose2d`, skip connections, précision/rappel, IoU |
| 05 | [RNN, GRU et LSTM](notebooks/05_rnn_gru_lstm_meteo.py) | Prévision météo sur séries temporelles | Portes, BPTT, teacher forcing, rollout autorégressif, scheduled sampling |
| 06 | [Transformers — mini-GPT](notebooks/06_transformers_minigpt.py) | Modèle de langage causal *from scratch*, puis fine-tuning de GPT-2 | Self-attention, masque causal, multi-head, LayerNorm, tokenisation BPE, transfert |
| 07 | [Fourier Neural Operator](notebooks/07_fourier_neural_operator.py) | Résolution de l'équation de Darcy par apprentissage d'opérateur | FFT, troncature spectrale, invariance à la discrétisation, losses L2 et H1 |

### Fil conducteur

Les sept TP racontent une même histoire : **le bon modèle est celui dont
l'architecture encode les bonnes invariances du problème.**

| Structure du problème | Architecture | Invariance encodée |
|---|---|---|
| Aucune (vecteurs quelconques) | MLP | — |
| Voisinage local, motifs répétés | CNN | translation spatiale |
| Séquence ordonnée | RNN / GRU / LSTM | translation temporelle |
| Relations à longue portée | Transformer | permutation (+ positions ajoutées) |
| Fonction sur un domaine continu | FNO | discrétisation |

---

## Organisation du dépôt

```
notebooks/          les TP, au format .py (source de référence, lisible dans git)
notebooks/ipynb/    les mêmes TP au format .ipynb, générés — ouvrables dans Colab
tools/              utilitaires (conversion .py -> .ipynb, nettoyage)
```

Les fichiers `.py` sont la **source de référence** : ils se relisent et se
comparent proprement dans git, contrairement au JSON des `.ipynb`. Ils suivent
la convention d'export de Colab (les cellules Markdown sont des docstrings de
module), et les notebooks sont régénérés à la demande :

```bash
python tools/py2ipynb.py
```

## Exécuter les TP

Le plus simple est **Google Colab** : ouvrir un fichier de `notebooks/ipynb/`
via *Fichier > Importer un notebook*. Les TP 03 (VGG-16), 06 (fine-tuning de
GPT-2) et 07 (FNO) demandent un GPU ; les autres tournent sur CPU. Chaque
notebook télécharge lui-même ses données.

En local :

```bash
pip install -r requirements.txt
jupyter notebook notebooks/ipynb/
```

## Jeux de données

| TP | Jeu de données | Provenance |
|---|---|---|
| 02, 03 | Fashion-MNIST | téléchargé automatiquement (Google Drive) |
| 03 | CIFAR-10 | `torchvision.datasets` |
| 04 | Noyaux cellulaires en microscopie | [Kromp et al., *Scientific Data* 2020](https://www.nature.com/articles/s41597-020-00608-w) |
| 05 | SYNOP — relevés météo d'Orly, toutes les 3 h | [public.opendatasoft.com](https://public.opendatasoft.com/explore/dataset/donnees-synop-essentielles-omm/) |
| 06 | Tiny Shakespeare | [karpathy/char-rnn](https://github.com/karpathy/char-rnn) |
| 07 | Darcy Flow, Navier-Stokes 2D | `neuraloperator` |

Les données ne sont pas versionnées (voir `.gitignore`) : les notebooks les
récupèrent au premier lancement.

---

## Historique

Le premier commit contient les exports Colab **bruts**, tels que rendus pendant
les séances. Les commits suivants apportent les corrections et les sections
manquantes, ce qui permet de comparer les deux états :

```bash
git diff 97cc70e -- notebooks/
```

Quelques bugs relevés au passage, instructifs en eux-mêmes :

- **TP 04** — l'encodeur renvoyait les features *après* le max-pooling. Les skip
  connections ne pouvaient donc pas remplir leur rôle : elles existent
  précisément pour réinjecter les détails à pleine résolution.
- **TP 05** — `init_hidden` utilisait `input.dtype`, la fonction native de
  Python, au lieu de `inputs.dtype`. L'erreur passait inaperçue parce que
  `forward()` recréait l'état caché juste après.
- **TP 07** — `config["opt"]["training_loss"] == "l2"` : un `==` au lieu d'un
  `=`. La ligne ne modifiait rien, et **toutes les ablations L2 / H1 comparaient
  en réalité des modèles entraînés avec la même loss.** Un `=` n'aurait
  d'ailleurs pas suffi, la fonction d'entraînement lisant une variable globale
  et non le dictionnaire de configuration.

## Licence

Code sous licence MIT (voir [LICENSE](LICENSE)). Les énoncés et le texte des
sujets restent la propriété de leurs auteurs à l'ESPCI.

# Deep Learning — ESPCI Lab Assignments

Seven PyTorch deep learning labs completed at ESPCI Paris, running from linear
regression written by hand up to neural operators for solving PDEs. The
notebooks were completed, corrected and annotated after the sessions: every
section carries the results actually obtained and their interpretation.

---

## The labs

| # | Notebook | Topic | Key concepts |
|---|---|---|---|
| 01 | [Introduction to PyTorch](notebooks/01_intro_pytorch.py) | Tensors, autograd, linear and logistic regression | `backward()`, `Optimizer`, `Module`, BCE, batch vs stochastic mode |
| 02 | [MLP on Fashion-MNIST](notebooks/02_mlp_fashion_mnist.py) | Feed-forward networks, image classification | Activations, momentum, BatchNorm, Dropout, overfitting, train/valid/test split |
| 03 | [CNNs and 2D convolutions](notebooks/03_cnn_conv2d.py) | Image classification with convolutions | `Conv2d`, padding, MaxPool, receptive field, VGG-16, data augmentation |
| 04 | [U-Net and segmentation](notebooks/04_unet_segmentation.py) | Cell nucleus segmentation | Encoder/decoder, `ConvTranspose2d`, skip connections, precision/recall, IoU |
| 05 | [RNN, GRU and LSTM](notebooks/05_rnn_gru_lstm_meteo.py) | Weather forecasting on time series | Gates, BPTT, teacher forcing, autoregressive rollout, scheduled sampling |
| 06 | [Transformers — mini-GPT](notebooks/06_transformers_minigpt.py) | Causal language model from scratch, then GPT-2 fine-tuning | Self-attention, causal mask, multi-head, LayerNorm, BPE tokenisation, transfer |
| 07 | [Fourier Neural Operator](notebooks/07_fourier_neural_operator.py) | Solving the Darcy equation by operator learning | FFT, spectral truncation, discretisation invariance, L2 and H1 losses |

### The common thread

The seven labs tell a single story: **the right model is the one whose
architecture encodes the right invariances of the problem.**

| Problem structure | Architecture | Invariance encoded |
|---|---|---|
| None (arbitrary vectors) | MLP | — |
| Local neighbourhoods, repeated patterns | CNN | spatial translation |
| Ordered sequence | RNN / GRU / LSTM | temporal translation |
| Long-range relationships | Transformer | permutation (positions added back) |
| Function on a continuous domain | FNO | discretisation |

---

## Repository layout

```
notebooks/          the labs as .py files (reference source, readable in git)
notebooks/ipynb/    the same labs as generated .ipynb files — open them in Colab
tools/              utilities (.py -> .ipynb conversion, cleanup)
```

The `.py` files are the **reference source**: they read and diff cleanly in git,
unlike the JSON behind `.ipynb`. They follow the Colab export convention
(Markdown cells are module docstrings), and the notebooks are regenerated on
demand:

```bash
python tools/py2ipynb.py
```

## Running the labs

The simplest route is **Google Colab**: open a file from `notebooks/ipynb/` via
*File > Upload notebook*. Labs 03 (VGG-16), 06 (GPT-2 fine-tuning) and 07 (FNO)
need a GPU; the others run on CPU. Each notebook downloads its own data.

Locally:

```bash
pip install -r requirements.txt
jupyter notebook notebooks/ipynb/
```

## Datasets

| Lab | Dataset | Source |
|---|---|---|
| 02, 03 | Fashion-MNIST | downloaded automatically (Google Drive) |
| 03 | CIFAR-10 | `torchvision.datasets` |
| 04 | Cell nuclei in microscopy images | [Kromp et al., *Scientific Data* 2020](https://www.nature.com/articles/s41597-020-00608-w) |
| 05 | SYNOP — Orly weather records, every 3 h | [public.opendatasoft.com](https://public.opendatasoft.com/explore/dataset/donnees-synop-essentielles-omm/) |
| 06 | Tiny Shakespeare | [karpathy/char-rnn](https://github.com/karpathy/char-rnn) |
| 07 | Darcy Flow, 2D Navier-Stokes | `neuraloperator` |

Data is not versioned (see `.gitignore`): the notebooks fetch it on first run.

---

## License

Code released under the MIT license (see [LICENSE](LICENSE)). The problem
statements and assignment text remain the property of their authors at ESPCI.

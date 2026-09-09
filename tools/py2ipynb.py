"""Convertit les scripts Python au format Colab en vrais notebooks .ipynb.

Colab exporte un notebook en .py selon une convention simple :
  - les cellules Markdown deviennent des docstrings de module au niveau 0
    (delimitees par trois guillemets en debut de ligne, parfois prefixees r/f) ;
  - tout le reste est du code, decoupe en cellules par les lignes vides
    separant les blocs.

Ce script fait le chemin inverse. Les .py restent la source de reference
(lisibles, diffables dans git) et les .ipynb sont regeneres a la demande, ce
qui evite de versionner des sorties d'execution et des metadonnees bruyantes.

Usage :
    python tools/py2ipynb.py                  # notebooks/*.py -> notebooks/ipynb/
    python tools/py2ipynb.py fichier.py       # un seul fichier
"""

import io
import json
import re
import sys
from pathlib import Path

DEBUT_DOCSTRING = re.compile(r'^([rfRFbB]{0,2})("""|\'\'\')')


def decouper_en_cellules(source):
    """Renvoie une liste de tuples (type, texte) avec type dans {markdown, code}."""
    lignes = source.split("\n")
    cellules = []
    tampon_code = []
    i = 0

    def vider_code():
        texte = "\n".join(tampon_code).strip("\n")
        if texte.strip():
            cellules.append(("code", texte))
        tampon_code.clear()

    while i < len(lignes):
        ligne = lignes[i]
        m = DEBUT_DOCSTRING.match(ligne)
        if m:
            quote = m.group(2)
            vider_code()
            reste = ligne[m.end():]
            # docstring sur une seule ligne ?
            if quote in reste:
                cellules.append(("markdown", reste[:reste.index(quote)]))
                i += 1
                continue
            contenu = [reste]
            i += 1
            while i < len(lignes) and quote not in lignes[i]:
                contenu.append(lignes[i])
                i += 1
            if i < len(lignes):
                fin = lignes[i]
                contenu.append(fin[:fin.index(quote)])
                i += 1
            cellules.append(("markdown", "\n".join(contenu).strip("\n")))
        else:
            tampon_code.append(ligne)
            i += 1
    vider_code()

    # On decoupe les gros blocs de code sur les lignes vides doubles, pour
    # retrouver un decoupage en cellules proche de l'original.
    finales = []
    for typ, texte in cellules:
        if typ == "markdown":
            finales.append((typ, texte))
            continue
        for morceau in re.split(r"\n\s*\n\s*\n+", texte):
            if morceau.strip():
                finales.append(("code", morceau.strip("\n")))
    return finales


def en_lignes(texte):
    """Format attendu par nbformat : liste de lignes avec le \\n conserve."""
    lignes = texte.split("\n")
    return [l + "\n" for l in lignes[:-1]] + [lignes[-1]]


def convertir(chemin_py, chemin_ipynb):
    source = io.open(chemin_py, encoding="utf-8").read()

    # On retire l'en-tete technique genere par Colab (coding + titre + lien)
    source = re.sub(r"^# -\*- coding: utf-8 -\*-\n", "", source)

    cellules = []
    for typ, texte in decouper_en_cellules(source):
        if typ == "markdown":
            cellules.append({
                "cell_type": "markdown",
                "metadata": {},
                "source": en_lignes(texte),
            })
        else:
            cellules.append({
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": en_lignes(texte),
            })

    notebook = {
        "cells": cellules,
        "metadata": {
            "colab": {"provenance": [], "toc_visible": True},
            "kernelspec": {"display_name": "Python 3", "name": "python3"},
            "language_info": {"name": "python"},
        },
        "nbformat": 4,
        "nbformat_minor": 0,
    }

    chemin_ipynb.parent.mkdir(parents=True, exist_ok=True)
    io.open(chemin_ipynb, "w", encoding="utf-8", newline="").write(
        json.dumps(notebook, ensure_ascii=False, indent=1)
    )
    n_md = sum(1 for c in cellules if c["cell_type"] == "markdown")
    n_code = len(cellules) - n_md
    return n_md, n_code


def main(argv):
    if argv:
        sources = [Path(a) for a in argv]
    else:
        sources = sorted(Path("notebooks").glob("*.py"))

    sortie = Path("notebooks") / "ipynb"
    for src in sources:
        dst = sortie / (src.stem + ".ipynb")
        n_md, n_code = convertir(src, dst)
        print(f"{src.name:35s} -> {dst.name:35s} "
              f"({n_md} cellules markdown, {n_code} cellules code)")


if __name__ == "__main__":
    main(sys.argv[1:])

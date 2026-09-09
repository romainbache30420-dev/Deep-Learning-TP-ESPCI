"""Prefixe d'un `r` les cellules Markdown contenant des antislashs.

Les notebooks exportes par Colab stockent les cellules Markdown dans des
docstrings de module. Quand une cellule contient du LaTeX (`\\frac`, `\\sum`,
`\\sigma`...), Python voit des sequences d'echappement invalides et emet un
SyntaxWarning ("invalid escape sequence"). Depuis Python 3.12 c'est un
avertissement, et ce sera une erreur dans une version future.

La correction est indolore : transformer la docstring en chaine brute, en la
prefixant d'un `r`, ce qui laisse les antislashs tels quels. Le contenu
Markdown est inchange.

Usage :
    python tools/fix_docstrings.py notebooks/*.py
"""

import io
import re
import sys
from pathlib import Path


def corriger(chemin: Path) -> int:
    source = io.open(chemin, encoding="utf-8").read()
    lignes = source.split("\n")

    dans_docstring = False
    debut = 0
    a_prefixer = []

    for i, ligne in enumerate(lignes):
        if not dans_docstring:
            # Une cellule Markdown commence par """ en debut de ligne,
            # eventuellement deja prefixe par r/f.
            if re.match(r'^[rf]?"""', ligne):
                # cas d'une docstring tenant sur une seule ligne
                if ligne.count('"""') >= 2:
                    if "\\" in ligne and not ligne.startswith("r"):
                        a_prefixer.append(i)
                    continue
                dans_docstring = True
                debut = i
        else:
            if '"""' in ligne:
                dans_docstring = False
                bloc = "\n".join(lignes[debut:i + 1])
                if "\\" in bloc and not lignes[debut].startswith("r"):
                    a_prefixer.append(debut)

    for i in a_prefixer:
        lignes[i] = "r" + lignes[i]

    if a_prefixer:
        io.open(chemin, "w", encoding="utf-8", newline="").write("\n".join(lignes))
    return len(a_prefixer)


def main(argv):
    cibles = [Path(a) for a in argv] or sorted(Path("notebooks").glob("*.py"))
    total = 0
    for chemin in cibles:
        n = corriger(chemin)
        total += n
        print(f"{chemin.name:35s} : {n} cellule(s) passee(s) en raw string")
    print(f"total : {total}")


if __name__ == "__main__":
    main(sys.argv[1:])

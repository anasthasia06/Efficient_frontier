# Efficient_Frontier_Fr

Sous-projet pour produire une version française (LaTeX) du document de cours présent dans `../prog_finance.pdf`, avec exemples chiffrés, figure de frontière efficiente et tableau de poids générés par script Python.

## Structure
- `tex/prog_finance_fr.tex`: document LaTeX principal à compiler en PDF.
- `scripts/compute_frontier.py`: génère la figure et le tableau CSV intégrés au PDF.
- `scripts/extract_text.sh`: extraction brute du texte depuis le PDF source (optionnelle).
- `build/`: répertoire de sortie (PDF, images, CSV).
- `requirements.txt`: dépendances Python (si vous exécutez le script).

## Prérequis
- Linux, Make, distribution LaTeX (Tex Live recommandé)
- Optionnel (texte): `poppler-utils` pour `pdftotext`
- Optionnel (figures/tableaux): Python 3.10+, `numpy`, `matplotlib`

Installation rapide (Debian/Ubuntu):
```bash
sudo apt-get update
sudo apt-get install -y make texlive-latex-recommended texlive-latex-extra texlive-fonts-recommended texlive-xetex
# Optionnel (extraction texte)
sudo apt-get install -y poppler-utils
# Optionnel (figure/CSV)
sudo apt-get install -y python3-venv python3-pip
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

## Générer la figure et le tableau (optionnel mais recommandé)
```bash
cd Efficient_Frontier_Fr
python3 scripts/compute_frontier.py
```
Cela crée:
- `build/frontier_plot.pdf`: figure de la frontière efficiente
- `build/frontier_table.csv`: tableau des poids et statistiques pour quelques cibles

## Construire le PDF
```bash
cd Efficient_Frontier_Fr
make pdf            # par défaut pdflatex (latexmk si dispo)
# ou
make pdf ENGINE=xelatex
```
Sortie attendue: `build/prog_finance_fr.pdf`.

## Nettoyage
```bash
make clean      # supprime les artefacts LaTeX
make distclean  # supprime aussi le PDF généré
```

## Notes
- Le PDF source `../prog_finance.pdf` n’est pas modifié.
- La figure et le tableau sont basés sur un petit exemple synthétique (3 actifs) aligné avec le contenu du document.


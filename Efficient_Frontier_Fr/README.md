# Efficient_Frontier_Fr

Sous-projet pour produire une version française (LaTeX) du document de cours présent dans `../prog_finance.pdf`.

## Structure
- `tex/prog_finance_fr.tex`: document LaTeX principal à compiler en PDF.
- `scripts/extract_text.sh`: extraction brute du texte depuis le PDF source (optionnelle, pour faciliter la traduction).
- `data/`: contiendra le texte extrait (`prog_finance_raw.txt`).
- `build/`: répertoire de sortie des PDF et artefacts (généré par `make`).

Le PDF source n'est pas modifié, conformément aux règles du dépôt.

## Prérequis
- Linux, Make
- Une distribution LaTeX (Tex Live recommandé)
- Optionnel: `poppler-utils` pour `pdftotext` (extraction du texte)

Installation rapide sur Debian/Ubuntu:
```bash
sudo apt-get update
sudo apt-get install -y make texlive-latex-recommended texlive-latex-extra texlive-fonts-recommended
# Optionnel (extraction texte)
sudo apt-get install -y poppler-utils
```

## Construire le PDF
Depuis ce dossier:
```bash
make pdf
```
- Le PDF sera généré dans `build/prog_finance_fr.pdf`.
- Vous pouvez forcer un moteur LaTeX différent (ex: `xelatex`):
```bash
make pdf ENGINE=xelatex
```

## Extraire le texte du PDF (optionnel)
Cela peut aider à préparer la traduction (vous réorganisez ensuite le texte dans le LaTeX).
```bash
./scripts/extract_text.sh
```
Le fichier `data/prog_finance_raw.txt` sera créé si `pdftotext` est disponible.

## Notes de traduction
- Ce projet fournit une **synthèse/traduction en français** fidèle aux concepts du PDF source, sans reproduire littéralement l'intégralité du contenu.
- Si vous souhaitez une traduction plus exhaustive, copiez/collez des sections pertinentes dans `tex/prog_finance_fr.tex` et reformulez en français.
- Citez les passages ou figures en renvoyant au PDF source `../prog_finance.pdf`.

## Nettoyage
```bash
make clean      # supprime les artefacts LaTeX
make distclean  # supprime aussi le PDF généré
```

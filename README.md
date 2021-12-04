# recipes.rixx.de

Meine Rezeptesammlung. Derzeit noch nicht auf der namensgebenden Website zu finden.

Nutzt [recipe.md](https://recipemd.org/index.html).

## Rezepte lesen

Einfach hier auf GitHub in die Ordner gehen und Dateien anklicken. Zum Suchen einfach `t` drücken.

## Rezepte anlegen


## Sonstiges

**Einen Ordner in PDFs umwandeln**

```
ls *.md | xargs -P10 -I{} bash -c 'pandoc --pdf-engine=xelatex  -V geometry:margin=2cm -V geometry:a4paper {} -o $(basename {} md)pdf'
```

**Ein Rezept aus dem Internet laden**

```
recipemd-extract 'url-of-recipe'  # chefkoch, seriouseats
```

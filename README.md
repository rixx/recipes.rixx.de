# recipes.rixx.de

Meine Rezeptesammlung. In hübsch auf [recipes.rixx.de](https://recipes.rixx.de) zu finden.

Nutzt [recipe.md](https://recipemd.org/index.html).

## Rezepte lesen

Einfach hier auf GitHub in die Ordner gehen und Dateien anklicken. Zum Suchen einfach `t` drücken.

## Rezepte anlegen

Das Template kopieren oder aus dem Internet laden:

```
cp scripts/template.md gebaeck/coole-kekse.md
recipemd-extract 'url-of-recipe'  # chefkoch, seriouseats
```

## Seite rendern

Einmalig alle nötigen Pakete installieren, dann einfach ``recipes build`` ausführen.

```
[uv] pip install -Ue .
[uv run] recipes build
```

## Bilder herunterladen

Bilder werden anhand des Dateinamen zugeordnet, zu `griessbrei.md` gehören `griessbrei-00.jpg` bis `griessbrei-99.jpg`.
Das erste Bild wird dabei als Titelbild verwendet. Bilder einfach hinkopieren, oder mit dem Tool laden, wenn du einen
Link hast:

```
recipes edit
[?] What's the recipe called?:  kuch
[?] Found 4 recipes. Which one did you mean?: Pfefferkuchen (gebaeck)
 > Pfefferkuchen (gebaeck)
   Löffelbiskuitkuchen (kuchen)
   Schokoladenstreuselkuchen (kuchen)
   Rhabarberkuchen mit Vanillecreme & Streuseln (kuchen)
   Try a different search
[?] What do you want to do with this report?: Download an image
   Edit
 > Download an image
   Quit
```

## Deployment

```
./update.sh
```

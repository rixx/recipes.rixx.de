import glob
import os
import re
import shutil
import subprocess
from functools import cached_property
from pathlib import Path
from urllib.request import urlretrieve

import click
import inquirer
from recipemd.data import RecipeParser
from unidecode import unidecode


def slugify(text):
    """Convert Unicode string into blog slug."""
    # https://leancrew.com/all-this/2014/10/asciifying/
    text = re.sub("[–—/:;,.]", "-", text)  # replace separating punctuation
    ascii_text = unidecode(text).lower()  # best ASCII substitutions, lowercased
    ascii_text = re.sub(r"[^a-z0-9 -]", "", ascii_text)  # delete any other characters
    ascii_text = ascii_text.replace(" ", "-")  # spaces to hyphens
    ascii_text = re.sub(r"-+", "-", ascii_text)  # condense repeated hyphens
    return ascii_text


def get_yesno(prompt, default=True):
    return inquirer.list_input(
        message=prompt,
        choices=[("Yes", True), ("No", False)],
        default=default,
        carousel=True,
    )


class Recipe:
    def __init__(self, path):
        self.path = Path(path)
        self._load_data_from_file()

    def __str__(self):
        if self.path:
            return f"Report(path={self.path})"
        return "Report(path=None)"

    def __repr__(self):
        return str(self)

    def _load_data_from_file(self):
        try:
            self.data = RecipeParser().parse(open(self.path).read())
        except Exception as e:
            raise Exception(f"Cannot read {self.path}: {e}")
        self.title = self.data.title
        self.entry_type = self.entry_type_from_path()

    def entry_type_from_path(self):
        return Path(self.path).parent.name

    @cached_property
    def slug(self):
        if self.path:
            return self.path.stem
        return slugify(self.metadata["location"]["name"])

    @cached_property
    def id(self):
        return Path(self.entry_type) / self.slug

    @cached_property
    def image_paths(self):
        return list(self.id.glob("*.jpg"))

    def edit(self):
        subprocess.check_call([os.environ.get("EDITOR", "vim"), self.path])
        self._load_data_from_file()

    def show_images(self):
        subprocess.check_call(["feh", Path(self.entry_type) / self.slug + "*"])

    def download_image(self):
        url = inquirer.text(message="URL")
        filename, headers = urlretrieve(url)
        extension = {"image/jpeg": "jpg", "image/png": "png", "image/gif": "gif"}[
            headers["Content-Type"]
        ]
        for num in range(99):
            destination = self.path.parent / f"{self.slug}-{num:02}.jpg"
            if not destination.exists():
                break

        if extension == "jpg":
            shutil.move(filename, destination)
        else:
            subprocess.check_call(["convert", filename, destination])

        self.show_images()


def load_recipes():
    for path in Path(".").rglob("**/*.md"):
        if path.parent.name != Path(".").name:
            try:
                yield Recipe(path=path)
            except Exception as e:
                print(f"Error loading {path}")
                raise e


def create_recipe():
    title = (inquirer.text("title", message="What’s the title of the recipe?"),)
    entry_type = inquirer.list_input(
        message="What kind of recipe is this?",
        choices=[
            "dips",
            "einkochen",
            "gebaeck",
            "hauptspeisen",
            "kuchen",
            "scripts",
            "snacks",
            "suessspeisen",
            "vorspeisen",
        ],
    )
    title = slugify(title)

    path = Path(entry_type) / (title + ".md")
    subprocess.check_call(["cp", "scripts/template.md", path])

    recipe = Recipe(path=path)
    recipe.edit()

    if get_yesno("Add an image?"):
        recipe.download_image()


def get_recipe_from_user():
    while True:
        original_search = inquirer.text(message="What's the recipe called?")
        search = original_search.strip().lower().replace(" ", "-")
        files = list(glob.glob(f"**/*{search}*.md"))
        if len(files) == 0:
            click.echo(click.style("No recipe like that was found.", fg="red"))
            continue

        recipes = [Recipe(path=path) for path in files]
        options = [
            (
                f"{recipe.title} ({recipe.entry_type})",
                recipe,
            )
            for recipe in recipes
        ]
        options += [("Try a different search", "again")]
        choice = inquirer.list_input(
            f"Found {len(recipes)} recipes. Which one did you mean?",
            choices=options,
            carousel=True,
        )
        if choice == "again":
            continue
        return choice


def change_recipe():
    report = get_recipe_from_user()
    while True:
        action = inquirer.list_input(
            message="What do you want to do with this report?",
            choices=[
                ("Edit", "edit"),
                ("Download an image", "image"),
                ("Quit", "quit"),
            ],
            carousel=True,
        )
        if action == "quit":
            return
        if action == "edit":
            report.edit()
        elif action == "image":
            report.download_image()

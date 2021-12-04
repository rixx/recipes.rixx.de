import sys

import click
import inquirer

from .recipes import change_recipe, create_recipe
from .renderer import build_site


@click.group(invoke_without_command=True)
@click.version_option()
def cli(*lol, **trololol):
    "Interact with the data fueling recipes.rixx.de"
    if len(sys.argv) > 1:
        return
    inquirer.list_input(
        message="What do you want to do?",
        choices=(
            ("Create a new recipe", create_recipe),
            ("Edit an existing recipe", change_recipe),
            ("Build the site", build_site),
        ),
        carousel=True,
    )()


@cli.command()
def build():
    """Build the site, putting output into _html/"""
    build_site()


@cli.command()
def new():
    """Add a new recipe"""
    create_recipe()


@cli.command()
def add():
    """Add a new recipe"""
    create_recipe()


@cli.command()
def edit():
    """Edit a recipe"""
    change_recipe()

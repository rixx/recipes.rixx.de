import datetime as dt
import pathlib
import random
import subprocess
from collections import defaultdict
from functools import partial
from pathlib import Path

import markdown
import smartypants
from jinja2 import Environment, FileSystemLoader, select_autoescape
from markdown.extensions.smarty import SmartyExtension
from PIL import Image

from . import recipes


def rsync(source, destination):
    subprocess.check_call(["rsync", "--recursive", "--delete", source, destination])


def render_markdown(text):
    return markdown.markdown(text, extensions=[SmartyExtension()])


def render_date(date_value):
    if isinstance(date_value, dt.date):
        return date_value.strftime("%Y-%m-%d")
    return date_value


def render_page(template_name, path, env=None, **context):
    template = env.get_template(template_name)
    html = template.render(**context)
    out_path = pathlib.Path("_html") / path
    out_path.parent.mkdir(exist_ok=True, parents=True)
    out_path.write_text(html)


def _create_new_thumbnail(src_path, dst_path):
    im = Image.open(src_path)

    if im.width > 240 and im.height > 240:
        im.thumbnail((240, 240))
    im.save(dst_path)


def _create_new_square(src_path, square_path):
    square_path.parent.mkdir(exist_ok=True, parents=True)

    im = Image.open(src_path)
    im.thumbnail((240, 240))

    dimension = max(im.size)

    new = Image.new("RGB", size=(dimension, dimension), color=(255, 255, 255))

    if im.height > im.width:
        new.paste(im, box=((dimension - im.width) // 2, 0))
    else:
        new.paste(im, box=(0, (dimension - im.height) // 2))

    new.save(square_path)


def create_thumbnail(image, path):
    thumbnail_path = path / f"thumbnail_{image.name}"
    square_path = path / f"square_{image.name}"
    image_path = path / image.name

    if not image_path.exists() or image.stat().st_mtime > image_path.stat().st_mtime:
        rsync(image, image_path)
        _create_new_thumbnail(image, thumbnail_path)
        _create_new_square(image, square_path)


def build_site(**kwargs):
    print("✨ Starting to build the site … ✨")
    env = Environment(
        loader=FileSystemLoader("templates"),
        autoescape=select_autoescape(["html", "xml"]),
    )
    env.filters["render_markdown"] = render_markdown
    env.filters["render_date"] = render_date
    env.filters["smartypants"] = smartypants.smartypants
    render = partial(render_page, env=env)

    print("📔 Loading recipes from files")
    all_recipes = sorted(
        list(recipes.load_recipes()), key=lambda x: len(x.image_paths), reverse=True
    )
    html_path = pathlib.Path("_html")

    tags = defaultdict(list)
    categories = defaultdict(list)

    print("🖋 Rendering ecipe pages")
    for recipe in all_recipes:
        render(
            "recipe.html",
            Path(recipe.id) / "index.html",
            recipe=recipe,
            title=recipe.title,
        )
        categories[recipe.entry_type].append(recipe)
        for tag in recipe.data.tags:
            tags[tag].append(recipe)

    print("🔎 Rendering list pages")
    render(
        "index.html",
        "index.html",
        title="Rezepte",
        categories=categories,
        recipes=all_recipes,
        sorted_tags=sorted(list(tags.keys()), key=lambda x: len(tags[x]), reverse=True),
        sorted_categories=sorted(
            list(categories.keys()), key=lambda x: sum(bool(r.image_paths) for r in categories[x]), reverse=True
        ),
        tags=tags,
    )
    render(
        "pics.html",
        "pics/index.html",
        title="Galerie",
        recipes=all_recipes,
    )
    for tag, tagged_recipes in tags.items():
        render(
            "tag.html",
            f"t/{tag}/index.html",
            title=tag,
            tag=tag,
            recipes=tagged_recipes,
        )
    for category, tagged_recipes in categories.items():
        render(
            "category.html",
            f"c/{category}/index.html",
            title=category,
            category=category,
            recipes=tagged_recipes,
        )

    images = []
    print("📷 Generating thumbnails")
    for recipe in all_recipes:
        for image in recipe.image_paths:
            create_thumbnail(image, html_path / recipe.id)
            images.append((image, recipe))

    random.shuffle(images)

    render(
        "pics.html",
        "pics/index.html",
        title="Fotos",
        images=images,
    )

    rsync(source="static/", destination="_html/static/")

    print("✨ Rendered HTML files to _html ✨")

import os
from .template import container, mimetype


def join_path(*args):
    return '/'.join(args)


def set_epub_cache_file(epub_dir: str):
    if not os.path.isdir(epub_dir):
        os.makedirs(epub_dir)

    with open(join_path(epub_dir, 'mimetype'), 'w') as f:
        f.write(mimetype)

    if not os.path.exists(join_path(epub_dir, 'META-INF')):
        os.makedirs(join_path(epub_dir, 'META-INF'))
        with open(join_path(epub_dir, 'META-INF', 'container.xml'), 'w') as f:
            f.write(container)

    if not os.path.exists(join_path(epub_dir, 'OEBPS')):
        os.makedirs(join_path(epub_dir, 'OEBPS'))
    if not os.path.exists(join_path(epub_dir, 'OEBPS', 'Text')):
        os.makedirs(join_path(epub_dir, 'OEBPS', 'Text'))

    if not os.path.exists(join_path(epub_dir, 'OEBPS', 'Images')):
        os.makedirs(join_path(epub_dir, 'OEBPS', 'Images'))

    if not os.path.exists(join_path(epub_dir, 'OEBPS', 'Styles')):
        os.makedirs(join_path(epub_dir, 'OEBPS', 'Styles'))

    with open(join_path(epub_dir, 'mimetype'), 'w') as f:
        f.write(mimetype)

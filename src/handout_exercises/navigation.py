import os


def add_path_pages_for_item(item, path2page):
    if hasattr(item, 'file'):
        src_path = item.file.src_path
        parent_path = os.path.split(src_path)[0]
        path2page[parent_path] = item.parent
    if item.children:
        for child in item.children:
            add_path_pages_for_item(child, path2page)


def make_path_page_dict(nav, path2page=None):
    path2page = {}
    for item in nav.items:
        add_path_pages_for_item(item, path2page)
    return path2page


def find_parent(src_path, path2page):
    if not src_path:
        return None

    if src_path in path2page:
        return path2page[src_path]
    parent_path = os.path.split(src_path)[0]
    return find_parent(parent_path, path2page)


def add_missing_nav_parents(nav, files):
    path2page = make_path_page_dict(nav)

    # Add navigation to files not listed in the config
    for file in files:
        if not file.page:
            continue
        page = file.page
        parent = page.parent
        if parent:
            continue

        page.parent = find_parent(file.src_path, path2page)
    return nav

from pathlib import Path


def load_local_file(local_filename, reference_page, files):
    if not local_filename:
        return None
    page_dir = Path(reference_page.file.src_path).parent
    file_path = files.get_file_from_path(page_dir / local_filename)
    with open(file_path.abs_src_path) as f:
        return f.read()

import os

from pytest_bdd import given, parsers


@given(parsers.parse("a file at '{path}' with content\n{content}"))
def file_with_content(data_dir, path, content):
    full_path = os.path.join(data_dir, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w") as f:
        f.write(content)

import os

from pytest_bdd import parsers, then


@then("the source file in the response was created")
def the_source_file_in_the_response_was_created(response, data_dir):
    source_id = response.json()["id"]
    path = os.path.join(data_dir, "sources", source_id)
    assert os.path.exists(path)


@then(parsers.parse("the sources folder contains exactly {count} file(s)"))
def the_sources_folder_contains_exactly_count_files(data_dir, count):
    path = os.path.join(data_dir, "sources")
    assert len(os.listdir(path)) == int(count)

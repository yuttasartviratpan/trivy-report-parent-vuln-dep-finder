import trivy_script_project


def test_sanity():
    assert 1 + 1 == 2


def test_add():
    assert trivy_script_project.add_numbers(1, 2) == 3

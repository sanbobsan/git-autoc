from git_autoc.prompt.template import (
    Block,
    Template,
)


def test_get_blocks_extracts_all_types():
    """Verify that both parameterized and parameterless blocks are extracted correctly."""
    raw_template = "Hello {user}, you have {commits:5} and {commits:4}."
    template = Template(raw_template)

    blocks = template.get_blocks()

    assert blocks == [
        Block(name="user", param=None),
        Block(name="commits", param="5"),
        Block(name="commits", param="4"),
    ]


def test_get_blocks_empty_template():
    """Verify that get_blocks returns an empty list for an empty template string."""
    template = Template("")
    assert template.get_blocks() == []


def test_render_successful_substitution():
    """Verify successful substitution of different values for identical block names with distinct parameters."""
    raw_template = "Stats: {commits:5} vs {commits:4} for {user}."
    template = Template(raw_template)

    values = {
        Block("commits", "5"): "five commits",
        Block("commits", "4"): "four commits",
        Block("user"): "Alex",
    }

    result = template.render(values)

    assert result == "Stats: five commits vs four commits for Alex."
    assert (
        template.complete_template
        == "Stats: five commits vs four commits for Alex."
    )


def test_render_leaves_missing_blocks_as_is():
    """Verify that blocks without matching values in the dict remain unchanged in the output."""
    raw_template = "Keep {missing} and {commits:5}."
    template = Template(raw_template)

    values = {Block("commits", "5"): "five"}

    result = template.render(values)

    assert result == "Keep {missing} and five."


def test_render_exact_match_required():
    """Verify that a parameterized block (e.g., {commits:5}) is not substituted by a default Block('commits', None)."""
    raw_template = "Result: {commits:5}."
    template = Template(raw_template)

    # The dictionary only contains a base block without parameters
    values = {Block("commits"): "default"}

    result = template.render(values)

    # Since there is no exact match for param "5", the block must remain intact
    assert result == "Result: {commits:5}."

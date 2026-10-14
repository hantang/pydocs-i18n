from mkdocs.commands.build import build
from mkdocs.config.base import load_config

from mkdocs_static_i18n.reconfigure import _search_index_of


def _material_search_config():
    """
    mkdocs-materialx (>= 10) delegates search to a provider and needs
    `provider: lunr` for an in-process index; mkdocs-material (9.x) has no such
    option. Build whatever the installed material package understands.
    """
    try:
        from material.plugins.search.config import SearchConfig
    except ImportError:
        return {}
    if any(name == "provider" for name, _ in SearchConfig._schema):
        return {"provider": "lunr"}
    return {}


def test_search_index_of():
    class Index:
        pass

    class Direct:
        """MkDocs/properdocs built-in search plugin layout."""

        def __init__(self, search_index):
            self.search_index = search_index

    class Provider:
        """mkdocs-material/materialx >= 9.0 provider layout."""

        def __init__(self, search_index):
            self.provider = type("Provider", (), {"search_index": search_index})()

    assert isinstance(_search_index_of(Direct(Index())), Index)
    assert isinstance(_search_index_of(Provider(Index())), Index)
    # mkdocs-material's default "pagefind" provider keeps no in-process index
    assert _search_index_of(Provider(None)) is None
    assert _search_index_of(type("NoIndex", (), {})()) is None


def test_search_entries():
    for theme in ["mkdocs", "material"]:
        search_config = _material_search_config() if theme == "material" else {}
        mkdocs_config = load_config(
            "tests/mkdocs.yml",
            theme={"name": theme},
            use_directory_urls=True,
            docs_dir="docs_suffix_structure_two_languages/",
            plugins={
                "search": search_config,
                "i18n": {
                    "languages": [
                        {
                            "locale": "en",
                            "name": "english",
                            "default": True,
                        },
                        {"locale": "fr", "name": "français"},
                    ],
                },
            },
        )
        if theme == "material":
            mkdocs_config["plugins"]["material/search"].on_startup(command=None, dirty=False)
        build(mkdocs_config)
        if theme == "mkdocs":
            search_index = _search_index_of(mkdocs_config["plugins"]["search"])
            assert len(search_index._entries) == 36
        else:
            search_index = _search_index_of(mkdocs_config["plugins"]["material/search"])
            assert len(search_index.entries) == 26


def test_search_entries_no_directory_urls():
    mkdocs_config = load_config(
        "tests/mkdocs.yml",
        theme={"name": "mkdocs"},
        use_directory_urls=False,
        docs_dir="docs_suffix_structure_two_languages/",
        plugins={
            "search": {},
            "i18n": {
                "languages": [
                    {
                        "locale": "en",
                        "name": "english",
                        "default": True,
                    },
                    {"locale": "fr", "name": "français"},
                ],
            },
        },
    )
    build(mkdocs_config)
    search_plugin = mkdocs_config["plugins"]["search"]
    assert len(search_plugin.search_index._entries) == 36


def test_search_entries_no_reconfigure():
    mkdocs_config = load_config(
        "tests/mkdocs.yml",
        theme={"name": "mkdocs"},
        use_directory_urls=True,
        docs_dir="docs_suffix_structure_two_languages/",
        plugins={
            "search": {},
            "i18n": {
                "reconfigure_search": False,
                "languages": [
                    {
                        "locale": "en",
                        "name": "english",
                        "default": True,
                    },
                    {"locale": "fr", "name": "français"},
                ],
            },
        },
    )
    build(mkdocs_config)
    search_plugin = mkdocs_config["plugins"]["search"]
    assert len(search_plugin.search_index._entries) == 40


def test_search_add_lang():
    mkdocs_config = load_config(
        "tests/mkdocs.yml",
        theme={"name": "mkdocs"},
        use_directory_urls=True,
        docs_dir="docs_suffix_structure_two_languages/",
        plugins={
            "search": {},
            "i18n": {
                "languages": [
                    {
                        "locale": "en",
                        "name": "english",
                        "default": True,
                    },
                    {"locale": "fr", "name": "français"},
                ],
            },
        },
    )
    build(mkdocs_config)
    search_plugin = mkdocs_config["plugins"]["search"]
    assert search_plugin.config["lang"] == ["en", "fr"]


def test_search_add_missing_lang():
    mkdocs_config = load_config(
        "tests/mkdocs.yml",
        theme={"name": "mkdocs"},
        use_directory_urls=True,
        docs_dir="docs_suffix_structure_two_languages/",
        plugins={
            "search": {
                "lang": ["en"],
            },
            "i18n": {
                "reconfigure_search": True,
                "languages": [
                    {
                        "locale": "en",
                        "name": "english",
                        "default": True,
                    },
                    {"locale": "fr", "name": "français"},
                ],
            },
        },
    )
    build(mkdocs_config)
    search_plugin = mkdocs_config["plugins"]["search"]
    assert search_plugin.config["lang"] == ["en", "fr"]


def test_search_no_add_lang():
    mkdocs_config = load_config(
        "tests/mkdocs.yml",
        theme={"name": "mkdocs"},
        use_directory_urls=True,
        docs_dir="docs_suffix_structure_two_languages/",
        plugins={
            "search": {
                "lang": ["en"],
            },
            "i18n": {
                "reconfigure_search": False,
                "languages": [
                    {
                        "locale": "en",
                        "name": "english",
                        "default": True,
                    },
                    {"locale": "fr", "name": "français"},
                ],
            },
        },
    )
    build(mkdocs_config)
    search_plugin = mkdocs_config["plugins"]["search"]
    assert search_plugin.config["lang"] == ["en"]

import logging
from importlib.metadata import files as package_files
from importlib.metadata import version
from pathlib import PurePath

try:
    from properdocs import localization, plugins, utils
    from properdocs.commands.build import build
    from properdocs.config import config_options
    from properdocs.config.base import Config, LegacyConfig, ValidationError
    from properdocs.config.defaults import ProperDocsConfig as MkDocsConfig
    from properdocs.plugins import BasePlugin, get_plugin_logger
    from properdocs.structure.files import File, Files
    from properdocs.structure.nav import Navigation
    from properdocs.structure.pages import Page
    from properdocs.theme import Theme

    ENGINE = "properdocs"

except ImportError:
    from mkdocs import localization, plugins, utils
    from mkdocs.commands.build import build
    from mkdocs.config import config_options
    from mkdocs.config.base import Config, LegacyConfig, ValidationError
    from mkdocs.config.defaults import MkDocsConfig
    from mkdocs.plugins import BasePlugin, get_plugin_logger
    from mkdocs.structure.files import File, Files
    from mkdocs.structure.nav import Navigation
    from mkdocs.structure.pages import Page
    from mkdocs.theme import Theme

    ENGINE = "mkdocs"

MATERIAL_PACKAGES = {
    "mkdocs-material": "material",
    "mkdocs-materialx": "materialx",
}

DEFAULT_LANGS = [
    "ar",
    "da",
    "de",
    "du",
    "en",
    "es",
    "fi",
    "fr",
    "hi",
    "hu",
    "hy",
    "it",
    "ja",
    "jp",
    "kn",
    "ko",
    "nl",
    "no",
    "pt",
    "ro",
    "ru",
    "sa",
    "sv",
    "ta",
    "te",
    "th",
    "tr",
    "vi",
    "zh",
]


MATERIAL_VERSION = ""
THEME_NAME = ""

for pkg_name, theme_name in MATERIAL_PACKAGES.items():
    try:
        MATERIAL_VERSION = version(pkg_name)
        THEME_NAME = theme_name
        break
    except Exception:
        # print(f"No material theme {e}")
        pass

LUNR_LANGUAGES = []
try:
    prefix = f"{ENGINE}/contrib/search/lunr-language/lunr."
    pkg_list = package_files(ENGINE)

    if pkg_list:
        LUNR_LANGUAGES = [
            PurePath(lang.stem).suffix.replace(".", "")
            for lang in pkg_list
            if prefix in lang.as_posix() and len(lang.stem) == 7
        ]
    assert len(LUNR_LANGUAGES) > 1
    LUNR_LANGUAGES.append("en")
except Exception:
    LUNR_LANGUAGES = DEFAULT_LANGS
    logging.warning("Unable to detect lunr languages from mkdocs/properdocs distribution")

# MKDOCS_THEMES = ["mkdocs", "readthedocs"]
BUILD_LOGGER_NAME = f"{ENGINE}.commands.build"

__all__ = [
    "localization",
    "plugins",
    "utils",
    "build",
    "config_options",
    "Config",
    "LegacyConfig",
    "ValidationError",
    "MkDocsConfig",
    "BasePlugin",
    "get_plugin_logger",
    "File",
    "Files",
    "Navigation",
    "Page",
    "Theme",
    "ENGINE",
    "BUILD_LOGGER_NAME",
    "LUNR_LANGUAGES",
    "THEME_NAME",
]

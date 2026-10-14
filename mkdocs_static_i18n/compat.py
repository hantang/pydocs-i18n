import logging
import sys
from importlib.metadata import files as package_files
from importlib.metadata import version
from pathlib import PurePath


def _running_engine():
    """
    Return the docs engine ("properdocs" or "mkdocs") driving this process.

    Both engines can be installed side by side and each defines its own
    ``BasePlugin``. A plugin class must inherit from the ``BasePlugin`` of the
    engine that loads it, otherwise the loader rejects it with "must be a
    subclass of <engine>.plugins.BasePlugin". The engine's package is always
    imported (and its ``__main__`` module registered when invoked as a CLI)
    before it loads plugins, so ``sys.modules`` tells us which one is running.
    """
    running = [e for e in ("properdocs", "mkdocs") if f"{e}.__main__" in sys.modules]
    if len(running) == 1:
        return running[0]

    if "properdocs" in sys.modules and "mkdocs" not in sys.modules:
        return "properdocs"
    if "mkdocs" in sys.modules and "properdocs" not in sys.modules:
        return "mkdocs"

    # Neither engine imported yet (or both are): honor properdocs when it is
    # installed, otherwise fall back to mkdocs.
    try:
        import properdocs  # noqa: F401

        return "properdocs"
    except ImportError:
        return "mkdocs"


ENGINE = _running_engine()

if ENGINE == "properdocs":
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

else:
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

# Names of every installed material theme, e.g. ["material", "materialx"]. Both
# mkdocs-material and mkdocs-materialx can be installed side by side and each
# provides its own material theme, so theme reconfiguration must match the theme
# name actually used by the running config, not only the first installed package.
MATERIAL_THEMES = []

for pkg_name, theme_name in MATERIAL_PACKAGES.items():
    try:
        material_version = version(pkg_name)
    except Exception:
        # print(f"No material theme {e}")
        continue
    MATERIAL_THEMES.append(theme_name)
    if not THEME_NAME:
        MATERIAL_VERSION = material_version
        THEME_NAME = theme_name

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
    "MATERIAL_THEMES",
]

"""
Chapter Extractor Package

A Python package for extracting chapters from HTML files and converting them to Markdown format.
"""

from .extractor import ChapterExtractor, roman_to_arabic, convert_chapter_title

__version__ = "1.0.0"
__author__ = "Neel Baronia"
__email__ = "neelbaronia@example.com"

__all__ = ["ChapterExtractor", "roman_to_arabic", "convert_chapter_title"]

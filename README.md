# Chapter Extractor

A Python package for extracting chapters from HTML files and converting them to various formats (Markdown, TXT, RTF).

## Features

- Extract chapters from HTML files with `<h2>` headings containing "CHAPTER"
- Convert Roman numerals to Arabic numbers in chapter titles
- Clean text formatting for audiobook production
- Support for multiple output formats (Markdown, TXT, RTF)
- Command-line interface for easy use
- Python API for programmatic use

## Installation

### From PyPI (when published)
```bash
pip install chapter-extractor
```

### From source
```bash
git clone https://github.com/neelbaronia/chapter-extractor.git
cd chapter-extractor
pip install -e .
```

## Usage

### Command Line Interface

```bash
# Extract chapters to Markdown files
chapter-extractor book.html

# Extract to specific directory
chapter-extractor book.html -o my_chapters

# Extract to TXT format
chapter-extractor book.html -f txt

# Extract to RTF format
chapter-extractor book.html -f rtf

# Just extract without saving files
chapter-extractor book.html --no-save
```

### Python API

```python
from chapter_extractor import ChapterExtractor

# Create extractor
extractor = ChapterExtractor("book.html")

# Extract chapters
chapters = extractor.extract_chapters()

# Save to specific directory and format
extractor.save_chapters("output_dir", "markdown")

# Access individual chapters
for chapter in chapters:
    print(f"Title: {chapter['title']}")
    print(f"Content: {chapter['content'][:100]}...")
```

### Individual Functions

```python
from chapter_extractor import roman_to_arabic, convert_chapter_title

# Convert Roman numerals
arabic = roman_to_arabic("XXI")  # Returns 21

# Convert chapter title
title = convert_chapter_title("CHAPTER I. THE BEGINNING")
# Returns "CHAPTER 1. THE BEGINNING"
```

## Requirements

- Python 3.8+
- beautifulsoup4

## Development

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black chapter_extractor/

# Type checking
mypy chapter_extractor/
```

## License

MIT License - see LICENSE file for details.

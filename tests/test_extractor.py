"""
Tests for chapter_extractor package.
"""

import pytest
from chapter_extractor import roman_to_arabic, convert_chapter_title, clean_text


def test_roman_to_arabic():
    """Test Roman numeral to Arabic conversion."""
    assert roman_to_arabic("I") == 1
    assert roman_to_arabic("V") == 5
    assert roman_to_arabic("X") == 10
    assert roman_to_arabic("IV") == 4
    assert roman_to_arabic("IX") == 9
    assert roman_to_arabic("XXI") == 21
    assert roman_to_arabic("XL") == 40
    assert roman_to_arabic("XC") == 90


def test_convert_chapter_title():
    """Test chapter title conversion."""
    assert convert_chapter_title("CHAPTER I. THE BEGINNING") == "CHAPTER 1. THE BEGINNING"
    assert convert_chapter_title("CHAPTER II. THE MIDDLE") == "CHAPTER 2. THE MIDDLE"
    assert convert_chapter_title("CHAPTER XXI. THE END") == "CHAPTER 21. THE END"
    assert convert_chapter_title("CHAPTER IV. BARBARA ENGAGES COUNSEL") == "CHAPTER 4. BARBARA ENGAGES COUNSEL"


def test_clean_text():
    """Test text cleaning functionality."""
    # Test paragraph preservation
    text = "First paragraph.\n\nSecond paragraph.\n\nThird paragraph."
    cleaned = clean_text(text)
    assert "First paragraph." in cleaned
    assert "Second paragraph." in cleaned
    assert "Third paragraph." in cleaned
    
    # Test whitespace cleanup
    text = "Multiple    spaces   and\ttabs"
    cleaned = clean_text(text)
    assert "Multiple spaces and tabs" in cleaned

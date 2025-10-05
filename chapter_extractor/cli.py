#!/usr/bin/env python3
"""
Command-line interface for Chapter Extractor package.
"""

import argparse
import sys
from pathlib import Path
from chapter_extractor import ChapterExtractor


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description="Extract chapters from HTML files and convert to various formats"
    )
    parser.add_argument(
        "html_file",
        help="Path to the HTML file containing chapters"
    )
    parser.add_argument(
        "-o", "--output-dir",
        default="chapters",
        help="Output directory for extracted chapters (default: chapters)"
    )
    parser.add_argument(
        "-f", "--format",
        choices=["markdown", "txt", "rtf"],
        default="markdown",
        help="Output format (default: markdown)"
    )
    parser.add_argument(
        "--no-save",
        action="store_true",
        help="Extract chapters but don't save to files"
    )
    
    args = parser.parse_args()
    
    # Check if HTML file exists
    if not Path(args.html_file).exists():
        print(f"Error: HTML file '{args.html_file}' not found")
        sys.exit(1)
    
    # Create extractor and extract chapters
    extractor = ChapterExtractor(args.html_file)
    
    try:
        if args.no_save:
            chapters = extractor.extract_chapters()
            print(f"\nExtracted {len(chapters)} chapters:")
            for i, chapter in enumerate(chapters, 1):
                print(f"{i:2d}. {chapter['title']}")
        else:
            extractor.extract_chapters(args.output_dir, args.format)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Script to extract chapters from HTML file and save as individual Markdown files.
"""

import re
import os
from bs4 import BeautifulSoup

def roman_to_arabic(roman):
    """Convert Roman numerals to Arabic numbers."""
    roman_numerals = {
        'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000
    }
    
    result = 0
    prev_value = 0
    
    for char in reversed(roman):
        value = roman_numerals[char]
        if value < prev_value:
            result -= value
        else:
            result += value
        prev_value = value
    
    return result

def convert_chapter_title(title):
    """Convert Roman numerals in chapter title to Arabic numbers."""
    # Match patterns like "CHAPTER I.", "CHAPTER II.", etc.
    def replace_roman(match):
        roman = match.group(1)
        arabic = roman_to_arabic(roman)
        return f"CHAPTER {arabic}."
    
    # Replace Roman numerals in chapter titles
    title = re.sub(r'CHAPTER ([IVXLCDM]+)\.', replace_roman, title)
    return title

def clean_text(text):
    """Clean and format text for audiobook production."""
    # Remove line breaks within paragraphs but preserve paragraph breaks
    # First, identify paragraph breaks (double newlines or more)
    # Replace multiple newlines with a special marker
    text = re.sub(r'\n\s*\n\s*\n*', '|||PARAGRAPH_BREAK|||', text)
    
    # Now remove all remaining single newlines (within paragraphs)
    text = re.sub(r'\n', ' ', text)
    
    # Replace the paragraph break markers with double newlines
    text = re.sub(r'\|\|\|PARAGRAPH_BREAK\|\|\|', '\n\n', text)
    
    # Clean up excessive whitespace
    text = re.sub(r'[ \t]+', ' ', text)
    
    # Remove empty lines at start and end
    text = text.strip()
    
    return text

def create_markdown_content(title, content):
    """Create Markdown formatted content."""
    # Format as plain text with title and content, no markdown formatting
    markdown_content = f"{title}\n\n{content}"
    return markdown_content

def extract_chapters(html_file):
    """Extract chapters from HTML file and save as Markdown files."""
    
    # Read the HTML file
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Parse HTML
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find all chapter headings
    chapter_headings = soup.find_all('h2')
    
    chapters = []
    
    for i, heading in enumerate(chapter_headings):
        if 'CHAPTER' in heading.get_text().upper():
            chapter_title = heading.get_text().strip()
            print(f"Found: {chapter_title}")
            
            # Get the content after this heading until the next heading
            content_elements = []
            current = heading.next_sibling
            
            while current:
                if current.name == 'h2' and 'CHAPTER' in current.get_text().upper():
                    break
                if hasattr(current, 'get_text'):
                    content_elements.append(current.get_text())
                elif isinstance(current, str):
                    content_elements.append(current)
                current = current.next_sibling
            
            # Join all content
            chapter_content = ' '.join(content_elements)
            chapter_content = clean_text(chapter_content)
            
            # Convert Roman numerals to Arabic numbers in title
            converted_title = convert_chapter_title(chapter_title)
            
            chapters.append({
                'title': converted_title,
                'content': chapter_content
            })
    
    # Create output directory
    output_dir = os.path.join(os.path.dirname(html_file), 'chapters')
    os.makedirs(output_dir, exist_ok=True)
    
    # Save each chapter as Markdown
    for i, chapter in enumerate(chapters, 1):
        # Create filename
        safe_title = re.sub(r'[^\w\s-]', '', chapter['title'])
        safe_title = re.sub(r'[-\s]+', '_', safe_title)
        filename = f"Chapter_{i:02d}_{safe_title}.md"
        filepath = os.path.join(output_dir, filename)
        
        # Create Markdown content
        markdown_content = create_markdown_content(chapter['title'], chapter['content'])
        
        # Write to file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        print(f"Created: {filename}")
    
    print(f"\nExtracted {len(chapters)} chapters to {output_dir}/")
    return chapters

if __name__ == "__main__":
    html_file = "/Users/nbaronia/Downloads/pg1747-h/pg1747-images.html"
    chapters = extract_chapters(html_file)

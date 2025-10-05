"""
Chapter extraction functionality for HTML to Markdown conversion.
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


class ChapterExtractor:
    """Main class for extracting chapters from HTML files."""
    
    def __init__(self, html_file):
        """Initialize with HTML file path."""
        self.html_file = html_file
        self.chapters = []
    
    def extract_chapters(self, output_dir=None, output_format='markdown'):
        """
        Extract chapters from HTML file and save as individual files.
        
        Args:
            output_dir (str): Directory to save extracted chapters. Defaults to 'chapters' in same dir as HTML file.
            output_format (str): Output format ('markdown', 'txt', 'rtf'). Defaults to 'markdown'.
        
        Returns:
            list: List of chapter dictionaries with 'title' and 'content' keys.
        """
        # Read the HTML file
        with open(self.html_file, 'r', encoding='utf-8') as f:
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
        
        self.chapters = chapters
        
        # Save chapters if output directory is specified
        if output_dir:
            self.save_chapters(output_dir, output_format)
        
        return chapters
    
    def save_chapters(self, output_dir, output_format='markdown'):
        """Save extracted chapters to files."""
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Determine file extension
        extensions = {
            'markdown': '.md',
            'txt': '.txt',
            'rtf': '.rtf'
        }
        ext = extensions.get(output_format, '.md')
        
        # Save each chapter
        for i, chapter in enumerate(self.chapters, 1):
            # Create filename
            safe_title = re.sub(r'[^\w\s-]', '', chapter['title'])
            safe_title = re.sub(r'[-\s]+', '_', safe_title)
            filename = f"Chapter_{i:02d}_{safe_title}{ext}"
            filepath = os.path.join(output_dir, filename)
            
            # Create content based on format
            if output_format == 'markdown':
                content = create_markdown_content(chapter['title'], chapter['content'])
            elif output_format == 'txt':
                content = f"{chapter['title']}\n\n{chapter['content']}"
            elif output_format == 'rtf':
                content = self._create_rtf_content(chapter['title'], chapter['content'])
            else:
                content = create_markdown_content(chapter['title'], chapter['content'])
            
            # Write to file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"Created: {filename}")
        
        print(f"\nExtracted {len(self.chapters)} chapters to {output_dir}/")
    
    def _create_rtf_content(self, title, content):
        """Create RTF formatted content."""
        # Basic RTF header
        rtf_header = r"{\rtf1\ansi\deff0 {\fonttbl {\f0 Times New Roman;}}"
        rtf_header += r"\f0\fs24 "
        
        # Format title
        title_formatted = f"\\b\\fs28 {title}\\b0\\fs24\\par\\par"
        
        # Format content (escape RTF special characters)
        content_escaped = content.replace('\\', '\\\\')
        content_escaped = content_escaped.replace('{', '\\{')
        content_escaped = content_escaped.replace('}', '\\}')
        content_escaped = content_escaped.replace('\n', '\\par ')
        
        # Combine all parts
        rtf_content = rtf_header + title_formatted + content_escaped + "}"
        
        return rtf_content

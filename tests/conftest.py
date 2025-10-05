"""
Test configuration and fixtures.
"""

import pytest
import tempfile
import os
from pathlib import Path


@pytest.fixture
def sample_html():
    """Create a sample HTML file for testing."""
    html_content = """
    <html>
    <body>
        <h2>CHAPTER I. THE BEGINNING</h2>
        <p>This is the first chapter content.</p>
        <p>It has multiple paragraphs.</p>
        
        <h2>CHAPTER II. THE MIDDLE</h2>
        <p>This is the second chapter content.</p>
        
        <h2>CHAPTER III. THE END</h2>
        <p>This is the final chapter content.</p>
    </body>
    </html>
    """
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
        f.write(html_content)
        temp_path = f.name
    
    yield temp_path
    
    # Cleanup
    os.unlink(temp_path)


@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir

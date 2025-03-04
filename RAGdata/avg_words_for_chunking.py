#!/usr/bin/env python3
import re
import sys

def calculate_avg_words(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading file {filename}: {e}")
        sys.exit(1)

    # Split content on headings indicated by "## " at the beginning of a line.
    # This splits the document into sections where the first element might be content before any heading.
    sections = re.split(r'^\s*##\s+', content, flags=re.MULTILINE)
    
    # If there's text before the first heading, remove it:
    if sections and not sections[0].strip():
        sections = sections[1:]
    
    word_counts = []
    for section in sections:
        # Each section starts with the heading on its first line.
        lines = section.splitlines()
        if not lines:
            continue
        # Remove the heading (first line) so we only count words in the content under that heading.
        content_text = " ".join(lines[1:]).strip()
        # Count words using split (this is a simple approach; punctuation is attached to words).
        words = content_text.split()
        count = len(words)
        word_counts.append(count)

    if not word_counts:
        print("No sections with headings found.")
        return

    average = sum(word_counts) / len(word_counts)
    print(f"Average number of words per section: {average:.2f}\n")
    for i, count in enumerate(word_counts, start=1):
        print(f"Section {i} has {count} words.")

def main():
    if len(sys.argv) < 2:
        print("Usage: python average_words.py <path/to/MonumentsData.txt>")
        sys.exit(1)
    
    filename = sys.argv[1]
    calculate_avg_words(filename)

if __name__ == '__main__':
    main()
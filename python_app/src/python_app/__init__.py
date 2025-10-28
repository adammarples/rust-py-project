"""Python application using Rust-powered text analysis."""

from rust_core import TextAnalyzer

__all__ = ["TextAnalyzer", "analyze_file"]


def analyze_file(filepath: str) -> dict:
    """
    Analyze a text file and return statistics.

    Args:
        filepath: Path to the text file to analyze

    Returns:
        Dictionary with analysis results including word counts and character count
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    analyzer = TextAnalyzer(text)

    return {
        'char_count': analyzer.char_count(),
        'word_count': analyzer.word_count(),
        'top_10_words': analyzer.most_common(10),
    }

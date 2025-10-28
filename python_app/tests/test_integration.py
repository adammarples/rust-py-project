"""Integration tests for TextAnalyzer functionality."""

import pytest
from rust_core import TextAnalyzer


class TestTextAnalyzer:
    """Test suite for TextAnalyzer class."""

    def test_basic_word_count(self):
        """Test basic word counting functionality."""
        analyzer = TextAnalyzer("hello world hello")
        word_count = analyzer.word_count()

        assert word_count["hello"] == 2
        assert word_count["world"] == 1
        assert len(word_count) == 2

    def test_char_count(self):
        """Test character counting."""
        analyzer = TextAnalyzer("hello world")
        assert analyzer.char_count() == 11

    def test_char_count_with_unicode(self):
        """Test character counting with unicode characters."""
        analyzer = TextAnalyzer("hello 世界")
        assert analyzer.char_count() == 8

    def test_most_common_basic(self):
        """Test most_common returns correct top words."""
        text = "the quick brown fox jumps over the lazy dog the"
        analyzer = TextAnalyzer(text)
        most_common = analyzer.most_common(3)

        assert len(most_common) == 3
        assert most_common[0] == ("the", 3)
        assert most_common[1][1] == 1  # All other words appear once

    def test_most_common_with_punctuation(self):
        """Test word counting ignores punctuation."""
        analyzer = TextAnalyzer("Hello, world! Hello.")
        word_count = analyzer.word_count()

        assert word_count["hello"] == 2
        assert word_count["world"] == 1

    def test_most_common_zero_raises_error(self):
        """Test that most_common(0) raises ValueError."""
        analyzer = TextAnalyzer("hello world")

        with pytest.raises(ValueError, match="n must be greater than 0"):
            analyzer.most_common(0)

    def test_most_common_more_than_available(self):
        """Test requesting more words than available."""
        analyzer = TextAnalyzer("hello world")
        most_common = analyzer.most_common(10)

        assert len(most_common) == 2  # Only 2 unique words

    def test_empty_text(self):
        """Test analyzer with empty text."""
        analyzer = TextAnalyzer("")

        assert analyzer.char_count() == 0
        assert len(analyzer.word_count()) == 0

    def test_get_text(self):
        """Test retrieving original text."""
        original = "hello world"
        analyzer = TextAnalyzer(original)

        assert analyzer.get_text() == original

    def test_case_insensitive_counting(self):
        """Test that word counting is case-insensitive."""
        analyzer = TextAnalyzer("Hello HELLO hello")
        word_count = analyzer.word_count()

        assert word_count["hello"] == 3
        assert "Hello" not in word_count
        assert "HELLO" not in word_count

    def test_multiline_text(self):
        """Test analyzer with multiline text."""
        text = """first line
        second line
        third line with words words"""
        analyzer = TextAnalyzer(text)
        word_count = analyzer.word_count()

        assert word_count["line"] == 3
        assert word_count["words"] == 2

    def test_repr(self):
        """Test string representation."""
        analyzer = TextAnalyzer("hello world")
        repr_str = repr(analyzer)

        assert "TextAnalyzer" in repr_str
        assert "hello world" in repr_str

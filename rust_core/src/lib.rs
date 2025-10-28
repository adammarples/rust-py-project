use pyo3::prelude::*;
use std::collections::HashMap;

/// A text analyzer that provides various text statistics and analysis methods.
#[pyclass]
struct TextAnalyzer {
    text: String,
}

#[pymethods]
impl TextAnalyzer {
    /// Create a new TextAnalyzer with the given text.
    #[new]
    fn new(text: String) -> Self {
        TextAnalyzer { text }
    }

    /// Count the frequency of each word in the text.
    /// Returns a dictionary mapping words to their counts.
    fn word_count(&self) -> HashMap<String, usize> {
        let mut counts = HashMap::new();

        for word in self.text
            .to_lowercase()
            .split_whitespace()
            .map(|w| w.trim_matches(|c: char| !c.is_alphanumeric()))
            .filter(|w| !w.is_empty())
        {
            *counts.entry(word.to_string()).or_insert(0) += 1;
        }

        counts
    }

    /// Count the total number of characters in the text (including whitespace).
    fn char_count(&self) -> usize {
        self.text.chars().count()
    }

    /// Get the n most common words with their counts.
    /// Returns a list of tuples (word, count) sorted by frequency.
    fn most_common(&self, n: usize) -> PyResult<Vec<(String, usize)>> {
        if n == 0 {
            return Err(pyo3::exceptions::PyValueError::new_err(
                "n must be greater than 0"
            ));
        }

        let word_counts = self.word_count();
        let mut word_vec: Vec<(String, usize)> = word_counts.into_iter().collect();

        // Sort by count (descending), then alphabetically for ties
        word_vec.sort_by(|a, b| {
            b.1.cmp(&a.1).then_with(|| a.0.cmp(&b.0))
        });

        Ok(word_vec.into_iter().take(n).collect())
    }

    /// Get the original text.
    fn get_text(&self) -> String {
        self.text.clone()
    }

    /// Python repr for debugging.
    fn __repr__(&self) -> String {
        format!("TextAnalyzer(text=\"{}...\")",
                self.text.chars().take(50).collect::<String>())
    }
}

/// A Rust-powered text analysis library.
#[pymodule]
fn rust_core(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<TextAnalyzer>()?;
    Ok(())
}

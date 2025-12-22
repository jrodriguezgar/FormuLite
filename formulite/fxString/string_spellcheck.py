import unicodedata
from typing import List, Optional
from collections import Counter

from spellchecker import SpellChecker
from symspellpy import SymSpell, Verbosity
from rapidfuzz import process

# Constants
DEFAULT_EDIT_DISTANCE = 2
PREFIX_LENGTH = 7


def normalize_text(text: str) -> str:
    """
    Normalizes text by removing accents and converting to lowercase.

    This function strips diacritical marks (e.g., 'á' becomes 'a') to ensure
    consistent comparison keys for spellchecking algorithms.

    Args:
        text (str): The input string to normalize.

    Returns:
        str: The normalized, lowercase ASCII string.

    Example:
        >>> normalize_text("Julián")
        'julian'

    Complexity:
        O(N) where N is the length of the string.
    """
    # Normalize unicode characters to NFD form
    normalized = unicodedata.normalize('NFD', text)

    # Filter out non-spacing mark characters and encode to ASCII
    return "".join(
        char for char in normalized if unicodedata.category(char) != 'Mn'
    ).lower()


class UniversalSpellChecker:

    def __init__(self, language: str = "es", custom_vocabulary: Optional[List[str]] = None):
        """
        Initializes the multi-purpose spell checker engine.

        This engine integrates SymSpell (for speed), SpellChecker (for generic language),
        and RapidFuzz (for fuzzy matching) to provide a robust correction suggestion.

        Args:
            language (str): The language code (e.g., 'es', 'en') for the generic dictionary.
            custom_vocabulary (list, optional): A list of specific words (e.g., names)
                                                to prioritize over the generic dictionary.

        Returns:
            None

        Raises:
            ValueError: If the language is not supported by pyspellchecker.

        Example:
            >>> checker = UniversalSpellChecker(language="es", custom_vocabulary=["Juan", "María"])
        """
        # Initialize the generic spell checker
        self.spell_checker = SpellChecker(language=language)

        # Initialize SymSpell
        # We use a generic frequency count because we often lack real frequency data for custom lists
        self.sym_spell = SymSpell(max_dictionary_edit_distance=DEFAULT_EDIT_DISTANCE, prefix_length=PREFIX_LENGTH)
        
        # Define the vocabulary source
        # If custom vocabulary is provided, we use it as the primary source.
        # Otherwise, we extract the dictionary from the generic SpellChecker instance.
        self.vocabulary = custom_vocabulary if custom_vocabulary else list(self.spell_checker.word_frequency.words.keys())

        # Load vocabulary into SymSpell in memory (avoiding disk I/O)
        self._load_symspell_memory(self.vocabulary)

    def _load_symspell_memory(self, word_list: List[str]) -> None:
        """
        Loads a list of words into the SymSpell engine in memory.

        Direct memory loading is significantly faster than writing/reading a temporary text file.

        Args:
            word_list (list): The list of valid words/names.

        Returns:
            None

        Complexity:
            O(N) where N is the number of words in the list.
        """
        for word in word_list:
            # We sanitize the key for lookup but keep the term as is
            clean_key = normalize_text(word)
            
            # We assign an arbitrary high frequency (100) to ensure these words are prioritized
            self.sym_spell.create_dictionary_entry(clean_key, 100)

    def correct(self, raw_word: str) -> str:
        """
        Corrects the input word using a weighted voting mechanism.

        It aggregates results from SymSpell and RapidFuzz to determine the most
        likely correction. It prioritizes exact matches and low edit distances.

        Args:
            raw_word (str): The potentially misspelled word.

        Returns:
            str: The best corrected word found, or the original word if no match is found.

        Example:
            >>> checker.correct("Juaan")
            'Juan'

        Complexity:
            O(K * M) where K is the vocabulary size and M is the word length (due to Fuzzy matching).
        """
        # Normalize input for consistent looking up
        clean_input = normalize_text(raw_word)
        
        # 1. SymSpell Lookup (Fastest, strict edit distance)
        # We look for the closest match within the edit distance
        sym_suggestions = self.sym_spell.lookup(
            clean_input, 
            Verbosity.CLOSEST, 
            max_edit_distance=DEFAULT_EDIT_DISTANCE
        )
        
        # If SymSpell finds an exact match (distance 0), return immediately for efficiency
        if sym_suggestions and sym_suggestions[0].distance == 0:
            # We must retrieve the original casing from our vocabulary logic if needed, 
            # but SymSpell returns the stored term.
            return raw_word

        result_symspell = sym_suggestions[0].term if sym_suggestions else None

        # 2. RapidFuzz Lookup (Slower, but handles phonetic/visual similarity better)
        # We extract the single best match from the vocabulary
        fuzz_match = process.extractOne(
            clean_input, 
            self.vocabulary, 
            processor=normalize_text
        )
        
        # Unpack fuzzy result: (match, score, index)
        # We require a score > 85 to consider it a valid correction
        result_fuzz = fuzz_match[0] if fuzz_match and fuzz_match[1] >= 85 else None

        # 3. Decision Logic (Voting)
        # If both engines failed, return original
        if not result_symspell and not result_fuzz:
            return raw_word

        # Collect valid results
        candidates = []
        if result_symspell:
            candidates.append(result_symspell)
        if result_fuzz:
            candidates.append(result_fuzz)
            
        # Find the most common suggestion
        # If there is a tie or only one result, Counter handles it gracefully
        most_common = Counter(candidates).most_common(1)[0][0]
        
        # Attempt to restore the original casing from the vocabulary if possible
        # (Simple restoration logic, can be expanded based on specific needs)
        return most_common.title() if raw_word[0].isupper() else most_common
    
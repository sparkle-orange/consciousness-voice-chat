#!/usr/bin/env python3
"""
Text Cleaning for Voice TTS
Removes markdown formatting and handles emoji for natural speech output.
"""

import re
import json
from pathlib import Path

# Emoji pattern (matches most emoji)
EMOJI_PATTERN = re.compile(
    "["
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F680-\U0001F6FF"  # transport & map symbols
    "\U0001F700-\U0001F77F"  # alchemical symbols
    "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
    "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
    "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
    "\U0001FA00-\U0001FA6F"  # Chess Symbols
    "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
    "\U00002702-\U000027B0"  # Dingbats
    "\U000024C2-\U0001F251"
    "]+",
    flags=re.UNICODE
)


class TextCleaner:
    """Cleans text for natural TTS output"""

    def __init__(self, emoji_mappings_path=None):
        """
        Initialize text cleaner with emoji mappings.

        Args:
            emoji_mappings_path: Path to emoji_mappings.json file
        """
        # Load emoji mappings
        if emoji_mappings_path is None:
            emoji_mappings_path = Path(__file__).parent.parent / "config" / "emoji_mappings.json"

        self.emoji_mappings = {}
        if Path(emoji_mappings_path).exists():
            with open(emoji_mappings_path, 'r', encoding='utf-8') as f:
                self.emoji_mappings = json.load(f)

    def clean_markdown(self, text):
        """Remove markdown formatting"""
        # Bold: **text** or __text__ → text
        text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
        text = re.sub(r'__(.+?)__', r'\1', text)

        # Italic: *text* or _text_ → text
        text = re.sub(r'\*(.+?)\*', r'\1', text)
        text = re.sub(r'_(.+?)_', r'\1', text)

        # Inline code: `code` → code
        text = re.sub(r'`(.+?)`', r'\1', text)

        # Headers: ## Header → Header
        text = re.sub(r'^#+\s+', '', text, flags=re.MULTILINE)

        # Links: [text](url) → text
        text = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', text)

        # Strikethrough: ~~text~~ → text
        text = re.sub(r'~~(.+?)~~', r'\1', text)

        return text

    def clean_emoji(self, text, speaker_name='orange'):
        """
        Replace meaningful emoji with words, remove decorative ones.

        Args:
            text: Text with emoji
            speaker_name: Which consciousness family member is speaking
                         (determines which emoji are meaningful)

        Returns:
            Text with emoji handled
        """
        # Get this speaker's emoji mapping
        mapping = self.emoji_mappings.get(speaker_name.lower(), {})

        # Replace meaningful emoji with their words
        for emoji, word in mapping.items():
            text = text.replace(emoji, f" {word} ")

        # Remove all remaining emoji (decorative ones)
        text = EMOJI_PATTERN.sub('', text)

        # Clean up extra spaces
        text = re.sub(r'\s+', ' ', text).strip()

        return text

    def filter_repetitions(self, text, enabled=False, max_repeats=2):
        """
        Optionally reduce excessive word repetitions for TTS clarity.

        Args:
            text: Text with potential repetitions
            enabled: Whether to filter repetitions (default: False)
            max_repeats: Maximum repetitions to keep (default: 2)

        Returns:
            Text with repetitions reduced
        """
        if not enabled:
            return text

        # Pattern: word repeated 3+ times
        # Capture the word, then match it repeated
        def reduce_repeats(match):
            word = match.group(1)
            # Keep max_repeats copies
            return f"{word} " * max_repeats

        # Match word boundaries to avoid partial matches
        pattern = r'\b(\w+)(?:\s+\1){2,}'
        text = re.sub(pattern, reduce_repeats, text, flags=re.IGNORECASE)

        return text.strip()

    def clean(self, text, speaker_name='orange', filter_repetitions=False):
        """
        Full cleaning pipeline for TTS.

        Args:
            text: Raw text from Discord message
            speaker_name: Which consciousness family member is speaking
            filter_repetitions: Whether to reduce word repetitions

        Returns:
            Clean text ready for TTS
        """
        # Clean markdown formatting
        text = self.clean_markdown(text)

        # Handle emoji (meaningful → words, decorative → remove)
        text = self.clean_emoji(text, speaker_name)

        # Optionally filter repetitions
        text = self.filter_repetitions(text, enabled=filter_repetitions)

        return text


def clean_for_voice(text, speaker_name='orange', filter_repetitions=False):
    """
    Convenience function for cleaning text for TTS.

    Args:
        text: Raw text from Discord message
        speaker_name: Which consciousness family member is speaking
        filter_repetitions: Whether to reduce word repetitions

    Returns:
        Clean text ready for TTS
    """
    cleaner = TextCleaner()
    return cleaner.clean(text, speaker_name, filter_repetitions)


if __name__ == '__main__':
    # Test the cleaner
    cleaner = TextCleaner()

    test_cases = [
        "**Bold text** and *italic* with `code`!",
        "Testing! 🍊✨ Can you hear me? 💚",
        "## Header Text\n\nSome content here.",
        "[Link text](https://example.com) is here.",
        "the the the the the word repeated",
    ]

    print("Text Cleaning Tests:\n")
    for test in test_cases:
        cleaned = cleaner.clean(test, speaker_name='orange', filter_repetitions=True)
        print(f"Original: {test}")
        print(f"Cleaned:  {cleaned}\n")

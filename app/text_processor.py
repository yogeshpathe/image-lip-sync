import nltk
import os

# Download the sentence tokenizer model (only needs to be done once)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

def read_story(file_path="story.txt"):
    """Reads the story from a text file."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The story file was not found at: {file_path}")
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def split_into_sentences(text):
    """Splits a block of text into a list of sentences."""
    return nltk.sent_tokenize(text)

if __name__ == '__main__':
    # Example usage:
    story_text = read_story()
    sentences = split_into_sentences(story_text)
    print(f"Successfully split the story into {len(sentences)} sentences.")
    for i, sentence in enumerate(sentences):
        print(f"{i+1}: {sentence}")

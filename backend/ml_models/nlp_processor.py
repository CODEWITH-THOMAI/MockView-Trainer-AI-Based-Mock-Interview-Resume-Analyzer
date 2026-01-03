"""
NLP Processor
Natural Language Processing utilities using NLTK and SpaCy
"""

import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import string
import re

# Global variables for lazy initialization
_stopwords = None
_lemmatizer = None

def initialize_nltk():
    """
    Initialize NLTK by downloading required data
    This function should be called once when the application starts
    """
    try:
        # Download required NLTK data
        required_data = [
            'punkt',
            'stopwords',
            'wordnet',
            'averaged_perceptron_tagger',
            'omw-1.4'
        ]
        
        for data in required_data:
            try:
                nltk.data.find(f'tokenizers/{data}')
            except LookupError:
                nltk.download(data, quiet=True)
        
        print("NLTK initialized successfully")
        return True
    except Exception as e:
        print(f"Error initializing NLTK: {str(e)}")
        return False

def get_stopwords():
    """Get stopwords set (lazy initialization)"""
    global _stopwords
    if _stopwords is None:
        try:
            _stopwords = set(stopwords.words('english'))
        except:
            initialize_nltk()
            _stopwords = set(stopwords.words('english'))
    return _stopwords

def get_lemmatizer():
    """Get lemmatizer instance (lazy initialization)"""
    global _lemmatizer
    if _lemmatizer is None:
        _lemmatizer = WordNetLemmatizer()
    return _lemmatizer

def tokenize_text(text: str) -> list:
    """
    Tokenize text into words
    
    Args:
        text: Input text
        
    Returns:
        list: List of tokens
    """
    try:
        tokens = word_tokenize(text.lower())
        return tokens
    except Exception as e:
        print(f"Error tokenizing text: {str(e)}")
        # Fallback to simple split
        return text.lower().split()

def tokenize_sentences(text: str) -> list:
    """
    Tokenize text into sentences
    
    Args:
        text: Input text
        
    Returns:
        list: List of sentences
    """
    try:
        sentences = sent_tokenize(text)
        return sentences
    except Exception as e:
        print(f"Error tokenizing sentences: {str(e)}")
        # Fallback to split by period
        return [s.strip() for s in text.split('.') if s.strip()]

def remove_stopwords(tokens: list) -> list:
    """
    Remove stopwords from token list
    
    Args:
        tokens: List of tokens
        
    Returns:
        list: Tokens without stopwords
    """
    stop_words = get_stopwords()
    return [token for token in tokens if token not in stop_words]

def remove_punctuation(tokens: list) -> list:
    """
    Remove punctuation from tokens
    
    Args:
        tokens: List of tokens
        
    Returns:
        list: Tokens without punctuation
    """
    return [token for token in tokens if token not in string.punctuation]

def lemmatize(tokens: list) -> list:
    """
    Lemmatize tokens
    
    Args:
        tokens: List of tokens
        
    Returns:
        list: Lemmatized tokens
    """
    lemmatizer = get_lemmatizer()
    return [lemmatizer.lemmatize(token) for token in tokens]

def extract_keywords(text: str, top_n: int = 10) -> list:
    """
    Extract keywords from text using simple frequency analysis
    
    Args:
        text: Input text
        top_n: Number of keywords to extract
        
    Returns:
        list: Top keywords
    """
    # Tokenize and clean
    tokens = tokenize_text(text)
    tokens = remove_punctuation(tokens)
    tokens = remove_stopwords(tokens)
    tokens = lemmatize(tokens)
    
    # Count frequency
    freq_dist = {}
    for token in tokens:
        if len(token) > 2:  # Ignore very short words
            freq_dist[token] = freq_dist.get(token, 0) + 1
    
    # Sort by frequency and return top N
    sorted_keywords = sorted(freq_dist.items(), key=lambda x: x[1], reverse=True)
    return [keyword for keyword, count in sorted_keywords[:top_n]]

def calculate_text_similarity(text1: str, text2: str) -> float:
    """
    Calculate cosine similarity between two texts using TF-IDF
    
    Args:
        text1: First text
        text2: Second text
        
    Returns:
        float: Similarity score (0-1)
    """
    try:
        # Create TF-IDF vectors
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform([text1, text2])
        
        # Calculate cosine similarity
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        
        return round(similarity, 4)
    except Exception as e:
        print(f"Error calculating similarity: {str(e)}")
        return 0.0

def count_sentences(text: str) -> int:
    """Count number of sentences in text"""
    sentences = tokenize_sentences(text)
    return len(sentences)

def count_words(text: str) -> int:
    """Count number of words in text"""
    tokens = tokenize_text(text)
    tokens = remove_punctuation(tokens)
    return len(tokens)

def calculate_average_word_length(text: str) -> float:
    """Calculate average word length in text"""
    tokens = tokenize_text(text)
    tokens = remove_punctuation(tokens)
    
    if not tokens:
        return 0.0
    
    total_length = sum(len(token) for token in tokens)
    return round(total_length / len(tokens), 2)

def detect_grammar_errors_simple(text: str) -> list:
    """
    Simple grammar error detection based on basic rules
    Note: This is a basic implementation. For production, consider using LanguageTool or GrammarBot API
    
    Args:
        text: Input text
        
    Returns:
        list: List of potential errors
    """
    errors = []
    
    # Check for common patterns
    # 1. Double spaces
    if '  ' in text:
        errors.append("Multiple consecutive spaces found")
    
    # 2. No capital letter at start
    if text and not text[0].isupper():
        errors.append("Sentence should start with a capital letter")
    
    # 3. No punctuation at end
    if text and text[-1] not in '.!?':
        errors.append("Sentence should end with proper punctuation")
    
    # 4. Common word repetitions
    words = text.lower().split()
    for i in range(len(words) - 1):
        if words[i] == words[i + 1] and words[i] not in ['very', 'really']:
            errors.append(f"Repeated word: '{words[i]}'")
    
    return errors

def preprocess_text(text: str, remove_stops: bool = True, lemmatize_text: bool = True) -> str:
    """
    Complete text preprocessing pipeline
    
    Args:
        text: Input text
        remove_stops: Whether to remove stopwords
        lemmatize_text: Whether to lemmatize
        
    Returns:
        str: Preprocessed text
    """
    # Tokenize
    tokens = tokenize_text(text)
    
    # Remove punctuation
    tokens = remove_punctuation(tokens)
    
    # Remove stopwords
    if remove_stops:
        tokens = remove_stopwords(tokens)
    
    # Lemmatize
    if lemmatize_text:
        tokens = lemmatize(tokens)
    
    return ' '.join(tokens)

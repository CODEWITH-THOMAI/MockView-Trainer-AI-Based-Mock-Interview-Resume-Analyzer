"""
Sentiment Analyzer
Analyze sentiment and confidence in text using NLTK VADER
"""

from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

# Global sentiment analyzer instance
_sia = None

def initialize_sentiment_analyzer():
    """
    Initialize VADER sentiment analyzer
    Downloads required data if not present
    """
    global _sia
    try:
        # Download VADER lexicon if not present
        try:
            nltk.data.find('sentiment/vader_lexicon.zip')
        except LookupError:
            nltk.download('vader_lexicon', quiet=True)
        
        _sia = SentimentIntensityAnalyzer()
        print("Sentiment analyzer initialized successfully")
        return True
    except Exception as e:
        print(f"Error initializing sentiment analyzer: {str(e)}")
        return False

def get_sentiment_analyzer():
    """Get sentiment analyzer instance (lazy initialization)"""
    global _sia
    if _sia is None:
        initialize_sentiment_analyzer()
    return _sia

def analyze_sentiment(text: str) -> dict:
    """
    Analyze sentiment of text
    
    Args:
        text: Input text to analyze
        
    Returns:
        dict: Sentiment scores {
            'positive': float (0-1),
            'negative': float (0-1),
            'neutral': float (0-1),
            'compound': float (-1 to 1),
            'sentiment': str ('positive', 'negative', or 'neutral'),
            'confidence_level': str ('high', 'medium', 'low')
        }
    """
    try:
        sia = get_sentiment_analyzer()
        
        if sia is None:
            # Fallback to basic analysis
            return {
                'positive': 0.5,
                'negative': 0.0,
                'neutral': 0.5,
                'compound': 0.5,
                'sentiment': 'neutral',
                'confidence_level': 'medium'
            }
        
        # Get sentiment scores
        scores = sia.polarity_scores(text)
        
        # Determine overall sentiment
        compound = scores['compound']
        if compound >= 0.05:
            sentiment = 'positive'
        elif compound <= -0.05:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'
        
        # Determine confidence level based on compound score magnitude
        confidence_level = determine_confidence_level(scores)
        
        return {
            'positive': round(scores['pos'], 3),
            'negative': round(scores['neg'], 3),
            'neutral': round(scores['neu'], 3),
            'compound': round(scores['compound'], 3),
            'sentiment': sentiment,
            'confidence_level': confidence_level
        }
        
    except Exception as e:
        print(f"Error analyzing sentiment: {str(e)}")
        return {
            'positive': 0.0,
            'negative': 0.0,
            'neutral': 1.0,
            'compound': 0.0,
            'sentiment': 'neutral',
            'confidence_level': 'low',
            'error': str(e)
        }

def determine_confidence_level(scores: dict) -> str:
    """
    Determine confidence level from sentiment scores
    High confidence: strong positive or negative sentiment
    Medium confidence: moderate sentiment
    Low confidence: neutral or uncertain
    
    Args:
        scores: VADER sentiment scores
        
    Returns:
        str: 'high', 'medium', or 'low'
    """
    compound = abs(scores['compound'])
    
    # Confidence indicators from interview context
    if compound >= 0.6:
        return 'high'
    elif compound >= 0.3:
        return 'medium'
    else:
        return 'low'

def analyze_confidence_from_text(text: str) -> dict:
    """
    Analyze confidence level from text based on linguistic cues
    Looks for hesitation words, assertiveness, and clarity
    
    Args:
        text: Input text
        
    Returns:
        dict: Confidence analysis {
            'score': float (0-100),
            'level': str,
            'indicators': dict
        }
    """
    text_lower = text.lower()
    
    # Confidence indicators
    hesitation_words = ['maybe', 'perhaps', 'possibly', 'probably', 'might', 'could', 'i think', 'i guess', 'sort of', 'kind of', 'um', 'uh', 'like']
    assertive_words = ['definitely', 'certainly', 'absolutely', 'clearly', 'obviously', 'exactly', 'precisely', 'indeed']
    uncertainty_phrases = ['not sure', 'don\'t know', 'unsure', 'uncertain']
    
    # Count indicators
    hesitation_count = sum(1 for word in hesitation_words if word in text_lower)
    assertive_count = sum(1 for word in assertive_words if word in text_lower)
    uncertainty_count = sum(1 for phrase in uncertainty_phrases if phrase in text_lower)
    
    # Calculate confidence score (0-100)
    # Start with base score
    base_score = 70
    
    # Reduce score for negative indicators
    score = base_score
    score -= hesitation_count * 5
    score -= uncertainty_count * 10
    
    # Increase score for positive indicators
    score += assertive_count * 5
    
    # Get sentiment-based confidence
    sentiment = analyze_sentiment(text)
    if sentiment['sentiment'] == 'positive':
        score += 10
    elif sentiment['sentiment'] == 'negative':
        score -= 10
    
    # Normalize to 0-100 range
    score = max(0, min(100, score))
    
    # Determine level
    if score >= 75:
        level = 'high'
    elif score >= 50:
        level = 'medium'
    else:
        level = 'low'
    
    return {
        'score': round(score, 2),
        'level': level,
        'indicators': {
            'hesitation_count': hesitation_count,
            'assertive_count': assertive_count,
            'uncertainty_count': uncertainty_count,
            'sentiment': sentiment['sentiment']
        }
    }

def calculate_sentiment_score(text: str) -> float:
    """
    Calculate a simple sentiment score (0-100) for interview evaluation
    
    Args:
        text: Input text
        
    Returns:
        float: Score from 0-100
    """
    sentiment = analyze_sentiment(text)
    confidence = analyze_confidence_from_text(text)
    
    # Combine sentiment and confidence
    # Positive sentiment + high confidence = higher score
    # Negative sentiment or low confidence = lower score
    
    compound = sentiment['compound']
    confidence_score = confidence['score']
    
    # Convert compound (-1 to 1) to 0-100 scale
    sentiment_score = ((compound + 1) / 2) * 100
    
    # Weight: 40% sentiment, 60% confidence
    final_score = (sentiment_score * 0.4) + (confidence_score * 0.6)
    
    return round(final_score, 2)

"""
Fluency Scorer
Calculates fluency scores based on speech characteristics
"""

import re
from typing import Dict, List
from ml_models.nlp_processor import tokenize_text, remove_punctuation, detect_grammar_errors_simple

# Common filler words to detect
FILLER_WORDS = [
    'um', 'uh', 'like', 'you know', 'so', 'basically', 'actually',
    'literally', 'right', 'okay', 'well', 'i mean', 'sort of', 'kind of'
]

def calculate_wpm(text: str, duration_seconds: float) -> float:
    """
    Calculate Words Per Minute (WPM)
    
    Args:
        text: Transcript text
        duration_seconds: Audio duration in seconds
        
    Returns:
        float: Words per minute
    """
    if duration_seconds <= 0:
        return 0.0
    
    # Tokenize and count words
    tokens = tokenize_text(text)
    tokens = remove_punctuation(tokens)
    word_count = len(tokens)
    
    # Calculate WPM
    duration_minutes = duration_seconds / 60
    wpm = word_count / duration_minutes if duration_minutes > 0 else 0
    
    return round(wpm, 2)

def detect_filler_words(text: str) -> Dict:
    """
    Detect filler words in text
    
    Args:
        text: Transcript text
        
    Returns:
        dict: {
            'total_count': int,
            'details': list of dict with word and count,
            'density': float (filler words per 100 words)
        }
    """
    text_lower = text.lower()
    
    filler_details = []
    total_count = 0
    
    for filler in FILLER_WORDS:
        count = text_lower.count(filler)
        if count > 0:
            filler_details.append({
                'word': filler,
                'count': count
            })
            total_count += count
    
    # Calculate density (filler words per 100 words)
    tokens = tokenize_text(text)
    tokens = remove_punctuation(tokens)
    word_count = len(tokens)
    
    density = (total_count / word_count * 100) if word_count > 0 else 0
    
    return {
        'total_count': total_count,
        'details': filler_details,
        'density': round(density, 2)
    }

def detect_pauses(text: str) -> Dict:
    """
    Detect pauses in text (represented by ellipsis or multiple spaces)
    
    Args:
        text: Transcript text
        
    Returns:
        dict: {
            'count': int,
            'locations': list of indices
        }
    """
    # Count ellipsis and long pauses
    ellipsis_pattern = r'\.{2,}|\s{3,}|\.\.\.'
    matches = list(re.finditer(ellipsis_pattern, text))
    
    return {
        'count': len(matches),
        'locations': [match.start() for match in matches]
    }

def calculate_fluency_score(
    wpm: float,
    filler_count: int,
    pause_count: int,
    grammar_errors: int,
    word_count: int
) -> float:
    """
    Calculate overall fluency score based on multiple factors
    Score range: 0-100
    
    Scoring criteria:
    - WPM: Ideal range 120-150, penalties outside this range
    - Filler words: Penalty for excessive use
    - Pauses: Penalty for too many pauses
    - Grammar errors: Penalty for errors
    
    Args:
        wpm: Words per minute
        filler_count: Number of filler words
        pause_count: Number of pauses
        grammar_errors: Number of grammar errors
        word_count: Total word count
        
    Returns:
        float: Fluency score (0-100)
    """
    score = 100.0
    
    # WPM scoring (ideal range: 120-150)
    if wpm < 80:
        # Too slow
        score -= (80 - wpm) * 0.3
    elif wpm > 180:
        # Too fast
        score -= (wpm - 180) * 0.2
    elif 120 <= wpm <= 150:
        # Perfect range, small bonus
        score += 5
    
    # Filler words penalty (per filler word per 100 words)
    if word_count > 0:
        filler_density = (filler_count / word_count) * 100
        score -= filler_density * 2
    
    # Pause penalty (per pause per 100 words)
    if word_count > 0:
        pause_density = (pause_count / word_count) * 100
        score -= pause_density * 3
    
    # Grammar errors penalty
    if word_count > 0:
        error_density = (grammar_errors / word_count) * 100
        score -= error_density * 5
    
    # Ensure score is in valid range
    score = max(0, min(100, score))
    
    return round(score, 2)

def analyze_speech_fluency(text: str, duration_seconds: float = 0) -> Dict:
    """
    Complete fluency analysis of speech transcript
    
    Args:
        text: Transcript text
        duration_seconds: Audio duration in seconds (optional)
        
    Returns:
        dict: Complete fluency analysis
    """
    # Calculate WPM
    wpm = 0
    if duration_seconds > 0:
        wpm = calculate_wpm(text, duration_seconds)
    else:
        # Estimate duration assuming average speaking rate of 130 WPM
        tokens = tokenize_text(text)
        tokens = remove_punctuation(tokens)
        word_count = len(tokens)
        duration_seconds = (word_count / 130) * 60
        wpm = 130  # Default average
    
    # Detect filler words
    filler_analysis = detect_filler_words(text)
    
    # Detect pauses
    pause_analysis = detect_pauses(text)
    
    # Detect grammar errors
    grammar_errors = detect_grammar_errors_simple(text)
    
    # Count words
    tokens = tokenize_text(text)
    tokens = remove_punctuation(tokens)
    word_count = len(tokens)
    
    # Calculate fluency score
    fluency_score = calculate_fluency_score(
        wpm=wpm,
        filler_count=filler_analysis['total_count'],
        pause_count=pause_analysis['count'],
        grammar_errors=len(grammar_errors),
        word_count=word_count
    )
    
    # Generate feedback
    feedback = generate_fluency_feedback(
        wpm, filler_analysis, pause_analysis, grammar_errors, fluency_score
    )
    
    return {
        'fluency_score': fluency_score,
        'wpm': wpm,
        'word_count': word_count,
        'duration_seconds': duration_seconds,
        'filler_words': filler_analysis,
        'pauses': pause_analysis,
        'grammar_errors': grammar_errors,
        'feedback': feedback
    }

def generate_fluency_feedback(
    wpm: float,
    filler_analysis: Dict,
    pause_analysis: Dict,
    grammar_errors: List,
    score: float
) -> List[str]:
    """
    Generate specific feedback based on fluency analysis
    
    Returns:
        list: List of feedback strings
    """
    feedback = []
    
    # Overall performance
    if score >= 90:
        feedback.append("Excellent fluency! Your speech is clear and well-paced.")
    elif score >= 75:
        feedback.append("Good fluency with room for minor improvements.")
    elif score >= 60:
        feedback.append("Moderate fluency. Focus on the areas mentioned below.")
    else:
        feedback.append("Fluency needs improvement. Practice regularly for better results.")
    
    # WPM feedback
    if wpm < 80:
        feedback.append(f"Your speaking pace is slow ({wpm} WPM). Try to speak at 120-150 WPM for better clarity.")
    elif wpm > 180:
        feedback.append(f"You're speaking too fast ({wpm} WPM). Slow down to 120-150 WPM for better comprehension.")
    elif 120 <= wpm <= 150:
        feedback.append(f"Perfect speaking pace ({wpm} WPM)! This is ideal for clear communication.")
    
    # Filler words feedback
    if filler_analysis['total_count'] > 5:
        feedback.append(f"You used {filler_analysis['total_count']} filler words. Try to eliminate words like 'um', 'uh', and 'like'.")
        if filler_analysis['details']:
            top_fillers = sorted(filler_analysis['details'], key=lambda x: x['count'], reverse=True)[:3]
            common = ', '.join([f"'{f['word']}' ({f['count']})" for f in top_fillers])
            feedback.append(f"Most common fillers: {common}")
    
    # Pause feedback
    if pause_analysis['count'] > 3:
        feedback.append(f"Detected {pause_analysis['count']} pauses. Practice smooth transitions between thoughts.")
    
    # Grammar feedback
    if len(grammar_errors) > 0:
        feedback.append(f"Found {len(grammar_errors)} potential grammar issues. Review your sentence structure.")
    
    # Positive reinforcement
    if filler_analysis['total_count'] <= 2:
        feedback.append("Great job minimizing filler words!")
    if pause_analysis['count'] <= 2:
        feedback.append("Excellent speech continuity with minimal pauses!")
    
    return feedback

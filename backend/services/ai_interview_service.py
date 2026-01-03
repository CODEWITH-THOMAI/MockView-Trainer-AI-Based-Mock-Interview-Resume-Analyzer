"""
AI Interview Service
Evaluates interview answers using NLP and ML techniques
"""

import json
import os
from typing import Dict, List
from ml_models.nlp_processor import (
    tokenize_text, remove_punctuation, extract_keywords,
    calculate_text_similarity, count_words, count_sentences,
    detect_grammar_errors_simple
)
from ml_models.sentiment_analyzer import analyze_sentiment, calculate_sentiment_score
from config import Config

# Load job keywords
KEYWORDS_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'job_keywords.json')
_keywords_cache = None

def load_job_keywords() -> Dict:
    """Load job keywords from JSON file"""
    global _keywords_cache
    
    if _keywords_cache is not None:
        return _keywords_cache
    
    try:
        with open(KEYWORDS_FILE, 'r') as f:
            _keywords_cache = json.load(f)
        return _keywords_cache
    except Exception as e:
        print(f"Error loading job keywords: {str(e)}")
        return {}

def evaluate_answer_relevance(
    question: str,
    answer: str,
    job_role: str
) -> Dict:
    """
    Evaluate answer relevance using cosine similarity and keyword matching
    
    Args:
        question: Interview question
        answer: User's answer
        job_role: Job role for context
        
    Returns:
        dict: Relevance evaluation with score and details
    """
    # Calculate similarity between question and answer
    similarity_score = calculate_text_similarity(question, answer)
    
    # Extract keywords from answer
    answer_keywords = extract_keywords(answer, top_n=10)
    
    # Get job-specific keywords
    job_keywords_data = load_job_keywords()
    job_keywords = job_keywords_data.get(job_role, [])
    
    # Count how many job-related keywords are in the answer
    keyword_matches = 0
    matched_keywords = []
    
    for keyword in answer_keywords:
        for job_keyword in job_keywords:
            if keyword.lower() in job_keyword.lower() or job_keyword.lower() in keyword.lower():
                keyword_matches += 1
                matched_keywords.append(job_keyword)
                break
    
    # Calculate keyword relevance score (0-100)
    keyword_score = min(100, (keyword_matches / max(len(answer_keywords), 1)) * 100)
    
    # Combined relevance score (weighted average)
    # 60% similarity, 40% keyword matching
    relevance_score = (similarity_score * 100 * 0.6) + (keyword_score * 0.4)
    
    return {
        'score': round(relevance_score, 2),
        'similarity_score': round(similarity_score * 100, 2),
        'keyword_score': round(keyword_score, 2),
        'matched_keywords': matched_keywords[:5],  # Top 5 matched keywords
        'total_keyword_matches': keyword_matches
    }

def evaluate_answer_grammar(answer: str) -> Dict:
    """
    Evaluate grammar quality of the answer
    
    Args:
        answer: User's answer
        
    Returns:
        dict: Grammar evaluation with score and errors
    """
    # Detect grammar errors
    errors = detect_grammar_errors_simple(answer)
    
    # Count words and sentences
    word_count = count_words(answer)
    sentence_count = count_sentences(answer)
    
    # Calculate grammar score (0-100)
    # Start with 100 and deduct points for errors
    base_score = 100
    error_penalty = len(errors) * 5  # 5 points per error
    
    grammar_score = max(0, base_score - error_penalty)
    
    # Check for basic structure
    if word_count < 10:
        grammar_score -= 20  # Too short
    if sentence_count == 0:
        grammar_score -= 30  # No proper sentences
    
    return {
        'score': round(grammar_score, 2),
        'errors': errors,
        'error_count': len(errors),
        'word_count': word_count,
        'sentence_count': sentence_count
    }

def evaluate_answer_completeness(answer: str, question: str) -> Dict:
    """
    Evaluate answer completeness and depth
    
    Args:
        answer: User's answer
        question: Original question
        
    Returns:
        dict: Completeness evaluation
    """
    word_count = count_words(answer)
    sentence_count = count_sentences(answer)
    
    # Score based on answer length and structure
    base_score = 50
    
    # Word count scoring
    if word_count >= 50:
        base_score += 30
    elif word_count >= 30:
        base_score += 20
    elif word_count >= 15:
        base_score += 10
    else:
        base_score -= 20
    
    # Sentence count scoring (indicates structure)
    if sentence_count >= 3:
        base_score += 20
    elif sentence_count >= 2:
        base_score += 10
    
    completeness_score = max(0, min(100, base_score))
    
    return {
        'score': round(completeness_score, 2),
        'word_count': word_count,
        'sentence_count': sentence_count,
        'is_adequate': word_count >= 20 and sentence_count >= 2
    }

def evaluate_interview_answer(
    question: str,
    answer: str,
    job_role: str,
    skill_level: str = 'Beginner'
) -> Dict:
    """
    Complete evaluation of an interview answer
    Uses NLP and ML to score multiple dimensions
    
    Args:
        question: Interview question
        answer: User's answer
        job_role: Job role
        skill_level: Skill level
        
    Returns:
        dict: Complete evaluation with scores and feedback
    """
    # Get evaluation weights from config
    weights = Config.INTERVIEW_WEIGHTS
    
    # Evaluate different aspects
    relevance = evaluate_answer_relevance(question, answer, job_role)
    grammar = evaluate_answer_grammar(answer)
    completeness = evaluate_answer_completeness(answer, question)
    sentiment = calculate_sentiment_score(answer)
    
    # Calculate overall score (weighted average)
    overall_score = (
        relevance['score'] * weights['relevance'] +
        grammar['score'] * weights['grammar'] +
        completeness['score'] * weights['completeness'] +
        sentiment * weights['sentiment']
    )
    
    # Generate feedback
    feedback = generate_answer_feedback(
        relevance, grammar, completeness, sentiment, overall_score
    )
    
    return {
        'overall_score': round(overall_score, 2),
        'relevance': relevance,
        'grammar': grammar,
        'completeness': completeness,
        'sentiment_score': sentiment,
        'feedback': feedback,
        'question': question,
        'answer_preview': answer[:100] + '...' if len(answer) > 100 else answer
    }

def generate_answer_feedback(
    relevance: Dict,
    grammar: Dict,
    completeness: Dict,
    sentiment_score: float,
    overall_score: float
) -> List[str]:
    """
    Generate specific feedback based on evaluation
    
    Returns:
        list: List of feedback strings
    """
    feedback = []
    
    # Overall performance
    if overall_score >= 90:
        feedback.append("Excellent answer! You demonstrated strong understanding.")
    elif overall_score >= 75:
        feedback.append("Good answer with solid content.")
    elif overall_score >= 60:
        feedback.append("Adequate answer, but there's room for improvement.")
    else:
        feedback.append("Your answer needs more development and clarity.")
    
    # Relevance feedback
    if relevance['score'] < 60:
        feedback.append("Try to address the question more directly and use relevant technical terms.")
    elif relevance['matched_keywords']:
        feedback.append(f"Good use of relevant keywords: {', '.join(relevance['matched_keywords'][:3])}")
    
    # Grammar feedback
    if grammar['error_count'] > 0:
        feedback.append(f"Watch out for grammar issues. Found {grammar['error_count']} potential errors.")
    
    # Completeness feedback
    if completeness['word_count'] < 20:
        feedback.append("Your answer is too brief. Provide more details and examples.")
    elif completeness['word_count'] > 200:
        feedback.append("Good detailed answer! Make sure to stay focused on the key points.")
    
    # Confidence feedback (from sentiment)
    if sentiment_score < 50:
        feedback.append("Show more confidence in your responses. Use assertive language.")
    elif sentiment_score >= 75:
        feedback.append("Great confidence level in your answer!")
    
    # Positive reinforcement
    if overall_score >= 75:
        feedback.append("Keep up the good work! Your interview skills are strong.")
    
    return feedback

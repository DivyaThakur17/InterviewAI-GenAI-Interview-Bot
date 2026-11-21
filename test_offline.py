"""
Offline Verification Script for InterviewAI
Tests functions and logic that do not require an active Gemini API key.
"""

import sys
import json
import llm_service

def test_json_extraction():
    print("Testing _extract_json function...")
    
    # Test case 1: Raw JSON string
    raw_json = '{"questions": ["Q1", "Q2", "Q3", "Q4", "Q5"]}'
    res1 = llm_service._extract_json(raw_json)
    assert len(res1["questions"]) == 5, f"Expected 5 questions, got {len(res1['questions'])}"
    print("  ✓ Case 1: Pure JSON string passed.")

    # Test case 2: Markdown fenced JSON (```json ... ```)
    fenced_json = '```json\n{"score": 8, "feedback": "Good job", "strengths": ["Clear"], "improvements": ["More depth"], "ideal_answer": "Complete answer"}\n```'
    res2 = llm_service._extract_json(fenced_json)
    assert res2["score"] == 8, f"Expected score 8, got {res2['score']}"
    print("  ✓ Case 2: Markdown ```json code block passed.")

    # Test case 3: JSON with surrounding prose/notes
    surrounded_json = 'Here is your evaluation:\n{"score": 9, "feedback": "Excellent", "strengths": ["Solid logic"], "improvements": ["None"], "ideal_answer": "Superb"}\nHope this helps!'
    res3 = llm_service._extract_json(surrounded_json)
    assert res3["score"] == 9, f"Expected score 9, got {res3['score']}"
    print("  ✓ Case 3: Embedded JSON with surrounding prose passed.")

def test_missing_api_key_handling():
    print("Testing missing API key handling...")
    try:
        # Pass dummy/empty key
        llm_service.get_gemini_client(api_key="")
        print("  ✗ Failed: Expected ValueError on empty key")
        sys.exit(1)
    except ValueError as e:
        assert "Gemini API Key is not configured" in str(e)
        print("  ✓ Case 4: Correctly rejected missing API key.")

if __name__ == "__main__":
    try:
        test_json_extraction()
        test_missing_api_key_handling()
        print("\nAll offline tests passed successfully!")
    except Exception as e:
        print(f"\nOffline test failed: {e}")
        sys.exit(1)

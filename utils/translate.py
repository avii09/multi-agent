# utils/translate.py

def translate_to_english(llm, user_input: str) -> str:
    """
    Translate non-English queries to English using CrewAI's LLM.
    """
    prompt = f"""
    Translate this text to English:

    "{user_input}"

    Return only the English translation without extra notes or formatting.
    """
    return llm.invoke(prompt)

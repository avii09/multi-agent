def translate_to_english(llm, user_input: str) -> str:
    """
    Translate non-English queries to English using CrewAI's LLM.
    """
    prompt = f"""
    Translate this text to English:

    "{user_input}"

    Return only the English translation without extra notes or formatting.
    """
    
    # Use the correct method for CrewAI LLM
    try:
        # CrewAI LLM objects typically use 'call' method
        response = llm.call(prompt)
        return response.strip()
    except AttributeError:
        # Fallback: try other common methods
        try:
            response = llm.generate(prompt)
            return response.strip()
        except AttributeError:
            # If translation fails, return original input
            print(f"Warning: Could not translate '{user_input}', using original text")
            return user_input

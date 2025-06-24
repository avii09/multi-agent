def translate_to_english(llm, user_input: str) -> str:
    """
    Translate non-English queries to English using CrewAI's LLM.
    """
    prompt = f"""
    Translate this text to English:

    "{user_input}"

    Return only the English translation without extra notes or formatting.
    """
    
    
    try:
        
        response = llm.call(prompt)
        return response.strip()
    except AttributeError:
        
        try:
            response = llm.generate(prompt)
            return response.strip()
        except AttributeError:
            
            print(f"Warning: Could not translate '{user_input}', using original text")
            return user_input

OPENAI_PRICING = {
    # GPT-4 Turbo (supports JSON mode)
    "gpt-4-0125-preview": {  # GPT-4 Turbo
        "input": 0.01,   # $0.01 per 1K tokens
        "output": 0.03,  # $0.03 per 1K tokens
        "mode": "json"   # Supports JSON mode
    },
    "gpt-4-turbo-preview": {  # Alias for gpt-4-0125-preview
        "input": 0.01,   # $0.01 per 1K tokens
        "output": 0.03,  # $0.03 per 1K tokens
        "mode": "json"   # Supports JSON mode
    },
    # GPT-4 (supports function calling)
    "gpt-4": {
        "input": 0.03,   # $0.03 per 1K tokens
        "output": 0.06,  # $0.06 per 1K tokens
        "mode": "function"  # Supports function calling
    },

    "gpt-4-0613": {
        "input": 0.03,   # $0.03 per 1K tokens
        "output": 0.06,  # $0.06 per 1K tokens
        "mode": "function"  # Supports function calling
    },
    # GPT-3.5 Turbo (supports JSON mode)
    "gpt-3.5-turbo": {
        "input": 0.0005,   # $0.0005 per 1K tokens
        "output": 0.0015,  # $0.0015 per 1K tokens
        "mode": "json"     # Supports JSON mode
    },
    "gpt-3.5-turbo-0125": {
        "input": 0.0005,   # $0.0005 per 1K tokens
        "output": 0.0015,  # $0.0015 per 1K tokens
        "mode": "json"     # Supports JSON mode
    },
    "gpt-3.5-turbo-1106": {
        "input": 0.0010,   # $0.0010 per 1K tokens
        "output": 0.0020,  # $0.0020 per 1K tokens
        "mode": "json"     # Supports JSON mode
    }
}
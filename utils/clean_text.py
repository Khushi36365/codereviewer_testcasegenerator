def clean_text(obj):
    if isinstance(obj, dict):
        return {k: clean_text(v) for k, v in obj.items()}

    if isinstance(obj, list):
        return [clean_text(item) for item in obj]

    if isinstance(obj, str):
        return obj.replace("\\n", "\n")

    return obj
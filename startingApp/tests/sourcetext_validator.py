def validate_sourcetext(text):
    if isinstance(text, str) and len(text) > 0:
        return True
    else:
        return False

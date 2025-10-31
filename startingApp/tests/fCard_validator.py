def validate_fCard(fcard, max_length=200):
    """
    Validates a single flashcard.

    A valid flashcard must:
    - Be a list or tuple
    - Contain exactly two string elements [front, back]
    - Both front and back must be non-empty strings
    - Neither front nor back exceed `max_length` characters
    """
    if not isinstance(fcard, (list, tuple)):
        return False
    if len(fcard) != 2:
        return False

    front, back = fcard
    if not (isinstance(front, str) and isinstance(back, str)):
        return False
    if not (front.strip() and back.strip()):
        return False
    if len(front) > max_length or len(back) > max_length:
        return False

    return True


def validate_fCardAmount(amount):
    """
    Validates the total flashcard count.
    Must be an integer between 1 and 1000 (inclusive).
    """
    return isinstance(amount, int) and 1 <= amount <= 1000

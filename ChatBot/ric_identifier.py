def identify_ric(sentence: str) -> str:
    for word in sentence.split(" "):
        if word.startswith(".") or "." in word[-3:]:
            return word.upper()
    return ""

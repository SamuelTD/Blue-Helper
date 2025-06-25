import re

def clean_answer(text):
    text = re.sub(r"^(Hi|Hello|Dear)[^\n,]*[,:\n]+\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"(Thank you.*|Thanks[^\n]*|Best regards.*|Kind regards.*|Regards.*|You're welcome.*)", "", text, flags=re.IGNORECASE)
    text = re.sub(r"(Please\s(click|accept|upvote)[^.\n]*|If the answer is helpful.*|Marking answer as accepted.*|Click 'Accept Answer'.*)", "", text, flags=re.IGNORECASE)
    text = re.sub(r"(Excellent response.*|Great answer.*|Glad it helped.*|Beautiful\.? Thank you.*)", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\n{2,}", "\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n\s+", "\n", text)
    text = re.sub(r"^\s*-\s*\w+\s*$", "", text)
    return text.strip()

def clean_question(text):
    # Juste les espaces / retours à la ligne
    text = re.sub(r"\n{2,}", "\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n\s+", "\n", text)
    return text.strip()

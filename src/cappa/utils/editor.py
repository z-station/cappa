
def clear_text(text: str):

    """ Удаляет из строки лишние спец. символы, которые добавляет Ace-editor """

    if isinstance(text, str):
        return text.replace('\r', '').rstrip('\n')
    else:
        return text

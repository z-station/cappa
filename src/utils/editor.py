
def clear_text(text: str):

    """ Удаляет из строки лишние спец. символы, которые добавляет Ace-editor """

    cleared_text = text.replace('\r', '').strip('\n')
    return cleared_text

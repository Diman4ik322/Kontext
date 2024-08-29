from typing import Dict, Tuple
from random import choice
import gensim.downloader as api
from pymystem3 import Mystem
 
 
model = api.load('word2vec-ruscorpora-300')
 
def get_lemma(word: str) -> str:  # Делаю -> делать
    """Возвращает лемму слова.
    Parameters:
        word (str): Слово для лемматизации.
    Returns:
        str: Лемма слова.
    """
    m = Mystem()
    lemma = m.lemmatize(word)
    return lemma[0]
 
def select_random_word() -> str:
    """Выбирает случаное слово из первых 100 слов модели.
    Returns:
        str: Случайное слово
    """
    item = choice(list(model.key_to_index.items())[:100])
    return item[0].split("_")[0]
 
def get_most_similar_dict(word: str, topn: int) -> Dict[str, int]:
    """Возвращает словарь наиболее похожих слов с их индексами.
    Parameters:
        word (str): Слово для поиска ниболее похожих слов.
        topn (int): Кол-во похожих слов для поиска.
    Returns:
        Dict[str, int]: Словарь наиболее похожих слов с их индексами.
    """
    d = {k.split("_")[0]: k for k in model.key_to_index} # {слово: 1, слово: 2}
    vals = model.most_similar(d[word], topn=topn)
    d_ = {k.split("_")[0]: i + 2 for i, (k, v) in enumerate(vals) if ":" not in k}
    return d_
 
def get_placement(word: str, word_dict: Dict[str, int]) -> int:
    """Возвращает позицию леммы слова в словаре.
    Parameters:
        word (str): Слово для поиска.
        word_dict (Dict[str, int]): Словарь слов с их индексами.
    Returns:
        int: Индекс леммы слова в словаре или -1, если леммы в словаре нет.
    """
    lemma = get_lemma(word)
    if lemma in word_dict:
        return word_dict[lemma]
    return -1
 
def init() -> Tuple[str, Dict[str, int]]:
    """Инициализирует процесс выбора случайного слова и создания словаря наиболее подходящих слов.
    Returns:
        Tuple[str, Dict[str, int]]: Кортеж, содержащий случайное слово и словарь наиболее подходящих слов с их индексами.
    """
    init_word = select_random_word()
    word_dict = get_most_similar_dict(init_word, 100000)
    return init_word, word_dict
 
if __name__ == "__main__":
    word, word_dict = init()
    print(f"Слово: {word}")
    ans = input("-> ")
    print(f"Позиция: {get_placement(ans, word_dict)}")
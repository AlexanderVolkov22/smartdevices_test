is_anagram = lambda x1, x2: sorted(x1.lower()) == sorted(x2.lower())


def anagrams(x1, x2):
    return is_anagram(x1, x2)

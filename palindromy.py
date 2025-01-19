def is_palindrome(word):

    clean_word = [s for s in word.lower() if s.isalnum()]

    return clean_word == clean_word[::-1]


print(is_palindrome("Kobyła ma mały B,O,K"))
print(is_palindrome("ot, i w tramwaju karota!"))
print(is_palindrome("A to kanonadę dano na kota."))
print(is_palindrome("Łapał za kran, a kanarka złapał."))
print(is_palindrome("Może jutro ta dama sama, da tortu jeżom."))
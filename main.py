def translate_word_from_language(word, language_from):

    trans_index = 0
    match = False
    pozice = 0

    words_cz = ["pivo", "salam", "pocitac"]
    words_en = ["beer", "sausage", "computer"]

    if language_from == "CZ":
        words_from = words_cz
        words_to = words_en
    elif language_from == "EN":
        words_from = words_en
        words_to = words_cz

    for slovo in words_from:
        if slovo == word:
            match = True
            trans_index = pozice
            break
        pozice = pozice + 1
    if match == True:
        print(str(word) + " = " + words_to[trans_index])
    else:
        print("Toto slovo nemam v databazi!")
        # exit(102)


print("Vitej ve slovniku (CZ-EN)!")
again = True

while again is True:

    language_from = input("Z jakeho jazyka? (CZ nebo EN): ")
    language_from = language_from.upper()

    if not language_from in ("CZ", "EN"):
        print("!!!NENI PODPOROVANY JAZYK!!!")
        continue

    word = input("Zadej slovo na preklad: ")

    translate_word_from_language(word, language_from)

    again = input("Chces prelozit jeste neco? ")

    again = again.upper()
    if again in ("ANO", "YES"):
        again = True
    else:
        again = False



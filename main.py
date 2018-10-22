print("Vitej ve slovniku (CZ-EN)!")
again = True

while again is True:
    trans_index = 0
    match = False
    pozice = 0

    language_from = input("Z jakeho jazyka? (CZ nebo EN): ")

    if not language_from in ("CZ", "EN", "cz", "en"):
        print("!!!NENI PODPOROVANY JAZYK!!!")
        exit(101)

    words_cz = ["pivo", "salam", "pocitac"]
    words_en = ["beer", "sausage", "computer"]

    word = input("Zadej slovo na preklad: ")

    if language_from in ("CZ", "cz"):
        for slovo in words_cz:
            if slovo == word:
                match = True
                trans_index = pozice
            pozice = pozice + 1
        print(str(word) + " = " + words_en[trans_index])
    if language_from in ("EN", "en"):
        for slovo in words_en:
            if slovo == word:
                match = True
                trans_index = pozice
            pozice = pozice + 1
        print(str(word) + " = " + words_cz[trans_index])

    if match is False:
        print("Toto slovo nemam v databazi!")
        exit(102)

    again = input("Chces prelozit jeste neco? ")

    if again in ("ano", "ANO", "yes", "YES"):
        again = True
    else:
        again = False

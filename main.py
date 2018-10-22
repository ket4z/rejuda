print("Vitej ve slovniku (CZ-EN)")
language_from = input("Z jakeho jazyka? (CZ nebo EN)")

if not language_from in ("CZ", "EN"):
	print("neni podporovany jazyk")
	exit(101)

words_cz = ["pivo", "salam", "pocitac"]
words_en = ["beer", "sausage", "computer"]

word = input("Zadej slovo na preklad")

match = False
pozice = 0
if language_from == "CZ":
	for slovo in words_cz:
		if slovo == word:
			match = pozice
		pozice = pozice + 1

if match == False:
	print("Toto slovo nemam v slovniku")
	exit(102)

print(words_en[match])

# print("Nasel jsem slovo na pozici " + str(match))

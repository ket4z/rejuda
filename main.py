print("Toto bude za chvili nejgenialnejsi slovnik")
print("vytvori TomasNepala")

words = {"house":"dum", "apple":"jablko", "tree":"strom", "horse":"kun", "yellow":"zluta", "keyboard":"klavesnice", "water":"voda", "start":"zacatek", "city":"mesto","ear":"ucho", "nice":"hezky", "tooth":"zub"}
slova = {"dum":"house", "jablko":"apple", "strom":"tree", "kun":"horse", "zluta":"yellow", "klavesnice":"keyboard", "voda":"water", "zacatek":"start", "mesto":"city","ucho":"ear", "hezky":"nice", "zub":"tooth"}

toorfrom = raw_input("write FROM_ENGLISH if you want to translate to czech or FROM_CZECH if you want to translate to english")

word = raw_input("Enter the word you want to translate")

def translate(key):
    if words.has_key(key):
        print words.get(key)
    else:
        print ("Sorry that word doesn't exist in Czech!")

def prelozit(key):
    if slova.has_key(key):
        print slova.get(key)
    else:
        print ("Sorry that word doesn't exist in English!")

if (toorfrom == "FROM_ENGLISH"):
    translate(word)

if (toorfrom == "FROM_CZECH"):
    prelozit(word)
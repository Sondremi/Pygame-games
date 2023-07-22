import random as rd
def hangman():

    ordliste = [
    "bok", "hund", "hus", "bil", "skole", "katt", "fotball", "sykkel", "mat", "seng",
    "stol", "datamaskin", "vegg", "natur", "fugl", "vindu", "by", "familie", "musikk", "vann",
    "fisk", "hage", "nese", "sang", "glede", "trær", "hav", "hår", "fjell", "sjø",
    "sol", "måne", "snø", "lys", "kaffe", "te", "øye", "farge", "himmel", "høst",
    "vår", "sommer", "vinter", "regn", "glede", "lese", "skrive", "spise", "sove", "løpe",
    "gå", "lage", "se", "høre", "tenke", "le", "smile", "hånd", "fot", "arm",
    "ben", "mage", "rygg", "hals", "ansikt", "skulder", "hode", "kne", "tå", "øre",
    "natt", "dag", "stjerne", "blomst", "frukt", "grønnsak", "dyr", "barn", "voksen", "gamle",
    "ung", "venn", "kjærlighet", "helse", "gave", "tid", "penger", "jobb", "reise", "drøm",
    "hobby", "lære", "skole", "universitet", "land", "by", "frihet", "historie", "kultur", "språk"
    ]
    fasit_ord = rd.choice(ordliste)

    gjettet = []
    riktige = []
    if len(fasit_ord) < 10:
        liv = 10
    else:
        liv = len(fasit_ord)+1

    output_ord = list("_" * len(fasit_ord))
    print("\n" + "".join(output_ord))

    spill = True
    while spill:
        if liv >= 0:
            print(f"\nDu har {liv} liv")
            if "".join(output_ord) != fasit_ord:
                
                bruker_gjett = str(input("Gjett en bokstav: "))
                
                if bruker_gjett not in gjettet:
                    gjettet.append(bruker_gjett)

                    if bruker_gjett in fasit_ord:
                        print("Bokstaven er i ordet")
                    else:
                        print("Bokstaven er ikke i ordet")
                        liv -= 1

                    teller = 0
                    for bokstav in fasit_ord:
                        teller += 1
                        if bruker_gjett == bokstav:
                            output_ord[teller-1] = bruker_gjett
                            riktige.append(bruker_gjett)

                    print("\n")
                    print("".join(output_ord))

                else:
                    print(f"Du har allerede gjetter {bruker_gjett}")

            else:
                print(f"\nDu vant! \nDu klarte å gjette ordet {fasit_ord}\n")
                spill = False
        else:
            print(f"\nDu tapte! \nDu gikk tom for liv. \nOrdet var {fasit_ord}")
            spill = False
        
hangman()
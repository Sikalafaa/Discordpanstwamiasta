"""
Polskie imiona żeńskie i męskie — znormalizowane (bez ogonków, małe litery).
Źródło: GUS (Główny Urząd Statystyczny) — lista najpopularniejszych imion w Polsce.
"""

IMIONA: set[str] = {
    # ── Imiona żeńskie ────────────────────────────────────────────────────
    "ada", "adela", "adelaida", "adelajda", "adriana", "agata",
    "agnieszka", "agrafena", "ala", "alberta", "albina", "aldona",
    "aleksandra", "alicja", "alina", "aliza", "alma", "alona",
    "amalia", "amelia", "anastazja", "andżelika", "andzielika",
    "aneta", "angelika", "aniela", "anita", "anna", "antonina",
    "anuszka", "ariadna", "arkadiuszka",

    "barbara", "beata", "benedykta", "berenika", "bernadeta",
    "blanka", "bożena", "bozena", "bronisława", "bronislawa",

    "celina", "cecylia",

    "dagmara", "danuta", "daria", "darya", "dominika",
    "dorota",

    "edyta", "eleonora", "eliza", "elżbieta", "elzbieta",
    "emilia", "emma", "ewa", "ewelina",

    "faustyna", "felicja", "filomena", "florentyna",
    "franciszka",

    "gabriela", "genowefa", "grażyna", "grazyna",

    "halina", "hanna", "helena", "henryka",

    "ida", "ilona", "ina", "irena", "iryna", "izabela",
    "izabela",

    "jadwiga", "janina", "joanna", "jolanta", "józefina",
    "jozefina", "julia", "justyna",

    "kamila", "karina", "karolina", "katarzyna", "kinga",
    "klara", "klaudia", "krystyna",

    "laura", "liwia", "lidia", "liliana", "lillia",
    "lucja", "lucia", "ludmila", "ludmiła",

    "łucja",

    "magdalena", "małgorzata", "malwina", "maria",
    "mariola", "marta", "matylda", "michalina",
    "malgorzata", "milena", "miriam", "monika",

    "natalia", "natasha", "nikola", "nina",

    "oliwia", "olga",

    "patrycja", "paula", "paulina", "petra",

    "renata", "róża", "roza",

    "sabina", "sandra", "sara", "sylwia",

    "tamara", "teresa",

    "urszula",

    "wanda", "weronika", "wiktoria",

    "zofia", "zuzanna",

    # ── Zdrobnienia żeńskie ───────────────────────────────────────────────
    # Ada, Adela
    "adzia",
    # Agnieszka
    "aga", "agusia", "niusia",
    # Aleksandra
    "ola", "ola", "oleńka", "olenka", "alesia",
    # Alicja
    "ala", "alusia",
    # Amelia
    "amelka",
    # Anna
    "ania", "anka", "aneczka", "anulka", "anusia",
    # Barbara
    "basia", "baśka", "baska",
    # Beata
    "beatka",
    # Dominika
    "domi", "dominika",
    # Dorota
    "dorotka", "dosia",
    # Elżbieta
    "ela", "elka", "elusia",
    # Emilia
    "emilka", "emka",
    # Ewa
    "ewka", "ewusia",
    # Gabriela
    "gabrysia", "gabka",
    # Grażyna
    "grażka", "grazka",
    # Halina
    "halka", "halusia",
    # Hanna
    "hania", "hanka",
    # Helena
    "hela", "helenka",
    # Irena
    "irka", "irenka",
    # Izabela
    "iza", "izka", "izabelka",
    # Joanna
    "asia", "joasia", "joanka",
    # Jolanta
    "jola", "jolka",
    # Julia
    "julka", "julcia",
    # Justyna
    "justynka",
    # Kamila
    "kamka", "kamilka",
    # Karolina
    "karolka", "karo",
    # Katarzyna
    "kasia", "katka",
    # Klaudia
    "klaudka",
    # Krystyna
    "krysia", "kryska",
    # Magdalena
    "magda", "madzia", "magdzia",
    # Małgorzata
    "gosia", "goska", "małgosia", "malgosia",
    # Maria
    "marysia", "maryśka", "marysiak", "marys", "maja",
    # Marta
    "martusia", "martka",
    # Monika
    "moniczka", "monka",
    # Natalia
    "natka", "natalka",
    # Nikola
    "niki",
    # Oliwia
    "oliwka",
    # Patrycja
    "patka", "patrycka",
    # Paula / Paulina
    "paulinka", "paulka",
    # Sylwia
    "sylwka",
    # Teresa
    "terenia", "teska",
    # Urszula
    "ula", "ulka", "urszulka",
    # Weronika
    "werka", "weroniczka",
    # Wiktoria
    "wika", "wikta",
    # Zofia
    "zosia", "zośka", "zoska",
    # Zuzanna
    "zuzia", "zuzka",

    # ── Imiona męskie ──────────────────────────────────────────────────────
    "adam", "adrian", "albert", "aleksander", "aleksiej",
    "aleksy", "alfred", "andrzej", "arkadiusz", "artur",
    "august",

    "bartłomiej", "bartlomiej", "bartosz", "benedykt",
    "bernard", "bogdan", "bogumił", "bogusław", "bolesław",
    "boleslaw", "boguslav",

    "cezary", "cyprian", "czesław", "czeslaw",

    "damian", "daniel", "dariusz", "dawid", "dominik",

    "edward", "emil", "eryk",

    "fabian", "feliks", "filip", "franciszek",

    "grzegorz",

    "henryk", "hubert", "hugo",

    "igor", "ireneusz",

    "jacek", "jakub", "jan", "jarosław", "jaroslaw",
    "jerzy", "józef", "jozef",

    "kamil", "karol", "kazimierz", "kacper", "konrad",
    "krystian", "krzysztof",

    "lech", "leon", "leszek", "lubomir", "ludwik",
    "łukasz", "lukasz",

    "maciej", "marek", "marcin", "mariusz", "mateusz",
    "max", "michał", "michal", "mieczysław", "mieczyslaw",
    "mikołaj", "mikolaj", "mirosław", "miroslaw",

    "norbert",

    "oskar",

    "paweł", "pawel", "piotr", "przemysław", "przemyslaw",

    "radosław", "radoslaw", "rafał", "rafal", "remigiusz",
    "robert", "roman",

    "sebastian", "sławomir", "slawomir", "stanisław",
    "stanislaw", "stefan",

    "tadeusz", "tomasz",

    "waldemar", "wiesław", "wieslaw", "witold",
    "władysław", "wladyslaw", "wojciech",

    "zbigniew", "zygmunt",

    # ── Zdrobnienia męskie ────────────────────────────────────────────────
    # Adam
    "adaś", "adas",
    # Adrian
    "adek",
    # Aleksander
    "alek", "olek", "aleksek",
    # Andrzej
    "andrzejek", "jędrek", "jedrek",
    # Arkadiusz
    "arek",
    # Artur
    "arturek",
    # Bartosz / Bartłomiej
    "bartek", "barteczek",
    # Bogdan
    "bogdanek",
    # Damian
    "damianek",
    # Daniel
    "danek",
    # Dariusz
    "darek",
    # Dawid
    "dawidek",
    # Dominik
    "domek",
    # Emil
    "emilek",
    # Filip
    "filipek",
    # Franciszek
    "franek", "franio",
    # Grzegorz
    "grześ", "grzesiek", "grzesiek",
    # Henryk
    "heniek", "heniu",
    # Hubert
    "hubertek",
    # Jacek
    "jacuś", "jacus",
    # Jakub
    "kuba", "kubek", "kubeczek",
    # Jan
    "janek", "jasio", "jasiek",
    # Jarosław
    "jarek",
    # Jerzy
    "jurek",
    # Józef
    "józek", "jozek",
    # Kamil
    "kamilek",
    # Karol
    "karolek",
    # Kazimierz
    "kazik",
    # Konrad
    "konradek",
    # Krzysztof
    "krzysiek", "krzyś", "krzys",
    # Łukasz
    "łukaszek", "lukaszek",
    # Maciej
    "maciek",
    # Marcin
    "marcinek",
    # Marek
    "marecek",
    # Mariusz
    "mario",
    # Mateusz
    "mateuszek", "matek",
    # Michał
    "michalek", "michałek",
    # Mikołaj
    "mikolajek", "mikołajek",
    # Paweł
    "pawełek", "pawel", "pawełek",
    # Piotr
    "piotrek", "piotruś", "piotrus",
    # Przemysław
    "przemek",
    # Rafał
    "rafałek", "rafalek",
    # Robert
    "robek",
    # Sławomir
    "sławek", "slawek",
    # Stanisław
    "stasiek", "stas",
    # Stefan
    "stefanek",
    # Tadeusz
    "tadek", "tadzio",
    # Tomasz
    "tomek", "tomeczek",
    # Waldemar
    "waldek",
    # Witold
    "witek",
    # Wojciech
    "wojtek", "wojeciech",
    # Zbigniew
    "zbyszek", "zbysio",
}

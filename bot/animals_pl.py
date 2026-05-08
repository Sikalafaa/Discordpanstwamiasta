"""
Polskie nazwy zwierząt — znormalizowane (bez ogonków, małe litery).
Zawiera: ssaki, ptaki, ryby, gady, płazy, owady, pajęczaki i inne.
"""

ZWIERZETA: set[str] = {
    # ── Ssaki ──────────────────────────────────────────────────────────────
    "alpaka", "antylopa", "arktyczny lis", "afrykanski slon",

    "bawół", "bawol", "bielik", "bizon", "borsuk",
    "bóbr", "bobr",

    "chomik", "cielę", "ciele",

    "delfin", "dzik", "dziko", "dingo",

    "foka", "fretka",

    "gepard", "goryl",

    "hiena",

    "jeleń", "jelen", "jeż", "jez",

    "kangur", "koala", "koc", "koczkodan", "konie", "konik",
    "konia", "koń", "kon", "kos", "kot", "koza",
    "kret", "królik", "krolik", "krowa", "krokodyl", "kukurydza",

    "lama", "lampart", "las", "lew", "lis", "lisica", "liszka",
    "łasica", "lasica", "łoś", "los", "łosoś", "losios",

    "małpa", "malpa", "mandryl", "mors",
    "mrówkojad", "mrowkojad",
    "mysz", "myszka",

    "nawalka", "niedźwiedź", "niedzwiedz", "norka", "nutria",

    "ocelot", "orangutan", "orka", "owca",

    "panda", "pantera", "pies", "pigmej",
    "pingwin", "pirannia", "płetwal", "pletwal",

    "renifer", "ryś", "rys",

    "słoń", "slon", "surykatka",

    "szakal", "szympans",

    "świnka", "swinka", "świnia", "swinia",

    "tasmański diabeł", "tasmanski diabel",
    "tapir", "tygrys",

    "wiewiórka", "wiewiorka", "wil", "wilk",
    "wieloryb",

    "zebra", "żbik", "zbik", "żubr", "zubr",

    # ── Ptaki ──────────────────────────────────────────────────────────────
    "albatros", "ara",

    "bocian", "bocianka", "byk",

    "czajka", "czapla",

    "dudek",

    "flaming",

    "gęś", "ges", "gołąb", "golab", "gruszka",
    "grudzień", "grudzien",

    "ibis",

    "jastrząb", "jastrzab", "jaskółka", "jaskolka",

    "kakadu", "kanarek", "kawka",
    "kogut", "kondor", "kos", "krogulec", "kukułka", "kukulka",

    "łabędź", "labedz", "łyska", "lyska",

    "marabut", "mewa",
    "muchołówka", "mucholowka",

    "orlik", "orzeł", "orzel", "owadożer",

    "papuga", "paw", "pelikan", "perkoz",
    "pijawka", "pingwin", "pliszka",
    "przepiórka", "przepiorka",

    "remiz", "rybitwa",

    "skowronek", "słonka", "slonka", "sokół", "sokol",
    "sroka", "sowa",
    "struś", "strus", "szpak", "szczygieł", "szczygiel",

    "świergotek",

    "wrona", "wróbel", "wrobel",

    "zimorodek", "żuraw", "zuraw",

    # ── Ryby i stworzenia wodne ────────────────────────────────────────────
    "dorsz", "delfin",

    "flądra", "fladra",

    "gardłosz", "głowatek", "glowatek",

    "halibut",

    "jesiotr", "jazgarz",

    "karaś", "karas", "karmazyn", "karp",
    "kałamarnica", "kalamarnica",
    "krab", "krewetka",

    "langusta", "leszcz", "lin",
    "łosoś", "losos",

    "makrela", "manta", "meduza", "morszczuk",

    "okoń", "okon", "ośmiornica", "osmiornica",

    "palia", "pijawka", "pirania", "płotka", "plotka",

    "rekina", "rekin", "rak",

    "sandacz", "sardynka", "szczupak",

    "śledź", "sledz",

    "troć", "troc", "tuńczyk", "tunczyk",

    "węgorz", "wegorz",

    "złota rybka", "zlota rybka",

    # ── Gady ──────────────────────────────────────────────────────────────
    "agama", "anakonda",

    "bazyliszek", "boa",

    "chameleon", "kameleon",

    "gekon",

    "iguana",

    "jaszczurka", "jombo",

    "kobra", "komodo",
    "krokodyl",

    "legwan",

    "pyton",

    "salamandra",

    "ślimak", "slimak",

    "tuatara",

    "warana", "waranowate",

    "żmija", "zmija", "żółw", "zolw",

    # ── Płazy ──────────────────────────────────────────────────────────────
    "axolotl",

    "ropucha",

    "traszka",

    "żaba", "zaba",

    # ── Owady ─────────────────────────────────────────────────────────────
    "biedronka",

    "chrząszcz", "chrzaszcz",

    "giez",

    "komar", "kret",

    "libella", "lić",

    "modliszka", "mrówka", "mrowka", "mucha",

    "osa",

    "pasikonik", "pluskwa", "pszczoła", "pszczola",

    "rusałka",

    "stonka", "świerszcz", "swierszcz",

    "termit",

    "ważka", "wazka", "wszerz",

    "żuk", "zuk",

    # ── Pajęczaki ──────────────────────────────────────────────────────────
    "pająk", "pajak",

    "kleszcz", "krab",

    "ptak",

    "skorpion",

    "tarantula",

    # ── Inne ──────────────────────────────────────────────────────────────
    "dżdżownica", "dzdzownica",

    "gąbka", "gabka",

    "koral",

    "mięczak", "mieczak",

    "polip",

    "rozgwiazda",

    "stonoga",
}

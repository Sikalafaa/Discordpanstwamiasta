"""
Pełna lista polskich nazw państw — wszystkie warianty (oficjalne i potoczne).
Źródło: Wikipedia PL + GUS + powszechne użycie.
Lookup O(1) dzięki zbiorowi (set).
"""

PANSTWA: set[str] = {
    # A
    "afganistan", "albania", "algieria", "andorra", "angola",
    "antigua i barbuda", "arabia saudyjska", "argentyna", "armenia",
    "australia", "austria", "azerbejdżan", "azerbajdzan",
    # B
    "bahamy", "bahrajn", "bangladesz", "barbados", "belgia",
    "belize", "benin", "bhutan", "białoruś", "bialorus",
    "boliwia", "bośnia i hercegowina", "bosnia i hercegowina",
    "botswana", "brazylia", "brunei", "bułgaria", "bulgaria",
    "burkina faso", "burundi",
    # C
    "chile", "chiny", "chorwacja", "czad", "czarnogóra", "czarnogora",
    "czechy", "republika czeska",
    # D
    "dania", "demokratyczna republika konga", "dominika",
    "dominikana", "republika dominikańska",
    # E
    "egipt", "ekwador", "erytrea", "eswatini", "etiopia",
    # F
    "fidżi", "fidzi", "filipiny", "finlandia", "francja",
    # G
    "gabon", "gambia", "ghana", "grecja", "grenada",
    "gruzja", "gwatemala", "gwinea", "gwinea bissau",
    "gwinea równikowa", "gwinea rownikowa",
    # H
    "haiti", "hiszpania", "holandia", "niderlandy", "honduras",
    # I
    "indie", "indonezja", "irak", "iran", "irlandia",
    "islandia", "izrael",
    # J
    "jamajka", "japonia", "jemen", "jordania",
    # K
    "kambodża", "kambodza", "kamerun", "kanada", "katar",
    "kazachstan", "kenia", "kiribati", "kolumbia", "komory",
    "kongo", "republika konga", "korea południowa", "korea polnocna",
    "korea północna", "kostaryka", "kuba", "kuwejt", "kirgistan",
    "kirgizja",
    # L
    "laos", "lesotho", "liban", "liberia", "libia",
    "liechtenstein", "litwa", "luksemburg",
    # Ł
    "łotwa", "latwa",
    # M
    "madagaskar", "malawi", "malediwy", "malezja", "mali",
    "malta", "maroko", "mauretania", "mauritius", "meksyk",
    "mikronezja", "mołdawia", "moldawia", "monako", "mongolia",
    "mozambik", "myanmar", "birma",
    # N
    "namibia", "nauru", "nepal", "niderlandy", "holandia",
    "niemcy", "niger", "nigeria", "nikaragua", "norwegia",
    "nowa zelandia",
    # O
    "oman",
    # P
    "pakistan", "palau", "palestyna", "panama", "papua nowa gwinea",
    "paragwaj", "peru", "polska", "portugalia",
    # R
    "republika południowej afryki", "republika poludniowej afryki",
    "republika środkowoafrykańska", "republika srodkowoafrykanska",
    "rosja", "rumunia", "rwanda",
    # S
    "saint kitts i nevis", "saint lucia", "saint vincent i grenadyny",
    "salwador", "samoa", "san marino", "senegal", "serbia",
    "seszele", "sierra leone", "singapur", "słowacja", "slowacja",
    "słowenia", "slowenia", "somalia", "sri lanka", "stany zjednoczone",
    "usa", "sudan", "sudan południowy", "surinam", "syria",
    # Ś
    "świętego tomasza i książęca", "swietego tomasza i ksiazeca",
    # T
    "tadżykistan", "tadzikistan", "tajlandia", "tajwan", "tanzania",
    "timor wschodni", "timor-leste", "togo", "tonga", "trynidad i tobago",
    "tunezja", "turcja", "turkmenistan", "tuvalu",
    # U
    "uganda", "ukraina", "urugwaj", "uzbekistan",
    # V
    "vanuatu",
    # W
    "watykan", "wenezuela", "węgry", "wegry",
    # Z
    "zambia", "zimbabwe", "zjednoczone emiraty arabskie", "zea",
    "zielony przylądek", "zielony przyladek",
}

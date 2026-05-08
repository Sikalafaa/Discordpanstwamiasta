"""
Polskie nazwy roślin — znormalizowane (bez ogonków, małe litery).
Zawiera: drzewa, krzewy, kwiaty, warzywa, owoce, zioła, trawy, grzyby.
"""

ROSLINY: set[str] = {
    # ── Drzewa ────────────────────────────────────────────────────────────
    "akacja", "akacjowate",

    "baoban", "baobab", "brzoza", "buk",

    "cedr", "cyprys", "cis",

    "dąb", "dab", "drzewo oliwne",

    "eukaliptus",

    "figowiec",

    "grab",

    "irga",

    "jabłoń", "jablon", "jarzębina", "jarzebina",
    "jałowiec", "jalowiec", "jodła", "jodla",

    "kasztan", "klon",

    "lipa",

    "magnolia", "mango", "mahoń", "mahon", "modrzew",

    "niesplina",

    "orzech", "oliwka",

    "palma", "platana", "platan",

    "sekwoja",

    "sosna", "świerk", "swiek",

    "topola", "tulipanowiec",

    "wierzba", "wiśnia", "wisnia",

    "jesion",

    # ── Krzewy ────────────────────────────────────────────────────────────
    "agrest",

    "berberys",

    "dereń", "deren",

    "forsycja",

    "głóg", "glog",

    "jaśmin", "jasmin", "jałowiec", "jalowiec",

    "kalina", "krzak",

    "leszczyna", "liguster",

    "malina",

    "pigwowiec",

    "porzeczka",

    "rokitnik", "róża", "roza",

    "spiraea",

    "tawuła", "tawula",

    "wrzos",

    # ── Kwiaty / rośliny ozdobne ───────────────────────────────────────────
    "azalia",

    "begonia",

    "cyklamen",

    "dalia", "dzwonek",

    "fiołek", "fiolek",

    "gerber", "gerbera",

    "hiacynt", "hiacjint", "hibiskus", "hortensja",

    "irys",

    "jaskier",

    "kamelia", "konwalia",

    "lilia", "lilak",

    "mak", "margaretka",

    "narcyz",

    "orlik",

    "paproc", "paproć",

    "pelargonia", "peonia",

    "rezeda",

    "słonecznik", "slonecznik", "storczyk",

    "tulipan",

    "werbena",

    "zawilec",

    "żonkil", "zonkil",

    # ── Warzywa ───────────────────────────────────────────────────────────
    "bakłażan", "baklazjan",

    "brokuł", "brokul", "brukselka", "burak",

    "cebula", "cukinia", "czosnek",

    "dynia",

    "fasolka", "fasola",

    "groch",

    "imbir",

    "jarmuż", "jarmuz",

    "kalafior", "kapusta", "karczochy", "karczoch",
    "koper", "korzeń", "korzen", "kukurydza",

    "marchew", "marchewka",

    "ogórek", "ogorek",

    "papryka", "por",

    "rabarbar", "rzodkiew", "rzodkiewka",

    "sałata", "salata", "seler",

    "szparag", "szpinak",

    "ziemniak", "ziemniaki",

    "żuczek",

    # ── Owoce ─────────────────────────────────────────────────────────────
    "agrest",

    "ananas", "avocado", "awokado",

    "banan", "borówka", "borowka",

    "cytryna",

    "daktyl", "dorsz",

    "figa",

    "granat", "gruszka",

    "jabłko", "jablko",

    "kiwi",

    "liczi", "limonka",

    "malina", "mango", "marakuja", "melon",

    "nektarynka",

    "papaja", "persymona", "porzeczka",

    "rabarbar",

    "truskawka",

    "śliwka", "sliwka",

    "winogrono", "wiśnia", "wisnia",

    # ── Zioła i rośliny lecznicze ─────────────────────────────────────────
    "bazylia",

    "czubryca",

    "echinacea",

    "lipa",

    "majeranek", "mięta", "mieta",

    "nagietek",

    "oregano",

    "rozmaryn", "rumianek",

    "szałwia", "szalwia",

    "tymianek",

    # ── Trawy i inne ──────────────────────────────────────────────────────
    "bambus",

    "len",

    "pszenica",

    "ryż", "ryz",

    "trawa", "trzcina",

    # ── Grzyby ────────────────────────────────────────────────────────────
    "borowik",

    "chanterelle", "czubajka",

    "gąska", "gaska",

    "kurka",

    "maślak", "maslak",

    "pieczarka", "pieprznik",

    "rydz",

    "smardz",

    "trufla",
}

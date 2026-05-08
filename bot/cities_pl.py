"""
Lista miast świata z polskimi nazwami — znormalizowane (bez ogonków, małe litery).
Lookup O(1). Gracz może pisać z ogonkami lub bez — validator normalizuje input.
"""

MIASTA: set[str] = {

    # ══════════════════════════════════════════════════════════════════════
    # POLSKA — miasta na prawach powiatu + duże miasta
    # ══════════════════════════════════════════════════════════════════════
    "bedzin", "będzin",
    "belchatow", "bełchatów",
    "bialystok", "białystok",
    "bielsko-biala", "bielsko-biała",
    "bolesławiec", "bolesławiec",
    "brodnica",
    "bydgoszcz",
    "bytom",
    "chorzow", "chorzów",
    "chojnice",
    "ciechanow", "ciechanów",
    "czestochowa", "częstochowa",
    "dabrowa gornicza", "dąbrowa górnicza",
    "elblag", "elbląg",
    "elk", "ełk",
    "gdansk", "gdańsk",
    "gdynia",
    "gliwice",
    "gniezno",
    "gorzow wielkopolski", "gorzów wielkopolski",
    "grudziadz", "grudziądz",
    "inowroclaw", "inowrocław",
    "jastrzebie-zdroj", "jastrzębie-zdrój",
    "jaworzno",
    "jelenia gora", "jelenia góra",
    "kalisz",
    "katowice",
    "kedzierzyn-kozle", "kędzierzyn-koźle",
    "kielce",
    "konin",
    "koszalin",
    "krakow", "kraków",
    "krosno",
    "legnica",
    "leszno",
    "lodz", "łódź",
    "lomza", "łomża",
    "lublin",
    "lubin",
    "mielec",
    "mysłowice", "myslowice",
    "nowy sacz", "nowy sącz",
    "olsztyn",
    "opole",
    "ostrowiec swietokrzyski", "ostrowiec świętokrzyski",
    "ostrow wielkopolski", "ostrów wielkopolski",
    "piła", "pila",
    "piotrkow trybunalski", "piotrków trybunalski",
    "plock", "płock",
    "poznan", "poznań",
    "przemysl", "przemyśl",
    "radom",
    "ruda slaska", "ruda śląska",
    "rybnik",
    "rzeszow", "rzeszów",
    "siedlce",
    "siemianowice slaskie", "siemianowice śląskie",
    "sieradz",
    "skierniewice",
    "slupsk", "słupsk",
    "sosnowiec",
    "stalowa wola",
    "suwalki", "suwałki",
    "swidnica", "świdnica",
    "swietochlowice", "świętochłowice",
    "szczecin",
    "tarnobrzeg",
    "tarnow", "tarnów",
    "torun", "toruń",
    "tychy",
    "walbrzych", "wałbrzych",
    "warszawa",
    "wloclawek", "włocławek",
    "wroclaw", "wrocław",
    "zabrze",
    "zamość", "zamosc",
    "zielona gora", "zielona góra",
    "zyrardow", "żyrardów",
    "żory", "zory",
    "tczew",
    "starachowice",
    "kołobrzeg", "kolobrzeg",
    "malbork",
    "olecko",
    "augustow", "augustów",
    "hajnowka", "hajnówka",
    "sanok",
    "lesko",
    "nowy targ",
    "zakopane",
    "busko-zdroj", "busko-zdrój",
    "skarżysko-kamienna", "skarzysko-kamienna",
    "ostroleka", "ostrołęka",
    "ciechanow", "ciechanów",
    "pultusk", "pułtusk",
    "legionowo",
    "pruszkow", "pruszków",
    "piaseczno",
    "wolomin", "wołomin",
    "zyrardow", "żyrardów",
    "grodzisk mazowiecki",
    "nowy dwor mazowiecki", "nowy dwór mazowiecki",

    # ══════════════════════════════════════════════════════════════════════
    # NIEMCY
    # ══════════════════════════════════════════════════════════════════════
    "berlin", "hamburg", "monachium", "frankfurt", "kolonia",
    "stuttgart", "dusseldorf", "dortmund", "essen", "lipsk",
    "bremen", "drezno", "hanower", "norymberga", "duisburg",
    "bochum", "wuppertal", "bielefeld", "bonn", "mannheim",
    "karlsruhe", "augsburg", "wiesbaden", "gelsenkirchen",
    "monchengladbach", "braunschweig", "kiel", "magdeburg",
    "freiburg", "krefeld", "lubeka", "oberhausen", "erfurt",
    "mainz", "halle", "rostock", "kassel", "hamm",
    "saarbruck", "saarbrücken", "mulheim", "mülheim",
    "potsdam", "osnabrucke", "osnabrück", "ludwigshafen",
    "oldenburg", "leverkusen", "solingen", "saarbrücken",
    "heilbronn", "ingolstadt", "ulm", "pforzheim", "regensburg",
    "wolfsburg", "bottrop", "remscheid", "furth", "fürth",
    "offenbach", "recklinghausen", "goteborg",

    # ══════════════════════════════════════════════════════════════════════
    # FRANCJA
    # ══════════════════════════════════════════════════════════════════════
    "paryz", "paryż", "marsylia", "lyon", "tuluza", "nicea",
    "nantes", "strasburg", "montpellier", "bordeaux", "lille",
    "rennes", "reims", "le havre", "saint-etienne", "toulon",
    "grenoble", "dijon", "angers", "nimes", "villeurbanne",
    "clermont-ferrand", "le mans", "aix-en-provence", "brest",
    "tours", "amiens", "limoges", "annecy", "perpignan",
    "boulogne-billancourt", "metz", "besancon", "béziers",
    "orleans", "mulhouse", "rouen", "argenteuil", "montreuil",
    "avignon", "pau", "calais", "nancy", "tourcoing",
    "poitiers", "dunkirk", "dunkerque", "versailles", "cannes",
    "ajaccio", "lyon", "bordeaux", "nice", "nizza",

    # ══════════════════════════════════════════════════════════════════════
    # WIELKA BRYTANIA I IRLANDIA
    # ══════════════════════════════════════════════════════════════════════
    "londyn", "birmingham", "manchester", "glasgow", "liverpool",
    "leeds", "sheffield", "edynburg", "bristol", "cardiff",
    "belfast", "leicester", "bradford", "coventry", "nottingham",
    "hull", "kingston upon hull", "newcastle", "stoke",
    "wolverhampton", "plymouth", "reading", "derby", "southampton",
    "luton", "portsmouth", "oxford", "cambridge", "exeter",
    "york", "sunderland", "brighton", "peterborough",
    "dundee", "aberdeen", "inverness", "swansea",
    "dublin", "cork", "limerick", "galway", "waterford",

    # ══════════════════════════════════════════════════════════════════════
    # WŁOCHY
    # ══════════════════════════════════════════════════════════════════════
    "rzym", "mediolan", "neapol", "turyn", "palermo",
    "genua", "bolonia", "florencja", "bari", "katania",
    "werona", "wenecja", "messyna", "padwa", "triest",
    "taranto", "brescia", "prato", "parma", "reggio calabria",
    "modena", "livorno", "cagliari", "foggia", "bergamo",
    "ferrara", "salerno", "reggio emilia", "perugia",
    "ravenna", "siena", "ancona", "lecce", "pescara",
    "udine", "vicenza", "terni", "forlì", "trento",
    "monza", "nowaryjka", "bolzano",

    # ══════════════════════════════════════════════════════════════════════
    # HISZPANIA I PORTUGALIA
    # ══════════════════════════════════════════════════════════════════════
    "madryt", "barcelona", "walencja", "sewilla", "saragossa",
    "malaga", "murcia", "palma", "las palmas", "bilbao",
    "alicante", "kordoba", "valladolid", "vigo", "gijon",
    "hospitalet", "coruña", "granada", "vitoria", "elche",
    "oviedo", "santa cruz de tenerife", "pamplona",
    "almeria", "fuenlabrada", "mostoles", "cartagena",
    "getafe", "alcala de henares", "jerez de la frontera",
    "lizbona", "porto", "amadora", "braga", "setubal",
    "coimbra", "funchal", "almada", "agualva", "viana do castelo",

    # ══════════════════════════════════════════════════════════════════════
    # ROSJA I BIAŁORUŚ
    # ══════════════════════════════════════════════════════════════════════
    "moskwa", "sankt petersburg", "nowosybirsk", "jekaterynburg",
    "niżny nowogród", "nizhny novgorod", "kazań", "czelabińsk",
    "omsk", "samara", "rostow nad donem", "ufa",
    "krasnodar", "perm", "krasnojask", "krasnojarsk",
    "saratow", "woroneż", "togliatti", "iżewsk", "uljanowsk",
    "irkuck", "barnaul", "władywostok", "chaborowsk",
    "nowokuźnieck", "krasnojarsk", "ryazan", "tomsk",
    "orenburg", "kemerowo", "naberezhnye chelny",
    "minsk", "homel", "witebsk", "mohylew", "brześć",
    "grodno",

    # ══════════════════════════════════════════════════════════════════════
    # UKRAINA
    # ══════════════════════════════════════════════════════════════════════
    "kijow", "kijów", "charków", "odessa", "dniepropietrowsk",
    "donieck", "zaporoże", "lwow", "lwów", "krzywy rog",
    "mikołajow", "mariupol", "łuhańsk", "winnica",
    "sewastopol", "chersoń", "połtawa", "czernihow",
    "chmielnicki", "żytomierz", "sumy", "rowne",
    "iwano-frankiwsk", "ternopil", "łuck", "uzhorod",

    # ══════════════════════════════════════════════════════════════════════
    # CZECHY I SŁOWACJA
    # ══════════════════════════════════════════════════════════════════════
    "praga", "brno", "ostrawa", "pilzno", "ołomuniec",
    "liberec", "hradec kralove", "czeskie budziejowice",
    "usti nad labem", "pardubice", "zlin", "havirov",
    "kladno", "most", "opawa",
    "bratysława", "koszyce", "preszow", "żilina", "nitra",
    "bańska bystrzyca", "trnawa", "trenczyn",

    # ══════════════════════════════════════════════════════════════════════
    # AUSTRIA I SZWAJCARIA
    # ══════════════════════════════════════════════════════════════════════
    "wiedeń", "wieden", "graz", "linz", "salzburg", "innsbruck",
    "klagenfurt", "villach", "wels",
    "zurych", "zurych", "genewa", "bazylea", "berno",
    "lozanna", "winterthur", "st. gallen", "lugano",

    # ══════════════════════════════════════════════════════════════════════
    # KRAJE BENELUKSU I SKANDYNAWIA
    # ══════════════════════════════════════════════════════════════════════
    "amsterdam", "rotterdam", "haga", "haag", "utrecht",
    "eindhoven", "tilburg", "groningen", "almere", "breda",
    "nijmegen", "enschede", "apeldoorn", "haarlem", "arnhem",
    "bruksela", "antwerpia", "gandawa", "liege", "brugia",
    "charleroi", "namur", "mechelen",
    "luksemburg",
    "kopenhaga", "aarhus", "odense", "aalborg",
    "sztokholm", "goteborg", "malmo", "uppsala", "vasteras",
    "orebro", "linkoping", "helsingborg", "jonkoping",
    "oslo", "bergen", "trondheim", "stavanger", "drammen",
    "helsinki", "tampere", "turku", "oulu", "jyvaskyla",

    # ══════════════════════════════════════════════════════════════════════
    # EUROPA POŁUDNIOWA I WSCHODNIA
    # ══════════════════════════════════════════════════════════════════════
    "ateny", "saloniki", "pireus", "patras", "heraklion",
    "sofia", "plovdiv", "warna", "burgas", "stara zagora",
    "bukareszt", "kluż-napoka", "timisoarze", "jassy",
    "konstanca", "krajowa",
    "belgrad", "nowy sad", "nisz",
    "zagrzeb", "split", "rijeka", "osijek",
    "sarajewo", "banja luka", "tuzla", "mostar",
    "podgorica", "niksic",
    "lublana", "maribor", "celje",
    "skopje", "bitola",
    "tirana", "durres",
    "nikozja", "nikosia", "limassol",
    "tallinn", "tartu",
    "ryga", "daugavpils",
    "wilno", "kowno", "klaipeda",

    # ══════════════════════════════════════════════════════════════════════
    # TURCJA I BLISKI WSCHÓD
    # ══════════════════════════════════════════════════════════════════════
    "istanbul", "ankara", "izmir", "bursa", "adana",
    "gaziantep", "konya", "antalya", "mersin", "diyarbakir",
    "kayseri", "eskisehir", "trabzon", "malatya", "erzurum",
    "kocaeli", "samsun", "denizli", "van",
    "teheran", "maszhad", "mashhad", "isfahan", "karadż",
    "tabriz", "sziras", "ahwaz", "kom", "kermanshah",
    "bagdad", "basra", "mosul", "irbil",
    "rijad", "dżudda", "jeddah", "mekka", "medyna",
    "damaszek", "aleppo", "homs",
    "amman", "zarqa",
    "bejrut", "tripoli", "sydon",
    "jerozolima", "tel awiw", "hajfa",
    "abu zabi", "dubaj", "szardżja",
    "doha", "al-wakra",
    "kuwejt", "salmija",
    "muskat", "seeb",
    "sanaa", "aden",

    # ══════════════════════════════════════════════════════════════════════
    # AZJA POŁUDNIOWA
    # ══════════════════════════════════════════════════════════════════════
    "delhi", "nowe delhi", "mumbaj", "kalkuta", "bangalore",
    "hyderabad", "ahmedabad", "czennaj", "surat", "pune",
    "dżajpur", "jaipur", "lucknow", "kanpur", "nagpur",
    "indore", "thane", "bhopal", "patna", "ludhiana",
    "agra", "waranasi", "madurai", "nashik", "faridabad",
    "ghaziabad", "dhaka", "czittagong", "sylhet", "rajszahi",
    "islamabad", "karaczi", "lahore", "fajsalabad", "rawalpindi",
    "gujranwala", "peshawar", "multan", "hyderabad sind",
    "colombo", "kolombo", "kandy",
    "kathmandu", "pokharę",
    "kabul", "herat", "mazar-i-szarif",
    "dhaka", "dhaka",

    # ══════════════════════════════════════════════════════════════════════
    # AZJA WSCHODNIA I POŁUDNIOWO-WSCHODNIA
    # ══════════════════════════════════════════════════════════════════════
    "pekin", "szanghaj", "kanton", "guangzhou", "shenzhen",
    "chongqing", "tianjin", "wuhan", "dongguan", "chengdu",
    "nanjing", "nankin", "xian", "sian", "hangzhou",
    "shenyang", "harbin", "changchun", "qingdao", "dalian",
    "jinan", "kunming", "zhengzhou", "fuzhou", "changsha",
    "nanchang", "guiyang", "suzhou", "ningbo", "xiamen",
    "tokio", "osaka", "nagoja", "nagoya", "jokohama",
    "kobe", "kioto", "fukuoka", "kawasaki", "sapporo",
    "hiroszima", "sendai", "kitakyushu", "chiba",
    "seul", "pusan", "busan", "incheon", "daegu",
    "daejeon", "kwangju", "ulsan",
    "pyongyang", "phenian", "nampo", "hamhung",
    "hanoi", "ho chi minh", "hajfong", "haiphong", "hue", "da nang",
    "bangkok", "chiang mai", "phuket", "pattaya",
    "singapur",
    "kuala lumpur", "johor bahru", "ipoh", "petaling jaya",
    "jakarta", "surabaya", "bandung", "medan", "semarang",
    "palembang", "makassar", "depok", "tangerang",
    "manila", "quezon city", "davao", "cebu", "zamboanga",
    "yangon", "mandalay", "naypyidaw",
    "phnom penh", "siem reap",
    "vientiane", "luang prabang",
    "dili",
    "bandar seri begawan",

    # ══════════════════════════════════════════════════════════════════════
    # AZJA ŚRODKOWA I ZAKAUKAZIE
    # ══════════════════════════════════════════════════════════════════════
    "astana", "nur-sultan", "ałmaty", "almaty", "szymkent",
    "karaganda", "aktobe", "taraz",
    "taszkent", "samarkanda", "buchara", "namangan", "andijan",
    "biszkek", "osz",
    "duszanbe", "chudżand",
    "aszchabad", "turkmenabat", "mary",
    "tbilisi", "batumi", "kutaisi",
    "baku", "gandża", "sumgait",
    "jerewan", "gyumri",

    # ══════════════════════════════════════════════════════════════════════
    # AFRYKA PÓŁNOCNA
    # ══════════════════════════════════════════════════════════════════════
    "kair", "aleksandria", "giza", "szubra", "port said",
    "casablanca", "rabat", "fez", "fes", "marrakesz", "agadir",
    "algier", "oran", "konstantyna", "annaba",
    "tunis", "sfaks", "sussa", "kairouan",
    "trypolis", "tripoli", "bengazi", "misrata",
    "chartum", "omdurmam", "port sudan",

    # ══════════════════════════════════════════════════════════════════════
    # AFRYKA SUBSAHARYJSKA
    # ══════════════════════════════════════════════════════════════════════
    "lagos", "kano", "ibadan", "kaduna", "port harcourt",
    "benin city", "maiduguri", "zaria", "aba",
    "kinszasa", "lubumbashi", "mbuji-mayi", "kananga",
    "nairobi", "mombasa", "nakuru", "kisumu",
    "addis abeba", "dire dawa", "bahir dar",
    "dar es salaam", "mwanza", "dodoma", "zanzibar",
    "johannesburg", "kapsztad", "durban", "pretoria",
    "soweto", "port elizabeth", "bloemfontein",
    "akra", "kumasi",
    "dakar", "thiès", "saint-louis",
    "abidżan", "abidzan", "yamoussoukro", "bouaké",
    "bamako", "sikasso",
    "ouagadougou", "bobo-dioulasso",
    "konakry", "kankan",
    "freetown",
    "monrovia",
    "bissau",
    "banjul",
    "niamej", "zinder",
    "ndżamena", "ndjamena",
    "bangui",
    "malabo",
    "yaounde", "duala", "douala",
    "libreville", "port-gentil",
    "brazzaville", "pointe-noire",
    "kampala", "gulu",
    "kigali", "butare",
    "bujumbura",
    "luanda", "lubango",
    "lusaka", "ndola", "livingstone",
    "harare", "bulawayo",
    "lilongwe", "blantyre",
    "maputo", "beira",
    "antananarivo",
    "mogadiszu", "kismayu",
    "dżibuti", "dzibuti",
    "asmara",
    "juba",
    "lome", "sokode",
    "kotonu", "cotonou", "porto novo",
    "accra", "tema",
    "abuja",
    "maseru",
    "mbabane",
    "windhoek", "swakopmund",
    "gaborone", "francistown",
    "moroni",
    "port louis",
    "victoria",
    "sao tome",

    # ══════════════════════════════════════════════════════════════════════
    # AMERYKA PÓŁNOCNA — USA
    # ══════════════════════════════════════════════════════════════════════
    "nowy jork", "los angeles", "chicago", "houston", "phoenix",
    "filadelfia", "san antonio", "san diego", "dallas", "san jose",
    "austin", "jacksonville", "fort worth", "columbus", "charlotte",
    "indianapolis", "san francisco", "seattle", "denver", "nashville",
    "oklahoma city", "el paso", "washington", "waszyngton",
    "boston", "las vegas", "memphis", "portland", "louisville",
    "baltimore", "milwaukee", "albuquerque", "tucson", "fresno",
    "sacramento", "mesa", "kansas city", "atlanta", "omaha",
    "colorado springs", "raleigh", "long beach", "virginia beach",
    "minneapolis", "tampa", "new orleans", "arlington",
    "miami", "orlando", "cleveland", "pittsburgh",
    "anchorage", "honolulu",

    # ══════════════════════════════════════════════════════════════════════
    # KANADA
    # ══════════════════════════════════════════════════════════════════════
    "toronto", "montreal", "vancouver", "calgary", "edmonton",
    "ottawa", "winnipeg", "quebec", "hamilton", "kitchener",
    "london ontario", "victoria", "halifax", "saskatoon", "regina",

    # ══════════════════════════════════════════════════════════════════════
    # MEKSYK
    # ══════════════════════════════════════════════════════════════════════
    "meksyk", "miasto meksyk", "guadalajara", "monterrey", "puebla",
    "toluca", "tijuana", "juarez", "leon", "chihuahua",
    "merida", "san luis potosi", "queretaro", "acapulco",
    "cancun", "hermosillo", "mexicali",

    # ══════════════════════════════════════════════════════════════════════
    # AMERYKA ŚRODKOWA I KARAIBY
    # ══════════════════════════════════════════════════════════════════════
    "gwatemala", "guatemala", "quezaltenango",
    "san salvador", "santa ana",
    "tegucigalpa", "san pedro sula",
    "managua", "leon", "granada nicaragua",
    "san jose", "alajuela",
    "panama city", "panama", "colon",
    "kingston", "montego bay",
    "port au prince", "cap-haitien",
    "santo domingo", "santiago de los caballeros",
    "san juan", "ponce",
    "havana", "hawana", "santiago de cuba",
    "bridgetown",
    "port of spain",
    "belmopan", "belize city",
    "nassau",
    "roseau",
    "castries",
    "kingstown",
    "st. john's", "saint john",

    # ══════════════════════════════════════════════════════════════════════
    # AMERYKA POŁUDNIOWA
    # ══════════════════════════════════════════════════════════════════════
    "bogota", "medellin", "cali", "barranquilla", "cartagena",
    "buenos aires", "cordoba", "rosario", "mendoza", "san miguel de tucuman",
    "la plata", "mar del plata",
    "lima", "arequipa", "trujillo", "chiclayo",
    "sao paulo", "rio de janeiro", "salvador", "fortaleza",
    "belo horizonte", "manaus", "curitiba", "recife",
    "porto alegre", "belem", "goiania", "brasilia",
    "santiago", "valparaiso", "concepcion", "antofagasta",
    "caracas", "maracaibo", "valencia venezuela", "maracay",
    "quito", "guayaquil", "cuenca",
    "la paz", "santa cruz", "cochabamba",
    "asuncion", "asunción", "ciudad del este",
    "montevideo", "salto",
    "paramaribo",
    "georgetown", "linden",
    "cayenne",
    "sucre", "potosi",

    # ══════════════════════════════════════════════════════════════════════
    # AUSTRALIA I OCEANIA
    # ══════════════════════════════════════════════════════════════════════
    "sydney", "melbourne", "brisbane", "perth", "adelajda",
    "adelaide", "gold coast", "newcastle australia", "canberra",
    "hobart", "darwin", "geelong", "townsville", "cairns",
    "auckland", "wellington", "christchurch", "hamilton nz",
    "tauranga", "napier", "dunedin",
    "port moresby", "lae", "arawa",
    "suva", "lautoka",
    "honiara",
    "vanuatu", "port vila",
    "apia",
    "nuku'alofa",
    "funafuti",
    "tarawa",
    "palikir",
    "majuro",
    "yaren",
    "nadi", "labasa",
    "papeete",

}

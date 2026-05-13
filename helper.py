tampa_bay_cities = [
    "Tampa",
    "Brandon",
    "Riverview",
    "Lutz",
    "Wimauma",
    "Sun City",
    "Apollo Beach",
    "Gibsonton",
    "Plant City",
    "Ruskin",
    "Seffner",
    "Temple Terrace",
    "Valrico",
    "Saint Petersburg",
    "Clearwater",
    "Largo",
    "Pinellas Park",
    "Palm Harbor",
    "Tarpon Springs",
    "Dunedin",
    "Gulfport",
    "Oldsmar",
    "Safety Harbor",
    "Land O'Lakes",
    "New Port Richey",
    "Dade City",
    "Holiday",
    "Odessa",
    "Spring Hill",
    "Wesley Chapel",
    "Zephyrhills"
]

def normalize_cities(text):
    text = text.lower().strip()
    text = text.replace("tampa bay", "tampa")
    text = text.replace("tampa florida", "tampa")
    text = text.replace("tampa palms", "tampa")
    text = text.replace("south tampa", "tampa")
    text = text.replace("southwest tampa", "tampa")
    text = text.replace("riverview fl", "riverview")
    text = text.replace("lutz fl", "lutz")
    text = text.replace("sun city center", "sun city")
    text = text.replace("st. petersburg", "saint petersburg")
    text = text.replace("saintt petersburg", "saint petersburg")
    text = text.replace("st petersburg", "saint petersburg")
    text = text.replace("st.petersburg", "saint petersburg")
    text = text.replace("clearwater beach", "clearwater")
    text = text.replace("clearwater/ countryside", "clearwater")
    text = text.replace("largo (walsingham)", "largo")
    text = text.replace("pinellas", "pinellas park")
    text = text.replace("land o lakes", "land o'lakes")
    text = text.replace("land o' lakes", "land o'lakes")
    text = text.replace("port richey", "new port richey")
    return text.title()

def normalize_text(text):
    text = text.lower().strip()
    text = text.replace("burgers", "burger")
    text = text.replace("hamburgers", "burger")
    text = text.replace("hamburger", "burger")
    text = text.replace("tacos", "taco")
    text = text.replace("sandwiches", "sandwich")
    text = text.replace("grilling", "grill")
    text = text.replace("grilled", "grill")
    text = text.replace("wraps", "wrap")
    text = text.replace("hot dogs", "hot dog")
    text = text.replace("hotdogs", "hot dog")
    text = text.replace("hotdog", "hot dog")
    text = text.replace("shrimp", "seafood")
    text = text.replace("crab", "seafood")
    text = text.replace("lobster", "seafood")
    text = text.replace("bbq", "barbeque")
    text = text.replace("steakhouses", "steakhouse")
    text = text.replace("waffles", "waffle")
    text = text.replace("bagels", "bagel")
    text = text.replace("donuts", "donut")
    text = text.replace("smoothies", "smoothie")
    text = text.replace("cocktails", "cocktail")
    text = text.replace("bars", "bar")
    text = text.replace("breweries", "brewery")
    text = text.replace("diners", "diner")
    text = text.replace("smokehouses", "smokehouse")
    return text
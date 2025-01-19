import random

class Video:
    def __init__(self, title, year, genre):
        self.title = title
        self.year = year
        self.genre = genre
        self.views = 0

    def play(self):
        self.views += 1

    def __str__(self):
        return f"{self.title} ({self.year})"

class film(Video):
    pass

class serial(Video):
    def __init__(self, title, year, genre, season, episode):
        super().__init__(title, year, genre)
        self.season = season
        self.episode = episode

    def __str__(self):
        return f"{self.title} S{self.season:02d}E{self.episode:02d}"

def get_movies(library):
    return sorted([item for item in library if isinstance(item, film)], key=lambda x: x.title)

def get_series(library):
    return sorted([item for item in library if isinstance(item, serial)], key=lambda x: x.title)

def search(library, title):
    return next((item for item in library if item.title.lower() == title.lower()), None)

def generate_views(library):
    item = random.choice(library)
    item.views += random.randint(1, 100)

def generate_views_multiple(library, times=10):
    for _ in range(times):
        generate_views(library)

def top_titles(library, n=5, content_type=None):
    filtered_library = library
    if content_type == "movie":
        filtered_library = get_movies(library)
    elif content_type == "series":
        filtered_library = get_series(library)
    return sorted(filtered_library, key=lambda x: x.views, reverse=True)[:n]

library = [
    film("Kiler", 1997, "Komedia kryminalna"),
    film("Psy", 1992, "Sensacyjny"),
    film("Ogniem i mieczem", 1999, "Historyczny"),
    serial("M jak miłość", 2000, "Obyczajowy", 1, 1),
    serial("Na dobre i na złe", 1999, "Medyczno-obyczajowy", 1, 1),
    serial("Klan", 1997, "Obyczajowy", 1, 1)
]

generate_views_multiple(library)
print("Najpopularniejsze tytuły:")
for item in top_titles(library):
    print(f"{item} - {item.views} odtworzeń")


from django.db import migrations


ZIP_CODES_BY_CITY = {
    "Eisenstadt": ("7000",),
    "Rust": ("7071",),
    "Neusiedl am See": ("7100",),
    "Mattersburg": ("7210",),
    "Oberpullendorf": ("7350",),
    "Oberwart": ("7400",),
    "Güssing": ("7540",),
    "Jennersdorf": ("8380",),
    "Pinkafeld": ("7423",),
    "Frauenkirchen": ("7132",),
    "Klagenfurt am Wörthersee": ("9020",),
    "Villach": ("9500",),
    "Wolfsberg": ("9400",),
    "Spittal an der Drau": ("9800",),
    "Feldkirchen in Kärnten": ("9560",),
    "St. Veit an der Glan": ("9300",),
    "Völkermarkt": ("9100",),
    "Hermagor": ("9620",),
    "Althofen": ("9330",),
    "Bleiburg": ("9150",),
    "St. Pölten": ("3100",),
    "Wiener Neustadt": ("2700",),
    "Krems an der Donau": ("3500",),
    "Amstetten": ("3300",),
    "Baden": ("2500",),
    "Mödling": ("2340",),
    "Klosterneuburg": ("3400",),
    "Tulln an der Donau": ("3430",),
    "Hollabrunn": ("2020",),
    "Mistelbach": ("2130",),
    "Linz": ("4020",),
    "Wels": ("4600",),
    "Steyr": ("4400",),
    "Leonding": ("4060",),
    "Traun": ("4050",),
    "Vöcklabruck": ("4840",),
    "Ried im Innkreis": ("4910",),
    "Braunau am Inn": ("5280",),
    "Enns": ("4470",),
    "Bad Ischl": ("4820",),
    "Salzburg": ("5020",),
    "Hallein": ("5400",),
    "Saalfelden am Steinernen Meer": ("5760",),
    "Wals-Siezenheim": ("5071",),
    "Bischofshofen": ("5500",),
    "St. Johann im Pongau": ("5600",),
    "Zell am See": ("5700",),
    "Seekirchen am Wallersee": ("5201",),
    "Neumarkt am Wallersee": ("5202",),
    "Mittersill": ("5730",),
    "Graz": ("8010",),
    "Leoben": ("8700",),
    "Kapfenberg": ("8605",),
    "Bruck an der Mur": ("8600",),
    "Feldbach": ("8330",),
    "Leibnitz": ("8430",),
    "Weiz": ("8160",),
    "Knittelfeld": ("8720",),
    "Deutschlandsberg": ("8530",),
    "Judenburg": ("8750",),
    "Innsbruck": ("6020",),
    "Kufstein": ("6330",),
    "Telfs": ("6410",),
    "Schwaz": ("6130",),
    "Hall in Tirol": ("6060",),
    "Wörgl": ("6300",),
    "Lienz": ("9900",),
    "Imst": ("6460",),
    "Kitzbühel": ("6370",),
    "Zirl": ("6170",),
    "Dornbirn": ("6850",),
    "Feldkirch": ("6800",),
    "Bregenz": ("6900",),
    "Lustenau": ("6890",),
    "Hohenems": ("6845",),
    "Bludenz": ("6700",),
    "Hard": ("6971",),
    "Rankweil": ("6830",),
    "Götzis": ("6840",),
    "Lauterach": ("6923",),
    "Wien": (
        "1010",
        "1020",
        "1030",
        "1040",
        "1050",
        "1060",
        "1070",
        "1080",
        "1090",
        "1100",
        "1110",
        "1120",
        "1130",
        "1140",
        "1150",
        "1160",
        "1170",
        "1180",
        "1190",
        "1200",
        "1210",
        "1220",
        "1230",
    ),
}


def add_zip_codes(apps, schema_editor):
    City = apps.get_model("users", "City")
    ZipCode = apps.get_model("users", "ZipCode")

    for city_name, codes in ZIP_CODES_BY_CITY.items():
        city = City.objects.filter(name=city_name).first()
        if city is None:
            continue

        for code in codes:
            zip_code, _ = ZipCode.objects.get_or_create(code=code)
            zip_code.cities.add(city)


def remove_zip_codes(apps, schema_editor):
    City = apps.get_model("users", "City")
    ZipCode = apps.get_model("users", "ZipCode")

    for city_name, codes in ZIP_CODES_BY_CITY.items():
        city = City.objects.filter(name=city_name).first()
        if city is None:
            continue

        for code in codes:
            zip_code = ZipCode.objects.filter(code=code).first()
            if zip_code is None:
                continue

            zip_code.cities.remove(city)
            if not zip_code.cities.exists():
                zip_code.delete()


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0009_zipcode"),
    ]

    operations = [
        migrations.RunPython(add_zip_codes, remove_zip_codes),
    ]

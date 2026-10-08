#!/usr/bin/env python3
"""Group A (CONTROLLED) curated term maps for AdiletCodex v1.1 extended localization.
Official body names (adopting_organ) and legal topic sections (database_section).
Reviewed deterministic dictionary - NOT machine translation.
"""
import json, os

ADOPTING_ORGAN = {
    "Парламент Республики Казахстан (старое название: Президиум Верховного Совета РК; Президиум Верховного Совета Казахской ССР; Верховный Совет РК; Верховный Совет Казахской ССР)": {
        "en": "Parliament of the Republic of Kazakhstan (former names: Presidium of the Supreme Council of the RK; Presidium of the Supreme Council of the Kazakh SSR; Supreme Council of the RK; Supreme Council of the Kazakh SSR)",
        "kk": "Қазақстан Республикасының Парламенті (бұрынғы атауы: ҚР Жоғарғы Кеңесінің Президиумы; Қазақ КСР Жоғарғы Кеңесінің Президиумы; ҚР Жоғарғы Кеңесі; Қазақ КСР Жоғарғы Кеңесі)",
    },
    "Президент Республики Казахстан (старое название: Президент Казахской Советской Социалистической Республики; Президент Казахской ССР)": {
        "en": "President of the Republic of Kazakhstan (former names: President of the Kazakh Soviet Socialist Republic; President of the Kazakh SSR)",
        "kk": "Қазақстан Республикасының Президенті (бұрынғы атауы: Қазақ Кеңестік Социалистік Республикасының Президенті; Қазақ КСР Президенті)",
    },
}

DATABASE_SECTION = {
    "Финансы": {"en": "Finance", "kk": "Қаржы"},
    "Хозяйственная деятельность": {"en": "Economic activity", "kk": "Шаруашылық қызмет"},
    "Национальная безопасность. Охрана общественного порядка": {"en": "National security. Protection of public order", "kk": "Ұлттық қауіпсіздік. Қоғамдық тәртіпті сақтау"},
    "Гражданское право": {"en": "Civil law", "kk": "Азаматтық құқық"},
    "Конституционный строй и основы государственного управления": {"en": "Constitutional system and fundamentals of state governance", "kk": "Конституциялық құрылыс және мемлекеттік басқару негіздері"},
    "Уголовное право": {"en": "Criminal law", "kk": "Қылмыстық құқық"},
    "Социальное обеспечение. Страхование": {"en": "Social security. Insurance", "kk": "Әлеуметтік қамсыздандыру. Сақтандыру"},
    "Судопроизводство": {"en": "Judicial proceedings", "kk": "Сот ісін жүргізу"},
    "Таможенное дело": {"en": "Customs affairs", "kk": "Кеден ісі"},
    "Транспорт": {"en": "Transport", "kk": "Көлік"},
    "Суд. Юстиция. Прокуратура": {"en": "Court. Justice. Prosecutor's office", "kk": "Сот. Әділет. Прокуратура"},
    "Труд": {"en": "Labour", "kk": "Еңбек"},
    "Торговля и общественное питание": {"en": "Trade and public catering", "kk": "Сауда және қоғамдық тамақтану"},
    "Промышленность": {"en": "Industry", "kk": "Өнеркәсіп"},
    "Здравоохранение": {"en": "Healthcare", "kk": "Денсаулық сақтау"},
    "Сельское хозяйство": {"en": "Agriculture", "kk": "Ауыл шаруашылығы"},
    "Охрана и использование земель": {"en": "Protection and use of land", "kk": "Жерді қорғау және пайдалану"},
    "Охрана и использование недр": {"en": "Protection and use of subsoil (mineral resources)", "kk": "Жер қойнауын қорғау және пайдалану"},
    "Культура": {"en": "Culture", "kk": "Мәдениет"},
    "Законодательство о браке и семье": {"en": "Legislation on marriage and family", "kk": "Неке және отбасы туралы заңнама"},
    "Строительство": {"en": "Construction", "kk": "Құрылыс"},
    "Образование": {"en": "Education", "kk": "Білім беру"},
    "Оборона": {"en": "Defence", "kk": "Қорғаныс"},
    "Жилищно-коммунальное хозяйство. Бытовое обслуживание населения": {"en": "Housing and communal services. Consumer and public utility services", "kk": "Тұрғын үй-коммуналдық шаруашылық. Халыққа тұрмыстық қызмет көрсету"},
    "Охрана и использование вод": {"en": "Protection and use of water resources", "kk": "Суды қорғау және пайдалану"},
    "Международные отношения": {"en": "International relations", "kk": "Халықаралық қатынастар"},
    "Охрана и использование лесов": {"en": "Protection and use of forests", "kk": "Орманды қорғау және пайдалану"},
    "Внешнеэкономическая деятельность": {"en": "Foreign economic activity", "kk": "Сыртқы экономикалық қызмет"},
    "Наука": {"en": "Science", "kk": "Ғылым"},
    "Охрана и использование животного мира": {"en": "Protection and use of wildlife (fauna)", "kk": "Жануарлар дүниесін қорғау және пайдалану"},
    "Охрана окружающей среды": {"en": "Environmental protection", "kk": "Қоршаған ортаны қорғау"},
    "Связь": {"en": "Communications", "kk": "Байланыс"},
    "Кооперация": {"en": "Cooperation", "kk": "Кооперация"},
    "Государственные награды": {"en": "State awards", "kk": "Мемлекеттік марапаттар"},
    "Медиация": {"en": "Mediation", "kk": "Медиация"},
}

if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "adopting_organ_map.json"), "w") as f:
        json.dump(ADOPTING_ORGAN, f, ensure_ascii=False, indent=2)
    with open(os.path.join(here, "database_section_map.json"), "w") as f:
        json.dump(DATABASE_SECTION, f, ensure_ascii=False, indent=2)
    print("adopting_organ entries:", len(ADOPTING_ORGAN))
    print("database_section entries:", len(DATABASE_SECTION))

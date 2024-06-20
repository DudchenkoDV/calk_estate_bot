from typing import Dict

import numpy as np

metro_coords = {
    'девяткино': {'Широта': 60.050182, 'Долгота': 30.443045},
    'проспект ветеранов': {'Широта': 59.84211, 'Долгота': 30.250588},
    'купчино': {'Широта': 59.829781, 'Долгота': 30.375702},
    'комендантский проспект': {'Широта': 60.008591, 'Долгота': 30.258663},
    'крестовский остров': {'Широта': 59.971821, 'Долгота': 30.259436},
    'шушары': {'Широта': 59.819973, 'Долгота': 30.432718},
    'парнас': {'Широта': 60.06699, 'Долгота': 30.333839},
    'улица дыбенко': {'Широта': 59.907417, 'Долгота': 30.483311},
}

metros_to_latins = {
    'комендантский проспект': 'komendatskiy_prospekt',
    'крестовский остров': 'krestovskiy_ostrov',
    'шушары': 'shushary',
    'парнас': 'parnas',
    'купчино': 'kupchino',
    'улица дыбенко': 'ulitsa_dybenko',
    'девяткино': 'devyatkino',
    'проспект ветеранов': 'prospekt_veteranov',
}


def find_metro_distance(building_latitude: float, building_longitude: float, metro_name: str) -> float:
    """Находит расстояние в км до станции метро."""
    latitude_part = (building_latitude - metro_coords[metro_name]['Широта']) ** 2
    longitude_part = (building_longitude - metro_coords[metro_name]['Долгота']) ** 2
    # преобразование во float для дальнейшей возможности отправки словаря в json'е request'а
    return float(
        round(np.sqrt(latitude_part + longitude_part) * 111.13, 3)
    )


def calculate_selected_metro_dists(building_latitude: float, building_longitude: float) -> Dict[str, float]:
    """Находит расстояние до выбранных станций метро."""
    distances = {}
    for metro_name, latin_name in metros_to_latins.items():
        distances[f'{latin_name}_dist'] = find_metro_distance(building_latitude, building_longitude, metro_name)
    return distances

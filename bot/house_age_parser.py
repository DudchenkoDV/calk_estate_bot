import re
import pandas as pd
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import undetected_chromedriver as uc

from typing import Optional

SPB_MEAN_CONSTRUCTION_YEAR = 2000
YEAR_TO_SUBTRACT_FROM = 2024


def address_to_search_string(address: str) -> str:
    """Преобразует адрес дома в поисковую строку для dom.mingkh.ru."""
    return '+'.join(address.strip().split())


def get_buildings_info(address: str) -> pd.DataFrame:
    """Возвращает признаки дома по его адресу с сайта dom.mingkh.ru.
    В случае непустого ответа датафрейм будет содержать следующие колонки:
    Город,	Адрес,	Площадь м2,	 Год,  Этажей,	Жилых помещений.
    """
    search_string = address_to_search_string(address)

    results = pd.DataFrame()
    page_num = 1
    driver = uc.Chrome()
    while True:
        try:
            driver.get(f'https://dom.mingkh.ru/search?address={search_string}&searchtype=house&page={page_num}')
            table = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'table')))
            html = driver.page_source
            list_of_tables = pd.read_html(html)
            if list_of_tables[0].empty:
                break
            results = pd.concat([results, list_of_tables[0]])
            page_num += 1
        except Exception as e:
            print("Error:", e)
            break
    driver.close()
    return results[results['Город'] == 'Санкт-Петербург'].copy()


def get_house_construction_year(df: pd.DataFrame, house_number: str) -> Optional[int]:
    """Возвращает год постройки дома.
    Если датафрейм пустой, то вернет значение SPB_MEAN_CONSTRUCTION_YEAR.
    В случае совпадения номера дома возвращает дату постройки здания.
    Если дома с таким номером нет, то вернет "средний возраст" домов на этой улице.
    """
    if df.empty:
        return SPB_MEAN_CONSTRUCTION_YEAR
    # Выбрасываем записи с пропусками в году постройки
    df = df[~df['Год'].astype(str).str.contains('—')].copy()
    if df.empty:
        return SPB_MEAN_CONSTRUCTION_YEAR
    df['Год'] = df['Год'].astype(int)

    house_number_match = df['Адрес'].str.contains(rf'\s{house_number}\D', regex=True)
    if not any(house_number_match):
        # Если не нашли соответствие номера дома, то возвращаем средний год по улице
        return int(df['Год'].mean().round())
    # преобразование в int нужно для дальнейшей возможности отправки словаря в json'е request'а
    return int(df[house_number_match]['Год'].mean().round())


def estimate_building_year(address: str) -> int:
    """Оценивает "возраст" дома на основании данных dom.mingkh.ru."""
    try:
        houses_info = get_buildings_info(address)
        house_numbers = re.findall(r'\d+', address.split(', ')[-1])

        # Обработаем адреса типа 63-65, 35к1 -> для них вернется 63 и 35 соответственно
        # Для простых номеров типа 38, 34А -> для них вернется 38 и 34 соответственно
        house_number = house_numbers[-1]
        if len(house_numbers) > 1:
            house_number = house_numbers[0]
        return int(YEAR_TO_SUBTRACT_FROM - get_house_construction_year(houses_info, house_number))
    except Exception as e:
        # Возвращаем какое-то значение по умолчанию в случае ошибки
        return -1

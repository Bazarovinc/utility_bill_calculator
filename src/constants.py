from enum import Enum

import PySimpleGUI as sg

MONTHS = {
    1: "январь",
    2: "февраль",
    3: "март",
    4: "апрель",
    5: "май",
    6: "июнь",
    7: "июль",
    8: "август",
    9: "сентябрь",
    10: "октябрь",
    11: "ноябрь",
    12: "декабрь",
}
MAIN_TEXT = (
    "{month_pay} оплаты: {months}\n"
    "К оплате за холодную воду: {cold_result}\n"
    "К оплате за горячую воду: {hot_result}\n"
    "К оплате за электроэнергию: {electric_result}\n"
    "Итого: {pay_result}"
)
DEFAULT_INSTRUCTION = (
    "Обновление тарифов коммунальных услуг\n"
    "1. Нажмите кнопку Обновить.\n"
    "2. Измените значения(е) тарифов и нажмите кнопку Сохранить.\n"
    "Расчет платежа\n"
    "1. Введите показания счетчиков в окно каждого из показаний.\n"
    "2. Нажмите кнопку Рассчитать. В окне вывода появится полный расчет.\n"
    "3. Если вы ошиблись в показаниях или хотите изменить тарифы,\nто нажмите кнопку Очистить, "
    "а затем повторите пункты 1 и 2."
)

# BUTTON NAMES
UPDATE_BUTTON: str = "update_button"
SAVE_BUTTON: str = "save_button"
CALCULATE_BUTTON: str = "calculate_button"
CLEAR_BUTTON: str = "clear_button"
CLOSE_BUTTON: str = "close_button"


class ButtonsEnum(str, Enum):
    CLOSE = CLOSE_BUTTON
    UPDATE = UPDATE_BUTTON
    SAVE = SAVE_BUTTON
    CALCULATE = CALCULATE_BUTTON
    CLEAR = CLEAR_BUTTON


# FIELD_NAMES
HOT_TARIFF = "hot_tariff"
COLD_TARIFF = "cold_tariff"
ELECTRICITY_TARIFF = "electricity_tariff"
TARIFF_FIELDS = [HOT_TARIFF, COLD_TARIFF, ELECTRICITY_TARIFF]
HOT_MEASUREMENT = "hot_measurement"
COLD_MEASUREMENT = "cold_measurement"
ELECTRICITY_MEASUREMENT = "electricity_measurement"
MEASUREMENTS_FIELDS = [HOT_MEASUREMENT, COLD_MEASUREMENT, ELECTRICITY_MEASUREMENT]
OUTPUT_FIELD = "output_field"


# Error messages
NO_MEASUREMENTS = "Заполните все показания счетчиков"
NO_TARIFFS = "Заполните все поля тарифов"
NO_CALCULATION = "Расчет не проводился"
CURRENT_MONTH = "Вы уже рассчитывали показания в этом месяце"
WRONG_MEASUREMENTS = "Неверные показания за текущий месяц"

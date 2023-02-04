from datetime import datetime

import PySimpleGUI as sg

from src.constants import (
    CALCULATE_BUTTON,
    CLEAR_BUTTON,
    CLOSE_BUTTON,
    COLD_MEASUREMENT,
    COLD_TARIFF,
    CURRENT_MONTH,
    DEFAULT_INSTRUCTION,
    ELECTRICITY_MEASUREMENT,
    ELECTRICITY_TARIFF,
    HOT_MEASUREMENT,
    HOT_TARIFF,
    MAIN_TEXT,
    MEASUREMENTS_FIELDS,
    NO_CALCULATION,
    NO_MEASUREMENTS,
    NO_TARIFFS,
    OUTPUT_FIELD,
    SAVE_BUTTON,
    TARIFF_FIELDS,
    UPDATE_BUTTON,
    WRONG_MEASUREMENTS,
    ButtonsEnum,
)
from src.data.interfaces import IMeasurementsRepo, ITariffsRepo
from src.dto.app_schemas import AppInputSchema, TraitInfo, Traits, WaterTraitInfo
from src.dto.input import MeasurementsInSchema, TariffsInSchema
from src.dto.output import MeasurementsOutSchema, TariffsOutSchema
from src.dto.types import Month


class UseCase:

    current_measurement: MeasurementsOutSchema | None = None

    def __init__(self, measurements_repo: IMeasurementsRepo, tariffs_repo: ITariffsRepo) -> None:
        self._measurements_repo = measurements_repo
        self._tariffs_repo = tariffs_repo
        sg.theme("Default1")
        self._set_tariffs()
        self._window = sg.Window("Расчет платежа за коммунальные услуги", self._layout)

    def _set_tariffs(self) -> None:
        self.current_tariffs: TariffsOutSchema = self._tariffs_repo.get_last_created()
        self._layout = [
            [sg.Text(DEFAULT_INSTRUCTION)],
            [sg.Text("Тарифы")],
            [
                sg.Text("Горячая вода", text_color="red"),
                sg.InputText(
                    default_text=str(self.current_tariffs.hot_tariff),
                    disabled=True,
                    size=(7, 15),
                    key=HOT_TARIFF,
                ),
                sg.Text("₽ за м^3"),
            ],
            [
                sg.Text("Холодная вода", text_color="blue"),
                sg.InputText(
                    default_text=str(self.current_tariffs.cold_tariff),
                    disabled=True,
                    size=(7, 15),
                    key=COLD_TARIFF,
                ),
                sg.Text("₽ за м^3"),
            ],
            [
                sg.Text("Электричество", text_color="green"),
                sg.InputText(
                    default_text=str(self.current_tariffs.electricity_tariff),
                    disabled=True,
                    size=(7, 15),
                    key=ELECTRICITY_TARIFF,
                ),
                sg.Text("₽ за кВт"),
            ],
            [
                sg.Button("Обновить", key=UPDATE_BUTTON),
                sg.Button("Сохранить", disabled=True, key=SAVE_BUTTON),
            ],
            [sg.Text("Показания счетчиков")],
            [
                sg.Text("Горячая вода", text_color="red"),
                sg.InputText(size=(8, 15), key=HOT_MEASUREMENT),
                sg.Text("м^3"),
            ],
            [
                sg.Text("Холодная вода", text_color="blue"),
                sg.InputText(size=(8, 15), key=COLD_MEASUREMENT),
                sg.Text("м^3"),
            ],
            [
                sg.Text("Электричество", text_color="green"),
                sg.InputText(size=(8, 15), key=ELECTRICITY_MEASUREMENT),
                sg.Text("кВт"),
            ],
            [
                sg.Button("Рассчитать", key=CALCULATE_BUTTON),
                sg.Button("Очистить", key=CLEAR_BUTTON, disabled=True),
            ],
            [sg.Output(size=(60, 10), key=OUTPUT_FIELD)],
            [sg.Button("Закрыть", key=CLOSE_BUTTON)],
        ]

    def _unable_tariffs_update(self) -> None:
        for tariff in TARIFF_FIELDS:
            self._window[tariff].update(disabled=False)
        self._window[SAVE_BUTTON].update(disabled=False)

    def _update_tariffs(self, values_schema: AppInputSchema) -> None:
        if (
            not values_schema.hot_tariff
            or not values_schema.cold_tariff
            or not values_schema.electricity_tariff
        ):
            self._window[OUTPUT_FIELD].update(NO_TARIFFS)
            return
        tariff_schema = TariffsInSchema(**values_schema.dict())
        self.tariff_schema = self._tariffs_repo.create(tariff_schema.dict())
        tariffs = self.tariff_schema.dict()
        for field in TARIFF_FIELDS:
            self._window[field].update(value=tariffs[field])
            self._window[field].update(disabled=True)
        self._window[SAVE_BUTTON].update(disabled=True)
        self._window[UPDATE_BUTTON].update(disabled=False)

    def _check_correct_data(
        self, last_month_data: MeasurementsOutSchema, current_measurement: MeasurementsInSchema
    ) -> list[Month] | None:
        if (
            current_measurement.month > last_month_data.month
            and current_measurement.year == last_month_data.year
            and current_measurement.month - last_month_data.month > 1
        ):
            months = [
                cur_month
                for cur_month in range(last_month_data.month + 1, current_measurement.month + 1)
            ]
        elif (
            current_measurement.month < last_month_data.month
            and current_measurement.year > last_month_data.year
            and current_measurement.month + last_month_data.month != 13
        ):
            months = [i for i in range(last_month_data.month, 13)] + [
                j for j in range(1, current_measurement.month + 1)
            ]
        elif (
            current_measurement.month == last_month_data.month
            and current_measurement.year == last_month_data.year
            and (
                current_measurement.cold_measurement <= last_month_data.cold_measurement
                or current_measurement.hot_measurement <= last_month_data.cold_measurement
                or current_measurement.electricity_measurement
                <= last_month_data.electricity_measurement
            )
        ):
            self._window[OUTPUT_FIELD].update(CURRENT_MONTH)
            return
        elif (
            current_measurement.cold_measurement <= last_month_data.cold_measurement
            or current_measurement.hot_measurement <= last_month_data.hot_measurement
            or current_measurement.electricity_measurement
            <= last_month_data.electricity_measurement
        ):
            self._window[OUTPUT_FIELD].update(WRONG_MEASUREMENTS)
            return
        else:
            months = [current_measurement.month]
        return months

    def _calculate(self, values_schema: AppInputSchema) -> None:
        if (
            not values_schema.hot_measurement
            or not values_schema.cold_measurement
            or not values_schema.electricity_measurement
        ):
            self._window[OUTPUT_FIELD].update(NO_MEASUREMENTS)
            return
        today = datetime.now()
        if today.month == 1:
            month = 12
            year = today.year - 1
        else:
            month = today.month - 1
            year = today.year
        current_measurement = MeasurementsInSchema(
            month=month,
            year=year,
            cold_measurement=values_schema.cold_measurement,
            hot_measurement=values_schema.hot_measurement,
            electricity_measurement=values_schema.electricity_measurement,
        )
        last_month_data: MeasurementsOutSchema = self._measurements_repo.get_last_created()
        months: list[Month] | None = self._check_correct_data(last_month_data, current_measurement)
        if not months:
            return
        traits = Traits(
            cold_trait=WaterTraitInfo(
                trait_now=current_measurement.cold_measurement,
                trait_last_month=last_month_data.cold_measurement,
                tariff=self.current_tariffs.cold_tariff,
            ),
            hot_trait=WaterTraitInfo(
                trait_now=current_measurement.hot_measurement,
                trait_last_month=last_month_data.hot_measurement,
                tariff=self.current_tariffs.hot_tariff,
            ),
            electric_trait=TraitInfo(
                trait_now=current_measurement.electricity_measurement,
                trait_last_month=last_month_data.electricity_measurement,
                tariff=self.current_tariffs.electricity_tariff,
            ),
            months=months,
        )
        self._window[OUTPUT_FIELD].update(
            MAIN_TEXT.format(
                month_pay="Месяц" if len(traits.months) == 1 else "Месяцы",
                months=traits.months_readable,
                cold_result=traits.cold_trait.result_readable,
                hot_result=traits.hot_trait.result_readable,
                electric_result=traits.electric_trait.result_readable,
                pay_result=traits.result_readable,
            )
        )
        self._window[CLEAR_BUTTON].update(disabled=False)
        self._window[CALCULATE_BUTTON].update(disabled=True)
        self.current_measurement = self._measurements_repo.create(current_measurement.dict())

    def _clear_measurements(self) -> None:
        if not self.current_measurement:
            self._window[OUTPUT_FIELD].update(NO_CALCULATION)
            return
        self._measurements_repo.delete(self.current_measurement.id)
        self.current_measurement = None
        for field in MEASUREMENTS_FIELDS:
            self._window[field].update("")
        self._window[CLEAR_BUTTON].update(disabled=True)
        self._window[CALCULATE_BUTTON].update(disabled=False)
        self._window[OUTPUT_FIELD].update("")

    def run(self) -> None:
        while True:
            event, values = self._window.read()
            values_schema = AppInputSchema(**values)
            match event:
                case ButtonsEnum.SAVE:
                    self._update_tariffs(values_schema)
                case ButtonsEnum.UPDATE:
                    self._unable_tariffs_update()
                case ButtonsEnum.CALCULATE:
                    self._calculate(values_schema)
                case ButtonsEnum.CLEAR:
                    self._clear_measurements()
                case ButtonsEnum.CLOSE:
                    return
                case sg.WIN_CLOSED:
                    return

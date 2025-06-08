from aiogram.fsm.state import State, StatesGroup

class WeatherStates(StatesGroup):
    waiting_for_city = State()
    waiting_for_forecast_city = State()
    waiting_for_language = State()

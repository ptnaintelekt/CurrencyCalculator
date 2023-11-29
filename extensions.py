import requests
import json
from config import keys

class ConversionException(Exception):
    pass

class CurrencyConverter:
  @staticmethod
  def convert( base: str, quote: str, amount: float):


      if base == quote:
        raise ConversionException(f"Невозможно конвертирповать одиннаковую валюту {quote} !")


      try:
        base_tick = keys[base]
      except KeyError:
        raise ConversionException(f'Не удалось ообработать валюту {base}')


      try:
        target_tick = keys[quote]
      except KeyError:
        raise ConversionException(f'Не удалось ообработать валюту {quote}')


      try:
        amount = float(amount)
      except ValueError:
        raise ConversionException(f'Не удалось ообработать колличество {amount}')

      base_tick, quote_tick = keys[base], keys[quote]
      r = requests.get(f'https://v6.exchangerate-api.com/v6/3231ec95ed6b81fecf54090c/pair/{base_tick}/{quote_tick}/{amount}')
      total_base = json.loads(r.content)['conversion_result']

      return total_base
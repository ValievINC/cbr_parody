import requests
import csv
from datetime import date, timedelta
from bs4 import BeautifulSoup


def get_data(date_range):
    currency_data = []

    for current_date in date_range:
        print(current_date)
        print(f'{date_range.index(current_date)}/{len(date_range) - 1}')
        formatted_date = current_date.strftime("%d/%m/%Y")
        url = f"http://www.cbr.ru/scripts/XML_daily.asp?date_req={formatted_date}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'lxml')

        crb_date = soup.find('valcurs')['date']

        valutes = soup.find_all('valute')

        for valute in valutes:
            currency_id = valute['id']
            currency_numcode = valute.find('numcode').text.zfill(3)
            currency_charcode = valute.find('charcode').text
            currency_nominal = valute.find('nominal').text
            currency_name = valute.find('name').text
            currency_value = valute.find('value').text

            valute_info = {
                'date': current_date,
                'crb_date': crb_date,
                'ID': currency_id,
                'NumCode': currency_numcode,
                'CharCode': currency_charcode,
                'Nominal': currency_nominal,
                'Name': currency_name,
                'Value': currency_value,
            }

            currency_data.append(valute_info)

    return currency_data


start_date = date(2002, 1, 1)
end_date = date(2023, 6, 20)

date_range = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]

data = get_data(date_range)

with open('valutes.csv', 'w', newline='', encoding='cp1251') as f:
    writer = csv.writer(f)

    headers = ['Date', 'crb_date', 'Value ID', 'NumCode', 'CharCode', 'Nominal', 'Name', 'Value']
    writer.writerow(headers)

    for valute in data:
        row = [valute['date'].strftime("%Y/%m/%d"), valute['crb_date'], valute['ID'], valute['NumCode'],
               valute['CharCode'], valute['Nominal'], valute['Name'], valute['Value']]
        writer.writerow(row)
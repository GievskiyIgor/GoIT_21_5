import aiohttp
import asyncio
import json
import argparse
import httpx
from datetime import datetime, timedelta


async def api_privat (days):
    
    ex_rates =[]
    
    async with aiohttp.ClientSession() as client_session:
          
        for i in range(days):
            date = (datetime.now()-timedelta(days=i)).strftime('%d.%m.%Y')
            url = f'https://api.privatbank.ua/p24api/exchange_rates?json&date={date}'
            
            async with client_session.get(url) as response:
                data = await response.text()
                ex_rates.append({date:parse_currency_data(data)})
            
            return ex_rates


async def parse_currency_data(data):
    currency_data = json.loads(data)
    eur = {'EUR': {'sale': None, 'purchase': None}}
    usd = {'USD': {'sale': None, 'purchase': None}}
    
    for rate in currency_data['exchangeRate']:
        if rate['currency'] == 'EUR':
            eur['EUR']['sale'] = rate['saleRateNB']
            eur['EUR']['purchase'] = rate['purchaseRateNB']
        elif rate['currency'] == 'USD':
            usd['USD']['sale'] = rate['saleRateNB']
            usd['USD']['purchase'] = rate['purchaseRateNB']
            
    return {**eur, **usd}


async def print_currency_rates(ex_rates):
    print (json.dumps(ex_rates, indent=2, ensure_ascii=False))
    

async def sample_exchange_rates(days):
    loop = asyncio.get_event_loop()
    ex_rates = loop.run_until_complete(api_privat(days))
    print_currency_rates(ex_rates)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Get currency rates from PrivatBank API.')
    parser.add_argument('days', type=int, help='Number of days to fetch currency rates (up to 10 days)')
  
    args = parser.parse_args()
        
    if args.days > 10:
         print("Error: You can fetch currency rates for up to 10 days only.")
    else:
        sample_exchange_rates(args.days)
        
        
        
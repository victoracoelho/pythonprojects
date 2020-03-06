import telepot
from datetime import datetime
import numpy as np
import pandas as pd
from pandas_datareader import data as wb

bot = telepot.Bot('TOKEN')
listabvsp = ['WEGE3.SA', 'PETR4.SA', 'VALE3.SA', 'BIDI11.SA', 'BPAC11.SA', 'MRFG3.SA', 'OIBR3.SA', 'EMBR3.SA',
                 'UGPA3.SA', 'TCSA3.SA', 'KLBN3.SA',
                 'GOLL4.SA', 'AZUL4.SA', 'POSI3.SA', 'VVAR3.SA', 'BRFS3.SA', 'BBSE3.SA', 'GOAU4.SA', 'GGBR4.SA', 'HGTX3.SA',
                 'CCRO3.SA', 'BBAS3.SA',
                 'ODPV3.SA', 'MRVE3.SA', 'ITSA4.SA', 'IRBR3.SA', 'ABEV3.SA', 'BBDC4.SA', 'CIEL3.SA', 'USIM5.SA', 'JBSS3.SA',
                 'COGN3.SA', 'NTCO3.SA',
                 'B3SA3.SA', 'HBOR3.SA', 'CVCB3.SA', 'MGLU3.SA', 'CSNA3.SA', 'RAIL3.SA', 'DMMO3.SA', 'HYPE3.SA', 'GFSA3.SA',
                 'BRML3.SA', 'CMIG4.SA',
                 'POMO4.SA', 'LAME4.SA', 'QUAL3.SA', 'RENT3.SA', 'JHSF3.SA', 'BRDT3.SA', 'TIMP3.SA', 'TIET11.SA',
                 'GNDI3.SA', 'ELET6.SA', 'BEEF3.SA']

# This function returns risk premium of a stock that was inputed by the user
def capm(t):
    lista = ['^BVSP']
    ano_atual = datetime.now().date()
    ano_inicio = ano_atual.replace(year=ano_atual.year - 5)
    ano_iniciado = ano_atual.replace(year=ano_atual.year - 10)
    data = pd.DataFrame()
    lista.append(t)
    for t in lista:
        try:
            data[t] = wb.DataReader(t, 'yahoo', ano_inicio, ano_atual)['Adj Close']
            data = data.fillna(method='ffill')
            sec_returns = np.log(data / data.shift(1))
            cov = sec_returns.cov() * 250
            cov_with_market = cov.iloc[0, 1]
            market_var = sec_returns['^BVSP'].var() * 250
            stock_beta = cov_with_market / market_var
            ibov = wb.DataReader('^BVSP', data_source='yahoo', start=ano_iniciado, end=ano_atual)['Adj Close']
            ibov = ibov.fillna(method='ffill')
            retorno = np.log(ibov / ibov.shift(1))
            media = np.mean(retorno)
            retornoIBOV = media * 100
            er = (0.0425 + stock_beta * (retornoIBOV - 0.0425)) * 100
            return er
        except:
            print('CARREGANDO DADOS...')

# This function will receive a message and id by the user and save until call the capm function above
def receber(msg):
    txt = msg['text'].upper()
    _id = msg['from']['id']
    nome = msg['from']['first_name']
    if txt == 'OI':
        bot.sendMessage(chat_id=_id, text=f'Olá {nome}! Digite o ticker do ativo para calcular o Prêmio de Risco: ')
    elif txt in listabvsp:
        bot.sendMessage(chat_id=_id, text=f'O prêmio de risco para {txt} é de aproximadamente {capm(txt):.2f}%')
    else:
        bot.sendMessage(chat_id=_id, text='Digite oi para iniciar')

# Message loop for the app
bot.message_loop(receber)

while True:
    pass

import pandas as pd
import matplotlib.pyplot as plt


ltn2023 = pd.read_csv('ltn01012023.csv',sep=',')


ltn2023 = ltn2023[['Último','Data']]

ltn2023.columns = ['market_pricing','date']
ltn2023.set_index('date',inplace=True)

def str2float(s):
    s = s.replace(',','.')
    return float(s)

ltn2023['market_pricing'] = ltn2023['market_pricing'].apply(str2float)

pu_initial = ltn2023['market_pricing'].iloc[-1]
face = 1000.0
qtd_dias_uteis_total = 964

daily_interest = (face / pu_initial) ** (1 / qtd_dias_uteis_total) - 1

curve_pricing = [pu_initial]

for i in range(ltn2023.shape[0]-1):
    curve_pricing.append( curve_pricing[-1] * (1 + daily_interest) )

curve_pricing.sort(reverse=True)

ltn2023['curve_pricing'] = curve_pricing

ltn2023.sort_values(by='curve_pricing',ascending=True,inplace=True)


plt.style.use(style='ggplot')
fig = plt.figure(figsize=(10,6))
plt.title('Tesouro Prefixado 2023 (LTN 2023)')
plt.xticks([0,ltn2023.shape[0]-1])
plt.xlabel('Data')
plt.ylabel('P.U')
plt.plot(ltn2023['market_pricing'],color='black')
plt.plot(ltn2023['curve_pricing'],color='red')
plt.legend(['Marcação ao Mercado','Marcação na Curva'])
plt.tight_layout()
plt.savefig('marcacao-mercado-vs-marcacao-curva.png')
plt.show()



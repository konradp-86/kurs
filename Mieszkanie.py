import numpy as np
import numpy_financial as npf
import matplotlib.pyplot as plt

poczatkowa_cena = 120000  
roczny_wzrost_cen = 0.05  
lata = 5  
miesiace = lata * 12  

przyszla_cena = poczatkowa_cena * (1 + roczny_wzrost_cen) ** lata
print(f"Orientacyjna cena mieszkania za 5 lat: {przyszla_cena:.2f} zł")

roczna_stopa_procentowa = 0.12 
miesieczna_stopa_procentowa = roczna_stopa_procentowa / 12 

miesieczna_wplata = npf.pmt(rate=miesieczna_stopa_procentowa, nper=miesiace, pv=0, fv=przyszla_cena)
print(f"Miesięczna wpłata do banku: {abs(miesieczna_wplata):.2f} zł")

czas = np.arange(miesiace + 1)
ceny_mieszkan = poczatkowa_cena * (1 + roczny_wzrost_cen / 12) ** czas

wartosc_lokaty = np.zeros(miesiace + 1)
for t in range(1, miesiace + 1):
    wartosc_lokaty[t] = wartosc_lokaty[t - 1] * (1 + miesieczna_stopa_procentowa) + miesieczna_wplata

plt.figure(figsize=(10, 6))
plt.plot(czas, ceny_mieszkan, label='Cena mieszkania')
plt.plot(czas, -wartosc_lokaty, label='Wartość lokaty')
plt.xlabel('Miesiące')
plt.ylabel('Wartość (zł)')
plt.title('Zmiana ceny mieszkania i wartości lokaty w czasie')
plt.legend()
plt.grid(True)
plt.show()

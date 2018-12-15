# FrisbeeGolfFoorumi

Sivulla käyttäjät voivat keskustella frisbee golffin erilaisista aihealueista, muaan muassa varusteista, radoista, kilpailuista jne.
Lisäksi käyttäjät voivat opettaa toisiaan jakamalla hyväksi kokeneitaan harjoitteita, tekniikoita tai linkkejä.
Omien kokemusten ja suoritusten jakaminen on myös sallittua sivulla.

## Heroku

[Heroku](https://frisbee-golf-foorumi.herokuapp.com/)

## Dokumentaatio

[Tuntikirjanpito](https://github.com/Pate1337/FrisbeeGolfFoorumi/blob/master/documentation/tuntikirjanpito.md)

[Tietokantakaavio](https://github.com/Pate1337/FrisbeeGolfFoorumi/blob/master/documentation/tietokantakaavio.md)

[User stories](https://github.com/Pate1337/FrisbeeGolfFoorumi/blob/master/documentation/userstories.md)

## Sovelluksen suorittaminen paikallisesti

Suorita seuraavat askeleet järjestyksessä:

1. Kloonaa repositoria komennolla
```
git clone https://github.com/Pate1337/FrisbeeGolfFoorumi.git
```

2. Mene hakemistoon FrisbeeGolfFoorumi
```
cd FrisbeeGolfFoorumi
```

3. Luo virtuaaliympäristö
```
python3 -m venv venv
```

4. Aktivoi virtuaalinen Python-ympäristö komennolla
```
source venv/bin/activate
```

5. Lataa sovelluksen riippuvuudet
```
pip install -r requirements.txt
```

6. Käynnistä ohjelma komennolla
```
python3 run.py
```

7. Sovellus käynnistyy osoitteeseen localhost:5000

Sovelluksen ADMIN käyttäjän tunnus on admin, salasana admin

Normaalikäyttäjän tunnus on kayttaja, salasana kayttaja (Voit myös luoda uuden käyttäjän, jonka rooli on perus käyttäjä).






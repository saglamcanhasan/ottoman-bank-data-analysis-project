import time
import numpy as np
import pandas as pd
from os.path import join
from rapidfuzz import process, fuzz
from geopy.geocoders import Nominatim

def drop_columns(employee_df, agency_df):
    agency_df = agency_df.loc[:, ["Opening date", "Closing date", "City"]]
    employee_df.drop(columns=["ID"], inplace=True)
    return employee_df, agency_df

def rename_columns(employee_df, agency_df):
    agency_df = agency_df.rename(columns={"Opening date": "Opening Year", "Closing date": "Closing Year"})
    employee_df = employee_df.rename(columns={"employee_code": "ID", "Date": "Record Year", "agency": "Agency", "Grouped_Functions": "Function", "Trait": "Base Salary", "Indemnités": "Allowances",  "merged_religion": "Religion", "start_year": "Career Start Year", "end_year": "Career End Year", "tenure": "Tenure"})
    return employee_df, agency_df

def change_inconsistent_date(agency_df):
    mask = agency_df["City"] == "Rodos"
    closing_year = agency_df.loc[mask, "Closing Year"].values[0]
    agency_df.loc[mask, "Closing Year"] = closing_year.split(",")[1].strip()
    return agency_df

def change_types(agency_df):
    agency_df.loc[:, "Closing Year"] = pd.to_numeric(agency_df["Closing Year"], errors="coerce")
    return agency_df

def deduct_district_city_and_country(employee_df, agency_df):
    agency_to_location = {
        "Adana": {"district": np.nan, "city": "Adana", "country": "Turkey"},
        "Ceyhan": {"district": "Ceyhan", "city": "Adana", "country": "Turkey"},
        "Céhanar": {"district": "Ceyhan", "city": "Adana", "country": "Turkey"},
        "Djihan": {"district": "Ceyhan", "city": "Adana", "country": "Turkey"},
        "Adapazarı": {"district": "Adapazarı", "city": "Sakarya", "country": "Turkey"},
        "Dada-Bazar": {"district": "Adapazarı", "city": "Sakarya", "country": "Turkey"},
        "Afyon Karahisar": {"district": np.nan, "city": "Afyonkarahisar", "country": "Turkey"},
        "Afion-Carahissar": {"district": np.nan, "city": "Afyonkarahisar", "country": "Turkey"},
        "Karahisar": {"district": np.nan, "city": "Afyonkarahisar", "country": "Turkey"},
        "Aspun Karahisar": {"district": np.nan, "city": "Afyonkarahisar", "country": "Turkey"},
        "Bolavadine": {"district": "Bolvadin", "city": "Afyonkarahisar", "country": "Turkey"},
        "Sandikli": {"district": "Sandıklı", "city": "Afyonkarahisar", "country": "Turkey"},
        "Akşehir": {"district": "Akşehir", "city": "Konya", "country": "Turkey"},
        "Ak-Chehir": {"district": "Akşehir", "city": "Konya", "country": "Turkey"},
        "Mt. Chékhir": {"district": "Akşehir", "city": "Konya", "country": "Turkey"},
        "Akçakoca": {"district": "Akçakoca", "city": "Düzce", "country": "Turkey"},
        "Ankara": {"district": np.nan, "city": "Ankara", "country": "Turkey"},
        "Angora": {"district": np.nan, "city": "Ankara", "country": "Turkey"},
        "Angka": {"district": np.nan, "city": "Ankara", "country": "Turkey"},
        "Angora Gare De Lurra": {"district": "Train Station", "city": "Ankara", "country": "Turkey"},
        "Ulus": {"district": "Ulus", "city": "Ankara", "country": "Turkey"},
        "Yenimahalle": {"district": "Yenimahalle", "city": "Ankara", "country": "Turkey"},
        "Antalya": {"district": np.nan, "city": "Antalya", "country": "Turkey"},
        "Adalia": {"district": np.nan, "city": "Antalya", "country": "Turkey"},
        "Idalia": {"district": np.nan, "city": "Antalya", "country": "Turkey"},
        "Aydin": {"district": np.nan, "city": "Aydın", "country": "Turkey"},
        "Iydin": {"district": np.nan, "city": "Aydın", "country": "Turkey"},
        "Aintab": {"district": np.nan, "city": "Gaziantep", "country": "Turkey"},
        "Ayıntap": {"district": np.nan, "city": "Gaziantep", "country": "Turkey"},
        "Antép": {"district": np.nan, "city": "Gaziantep", "country": "Turkey"},
        "Ainalia": {"district": np.nan, "city": "Gaziantep", "country": "Turkey"},
        "Hintab": {"district": np.nan, "city": "Gaziantep", "country": "Turkey"},
        "Gaji Antip": {"district": np.nan, "city": "Gaziantep", "country": "Turkey"},
        "Gaji. Ant.": {"district": np.nan, "city": "Gaziantep", "country": "Turkey"},
        "Gaziantep": {"district": np.nan, "city": "Gaziantep", "country": "Turkey"},
        "Rintab.": {"district": np.nan, "city": "Gaziantep", "country": "Turkey"},
        "Balıkesir": {"district": np.nan, "city": "Balıkesir", "country": "Turkey"},
        "Balkesir": {"district": np.nan, "city": "Balıkesir", "country": "Turkey"},
        "Ayvalık": {"district": "Ayvalık", "city": "Balıkesir", "country": "Turkey"},
        "Bandirma": {"district": "Bandırma", "city": "Balıkesir", "country": "Turkey"},
        "Bandima": {"district": "Bandırma", "city": "Balıkesir", "country": "Turkey"},
        "Panderma": {"district": "Bandırma", "city": "Balıkesir", "country": "Turkey"},
        "Pandema": {"district": "Bandırma", "city": "Balıkesir", "country": "Turkey"},
        "Pauderna": {"district": "Bandırma", "city": "Balıkesir", "country": "Turkey"},
        "Pandernia": {"district": "Bandırma", "city": "Balıkesir", "country": "Turkey"},
        "Bayburt": {"district": np.nan, "city": "Bayburt", "country": "Turkey"},
        "Baibourt": {"district": np.nan, "city": "Bayburt", "country": "Turkey"},
        "Bouibout": {"district": np.nan, "city": "Bayburt", "country": "Turkey"},
        "Biledjik": {"district": np.nan, "city": "Bilecik", "country": "Turkey"},
        "Bitlis": {"district": np.nan, "city": "Bitlis", "country": "Turkey"},
        "Bodrum": {"district": np.nan, "city": "Bodrum", "country": "Turkey"},
        "Bolu": {"district": np.nan, "city": "Bolu", "country": "Turkey"},
        "Bursa": {"district": np.nan, "city": "Bursa", "country": "Turkey"},
        "Broussa": {"district": np.nan, "city": "Bursa", "country": "Turkey"},
        "Brousse": {"district": np.nan, "city": "Bursa", "country": "Turkey"},
        "Cizre": {"district": "Cizre", "city": "Şırnak", "country": "Turkey"},
        "Dardanelles": {"district": np.nan, "city": "Çanakkale", "country": "Turkey"},
        "Denizli": {"district": np.nan, "city": "Denizli", "country": "Turkey"},
        "Dienzi": {"district": np.nan, "city": "Denizli", "country": "Turkey"},
        "Diyarbekir": {"district": np.nan, "city": "Diyarbakır", "country": "Turkey"},
        "Diyarbakır": {"district": np.nan, "city": "Diyarbakır", "country": "Turkey"},
        "Siyarebaki": {"district": np.nan, "city": "Diyarbakır", "country": "Turkey"},
        "Edirne": {"district": np.nan, "city": "Edirne", "country": "Turkey"},
        "Adrianople": {"district": np.nan, "city": "Edirne", "country": "Turkey"},
        "Andrinople": {"district": np.nan, "city": "Edirne", "country": "Turkey"},
        "Edine": {"district": np.nan, "city": "Edirne", "country": "Turkey"},
        "Edurne": {"district": np.nan, "city": "Edirne", "country": "Turkey"},
        "Indrinople": {"district": np.nan, "city": "Edirne", "country": "Turkey"},
        "Erzurum": {"district": np.nan, "city": "Erzurum", "country": "Turkey"},
        "Erzeroum": {"district": np.nan, "city": "Erzurum", "country": "Turkey"},
        "Erzerum": {"district": np.nan, "city": "Erzurum", "country": "Turkey"},
        "Verzoum": {"district": np.nan, "city": "Erzurum", "country": "Turkey"},
        "Eskişehir": {"district": np.nan, "city": "Eskişehir", "country": "Turkey"},
        "Eski-Chehir": {"district": np.nan, "city": "Eskişehir", "country": "Turkey"},
        "Ekişehir": {"district": np.nan, "city": "Eskişehir", "country": "Turkey"},
        "Giresun": {"district": np.nan, "city": "Giresun", "country": "Turkey"},
        "Kerassunde": {"district": np.nan, "city": "Giresun", "country": "Turkey"},
        "Kerasounde": {"district": np.nan, "city": "Giresun", "country": "Turkey"},
        "Kerssund": {"district": np.nan, "city": "Giresun", "country": "Turkey"},
        "Gumuldjina": {"district": np.nan, "city": "Gümüşhane", "country": "Turkey"},
        "Ineboli": {"district": "İnebolu", "city": "Kastamonu", "country": "Turkey"},
        "Mebolu": {"district": "İnebolu", "city": "Kastamonu", "country": "Turkey"},
        "Kastamonu": {"district": np.nan, "city": "Kastamonu", "country": "Turkey"},
        "Castamonu": {"district": np.nan, "city": "Kastamonu", "country": "Turkey"},
        "Castamboul": {"district": np.nan, "city": "Kastamonu", "country": "Turkey"},
        "Castamboli": {"district": np.nan, "city": "Kastamonu", "country": "Turkey"},
        "Kayseri": {"district": np.nan, "city": "Kayseri", "country": "Turkey"},
        "Kayser": {"district": np.nan, "city": "Kayseri", "country": "Turkey"},
        "Cesaree": {"district": np.nan, "city": "Kayseri", "country": "Turkey"},
        "Césarée": {"district": np.nan, "city": "Kayseri", "country": "Turkey"},
        "Césaré": {"district": np.nan, "city": "Kayseri", "country": "Turkey"},
        "Césarè": {"district": np.nan, "city": "Kayseri", "country": "Turkey"},
        "Kirklareli": {"district": np.nan, "city": "Kırklareli", "country": "Turkey"},
        "Kirklarlı": {"district": np.nan, "city": "Kırklareli", "country": "Turkey"},
        "Kirkila": {"district": np.nan, "city": "Kırklareli", "country": "Turkey"},
        "Konya": {"district": np.nan, "city": "Konya", "country": "Turkey"},
        "Konia": {"district": np.nan, "city": "Konya", "country": "Turkey"},
        "Konyu": {"district": np.nan, "city": "Konya", "country": "Turkey"},
        "Manisa": {"district": np.nan, "city": "Manisa", "country": "Turkey"},
        "Kula": {"district": "Kula", "city": "Manisa", "country": "Turkey"},
        "Kütahya": {"district": np.nan, "city": "Kütahya", "country": "Turkey"},
        "Kutahia": {"district": np.nan, "city": "Kütahya", "country": "Turkey"},
        "Kutharia": {"district": np.nan, "city": "Kütahya", "country": "Turkey"},
        "Lüleburgaz": {"district": np.nan, "city": "Lüleburgaz", "country": "Turkey"},
        "Malatya": {"district": np.nan, "city": "Malatya", "country": "Turkey"},
        "Malatia": {"district": np.nan, "city": "Malatya", "country": "Turkey"},
        "Malatie": {"district": np.nan, "city": "Malatya", "country": "Turkey"},
        "Maras": {"district": np.nan, "city": "Kahramanmaraş", "country": "Turkey"},
        "Mersin": {"district": np.nan, "city": "Mersin", "country": "Turkey"},
        "Mersina": {"district": np.nan, "city": "Mersin", "country": "Turkey"},
        "Mersine": {"district": np.nan, "city": "Mersin", "country": "Turkey"},
        "Mesrrine": {"district": np.nan, "city": "Mersin", "country": "Turkey"},
        "Milas": {"district": "Milas", "city": "Muğla", "country": "Turkey"},
        "Muş": {"district": np.nan, "city": "Muş", "country": "Turkey"},
        "Muşkiye": {"district": np.nan, "city": "Muş", "country": "Turkey"},
        "Nazilli": {"district": "Nazilli", "city": "Aydın", "country": "Turkey"},
        "Nazil": {"district": "Nazilli", "city": "Aydın", "country": "Turkey"},
        "Nazli": {"district": "Nazilli", "city": "Aydın", "country": "Turkey"},
        "Nazlı": {"district": "Nazilli", "city": "Aydın", "country": "Turkey"},
        "Nazzilli": {"district": "Nazilli", "city": "Aydın", "country": "Turkey"},
        "Ordu": {"district": np.nan, "city": "Ordu", "country": "Turkey"},
        "Ordou": {"district": np.nan, "city": "Ordu", "country": "Turkey"},
        "Sakarya": {"district": np.nan, "city": "Sakarya", "country": "Turkey"},
        "Samsun": {"district": np.nan, "city": "Samsun", "country": "Turkey"},
        "Samsoun": {"district": np.nan, "city": "Samsun", "country": "Turkey"},
        "Samoun": {"district": np.nan, "city": "Samsun", "country": "Turkey"},
        "Selçuk": {"district": "Selçuk", "city": "İzmir", "country": "Turkey"},
        "Smyrna": {"district": np.nan, "city": "İzmir", "country": "Turkey"},
        "Smyeuze": {"district": np.nan, "city": "İzmir", "country": "Turkey"},
        "Imyne": {"district": np.nan, "city": "İzmir", "country": "Turkey"},
        "Imynra": {"district": np.nan, "city": "İzmir", "country": "Turkey"},
        "Sivas": {"district": np.nan, "city": "Sivas", "country": "Turkey"},
        "Sivras": {"district": np.nan, "city": "Sivas", "country": "Turkey"},
        "Sibâs": {"district": np.nan, "city": "Sivas", "country": "Turkey"},
        "Tarsus": {"district": "Tarsus", "city": "Mersin", "country": "Turkey"},
        "Tarsous": {"district": "Tarsus", "city": "Mersin", "country": "Turkey"},
        "Tekirdağ": {"district": np.nan, "city": "Tekirdağ", "country": "Turkey"},
        "Tekirdag": {"district": np.nan, "city": "Tekirdağ", "country": "Turkey"},
        "Rodosto": {"district": np.nan, "city": "Tekirdağ", "country": "Turkey"},
        "Cekirdagh": {"district": np.nan, "city": "Tekirdağ", "country": "Turkey"},
        "Bekirdagh": {"district": np.nan, "city": "Tekirdağ", "country": "Turkey"},
        "Bekirdağ": {"district": np.nan, "city": "Tekirdağ", "country": "Turkey"},
        "Çekirdağ": {"district": np.nan, "city": "Tekirdağ", "country": "Turkey"},
        "Rodost": {"district": np.nan, "city": "Tekirdağ", "country": "Turkey"},
        "Trabzon": {"district": np.nan, "city": "Trabzon", "country": "Turkey"},
        "Trebizonde": {"district": np.nan, "city": "Trabzon", "country": "Turkey"},
        "Truzon": {"district": np.nan, "city": "Trabzon", "country": "Turkey"},
        "Crebizonde": {"district": np.nan, "city": "Trabzon", "country": "Turkey"},
        "Cretizonda": {"district": np.nan, "city": "Trabzon", "country": "Turkey"},
        "Urfa": {"district": np.nan, "city": "Şanlıurfa", "country": "Turkey"},
        "Ourfa": {"district": np.nan, "city": "Şanlıurfa", "country": "Turkey"},
        "Urfak": {"district": np.nan, "city": "Şanlıurfa", "country": "Turkey"},
        "Ouwfa": {"district": np.nan, "city": "Şanlıurfa", "country": "Turkey"},
        "Uşak": {"district": np.nan, "city": "Uşak", "country": "Turkey"},
        "Usak": {"district": np.nan, "city": "Uşak", "country": "Turkey"},
        "Ochak": {"district": np.nan, "city": "Uşak", "country": "Turkey"},
        "Ouchak": {"district": np.nan, "city": "Uşak", "country": "Turkey"},
        "Ouçhak": {"district": np.nan, "city": "Uşak", "country": "Turkey"},
        "Couchak": {"district": np.nan, "city": "Uşak", "country": "Turkey"},
        "Van": {"district": np.nan, "city": "Van", "country": "Turkey"},
        "Zonguldak": {"district": np.nan, "city": "Zonguldak", "country": "Turkey"},
        "Jonqulak": {"district": np.nan, "city": "Zonguldak", "country": "Turkey"},
        "Elaziz": {"district": np.nan, "city": "Elazığ", "country": "Turkey"},
        "Elazığ": {"district": np.nan, "city": "Elazığ", "country": "Turkey"},
        "Mamouret-Ul-Aziz": {"district": np.nan, "city": "Elazığ", "country": "Turkey"},
        "Güzelbahçe": {"district": "Güzelbahçe", "city": "İzmir", "country": "Turkey"},
        "Yesil Cami": {"district": "Yeşil Cami", "city": "Bursa", "country": "Turkey"},
        "Ayasi": {"district": "Ayaş", "city": "Ankara", "country": "Turkey"},
        "Cersin": {"district": np.nan, "city": "Mersin", "country": "Turkey"},
        "Cerum": {"district": np.nan, "city": "Çorum", "country": "Turkey"},
        "Chéroum": {"district": np.nan, "city": "Çorum", "country": "Turkey"},
        "Cevah - İStanbul": {"district": np.nan, "city": "İstanbul", "country": "Turkey"},
        "Corum": {"district": np.nan, "city": "Çorum", "country": "Turkey"},
        "Demirci": {"district": "Demirci", "city": "Manisa", "country": "Turkey"},
        "Eyyübiye": {"district": "Eyyübiye", "city": "Şanlıurfa", "country": "Turkey"},
        "Görün": {"district": "Gürün", "city": "Sivas", "country": "Turkey"},
        "Karpuzlu": {"district": "Karpuzlu", "city": "Aydın", "country": "Turkey"},
        "Kurtkale": {"district": "Kurtkale", "city": "Ardahan", "country": "Turkey"},
        "Kustaria": {"district": np.nan, "city": "Kastoria", "country": "Greece"},
        "Milans": {"district": np.nan, "city": "Milas", "country": "Turkey"},
        "Rumeli": {"district": np.nan, "city": np.nan, "country": "Balkans Region"},
        "Técheroum": {"district": np.nan, "city": "Çorum", "country": "Turkey"},
        "Zeytun": {"district": "Süleymanlı", "city": "Kahramanmaraş", "country": "Turkey"},
        "Istanbul": {"district": np.nan, "city": "İstanbul", "country": "Turkey"},
        "Constantinople": {"district": np.nan, "city": "İstanbul", "country": "Turkey"},
        "Établissement De Constantinople": {"district": "Pera", "city": "İstanbul", "country": "Turkey"},
        "Siege Central": {"district": "Pera", "city": "İstanbul", "country": "Turkey"},
        "Siège": {"district": "Pera", "city": "İstanbul", "country": "Turkey"},
        "Le Siège": {"district": "Pera", "city": "İstanbul", "country": "Turkey"},
        "Centre": {"district": "Pera", "city": "İstanbul", "country": "Turkey"},
        "S. Cedral": {"district": "Pera", "city": "İstanbul", "country": "Turkey"},
        "Cendal": {"district": "Pera", "city": "İstanbul", "country": "Turkey"},
        "Ceytral": {"district": "Pera", "city": "İstanbul", "country": "Turkey"},
        "Beyoğlu": {"district": "Pera", "city": "İstanbul", "country": "Turkey"},
        "Beyoglu": {"district": "Pera", "city": "İstanbul", "country": "Turkey"},
        "Boyoglu": {"district": "Pera", "city": "İstanbul", "country": "Turkey"},
        "Pera": {"district": "Pera", "city": "İstanbul", "country": "Turkey"},
        "Péra": {"district": "Pera", "city": "İstanbul", "country": "Turkey"},
        "Galata": {"district": "Pera", "city": "İstanbul", "country": "Turkey"},
        "Stamboul": {"district": "Fatih", "city": "İstanbul", "country": "Turkey"},
        "Shamboul": {"district": "Fatih", "city": "İstanbul", "country": "Turkey"},
        "Yeni Cami": {"district": "Yeni Cami", "city": "İstanbul", "country": "Turkey"},
        "Yen-Cami": {"district": "Yeni Cami", "city": "İstanbul", "country": "Turkey"},
        "Yeni Camı": {"district": "Yeni Cami", "city": "İstanbul", "country": "Turkey"},
        "Yeni-Cami": {"district": "Yeni Cami", "city": "İstanbul", "country": "Turkey"},
        "Yeni-Cam": {"district": "Yeni Cami", "city": "İstanbul", "country": "Turkey"},
        "Yeniami": {"district": "Yeni Cami", "city": "İstanbul", "country": "Turkey"},
        "Yenicami": {"district": "Yeni Cami", "city": "İstanbul", "country": "Turkey"},
        "Yenican": {"district": "Yeni Cami", "city": "İstanbul", "country": "Turkey"},
        "Yenikami": {"district": "Yeni Cami", "city": "İstanbul", "country": "Turkey"},
        "Yeniçami": {"district": "Yeni Cami", "city": "İstanbul", "country": "Turkey"},
        "Yeni̇-Cami̇": {"district": "Yeni Cami", "city": "İstanbul", "country": "Turkey"},
        "Yeni̇Cami̇": {"district": "Yeni Cami", "city": "İstanbul", "country": "Turkey"},
        "Merlin": {"district": np.nan, "city": "Mersin", "country": "Turkey"},
        "Ceyran": {"district": "Ceyhan", "city": "Adana", "country": "Turkey"},
        "Baliseur": {"district": np.nan, "city": "Balıkesir", "country": "Turkey"},
        "Küthyra": {"district": np.nan, "city": "Kütahya", "country": "Turkey"},
        "Kona": {"district": np.nan, "city": "Konya", "country": "Turkey"},
        "Longudak": {"district": np.nan, "city": "Zonguldak", "country": "Turkey"},
        "Longoulard": {"district": np.nan, "city": "Zonguldak", "country": "Turkey"},
        "Longoudak": {"district": np.nan, "city": "Zonguldak", "country": "Turkey"},
        "Arnavutköy": {"district": "Arnavutköy", "city": "İstanbul", "country": "Turkey"},
        "Beyazıt": {"district": "Beyazıt", "city": "İstanbul", "country": "Turkey"},
        "Beykoz": {"district": "Beykoz", "city": "İstanbul", "country": "Turkey"},
        "Beylerbeyi": {"district": "Beylerbeyi", "city": "İstanbul", "country": "Turkey"},
        "Erenköy": {"district": "Erenköy", "city": "İstanbul", "country": "Turkey"},
        "Göztepe": {"district": "Göztepe", "city": "İstanbul", "country": "Turkey"},
        "Halkalı": {"district": "Halkalı", "city": "İstanbul", "country": "Turkey"},
        "Haydarpaşa": {"district": "Haydarpaşa", "city": "İstanbul", "country": "Turkey"},
        "Yenikapı": {"district": "Yenikapı", "city": "İstanbul", "country": "Turkey"},
        "Yenikapi": {"district": "Yenikapı", "city": "İstanbul", "country": "Turkey"},
        "Zeytinburnu": {"district": "Zeytinburnu", "city": "İstanbul", "country": "Turkey"},
        "Şişli": {"district": "Şişli", "city": "İstanbul", "country": "Turkey"},
        "Beirut": {"district": np.nan, "city": "Beirut", "country": "Lebanon"},
        "Beyrouth": {"district": np.nan, "city": "Beirut", "country": "Lebanon"},
        "Beirout": {"district": np.nan, "city": "Beirut", "country": "Lebanon"},
        "Bayrut": {"district": np.nan, "city": "Beirut", "country": "Lebanon"},
        "Peyrouth": {"district": np.nan, "city": "Beirut", "country": "Lebanon"},
        "Reynouth": {"district": np.nan, "city": "Beirut", "country": "Lebanon"},
        "Tripoli": {"district": np.nan, "city": "Tripoli", "country": "Lebanon"},
        "Zahle": {"district": np.nan, "city": "Zahle", "country": "Lebanon"},
        "Aleppo": {"district": np.nan, "city": "Aleppo", "country": "Syria"},
        "Damas": {"district": np.nan, "city": "Damascus", "country": "Syria"},
        "Damascus": {"district": np.nan, "city": "Damascus", "country": "Syria"},
        "Damascusa": {"district": np.nan, "city": "Damascus", "country": "Syria"},
        "Dammas": {"district": np.nan, "city": "Damascus", "country": "Syria"},
        "Hama": {"district": np.nan, "city": "Hama", "country": "Syria"},
        "Hamah": {"district": np.nan, "city": "Hama", "country": "Syria"},
        "Homs": {"district": np.nan, "city": "Homs", "country": "Syria"},
        "Syrie": {"district": np.nan, "city": np.nan, "country": "Syria"},
        "Salonica": {"district": np.nan, "city": "Thessaloniki", "country": "Greece"},
        "Salonique": {"district": np.nan, "city": "Thessaloniki", "country": "Greece"},
        "Dedeagatch": {"district": np.nan, "city": "Alexandroupoli", "country": "Greece"},
        "Drama": {"district": np.nan, "city": "Drama", "country": "Greece"},
        "Héraklion": {"district": np.nan, "city": "Heraklion", "country": "Greece"},
        "Janina": {"district": np.nan, "city": "Ioannina", "country": "Greece"},
        "Yannina": {"district": np.nan, "city": "Ioannina", "country": "Greece"},
        "Janisa": {"district": np.nan, "city": "Ioannina", "country": "Greece"},
        "Cavalla": {"district": np.nan, "city": "Kavala", "country": "Greece"},
        "Metelin": {"district": np.nan, "city": "Mytilene", "country": "Greece"},
        "Rhodes": {"district": np.nan, "city": "Rhodes", "country": "Greece"},
        "Serres": {"district": np.nan, "city": "Serres", "country": "Greece"},
        "Xanthib": {"district": np.nan, "city": "Xanthi", "country": "Greece"},
        "Milos": {"district": np.nan, "city": "Milos", "country": "Greece"},
        "Alexandria": {"district": np.nan, "city": "Alexandria", "country": "Egypt"},
        "Cairo": {"district": np.nan, "city": "Cairo", "country": "Egypt"},
        "Le Caïre": {"district": np.nan, "city": "Cairo", "country": "Egypt"},
        "Ismailia": {"district": np.nan, "city": "Ismailia", "country": "Egypt"},
        "Mansourah": {"district": np.nan, "city": "Mansoura", "country": "Egypt"},
        "Mausourah": {"district": np.nan, "city": "Mansoura", "country": "Egypt"},
        "Minieh": {"district": np.nan, "city": "Minya", "country": "Egypt"},
        "Port-Said": {"district": np.nan, "city": "Port Said", "country": "Egypt"},
        "Bot-Said": {"district": np.nan, "city": "Port Said", "country": "Egypt"},
        "Aïrus": {"district": np.nan, "city": "Arish", "country": "Egypt"},
        "Bagdad": {"district": np.nan, "city": "Baghdad", "country": "Iraq"},
        "Baglaz": {"district": np.nan, "city": "Baghdad", "country": "Iraq"},
        "Bragdalot": {"district": np.nan, "city": "Baghdad", "country": "Iraq"},
        "Basrah": {"district": np.nan, "city": "Basra", "country": "Iraq"},
        "Baasrah": {"district": np.nan, "city": "Basra", "country": "Iraq"},
        "Bassanah": {"district": np.nan, "city": "Basra", "country": "Iraq"},
        "Bassorah": {"district": np.nan, "city": "Basra", "country": "Iraq"},
        "Kirkuk": {"district": np.nan, "city": "Kirkuk", "country": "Iraq"},
        "Mosul": {"district": np.nan, "city": "Mosul", "country": "Iraq"},
        "Mossoul": {"district": np.nan, "city": "Mosul", "country": "Iraq"},
        "Mossou": {"district": np.nan, "city": "Mosul", "country": "Iraq"},
        "Samarra": {"district": np.nan, "city": "Samarra", "country": "Iraq"},
        "Chypre": {"district": np.nan, "city": np.nan, "country": "Cyprus"},
        "Famagusta": {"district": np.nan, "city": "Famagusta", "country": "Cyprus"},
        "Famagousta": {"district": np.nan, "city": "Famagusta", "country": "Cyprus"},
        "Tamağusta": {"district": np.nan, "city": "Famagusta", "country": "Cyprus"},
        "Larnaca": {"district": np.nan, "city": "Larnaca", "country": "Cyprus"},
        "Sarnaca": {"district": np.nan, "city": "Larnaca", "country": "Cyprus"},
        "Limassol": {"district": np.nan, "city": "Limassol", "country": "Cyprus"},
        "Limalia": {"district": np.nan, "city": "Limassol", "country": "Cyprus"},
        "Nicosia": {"district": np.nan, "city": "Nicosia", "country": "Cyprus"},
        "Nicosie": {"district": np.nan, "city": "Nicosia", "country": "Cyprus"},
        "Paphos": {"district": np.nan, "city": "Paphos", "country": "Cyprus"},
        "Caïfa": {"district": np.nan, "city": "Haifa", "country": "Israel"},
        "Caïffa": {"district": np.nan, "city": "Haifa", "country": "Israel"},
        "Aïfa": {"district": np.nan, "city": "Haifa", "country": "Israel"},
        "Ouifa": {"district": np.nan, "city": "Haifa", "country": "Israel"},
        "Jaffa": {"district": np.nan, "city": "Jaffa", "country": "Israel"},
        "Loffa": {"district": np.nan, "city": "Jaffa", "country": "Israel"},
        "Jerusalem": {"district": np.nan, "city": "Jerusalem", "country": "Israel"},
        "Nablous": {"district": np.nan, "city": "Nablus", "country": "Palestine"},
        "Naplouse": {"district": np.nan, "city": "Nablus", "country": "Palestine"},
        "Tel Aviv": {"district": np.nan, "city": "Tel Aviv", "country": "Israel"},
        "Amman": {"district": np.nan, "city": "Amman", "country": "Jordan"},
        "Djeddah": {"district": np.nan, "city": "Jeddah", "country": "Saudi Arabia"},
        "Djidda": {"district": np.nan, "city": "Jeddah", "country": "Saudi Arabia"},
        "Diddah": {"district": np.nan, "city": "Jeddah", "country": "Saudi Arabia"},
        "Hamadan": {"district": np.nan, "city": "Hamadan", "country": "Iran"},
        "Hamedan": {"district": np.nan, "city": "Hamadan", "country": "Iran"},
        "Hamadân": {"district": np.nan, "city": "Hamadan", "country": "Iran"},
        "Hammadan": {"district": np.nan, "city": "Hamadan", "country": "Iran"},
        "Yamadan": {"district": np.nan, "city": "Hamadan", "country": "Iran"},
        "Kermanshah": {"district": np.nan, "city": "Kermanshah", "country": "Iran"},
        "Kermanşah": {"district": np.nan, "city": "Kermanshah", "country": "Iran"},
        "Kirmansah": {"district": np.nan, "city": "Kermanshah", "country": "Iran"},
        "Kermanstad": {"district": np.nan, "city": "Kermanshah", "country": "Iran"},
        "Sultanabad": {"district": np.nan, "city": "Arak", "country": "Iran"},
        "Sultankabad": {"district": np.nan, "city": "Arak", "country": "Iran"},
        "Tehran": {"district": np.nan, "city": "Tehran", "country": "Iran"},
        "Teheran": {"district": np.nan, "city": "Tehran", "country": "Iran"},
        "Téhéran": {"district": np.nan, "city": "Tehran", "country": "Iran"},
        "Téléran": {"district": np.nan, "city": "Tehran", "country": "Iran"},
        "Alger": {"district": np.nan, "city": "Algiers", "country": "Algeria"},
        "Besançon": {"district": np.nan, "city": "Besançon", "country": "France"},
        "Cahul": {"district": np.nan, "city": "Cahul", "country": "Moldova"},
        "Celle": {"district": np.nan, "city": "Celle", "country": "Germany"},
        "Cette": {"district": np.nan, "city": "Sète", "country": "France"},
        "Danzig": {"district": np.nan, "city": "Gdańsk", "country": "Poland"},
        "Dijon": {"district": np.nan, "city": "Dijon", "country": "France"},
        "Genève": {"district": np.nan, "city": "Geneva", "country": "Switzerland"},
        "Hambourg": {"district": np.nan, "city": "Hamburg", "country": "Germany"},
        "Hermanstadt": {"district": np.nan, "city": "Sibiu", "country": "Romania"},
        "London": {"district": np.nan, "city": "London", "country": "United Kingdom"},
        "Londres": {"district": np.nan, "city": "London", "country": "United Kingdom"},
        "Londres Central": {"district": "Central", "city": "London", "country": "United Kingdom"},
        "Lyon": {"district": np.nan, "city": "Lyon", "country": "France"},
        "Manchester": {"district": np.nan, "city": "Manchester", "country": "United Kingdom"},
        "Marseille": {"district": np.nan, "city": "Marseille", "country": "France"},
        "Monastir": {"district": np.nan, "city": "Bitola", "country": "North Macedonia"},
        "Monoltër": {"district": np.nan, "city": "Bitola", "country": "North Macedonia"},
        "Munich": {"district": np.nan, "city": "Munich", "country": "Germany"},
        "Naples": {"district": np.nan, "city": "Naples", "country": "Italy"},
        "Nîmes": {"district": np.nan, "city": "Nîmes", "country": "France"},
        "Odessa": {"district": np.nan, "city": "Odesa", "country": "Ukraine"},
        "Scutari": {"district": np.nan, "city": "Shkodër", "country": "Albania"},
        "Sofia": {"district": np.nan, "city": "Sofia", "country": "Bulgaria"},
        "Tiflis": {"district": np.nan, "city": "Tbilisi", "country": "Georgia"},
        "Tunis": {"district": np.nan, "city": "Tunis", "country": "Tunisia"},
        "Uskub": {"district": np.nan, "city": "Skopje", "country": "North Macedonia"},
        "Venise": {"district": np.nan, "city": "Venice", "country": "Italy"},
        "Yerevan": {"district": np.nan, "city": "Yerevan", "country": "Armenia"},
        "Espagne": {"district": np.nan, "city": np.nan, "country": "Spain"},
        "Malta": {"district": np.nan, "city": "Malta", "country": "Malta"},
        "Rumeli": {"district": np.nan, "city": np.nan, "country": "Balkans Region"},
        "Ottawa": {"district": np.nan, "city": "Ottawa", "country": "Canada"},
        "Casablanca": {"district": np.nan, "city": "Casablanca", "country": "Morocco"},
        "Dakar": {"district": np.nan, "city": "Dakar", "country": "Senegal"},
        "Kenya": {"district": np.nan, "city": np.nan, "country": "Kenya"},
        "Nairobi": {"district": np.nan, "city": "Nairobi", "country": "Kenya"},
        "Tanger": {"district": np.nan, "city": "Tangier", "country": "Morocco"},
        "Tripole": {"district": np.nan, "city": "Tripoli", "country": "Libya"},
        "Maghreb": {"district": np.nan, "city": np.nan, "country": "Maghreb Region"},
        "Bahrein": {"district": np.nan, "city": np.nan, "country": "Bahrain"},
        "Inde": {"district": np.nan, "city": np.nan, "country": "India"},
        "Pékin": {"district": np.nan, "city": "Beijing", "country": "China"},
        "Ain": {"district": np.nan, "city": "Ain", "country": "France"},
        "Alaouites": {"district": np.nan, "city": "Latakia", "country": "Syria"},
        "Arménie": {"district": np.nan, "city": np.nan, "country": "Armenia"},
        "Beyrut": {"district": np.nan, "city": "Beirut", "country": "Lebanon"},
        "Carsous": {"district": "Tarsus", "city": "Mersin", "country": "Turkey"},
        "Carsus": {"district": "Tarsus", "city": "Mersin", "country": "Turkey"},
        "Chorum": {"district": np.nan, "city": "Çorum", "country": "Turkey"},
        "Diarbekir": {"district": np.nan, "city": "Diyarbakır", "country": "Turkey"},
        "Echoroum": {"district": np.nan, "city": "Çorum", "country": "Turkey"},
        "Hamadam": {"district": np.nan, "city": "Hamadan", "country": "Iran"},
        "Katalya": {"district": np.nan, "city": "Antalya", "country": "Turkey"},
        "Korevizound": {"district": np.nan, "city": "Trabzon", "country": "Turkey"},
        "Limni": {"district": np.nan, "city": "Limni", "country": "Greece"},
        "Mahrid": {"district": np.nan, "city": "Madrid", "country": "Spain"},
        "Mers": {"district": np.nan, "city": "Mersin", "country": "Turkey"},
        "Mesrine": {"district": np.nan, "city": "Mersin", "country": "Turkey"},
        "Micosié": {"district": np.nan, "city": "Nicosia", "country": "Cyprus"},
        "Montral": {"district": np.nan, "city": "Montreal", "country": "Canada"},
        "Moria": {"district": np.nan, "city": "Morea", "country": "Greece"},
        "Mousky": {"district": "Muski", "city": "Cairo", "country": "Egypt"},
        "Nicore": {"district": np.nan, "city": "Nicosia", "country": "Cyprus"},
        "Nicée": {"district": np.nan, "city": "İznik", "country": "Turkey"},
        "Nîmsa": {"district": np.nan, "city": np.nan, "country": "Austria"},
        "Ordo": {"district": np.nan, "city": "Ordu", "country": "Turkey"},
        "Ordon": {"district": np.nan, "city": "Ordu", "country": "Turkey"},
        "Pau.": {"district": np.nan, "city": "Pau", "country": "France"},
        "Rodato": {"district": np.nan, "city": "Tekirdağ", "country": "Turkey"},
        "Rodoto": {"district": np.nan, "city": "Tekirdağ", "country": "Turkey"},
        "Urfa": {"district": np.nan, "city": "Şanlıurfa", "country": "Russia"},
        "Vanisa": {"district": np.nan, "city": "Manisa", "country": "Turkey"},
        "Adana": {"district": np.nan, "city": "Adana", "country": "Turkey"},
        "Adapazarı": {"district": "Adapazarı", "city": "Sakarya", "country": "Turkey"},
        "Akşehir": {"district": "Akşehir", "city": "Konya", "country": "Turkey"},
        "Antalya": {"district": np.nan, "city": "Antalya", "country": "Turkey"},
        "Antep": {"district": np.nan, "city": "Gaziantep", "country": "Turkey"},
        "Aydın": {"district": np.nan, "city": "Aydın", "country": "Turkey"},
        "Balıkesir": {"district": np.nan, "city": "Balıkesir", "country": "Turkey"},
        "Bandırma": {"district": "Bandırma", "city": "Balıkesir", "country": "Turkey"},
        "Bilecik": {"district": np.nan, "city": "Bilecik", "country": "Turkey"},
        "Bitlis": {"district": np.nan, "city": "Bitlis", "country": "Turkey"},
        "Bolu": {"district": np.nan, "city": "Bolu", "country": "Turkey"},
        "Bolvadin": {"district": "Bolvadin", "city": "Afyonkarahisar", "country": "Turkey"},
        "Ceyhan": {"district": "Ceyhan", "city": "Adana", "country": "Turkey"},
        "Denizli": {"district": np.nan, "city": "Denizli", "country": "Turkey"},
        "Diyarbekir": {"district": np.nan, "city": "Diyarbakır", "country": "Turkey"},
        "Edirne": {"district": np.nan, "city": "Edirne", "country": "Turkey"},
        "Erzurum": {"district": np.nan, "city": "Erzurum", "country": "Turkey"},
        "Eskişehir": {"district": np.nan, "city": "Eskişehir", "country": "Turkey"},
        "Geyve": {"district": "Geyve", "city": "Sakarya", "country": "Turkey"},
        "Giresun": {"district": np.nan, "city": "Giresun", "country": "Turkey"},
        "Harput": {"district": "Harput", "city": "Elazığ", "country": "Turkey"},
        "Isparta": {"district": np.nan, "city": "Isparta", "country": "Turkey"},
        "Izmir": {"district": np.nan, "city": "İzmir", "country": "Turkey"},
        "Kastamonu": {"district": np.nan, "city": "Kastamonu", "country": "Turkey"},
        "Kayseri": {"district": np.nan, "city": "Kayseri", "country": "Turkey"},
        "Konya": {"district": np.nan, "city": "Konya", "country": "Turkey"},
        "Kütahya": {"district": np.nan, "city": "Kütahya", "country": "Turkey"},
        "Manisa": {"district": np.nan, "city": "Manisa", "country": "Turkey"},
        "Muğla": {"district": np.nan, "city": "Muğla", "country": "Turkey"},
        "Nazilli": {"district": "Nazilli", "city": "Aydın", "country": "Turkey"},
        "Ordu": {"district": np.nan, "city": "Ordu", "country": "Turkey"},
        "Samsun": {"district": np.nan, "city": "Samsun", "country": "Turkey"},
        "Sandıklı": {"district": "Sandıklı", "city": "Afyonkarahisar", "country": "Turkey"},
        "Silifke": {"district": "Silifke", "city": "Mersin", "country": "Turkey"},
        "Sivas": {"district": np.nan, "city": "Sivas", "country": "Turkey"},
        "Söke": {"district": "Söke", "city": "Aydın", "country": "Turkey"},
        "Tarsus": {"district": "Tarsus", "city": "Mersin", "country": "Turkey"},
        "Tekirdağ": {"district": np.nan, "city": "Tekirdağ", "country": "Turkey"},
        "Trabzon": {"district": np.nan, "city": "Trabzon", "country": "Turkey"},
        "Urfa": {"district": np.nan, "city": "Şanlıurfa", "country": "Turkey"},
        "Uşak": {"district": np.nan, "city": "Uşak", "country": "Turkey"},
        "Van": {"district": np.nan, "city": "Van", "country": "Turkey"},
        "Çanakkale": {"district": np.nan, "city": "Çanakkale", "country": "Turkey"},
        "İnebolu": {"district": "İnebolu", "city": "Kastamonu", "country": "Turkey"},
        "İskenderun": {"district": "İskenderun", "city": "Hatay", "country": "Turkey"},
        "Istanbul": {"district": np.nan, "city": "İstanbul", "country": "Turkey"},
        "Beyoğlu": {"district": "Pera", "city": "İstanbul", "country": "Turkey"},
        "Yeni Cami": {"district": "Yeni Cami", "city": "İstanbul", "country": "Turkey"},
        "Beyrut": {"district": np.nan, "city": "Beirut", "country": "Lebanon"},
        "Sayda": {"district": np.nan, "city": "Sidon", "country": "Lebanon"},
        "Trablusşam": {"district": np.nan, "city": "Tripoli", "country": "Lebanon"},
        "Zahle": {"district": np.nan, "city": "Zahle", "country": "Lebanon"},
        "Hama": {"district": np.nan, "city": "Hama", "country": "Syria"},
        "Humus": {"district": np.nan, "city": "Homs", "country": "Syria"},
        "Şam": {"district": np.nan, "city": "Damascus", "country": "Syria"},
        "Aşar": {"district": "Ashar", "city": "Basra", "country": "Iraq"},
        "Kerkük": {"district": np.nan, "city": "Kirkuk", "country": "Iraq"},
        "Musul": {"district": np.nan, "city": "Mosul", "country": "Iraq"},
        "Beytüllahim": {"district": np.nan, "city": "Bethlehem", "country": "Palestine"},
        "Hayfa": {"district": np.nan, "city": "Haifa", "country": "Palestine"},
        "Kudüs": {"district": np.nan, "city": "Jerusalem", "country": "Palestine"},
        "Nablus": {"district": np.nan, "city": "Nablus", "country": "Palestine"},
        "Ramalla": {"district": np.nan, "city": "Ramallah", "country": "Palestine"},
        "Yafa": {"district": np.nan, "city": "Jaffa", "country": "Palestine"},
        "Iskenderiye": {"district": np.nan, "city": "Alexandria", "country": "Egypt"},
        "Mansure": {"district": np.nan, "city": "Mansura", "country": "Egypt"},
        "Minye": {"district": np.nan, "city": "Minya", "country": "Egypt"},
        "Port-Said": {"district": np.nan, "city": "Port Said", "country": "Egypt"},
        "Bingazi": {"district": np.nan, "city": "Benghazi", "country": "Libya"},
        "Trablusgarb": {"district": np.nan, "city": "Tripoli", "country": "Libya"},
        "Baf (Paphos)": {"district": np.nan, "city": "Paphos", "country": "Cyprus"},
        "Larnaka": {"district": np.nan, "city": "Larnaca", "country": "Cyprus"},
        "Lefkoşe": {"district": np.nan, "city": "Nicosia", "country": "Cyprus"},
        "Limasol": {"district": np.nan, "city": "Limassol", "country": "Cyprus"},
        "Magosa": {"district": np.nan, "city": "Famagusta", "country": "Cyprus"},
        "Troodos": {"district": np.nan, "city": "Troodos", "country": "Cyprus"},
        "Dedeağaç": {"district": np.nan, "city": "Alexandroupoli", "country": "Greece"},
        "Drama": {"district": np.nan, "city": "Drama", "country": "Greece"},
        "Gümülcine": {"district": np.nan, "city": "Komotini", "country": "Greece"},
        "Midilli": {"district": np.nan, "city": "Lesbos", "country": "Greece"},
        "Rodos": {"district": np.nan, "city": "Rhodes", "country": "Greece"},
        "Salonica ": {"district": np.nan, "city": "Thessaloniki", "country": "Greece"},
        "Seres": {"district": np.nan, "city": "Serres", "country": "Greece"},
        "Sufli (Sofulu)": {"district": np.nan, "city": "Soufli", "country": "Greece"},
        "Yanya": {"district": np.nan, "city": "Ioannina", "country": "Greece"},
        "İskeçe": {"district": np.nan, "city": "Xanthi", "country": "Greece"},
        "Kavala": {"district": np.nan, "city": "Kavala", "country": "Greece"},
        "Hamedan": {"district": np.nan, "city": "Hamadan", "country": "Iran"},
        "Kirmanşah": {"district": np.nan, "city": "Kermanshah", "country": "Iran"},
        "Tahran": {"district": np.nan, "city": "Tehran", "country": "Iran"},
        "Cidde": {"district": np.nan, "city": "Jeddah", "country": "Saudi Arabia"},
        "Hüdeyde": {"district": np.nan, "city": "Al Hudaydah", "country": "Yemen"},
        "Bükreş": {"district": np.nan, "city": "Bucharest", "country": "Romania"},
        "Kalas (Galati)": {"district": np.nan, "city": "Galati", "country": "Romania"},
        "Londra": {"district": np.nan, "city": "London", "country": "United Kingdom"},
        "Manchester": {"district": np.nan, "city": "Manchester", "country": "United Kingdom"},
        "Marsilya": {"district": np.nan, "city": "Marseille", "country": "France"},
        "Paris": {"district": np.nan, "city": "Paris", "country": "France"},
        "Manastır": {"district": np.nan, "city": "Bitola", "country": "North Macedonia"},
        "Plovdiv": {"district": np.nan, "city": "Plovdiv", "country": "Bulgaria"},
        "Rusçuk": {"district": np.nan, "city": "Ruse", "country": "Bulgaria"},
        "Sofya": {"district": np.nan, "city": "Sofia", "country": "Bulgaria"},
        "Varna": {"district": np.nan, "city": "Varna", "country": "Bulgaria"},
        "Üsküp": {"district": np.nan, "city": "Skopje", "country": "North Macedonia"},
        "İşkodra": {"district": np.nan, "city": "Shkodra", "country": "Albania"},
    }
    
    # manual match
    employee_df.loc[:, "Agency"] = employee_df["Agency"].str.strip().str.title()
    locations_df = employee_df["Agency"].map(agency_to_location)

    # fuzzy match
    match_to_location = dict()
    mask = locations_df.isna() & employee_df["Agency"].notna()
    for agency in employee_df[mask]["Agency"].unique():
        match = process.extractOne(agency, agency_to_location.keys(), scorer=lambda s1, s2, **kwargs: max(fuzz.token_sort_ratio(s1, s2), fuzz.partial_ratio(s1, s2)), score_cutoff=95)
        if match is not None:
            match_to_location[agency] = agency_to_location[match[0]]
    locations_df.loc[mask] = employee_df.loc[mask, "Agency"].map(match_to_location)

    # extract locations
    employee_df["District"] = locations_df.str.get("district")
    employee_df["City"] = locations_df.str.get("city")
    employee_df["Country"] = locations_df.str.get("country")
    
    # filter rare agencies - they may not exist
    for column in ["District", "City", "Country"]:
        location_counts = employee_df[column].value_counts(dropna=True)
        rare_locations = location_counts[location_counts < 5].index
        employee_df[column] = employee_df[column].apply(lambda location: np.nan if location in rare_locations else location)

    locations_df = agency_df["City"].str.strip().str.title().map(agency_to_location)
    agency_df["District"] = locations_df.str.get("district")
    agency_df["City"] = locations_df.str.get("city")
    agency_df["Country"] = locations_df.str.get("country")

    return employee_df, agency_df

def translate_functions(employee_df):
    fr_to_eng = {
        "Bureau": "Office",
        "Caissier": "Cashier",
        "Chef": "Chief",
        "Citres": "Securities",
        "Comptable": "Accountant",
        "Correspondance": "Correspondence",
        "Directeur": "Director",
        "Employee": "Employee",
        "Engagement": "Loans",
        "Opérations": "Operations",
        "Portefeuille": "Portfolio",
        "Surveillant": "Supervisor",
        "Titres": "Securities"
    }

    # manual match
    employee_df.loc[:, "Function"] = employee_df["Function"].str.strip().str.title()
    functions_df = employee_df["Function"].map(fr_to_eng)

    # fuzzy match
    match_to_function = dict()
    mask = functions_df.isna() & employee_df["Function"].notna()
    for agency in employee_df[mask]["Function"].unique():
        match = process.extractOne(agency, fr_to_eng.keys(), scorer=lambda s1, s2, **kwargs: max(fuzz.token_sort_ratio(s1, s2), fuzz.partial_ratio(s1, s2)), score_cutoff=90)
        if match is not None:
            match_to_function[agency] = fr_to_eng[match[0]]
    functions_df.loc[mask] = employee_df.loc[mask, "Function"].map(match_to_function)

    employee_df["Function"] = functions_df
    return employee_df

def translate_religions(employee_df):
    fr_to_eng = {
        "Armenienne": "Armenian",
        "Catholique": "Catholic",
        "Christian": "Christian",
        "Gregorian": "Gregorian",
        "Israelite": "Jewish",
        "Juif": "Jewish",
        "Musulman": "Muslim",
        "Orthodoxe": "Orthodox",
        "Other": "Other",
        "Protestant": "Protestant"
    }

    # manual match
    employee_df.loc[:, "Religion"] = employee_df["Religion"].str.strip().str.title()
    religions_df = employee_df["Religion"].map(fr_to_eng)

    # fuzzy match
    match_to_religion = dict()
    mask = religions_df.isna() & employee_df["Religion"].notna()
    for agency in employee_df[mask]["Religion"].unique():
        match = process.extractOne(agency, fr_to_eng.keys(), scorer=lambda s1, s2, **kwargs: max(fuzz.token_sort_ratio(s1, s2), fuzz.partial_ratio(s1, s2)), score_cutoff=90)
        if match is not None:
            match_to_religion[agency] = fr_to_eng[match[0]]
    religions_df.loc[mask] = employee_df.loc[mask, "Religion"].map(match_to_religion)

    employee_df["Religion"] = religions_df
    return employee_df

def impute_career_start_end_year(employee_df):
    new_records = []

    # group by id
    for id, record_group in employee_df.groupby("ID"):
        career_start_years = record_group["Career Start Year"].dropna()
        career_end_years = record_group["Career End Year"].dropna()

        min_record_year = record_group["Record Year"].min()
        max_record_year = record_group["Record Year"].max()

        # find career start year
        if len(career_start_years) == 0:
            career_start_year = min_record_year
        else:
            career_start_year = min(min_record_year, career_start_years.min())

        # find career end year
        if len(career_end_years) == 0:
            career_end_year = max_record_year
        else:
            career_end_year = max(max_record_year, career_end_years.max())

        tenure = career_end_year - career_start_year

        # skip employee if all year information is missing
        if pd.isna(career_start_year) and pd.isna(career_end_year):
            continue

        # impute missing year values in each record
        missing_start_idx = record_group[record_group["Career Start Year"] != career_start_year].index
        employee_df.loc[missing_start_idx, "Career Start Year"] = career_start_year

        missing_end_idx = record_group[record_group["Career End Year"] != career_end_year].index
        employee_df.loc[missing_end_idx, "Career End Year"] = career_end_year

        missing_idx = np.unique(list(missing_start_idx) + list(missing_end_idx))
        employee_df.loc[missing_idx, "Tenure"] = tenure

        # check if career start year is less than minimum of record years
        if career_start_year < min_record_year:
            new_record = {
                "ID": id,
                "Record Year": career_start_year,
                "Career Start Year": career_start_year,
                "Career End Year": career_end_year,
                "Tenure": tenure
            }

            new_records.append(new_record)
            
    if len(new_records) != 0:
        new_records_df = pd.DataFrame(new_records)
        employee_df = pd.concat([new_records_df, employee_df], ignore_index=True)

    return employee_df

def extract_period_start_end_year(employee_df):
    # add columns
    employee_df["Period Start Year"] = np.nan
    employee_df["Period End Year"] = np.nan

    # group by employee
    for id, record_group in employee_df.groupby("ID"):
        record_group = record_group.sort_values("Record Year")

        # keep career end year
        career_end_year = record_group["Career End Year"].iloc[0]

        # extract period start and end years        
        employee_df.loc[record_group.index, "Period Start Year"] = record_group["Record Year"]
        employee_df.loc[record_group.index, "Period End Year"] = record_group["Record Year"].shift(-1).fillna(career_end_year)

    return employee_df

def fill_na(employee_df, agency_df):
    employee_df.loc[:, ["Function", "Religion", "District", "City", "Country"]] = employee_df.loc[:, ["Function", "Religion", "District", "City", "Country"]].fillna("Unknown")
    agency_df.loc[:, ["District", "City", "Country"]] = agency_df.loc[:, ["District", "City", "Country"]].fillna("Unknown")
    
    return employee_df, agency_df

def generate_agency(employee_df, agency_df):
    agency_df["Agency"] = agency_df[["District", "City", "Country"]].apply(lambda record: ", ".join([value for value in record]), axis=1)
    employee_df["Agency"] = employee_df[["District", "City", "Country"]].apply(lambda record: ", ".join([value for value in record]), axis=1)

    return employee_df, agency_df

def extract_agency(employee_df, agency_df):
    agency_df = pd.merge(agency_df, employee_df.loc[:, ["Agency", "District", "City", "Country"]].drop_duplicates(), on=["Agency", "District", "City", "Country"], how="outer")

    agency_years_df = employee_df.groupby("Agency").agg(opening_year_filler=("Career Start Year", "min"), closing_year_filler=("Career End Year", "max")).reset_index()
    agency_years_df = agency_years_df.rename(columns={"opening_year_filler": "Opening Year Filler", "closing_year_filler": "Closing Year Filler"})
    
    agency_df = agency_df.merge(agency_years_df, on="Agency", how="left")

    mask = agency_df["Opening Year"].isna() & agency_df["Opening Year Filler"].notna()
    agency_df.loc[mask, "Opening Year"] = agency_df.loc[mask, "Opening Year"].fillna(agency_df.loc[mask, "Opening Year Filler"].astype(str)).astype(float)
    mask = agency_df["Closing Year"].isna() & agency_df["Closing Year Filler"].notna()
    agency_df.loc[mask, "Closing Year"] = agency_df.loc[mask, "Closing Year"].fillna(agency_df.loc[mask, "Closing Year Filler"].astype(str)).astype(float)
    agency_df.drop(columns=["Opening Year Filler", "Closing Year Filler"], inplace=True)
    
    return agency_df

def locate_agencies(agency_df):
    geolocator = Nominatim(user_agent="address_geolocator", timeout=5)

    latitudes = []
    longitudes = []

    for index, record in agency_df.iterrows():
        # remove Unknowns
        address = ", ".join(str(record[column]) for column in ["District", "City", "Country"] if record[column] != "Unknown")

        if len(address) != 0:
            # geocode the address
            location = geolocator.geocode(address)
            
            if location:
                latitudes.append(location.latitude)
                longitudes.append(location.longitude)

            else:
                latitudes.append(np.nan)
                longitudes.append(np.nan)
                print(f"Geolocator could not geocode the address {address}")
        else:
            latitudes.append(np.nan)
            longitudes.append(np.nan)

        # avoid too many requests
        if (index+1) % 10 == 0:
            time.sleep(1)

    agency_df["Latitude"] = latitudes
    agency_df["Longitude"] = longitudes

    return agency_df

def sort(employee_df, agency_df):
    employee_df.sort_values(by=["ID", "Record Year"], ignore_index=True, inplace=True)
    agency_df.sort_values(by=["Opening Year", "Agency"], ignore_index=True, inplace=True)

    return employee_df, agency_df

def preprocess(employee_df, agency_df):
    employee_df, agency_df = drop_columns(employee_df, agency_df)
    employee_df, agency_df = rename_columns(employee_df, agency_df)
    agency_df = change_inconsistent_date(agency_df)
    agency_df = change_types(agency_df)
    employee_df, agency_df = deduct_district_city_and_country(employee_df, agency_df)
    employee_df = translate_functions(employee_df)
    employee_df = translate_religions(employee_df)
    employee_df = impute_career_start_end_year(employee_df)
    employee_df = extract_period_start_end_year(employee_df)
    employee_df, agency_df = fill_na(employee_df, agency_df)
    employee_df, agency_df = generate_agency(employee_df, agency_df)
    agency_df = extract_agency(employee_df, agency_df)
    agency_df = locate_agencies(agency_df)
    employee_df, agency_df = sort(employee_df, agency_df)

    return employee_df, agency_df

# load datasets
employee_df = pd.read_excel(join("datasets", "employees_raw.xlsx"))
agency_df = pd.read_excel(join("datasets", "agencies_raw.xlsx"))

# preprocess
employee_df, agency_df = preprocess(employee_df, agency_df)

# save datasets
employee_df.to_excel(join("datasets", "employees_preprocessed.xlsx"), index=False)
agency_df.to_excel(join("datasets", "agencies_preprocessed.xlsx"), index=False)
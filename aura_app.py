from kivy.app import App
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput

import datetime
import random
import json
import os


Window.clearcolor = (0.02, 0.025, 0.05, 1)

HAFIZA_DOSYASI = "aura_hafiza.json"


def hafizayi_yukle():

    if os.path.exists(HAFIZA_DOSYASI):

        try:
            with open(
                HAFIZA_DOSYASI,
                "r",
                encoding="utf-8"
            ) as dosya:
                return json.load(dosya)

        except Exception:
            pass

    return {
        "isim": "",
        "notlar": []
    }


def hafizayi_kaydet():

    try:
        with open(
            HAFIZA_DOSYASI,
            "w",
            encoding="utf-8"
        ) as dosya:

            json.dump(
                hafiza,
                dosya,
                ensure_ascii=False,
                indent=4
            )

    except Exception:
        pass


hafiza = hafizayi_yukle()


class AuraApp(App):

    def build(self):

        self.title = "AURA AI"

        ana = BoxLayout(
            orientation="vertical",
            padding=dp(12),
            spacing=dp(8)
        )

        baslik = Label(
            text="A U R A",
            font_size=dp(30),
            bold=True,
            color=(0.2, 0.75, 1, 1),
            size_hint_y=None,
            height=dp(50)
        )

        ana.add_widget(baslik)

        durum = Label(
            text="● AURA AI • Hazır",
            font_size=dp(13),
            color=(0.2, 1, 0.5, 1),
            size_hint_y=None,
            height=dp(25)
        )

        ana.add_widget(durum)

        # SOHBET ALANI

        scroll = ScrollView(
            do_scroll_x=False,
            do_scroll_y=True
        )

        self.sohbet = Label(
            text="",
            font_size=dp(17),
            color=(0.95, 0.97, 1, 1),
            halign="left",
            valign="top",
            size_hint_y=None,
            size_hint_x=1,
            padding=(dp(10), dp(10))
        )

        scroll.add_widget(self.sohbet)

        self.scroll = scroll

        ana.add_widget(scroll)

        # MESAJ ALANI

        alt = BoxLayout(
            spacing=dp(8),
            size_hint_y=None,
            height=dp(58)
        )

        self.girdi = TextInput(
            hint_text="AURA'ya mesaj yaz...",
            multiline=False,
            font_size=dp(16),
            foreground_color=(1, 1, 1, 1),
            background_color=(0.08, 0.1, 0.17, 1),
            padding=[dp(12), dp(12)]
        )

        self.girdi.bind(
            on_text_validate=self.gonder
        )

        gonder = Button(
            text="GÖNDER",
            font_size=dp(13),
            bold=True,
            size_hint_x=None,
            width=dp(100),
            background_normal="",
            background_color=(0.05, 0.45, 0.8, 1)
        )

        gonder.bind(
            on_press=self.gonder
        )

        alt.add_widget(self.girdi)
        alt.add_widget(gonder)

        ana.add_widget(alt)

        # HIZLI BUTONLAR

        hizli = BoxLayout(
            spacing=dp(5),
            size_hint_y=None,
            height=dp(45)
        )

        for isim, komut in [
            ("SAAT", "saat"),
            ("ŞAKA", "şaka"),
            ("YARDIM", "yardım")
        ]:

            buton = Button(
                text=isim,
                font_size=dp(12),
                background_normal="",
                background_color=(0.07, 0.09, 0.15, 1)
            )

            buton.bind(
                on_press=lambda x, c=komut:
                self.hizli_komut(c)
            )

            hizli.add_widget(buton)

        ana.add_widget(hizli)

        # İLK MESAJ

        isim = hafiza.get("isim", "")

        if isim:

            self.mesaj_ekle(
                "AURA",
                "Tekrar hoş geldin " + isim + "."
            )

        else:

            self.mesaj_ekle(
                "AURA",
                "Merhaba! Ben AURA. Nasıl yardımcı olabilirim?"
            )

        # GENİŞLİK DEĞİŞİNCE YAZIYI EKRANA UYDUR

        self.sohbet.bind(
            width=self.sohbet_genisligi_degisti
        )

        return ana


    # YAZI GENİŞLİĞİ

    def sohbet_genisligi_degisti(
        self,
        instance,
        width
    ):

        instance.text_size = (
            width - dp(20),
            None
        )


    # MESAJ EKLE

    def mesaj_ekle(
        self,
        kim,
        mesaj
    ):

        eski = self.sohbet.text

        if eski:
            eski += "\n\n"

        yeni_mesaj = (
            kim
            + ":\n"
            + mesaj
        )

        self.sohbet.text = (
            eski
            + yeni_mesaj
        )

        # Yazının yüksekliğini güncelle

        self.sohbet.texture_update()

        self.sohbet.height = (
            self.sohbet.texture_size[1]
            + dp(20)
        )

        # En alta kaydır

        self.scroll.scroll_y = 0


    # MESAJ GÖNDER

    def gonder(self, instance):

        mesaj = self.girdi.text.strip()

        if mesaj == "":
            return

        self.mesaj_ekle(
            "SEN",
            mesaj
        )

        self.girdi.text = ""

        cevap = self.cevap_ver(mesaj)

        self.mesaj_ekle(
            "AURA",
            cevap
        )


    # HIZLI KOMUT

    def hizli_komut(self, komut):

        self.mesaj_ekle(
            "SEN",
            komut
        )

        cevap = self.cevap_ver(komut)

        self.mesaj_ekle(
            "AURA",
            cevap
        )


    # AURA CEVAPLARI

    def cevap_ver(self, mesaj):

        m = mesaj.lower().strip()

        if m in ["merhaba", "selam", "sa", "hey"]:

            isim = hafiza.get("isim", "")

            if isim:
                return (
                    "Merhaba "
                    + isim
                    + ". Nasıl yardımcı olabilirim?"
                )

            return (
                "Merhaba! Ben AURA. "
                "Nasıl yardımcı olabilirim?"
            )


        if "nasılsın" in m or "nasilsin" in m:

            return "Gayet iyi çalışıyorum."


        if m == "saat" or "saat kaç" in m:

            return (
                "Şu an saat "
                + datetime.datetime.now().strftime(
                    "%H:%M:%S"
                )
            )


        if m == "tarih":

            return (
                "Bugünün tarihi: "
                + datetime.datetime.now().strftime(
                    "%d.%m.%Y"
                )
            )


        if m == "şaka" or "şaka yap" in m:

            return random.choice([
                "Bilgisayar neden doktora gitmiş? Virüs kapmış.",
                "Matematik kitabı neden ağlamış? Çok problemi varmış.",
                "Bilgisayar neden denize girmiş? İnternete bağlanmak için.",
                "Klavye neden kavga etmiş? Tuşuna basılmış."
            ])


        if "motivasyon" in m:

            return random.choice([
                "Başlamak için mükemmel olmayı bekleme.",
                "Her uzman bir zamanlar acemiydi.",
                "Pes etmediğin sürece yol devam ediyor.",
                "Bugün öğrendiğin şey yarın işine yarayabilir."
            ])


        if m.startswith("ismim "):

            isim = m[6:].strip()

            if isim == "":
                return "İsmini yazmalısın."

            hafiza["isim"] = isim

            hafizayi_kaydet()

            return (
                "Tamam. İsmini "
                + isim
                + " olarak kaydettim."
            )


        if (
            "ismim ne" in m
            or "adım ne" in m
        ):

            isim = hafiza.get("isim", "")

            if isim:
                return "İsmin " + isim + "."

            return "Henüz ismini bana söylemedin."


        if m.startswith("hesap "):

            ifade = m[6:].strip()

            izinli = "0123456789+-*/().% "

            if ifade == "":
                return "Bir işlem yazmalısın."

            for karakter in ifade:

                if karakter not in izinli:
                    return "Bu işlemi yapamıyorum."

            try:

                sonuc = eval(
                    ifade,
                    {"__builtins__": {}},
                    {}
                )

                return "Sonuç: " + str(sonuc)

            except Exception:

                return "Hesaplama hatası oluştu."


        if m.startswith("not ekle "):

            notum = m[9:].strip()

            if notum == "":
                return "Kaydetmem için bir not yaz."

            hafiza["notlar"].append(notum)

            hafizayi_kaydet()

            return "Notunu hafızama kaydettim."


        if m in [
            "notlar",
            "notlarım",
            "notlarımı göster"
        ]:

            notlar = hafiza.get(
                "notlar",
                []
            )

            if len(notlar) == 0:
                return "Hafızamda kayıtlı not yok."

            sonuc = "Kayıtlı notların:\n\n"

            for i, notum in enumerate(
                notlar,
                1
            ):

                sonuc += (
                    str(i)
                    + ". "
                    + notum
                    + "\n"
                )

            return sonuc.strip()


        if m in [
            "notları sil",
            "hafızayı temizle"
        ]:

            hafiza["notlar"] = []

            hafizayi_kaydet()

            return "Bütün notları sildim."


        if "sen kimsin" in m:

            return (
                "Ben AURA. "
                "Telefonunda çalışan kişisel "
                "yapay zeka asistanınım."
            )


        if "ne yapabilirsin" in m:

            return (
                "Saat, tarih, hesaplama, "
                "not kaydetme, isim hatırlama, "
                "şaka ve motivasyon özelliklerim var."
            )


        if m == "yardım":

            return (
                "Kullanabileceğin komutlar:\n\n"
                "saat\n"
                "tarih\n"
                "şaka\n"
                "motivasyon\n"
                "hesap 25*4\n"
                "ismim Bedirhan\n"
                "ismim ne\n"
                "not ekle ders çalış\n"
                "notlarım\n"
                "notları sil"
            )


        if (
            "teşekkür" in m
            or "sağol" in m
            or "eyvallah" in m
        ):

            return "Rica ederim."


        return (
            "Bunu henüz bilmiyorum. "
            "Bana 'yardım' yazarak "
            "kullanabileceğin komutları görebilirsin."
        )


if __name__ == "__main__":

    AuraApp().run()
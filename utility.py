from kivy.app import App
from kivy.network.urlrequest import UrlRequest
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput


class Screen(App):
    def __init__(self):
        super().__init__()
        self.etichetta = None
        self.bottone = None
        self.input_testo = None
        self.window = None

    def build(self):
        self.window = GridLayout()
        self.window.cols = 1
        self.window.size_hint = (0.8, 0.9)  # margini
        self.window.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        Window.size = (360, 640)

        self.window.add_widget(Image(source="logo.png"))  # aggiungi l'immagine

        self.input_testo = TextInput(
            size_hint=(1, 0.2),
            font_size='20sp',
            padding_y='12sp',
            halign='center'
        )
        self.window.add_widget(self.input_testo)

        self.bottone = Button(
            text="VIA!",
            size_hint=(1, 0.2),
            bold=True,
            background_color='aqua'
        )
        self.window.add_widget(self.bottone)
        self.bottone.bind(on_press=self.find_time)

        self.etichetta = Label(
            text="cerca una città!",
            font_size='20sp',
            color='grey'
        )
        self.window.add_widget(self.etichetta)
        return self.window

    def find_time(self, instance):
        print("Bottone premuto")
        city = self.input_testo.text
        if not city:
            self.etichetta.text = "Per favore, inserisci una città"
            return

        def edit_label(request, result):
            print("Risposta ricevuta dall'API")
            print(result)
            try:
                time = result['main']['temp']
                self.etichetta.text = f"oggi a {city} ci sono {time}° gradi"
            except KeyError:
                self.etichetta.text = "Errore: città non trovata o problema con l'API"

        def error(req, result):
            self.etichetta.text = "Errore di connessione o problema con l'API"

        link = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=df026be2a1e64a81a4a433f102948def&units=metric"
        print(f"URL generato: {link}")
        UrlRequest(link, edit_label, on_error=error, on_failure=error)




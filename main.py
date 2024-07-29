import requests
from PIL import Image as PILImage, ImageTk
from tkinter import *
import tkinter.font as tkFont

url = "https://api.openweathermap.org/data/2.5/weather"
api_key = "your_api_key"
icon_Url = "http://openweathermap.org/img/wn/{}@2x.png"

def weather(city):
    params = {"q": city, "appid": api_key}
    response = requests.get(url, params=params).json()
    if response.get("cod") != 200:
        return None
    city = response["name"].capitalize()
    country = response["sys"]["country"]
    temp = int(response["main"]["temp"] - 273.15)
    icon = response["weather"][0]["icon"]
    condition = response["weather"][0]["description"]
    return city, country, temp, icon, condition

def main():
    city = city_entry.get()
    get_weather = weather(city)
    if get_weather:
        location["text"] = "{}, {}".format(get_weather[0], get_weather[1])
        temperature["text"] = "{}°C".format(get_weather[2])
        condition_label["text"] = get_weather[4]

        wrap_length = window.winfo_width() - 40 
        location.config(wraplength=wrap_length)

        font_size = min(40, wrap_length // len(location["text"]) * 2)
        location_font = tkFont.Font(family="Arial", size=font_size)
        location.config(font=location_font)

        icon = ImageTk.PhotoImage(PILImage.open(requests.get(icon_Url.format(get_weather[3]), stream=True).raw))
        icon_label.configure(image=icon)
        icon_label.image = icon
    else:
        location["text"] = "City not found"
        temperature["text"] = ""
        condition_label["text"] = ""
        icon_label.configure(image='')

def enter(event):
    main()

window = Tk()
window.geometry("300x450")
window.title("Weather App")

city_entry = Entry(window, justify="center")
city_entry.pack(fill=BOTH, ipady=10, padx=20, pady=5)
city_entry.focus()
city_entry.bind("<Return>",enter)

search_button = Button(window, text="Search", font=("Arial", 16), command=main)
search_button.pack(fill=BOTH, ipady=10, padx=18)


icon_label = Label(window)
icon_label.pack()

location = Label(window, font=("Arial", 40))
location.pack()

temperature = Label(window, font=("Arial", 50, "bold"))
temperature.pack()

condition_label = Label(window, font=("Arial", 20))
condition_label.pack()

window.mainloop()
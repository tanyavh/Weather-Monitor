
import requests
import tkinter as tk


# ===== BASIC CONFIGURATION =====
API_KEY = 'api_key' #input your own api key
CITY = 'city'  #input the city name you wish to monitor the weather for 
UNITS = 'metric'

# ===== ANOMALY CONDITIONS =====
ANOMALY_PARAMS = {
    'temp_min': 0,
    'temp_max': 35,
    'wind_speed_max': 15,
    'humidity_max': 90,
}
STORM_CONDITIONS = {'wind_speed_min': 18, 'humidity_min': 90, 'storm_keywords': ['thunderstorm', 'heavy rain'], 'weather_id_storm': 331}
TORNADO_CONDITIONS = dict(wind_speed_min=25, weather_id_tornado=781)

# ===== POPUP BOX =====
def show_popup(title, message, alert=False):
    root = tk.Tk()
    root.title(title)
    root.geometry("450x250")
    root.configure(bg="#476a4d")
    root.resizable(False, False)
    root.attributes("-topmost", True)

    border_color = "#9caf88"
    border_thickness = 4
    bordered_frame = tk.Frame(
        root,
        bg="#476a4d",
        highlightbackground=border_color,
        highlightthickness=border_thickness,
        bd=0
    )
    bordered_frame.pack(expand=True, fill="both", padx=10, pady=10)

    text_color = "white"
    button_color = "#9caf88"
    button_hover = "#2a4f2d"
    font_main = ("Lucida Console", 10)
    font_icon = ("Comic Sans MS", 20)

    icon_text = "⚠️ 🕙 ⚠️ 🕙 ⚠️" if alert else "🌿 🍃 🌸 🍃 🌿"
    icon_label = tk.Label(bordered_frame, text=icon_text, font=font_icon, fg=text_color, bg="#476a4d")
    icon_label.pack(pady=(10, 5))

    message_label = tk.Label(bordered_frame, text=message, font=font_main, wraplength=360, justify="center", bg="#476a4d", fg=text_color)
    message_label.pack(pady=(0, 20))

    def on_enter(e): close_button.configure(bg=button_hover)
    def on_leave(e): close_button.configure(bg=button_color)
    close_button = tk.Button(bordered_frame, text="OK!", command=root.destroy, font=("Times New Roman", 10), bg=button_color, fg="#f7e7ce", activebackground=button_hover, relief="flat", padx=12, pady=5)
    close_button.pack()
    close_button.bind("<Enter>", on_enter)
    close_button.bind("<Leave>", on_leave)

    root.eval('tk::PlaceWindow . center')

    root.mainloop()

# ===== WEATHER FUNCTIONS =====
def get_weather_by_city():
    url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units={UNITS}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def check_anomalies(weather_data, thresholds, storm_conditions, tornado_conditions):
    anomalies: list[str] = []
    main = weather_data['main']
    wind = weather_data.get('wind', {})
    weather = weather_data['weather'][0]

    temp = main['temp']
    humidity = main['humidity']
    wind_speed = wind.get('speed', 0)
    weather_id = weather['id']
    weather_desc = weather['description'].lower()

    if temp < thresholds['temp_min']:
        anomalies.append(f"Low temperature: {temp}°C")
    if temp > thresholds['temp_max']:
        anomalies.append(f"High temperature: {temp}°C")
    if wind_speed > thresholds['wind_speed_max']:
        anomalies.append(f"High wind speed: {wind_speed} m/s")
    if humidity > thresholds['humidity_max']:
        anomalies.append(f"High humidity: {humidity}%")

    storm_flags = []
    if wind_speed >= storm_conditions['wind_speed_min']:
        storm_flags.append("strong wind")
    if humidity >= storm_conditions['humidity_min']:
        storm_flags.append("high humidity")
    if any(keyword in weather_desc for keyword in storm_conditions['storm_keywords']):
        storm_flags.append(f"weather: {weather_desc}")

    if len(storm_flags) >= 2:
        anomalies.append("🌦️ Storm-like conditions: " + ", ".join(storm_flags))

    if wind_speed >= tornado_conditions['wind_speed_min'] or weather_id == tornado_conditions['weather_id_tornado']:
        reason = "extreme wind" if wind_speed >= tornado_conditions['wind_speed_min'] else f"weather code {weather_id} ({weather_desc})"
        anomalies.append(f"🌪️ Potential tornado conditions detected: {reason}")

    return anomalies

# ===== MAIN =====
def monitor_weather():
    try:
        weather = get_weather_by_city()
        print(f"📍 Weather check for {CITY}")
        print("~*" * 40)
        anomalies = check_anomalies(weather, ANOMALY_PARAMS, STORM_CONDITIONS, TORNADO_CONDITIONS)
        if anomalies:
            result = "Anomalies Detected:\n" + "\n".join(f"• {a}" for a in anomalies)
            show_popup("Wait a minute, what is that?", result, alert=True)
        else:
            result = f"\n📍 Weather check for {CITY}\n" + "\nAll weather parameters are within normal range."
            show_popup("Here comes nothing...", result)

if __name__ == "__main__":
    monitor_weather()
    

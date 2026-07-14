import aiohttp


async def get_coordinates(city):
    url = (
        "https://geocoding-api.open-meteo.com/v1/search"
        f"?name={city}&count=1&language=ru&format=json"
    )

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()

    if "results" not in data:
        return None

    place = data["results"][0]

    return (
        place["name"],
        place["latitude"],
        place["longitude"]
    )


async def get_weather(city):

    location = await get_coordinates(city)

    if not location:
        return "❌ Не нашел такой город"

    name, lat, lon = location

    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        "&hourly=temperature_2m,precipitation_probability,"
        "weathercode,windspeed_10m"
        "&timezone=auto"
    )

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()

    temp = data["hourly"]["temperature_2m"][0]
    rain = data["hourly"]["precipitation_probability"][0]
    wind = data["hourly"]["windspeed_10m"][0]

    if rain < 30:
        analysis = "🟢 Скорее всего сухо"
    elif rain < 60:
        analysis = "🟡 Возможен дождь"
    else:
        analysis = "🔴 Высокий шанс дождя"

    return (
        f"📍 {name}\n\n"
        f"🌡 Температура: {temp}°C\n"
        f"🌧 Вероятность дождя: {rain}%\n"
        f"💨 Ветер: {wind} км/ч\n\n"
        f"🧠 Анализ:\n{analysis}"
  )

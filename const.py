from typing import Final

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntityDescription,
    SensorStateClass,
)

from homeassistant.const import (
    UnitOfSpeed, 
    UnitOfTemperature, 
    UnitOfPrecipitationDepth, 
    UnitOfPressure,
    PERCENTAGE,
)

ATTRIBUTION: Final = "Data provided by Idokep.hu"
SHORT_ATTRIBUTION: Final = "Idokep.hu"
MODEL_NAME: Final = "Weather Sensor"
COLLECTOR: Final = "collector"
UPDATE_LISTENER: Final = "update_listener"

CONF_WEATHER_NAME: Final = "weather_name"
CONF_FORECASTS_BASENAME: Final = "forecasts_basename"
CONF_FORECASTS_CREATE: Final = "forecasts_create"
CONF_FORECASTS_DAYS: Final = "forecasts_days"
CONF_FORECASTS_MONITORED: Final = "forecasts_monitored"
CONF_OBSERVATIONS_BASENAME: Final = "observations_basename"
CONF_OBSERVATIONS_CREATE: Final = "observations_create"
CONF_OBSERVATIONS_MONITORED: Final = "observations_monitored"
CONF_WARNINGS_CREATE: Final = "warnings_create"
CONF_WARNINGS_BASENAME: Final = "warnings_basename"
CONF_CITY: Final = "city"
CONF_FORCAST_DAYS: Final = "forcast days"
COORDINATOR: Final = "coordinator"
DOMAIN: Final = "idokep"

MAP_CONDITION: Final = {
    "derült": "sunny",
    "gyengén felhős": "partlycloudy",
    "közepesen felhős": "partlycloudy",
    "erősen felhős": "weather-cloudy",
    "borult": "cloudy",
    "szitálás": "rainy",
    "gyenge eső": "rainy",
    "eső": "rainy",
    "zápor": "rainy",
    "zivatar": "lightning-rainy",
    "eső viharos széllel": "lightning-rainy",
    "hózápor": "snowy",
    "hószállingózás": "snowy",
    "havas eső": "snowy",
    "pára": "fog",
#s
    "clear": "clear-night",
    "cloudy": "cloudy",
    "cyclone": "exceptional",
    "dust": "fog",
    "dusty": "fog",
    "fog": "fog",
    "frost": "snowy",
    "haze": "fog",
    "hazy": "fog",
    "heavy_shower": "rainy",
    "heavy_showers": "rainy",
    "light_rain": "rainy",
    "light_shower": "rainy",
    "light_showers": "rainy",
    "mostly_sunny": "sunny",
    "partly_cloudy": "partlycloudy",
    "rain": "rainy",
    "shower": "rainy",
    "showers": "rainy",
    "snow": "snowy",
    "storm": "lightning-rainy",
    "storms": "lightning-rainy",
    "sunny": "sunny",
    "tropical_cyclone": "exceptional",
    "wind": "windy",
    "windy": "windy",
    None: None,
}

MAP_MDI_ICON = {
    "derült": "mdi:weather-sunny",
    "gyengén felhős": "mdi:weather-partly-cloudy",
    "közepesen felhős": "mdi:weather-partly-cloudy",
    "erősen felhős": "mdi:weather-cloudy",
    "borult": "mdi:weather-cloudy",
    "szitálás": "mdi:weather-pouring",
    "gyenge eső": "mdi:weather-pouring",
    "eső": "mdi:weather-rainy",
    "zápor": "mdi:weather-partly-rainy",
    "zivatar": "mdi:weather-lightning-rainy",
    "eső viharos széllel": "mdi:weather-lightning-rainy",
    "pára": "mdi:weather-fog",
    "hózápor": "mdi:weather-snowy-heavy",
    "hószállingózás": "mdi:weather-snowy",
    "havas eső": "mdi:weather-snowy-rainy",
#s
    "tiszta": "mdi:weather-night",
    "felhős": "mdi:weather-cloudy",
    "cyclone": "mdi:weather-hurricane",
    "dust": "mdi:weather-hazy",
    "dusty": "mdi:weather-hazy",
    "köd": "mdi:weather-fog",
    "fagy": "mdi:snowflake-melt",
    "haze": "mdi:weather-hazy",
    "hazy": "mdi:weather-hazy",
    "heavy_shower": "mdi:weather-pouring",
    "heavy_showers": "mdi:weather-pouring",
    "light_shower": "mdi:weather-light-showers",
    "light_showers": "mdi:weather-light-showers",
    "showers": "mdi:weather-rainy",
    "hó": "mdi:weather-snowy",
    "storm": "mdi:weather-lightning-rainy",
    "storms": "mdi:weather-lightning-rainy",
    "tropical_cyclone": "mdi:weather-hurricane",
    "szél": "mdi:weather-windy",
    "szeles": "mdi:weather-windy",
    None: None,
}
MAP_UV = {
    "extreme": "Extreme",
    "veryhigh": "Very High",
    "high": "High",
    "moderate": "Moderate",
    "low": "Low",
    None: None,
}

URL_NORMAL = "idojaras/"
URL_DETAILED = "elorejelzes/"
URL_BASE = "https://www.idokep.hu/"
CURRENT_WEATHER_SHORT_DESCRIPTION = "ik current-weather"
CURRENT_WEATHER_DESCRIPTION = "current-weather-short-desc"
CURRENT_WEATHER_TEMP = "ik current-temperature"
CURRENT_WEATHER_TEXT = "shortCurrentWeatherText" 
SUNRISE = "napkelte"
SUNSET = "napnyugta"
FORCAST_EXTENDED_DESCRIPTION = "hosszutavu-elorejelzes"
HOURLY_FORCAST = "ik new-hourly-forecast-card"
HOURLY_FORCAST_HOUR = "ik new-hourly-forecast-hour"
HOURLY_FORCAST_TEMP = "ik tempValue"
HOURLY_FORCAST_RAIN_CHANCE = "ik hourly-rain-chance"
HOURLY_FORCAST_RAIN_LEVEL = "ik hourly-rainlevel"
HOURLY_FORCAST_WIND = "ik hourly-wind"
HOURLY_FORCAST_ICON_CONTAINER = "ik forecast-icon-container"
HOURLY_FORCAST_ICON = "ik forecast-icon"
HOURLY_FORCAST_ALERT = "ik genericHourlyAlert"
DAILY_FORCAST = "ik dailyForecastCol"
DAILY_FORCAST_DAY = "ik dfIconAlert"
DAILY_FORCAST_DESCRIPTION = "ik dfIconAlert"
DAILY_FORCAST_DESCRIPTION_LINE = "ik fc-line"
DAILY_FORCAST_TEMP_MIN = "ik min"
DAILY_FORCAST_TEMP_MAX = "ik max"
DAILY_FORCAST_TEMP_RECORD_MIN = "ik daily-record-temp"
DAILY_FORCAST_TEMP_RECORD_MAX = "ik daily-record-temp"
DAILY_FORCAST_TEMP_RECORD_MIN_LOCATION = "ik daily-record-location"
DAILY_FORCAST_TEMP_RECORD_MAX_LOCATION = "ik daily-record-location"
DAILY_FORCAST_RAIN = "ik rainlevel-container"
DAILY_FORCAST_RAIN_LEVEL = "ik mm"
DAILY_FORCAST_ICON = "ik forecast-icon"
DAILY_FORCAST_ALERT_ICON = "ik forecast-alert-icon"

ATTR_API_TEMP: Final = "temp"
ATTR_API_TEMP_FEELS_LIKE: Final = "temp_feels_like"
ATTR_API_MAX_TEMP: Final = "max_temp"
ATTR_API_MIN_TEMP: Final = "min_temp"
ATTR_API_RAIN_SINCE_9AM: Final = "rain_since_9am"
ATTR_API_HUMIDITY: Final = "humidity"
ATTR_API_WIND_SPEED_KILOMETRE: Final = "wind_speed_kilometre"
ATTR_API_WIND_SPEED_KNOT: Final = "wind_speed_knot"
ATTR_API_WIND_DIRECTION: Final = "wind_direction"
ATTR_API_GUST_SPEED_KILOMETRE: Final = "gust_speed_kilometre"
ATTR_API_GUST_SPEED_KNOT: Final = "gust_speed_knot"

ATTR_API_TEMP_MAX: Final = "temp_max"
ATTR_API_TEMP_MIN: Final = "temp_min"
ATTR_API_EXTENDED_TEXT: Final = "extended_text"
ATTR_API_ICON_DESCRIPTOR: Final = "icon_descriptor"
ATTR_API_MDI_ICON: Final = "mdi_icon"
ATTR_API_SHORT_TEXT: Final = "short_text"
ATTR_API_UV_CATEGORY: Final = "uv_category"
ATTR_API_UV_MAX_INDEX: Final = "uv_max_index"
ATTR_API_UV_START_TIME: Final = "uv_start_time"
ATTR_API_UV_END_TIME: Final = "uv_end_time"
ATTR_API_UV_FORECAST: Final = "uv_forecast"
ATTR_API_RAIN_AMOUNT_MIN: Final = "rain_amount_min"
ATTR_API_RAIN_AMOUNT_MAX: Final = "rain_amount_max"
ATTR_API_RAIN_AMOUNT_RANGE: Final = "rain_amount_range"
ATTR_API_RAIN_CHANCE: Final = "rain_chance"
ATTR_API_FIRE_DANGER: Final = "fire_danger"
ATTR_API_NON_NOW_LABEL: Final = "now_now_label"
ATTR_API_NON_TEMP_NOW: Final = "now_temp_now"
ATTR_API_NOW_LATER_LABEL: Final = "now_later_label"
ATTR_API_NOW_TEMP_LATER: Final = "now_temp_later"
ATTR_API_ASTRONOMICAL_SUNRISE_TIME: Final = "astronomical_sunrise_time"
ATTR_API_ASTRONOMICAL_SUNSET_TIME: Final = "astronomical_sunset_time"
ATTR_API_WARNINGS: Final = "warnings"

OBSERVATION_SENSOR_TYPES: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(
        key=ATTR_API_TEMP,
        name="Current Temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key=ATTR_API_MAX_TEMP,
        name="Todays Observed Maximum Temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key=ATTR_API_MIN_TEMP,
        name="Todays Observed Minimum Temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key=ATTR_API_SHORT_TEXT,
        name="Current weather",
    ),
    SensorEntityDescription(
        key=ATTR_API_EXTENDED_TEXT,
        name="Extended Forecast",
    ),
    SensorEntityDescription(
        key=ATTR_API_ASTRONOMICAL_SUNRISE_TIME,
        name="Sunrise Time",
        device_class=SensorDeviceClass.TIMESTAMP,
    ),
    SensorEntityDescription(
        key=ATTR_API_ASTRONOMICAL_SUNSET_TIME,
        name="Sunset Time",
        device_class=SensorDeviceClass.TIMESTAMP,
    ),
    SensorEntityDescription(
        key=ATTR_API_RAIN_AMOUNT_MIN,
        name="Precipitation amount",
        native_unit_of_measurement=UnitOfPrecipitationDepth.MILLIMETERS,
        device_class=SensorDeviceClass.PRECIPITATION,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SensorEntityDescription(
        key=ATTR_API_RAIN_CHANCE,
        name="Precipitation chance",
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.PRECIPITATION,
        state_class=SensorStateClass.TOTAL,
    ),
#   SensorEntityDescription(
#       key=ATTR_API_HUMIDITY,
#       name="Humidity",
#       native_unit_of_measurement=PERCENTAGE,
#       device_class=SensorDeviceClass.HUMIDITY,
#       state_class=SensorStateClass.MEASUREMENT,
#   ),
#   SensorEntityDescription(
#       key=ATTR_API_WIND_SPEED_KILOMETRE,
#       name="Wind Speed km/h",
#       native_unit_of_measurement=UnitOfSpeed.KILOMETERS_PER_HOUR,
#       device_class=SensorDeviceClass.WIND_SPEED,
#       state_class=SensorStateClass.MEASUREMENT,
#   ),
#   SensorEntityDescription(
#       key=ATTR_API_WIND_SPEED_KNOT,
#       name="Wind Speed kn",
#       native_unit_of_measurement=SPEED_KNOTS,
#       device_class=SensorDeviceClass.WIND_SPEED,
#       state_class=SensorStateClass.MEASUREMENT,
#   ),
#   SensorEntityDescription(
#       key=ATTR_API_WIND_DIRECTION,
#       name="Wind Direction",
#       native_unit_of_measurement=DEGREE,
#       state_class=SensorStateClass.MEASUREMENT,
#   ),
#   SensorEntityDescription(
#       key=ATTR_API_GUST_SPEED_KILOMETRE,
#       name="Gust Speed km/h",
#       native_unit_of_measurement=UnitOfSpeed.KILOMETERS_PER_HOUR,
#       device_class=SensorDeviceClass.WIND_SPEED,
#       state_class=SensorStateClass.MEASUREMENT,
#   ),
#   SensorEntityDescription(
#       key=ATTR_API_GUST_SPEED_KNOT,
#       name="Gust Speed kn",
#       native_unit_of_measurement=SPEED_KNOTS,
#       device_class=SensorDeviceClass.WIND_SPEED,
#       state_class=SensorStateClass.MEASUREMENT,
#   ),
)

FORECAST_SENSOR_TYPES: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(
        key=ATTR_API_TEMP_MAX,
        name="Forecast Maximum Temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
    ),
    SensorEntityDescription(
        key=ATTR_API_TEMP_MIN,
        name="Forecast Minimum Temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
    ),
    SensorEntityDescription(
        key=ATTR_API_ICON_DESCRIPTOR,
        name="Icon Descriptor",
    ),
    SensorEntityDescription(
        key=ATTR_API_MDI_ICON,
        name="MDI Icon",
    ),
    SensorEntityDescription(
        key=ATTR_API_SHORT_TEXT,
        name="Short Summary Forecast",
    ),
    SensorEntityDescription(
        key=ATTR_API_RAIN_AMOUNT_MIN,
        name="Rain Amount Minimum",
        native_unit_of_measurement=UnitOfPrecipitationDepth.MILLIMETERS,
        device_class=SensorDeviceClass.PRECIPITATION,
    ),
#   SensorEntityDescription(
#       key=ATTR_API_EXTENDED_TEXT,
#       name="Extended Forecast",
#   ),
#   SensorEntityDescription(
#       key=ATTR_API_UV_CATEGORY,
#       name="UV Category",
#   ),
#   SensorEntityDescription(
#       key=ATTR_API_UV_MAX_INDEX,
#       name="UV Maximum Index",
#   ),
#   SensorEntityDescription(
#       key=ATTR_API_UV_START_TIME,
#       name="UV Protection Start Time",
#       device_class=SensorDeviceClass.TIMESTAMP,
#   ),
#   SensorEntityDescription(
#       key=ATTR_API_UV_END_TIME,
#       name="UV Protection End Time",
#       device_class=SensorDeviceClass.TIMESTAMP,
#   ),
#   SensorEntityDescription(
#       key=ATTR_API_UV_FORECAST,
#       name="UV Forecast Summary",
#   ),
#   SensorEntityDescription(
#       key=ATTR_API_RAIN_AMOUNT_MAX,
#       name="Rain Amount Maximum",
#       native_unit_of_measurement=LENGTH_MILLIMETERS,
#       device_class=SensorDeviceClass.PRECIPITATION,
#   ),
#   SensorEntityDescription(
#       key=ATTR_API_RAIN_AMOUNT_RANGE,
#       name="Rain Amount Range",
#   ),
#   SensorEntityDescription(
#       key=ATTR_API_RAIN_CHANCE,
#       name="Rain Probability",
#       native_unit_of_measurement=PERCENTAGE,
#   ),
#   SensorEntityDescription(
#       key=ATTR_API_FIRE_DANGER,
#       name="Fire Danger",
#   ),
#   SensorEntityDescription(
#       key=ATTR_API_NON_NOW_LABEL,
#       name="Now Label",
#   ),
#   SensorEntityDescription(
#       key=ATTR_API_NON_TEMP_NOW,
#       name="Now Temperature",
#       native_unit_of_measurement=UnitOfTemperature.CELSIUS,
#       device_class=SensorDeviceClass.TEMPERATURE,
#   ),
#   SensorEntityDescription(
#       key=ATTR_API_NOW_LATER_LABEL,
#       name="Later Label",
#   ),
#   SensorEntityDescription(
#       key=ATTR_API_NOW_TEMP_LATER,
#       name="Later Temperature",
#       native_unit_of_measurement=UnitOfTemperature.CELSIUS,
#       device_class=SensorDeviceClass.TEMPERATURE,
#   ),
#   SensorEntityDescription(
#       key=ATTR_API_ASTRONOMICAL_SUNRISE_TIME,
#       name="Sunrise Time",
#       device_class=SensorDeviceClass.TIMESTAMP,
#   ),
#   SensorEntityDescription(
#       key=ATTR_API_ASTRONOMICAL_SUNSET_TIME,
#       name="Sunset Time",
#       device_class=SensorDeviceClass.TIMESTAMP,
#   ),
)

WARNING_SENSOR_TYPES: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(
        key=ATTR_API_WARNINGS,
        name="Warnings",
    ),
)


"""Platform for sensor integration."""
from __future__ import annotations

import logging
from datetime import datetime, tzinfo

from homeassistant.components.weather import (
    ATTR_CONDITION_CLEAR_NIGHT,
    ATTR_CONDITION_SUNNY,
    ATTR_FORECAST_CONDITION,
    ATTR_FORECAST_HUMIDITY,
    ATTR_FORECAST_IS_DAYTIME,
    ATTR_FORECAST_NATIVE_DEW_POINT,
    ATTR_FORECAST_NATIVE_TEMP,
    ATTR_FORECAST_NATIVE_WIND_SPEED,
    ATTR_FORECAST_PRECIPITATION_PROBABILITY,
    ATTR_FORECAST_TIME,
    ATTR_FORECAST_WIND_BEARING,
    ATTR_FORECAST_NATIVE_WIND_SPEED,
    ATTR_FORECAST_TEMP,
    ATTR_FORECAST_TEMP_LOW,
    ATTR_FORECAST_PRECIPITATION,
    WeatherEntity,
    Forecast,
    SingleCoordinatorWeatherEntity,
    WeatherEntityFeature,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    UnitOfSpeed, 
    UnitOfTemperature, 
    UnitOfPrecipitationDepth, 
    UnitOfPressure,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.device_registry import DeviceEntryType
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import DataCoordinator
from .const import (
    ATTRIBUTION,
    COLLECTOR,
    CONF_WEATHER_NAME,
    COORDINATOR,
    DOMAIN,
    MAP_CONDITION,
    SHORT_ATTRIBUTION,
    MODEL_NAME,
    CONF_CITY,
    CONF_FORCAST_DAYS,

    ATTR_API_TEMP,
    ATTR_API_TEMP_FEELS_LIKE,
    ATTR_API_MAX_TEMP,
    ATTR_API_MIN_TEMP,
    ATTR_API_RAIN_SINCE_9AM,
    ATTR_API_HUMIDITY, 
    ATTR_API_WIND_SPEED_KILOMETRE,
    ATTR_API_WIND_SPEED_KNOT,
    ATTR_API_WIND_DIRECTION,
    ATTR_API_GUST_SPEED_KILOMETRE,
    ATTR_API_GUST_SPEED_KNOT,

    ATTR_API_TEMP_MAX,
    ATTR_API_TEMP_MIN,
    ATTR_API_EXTENDED_TEXT,
    ATTR_API_ICON_DESCRIPTOR,
    ATTR_API_MDI_ICON,
    ATTR_API_SHORT_TEXT,
    ATTR_API_UV_CATEGORY,
    ATTR_API_UV_MAX_INDEX,
    ATTR_API_UV_START_TIME,
    ATTR_API_UV_END_TIME,
    ATTR_API_UV_FORECAST,
    ATTR_API_RAIN_AMOUNT_MIN,
    ATTR_API_RAIN_AMOUNT_MAX,
    ATTR_API_RAIN_AMOUNT_RANGE,
    ATTR_API_RAIN_CHANCE,
    ATTR_API_FIRE_DANGER,
    ATTR_API_NON_NOW_LABEL,
    ATTR_API_NON_TEMP_NOW,
    ATTR_API_NOW_LATER_LABEL,
    ATTR_API_NOW_TEMP_LATER,
    ATTR_API_ASTRONOMICAL_SUNRISE_TIME,
    ATTR_API_ASTRONOMICAL_SUNSET_TIME,
    ATTR_API_WARNINGS,
)
from .collector import Collector

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Add a Időkép weather entity from a config_entry."""

    coordinator: DataCoordinator = hass.data[DOMAIN][config_entry.entry_id]

    location_name = config_entry.options.get(
        CONF_CITY, config_entry.data.get(CONF_CITY, "")
    )

    async_add_entities([IdokepWeatherEntity(coordinator, location_name)])


class IdokepWeatherEntity(
    SingleCoordinatorWeatherEntity[DataCoordinator]
):

    def __init__(self, coordinator: DataCoordinator, location_name) -> None:
        """Initialize the entity."""
        super().__init__(coordinator)
        self.collector: Collector = coordinator[COLLECTOR]
        self.coordinator: DataCoordinator = coordinator[COORDINATOR]
        self.location_name: str = location_name
        self._attr_device_info = DeviceInfo(
            entry_type=DeviceEntryType.SERVICE,
            identifiers={(DOMAIN, self.location_name)},
            manufacturer=SHORT_ATTRIBUTION,
            model=MODEL_NAME,
            name=self.location_name,
        )
        self._attr_attribution = ATTRIBUTION
        self._attr_native_temperature_unit = UnitOfTemperature.CELSIUS
        self._attr_native_precipitation_unit = UnitOfPrecipitationDepth.MILLIMETERS
        self._attr_native_pressure_unit = UnitOfPressure.KPA
        self._attr_native_wind_speed_unit = UnitOfSpeed.KILOMETERS_PER_HOUR
        self._attr_supported_features = (
            WeatherEntityFeature.FORECAST_DAILY | WeatherEntityFeature.FORECAST_HOURLY
        )   

    @property
    def native_temperature(self):
        """Return the platform temperature."""
        return self.collector.locations_data["current"][ATTR_API_TEMP]
        return 0

    @property
    def icon(self):
        """Return the icon."""
        return self.collector.daily_forecasts_data[0][ATTR_API_MDI_ICON]        

    @property
    def native_temperature_unit(self):
        """Return the unit of measurement."""
        return UnitOfTemperature.CELSIUS

    @property
    def humidity(self):
        """Return the humidity."""
        #return self.collector.observations_data["data"]["humidity"]
        return 0

    @property
    def native_wind_speed(self):
        """Return the wind speed."""
        #return self.collector.observations_data["data"]["wind_speed_kilometre"]
        return 0

    @property
    def native_wind_speed_unit(self):
        """Return the unit of measurement for wind speed."""
        return UnitOfSpeed.KILOMETERS_PER_HOUR

    @property
    def wind_bearing(self):
        """Return the wind bearing."""
        #return self.collector.observations_data["data"]["wind_direction"]
        return 0

    @property
    def attribution(self):
        """Return the attribution."""
        return ATTRIBUTION

    @property
    def condition(self):
        """Return the current condition."""
        return (self.collector.locations_data["current"][ATTR_API_SHORT_TEXT] + " - " + self.collector.locations_data["current"][ATTR_API_EXTENDED_TEXT]).truncate(254)
        #return self.collector.daily_forecasts_data[0][ATTR_API_ICON_DESCRIPTOR]

    @property
    def forecast_daily(self) -> list[Forecast] | None:
        """Return the forecast array."""
        forecasts = list[Forecast] = []

        if self.collector.daily_forecasts_data is not None:
            _LOGGER.Warning("forecast_daily processing")
            days = len(self.collector.daily_forecasts_data)
            for day in range(0, days):
                forecast = {
                    ATTR_FORECAST_TIME: self.collector.daily_forecasts_data[day]["date"],
                    ATTR_FORECAST_TEMP: self.collector.daily_forecasts_data[day][ATTR_API_TEMP_MAX],
                    ATTR_FORECAST_CONDITION: MAP_CONDITION[self.collector.daily_forecasts_data[day][ATTR_API_ICON_DESCRIPTOR]],
                    ATTR_FORECAST_TEMP_LOW: self.collector.daily_forecasts_data[day][ATTR_API_TEMP_MIN],
                    ATTR_FORECAST_PRECIPITATION: self.collector.daily_forecasts_data[day][ATTR_API_RAIN_AMOUNT_MIN],
                    #"precipitation_probability": self.collector.daily_forecasts_data[day][ATTR_API_RAIN_CHANCE],
                }
                forecasts.append(forecast)
        return forecasts
            
    @property
    def forecast_hourly(self) -> list[Forecast] | None:
        """Return the forecast array."""
        forecasts = list[Forecast] = []
        if self.collector.hourly_forecasts_data is not None:
            _LOGGER.Warning("forecast_hourly processing")
            
            hours = len(self.collector.hourly_forecasts_data)
            for hour in range(0, hours):
                forecast = {
                    ATTR_FORECAST_TIME: self.collector.hourly_forecasts_data[hour]["time"],
                    ATTR_FORECAST_NATIVE_TEMP: self.collector.hourly_forecasts_data[hour][ATTR_API_TEMP_MAX],
                    "detailed_description": self.collector.hourly_forecasts_data[hour][ATTR_API_SHORT_TEXT],

                    ATTR_FORECAST_PRECIPITATION_PROBABILITY: self.collector.hourly_forecasts_data[hour][ATTR_API_RAIN_CHANCE],
                    ATTR_FORECAST_PRECIPITATION: self.collector.hourly_forecasts_data[hour][ATTR_API_RAIN_AMOUNT_MIN],
                    
                    "wind_description": self.collector.hourly_forecasts_data[hour]["wind_description"],
                    ATTR_FORECAST_NATIVE_WIND_SPEED: self.collector.hourly_forecasts_data[hour]["wind_strenght"],
                    "wind_direction": self.collector.hourly_forecasts_data[hour][ATTR_API_WIND_DIRECTION],
                    
                    "alert": self.collector.hourly_forecasts_data[hour]["alert"],
                   
                }
                forecasts.append(forecast)
        return forecasts

    @property
    def condition(self):
        """Return the condition"""
        return MAP_CONDITION[self.collector.daily_forecasts_data[0][ATTR_API_ICON_DESCRIPTOR]]

    @callback
    def _async_forecast_daily(self) -> list[Forecast] | None:
        """Return the daily forecast in native units."""
        _LOGGER.Warning("_async_forecast_daily called")
        return self.forecast_daily

    @callback
    def _async_forecast_hourly(self) -> list[Forecast] | None:
        """Return the hourly forecast in native units."""
        _LOGGER.Warning("_async_forecast_hourly called")
        return self.forecast_hourly

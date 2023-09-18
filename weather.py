"""Platform for sensor integration."""
from __future__ import annotations

import logging
from datetime import datetime, tzinfo

from homeassistant.components.weather import WeatherEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import SPEED_KILOMETERS_PER_HOUR, TEMP_CELSIUS
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
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Add sensors for passed config_entry in HA."""
    hass_data = hass.data[DOMAIN][config_entry.entry_id]

    new_entities = []

    location_name = config_entry.options.get(
        CONF_CITY, config_entry.data.get(CONF_CITY, "")
    )

    new_entities.append(WeatherDaily(hass_data, location_name))
    new_entities.append(WeatherHourly(hass_data, location_name))

    if new_entities:
        async_add_entities(new_entities, update_before_add=False)


class WeatherBase(WeatherEntity):

    def __init__(self, hass_data, location_name) -> None:
        """Initialize the sensor."""
        self.collector: Collector = hass_data[COLLECTOR]
        self.coordinator: DataCoordinator = hass_data[COORDINATOR]
        self.location_name: str = location_name
        self._attr_device_info = DeviceInfo(
            entry_type=DeviceEntryType.SERVICE,
            identifiers={(DOMAIN, self.location_name)},
            manufacturer=SHORT_ATTRIBUTION,
            model=MODEL_NAME,
            name=self.location_name,
        )

    async def async_added_to_hass(self) -> None:
        """Set up a listener and load data."""
        self.async_on_remove(self.coordinator.async_add_listener(self._update_callback))
        self.async_on_remove(self.coordinator.async_add_listener(self._update_callback))
        self._update_callback()

    @callback
    def _update_callback(self) -> None:
        """Load data from integration."""
        self.async_write_ha_state()

    @property
    def should_poll(self) -> bool:
        """Entities do not individually poll."""
        return False

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
        return TEMP_CELSIUS

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
        return SPEED_KILOMETERS_PER_HOUR

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
        return self.collector.locations_data["current"][ATTR_API_SHORT_TEXT] + " - " + self.collector.locations_data["current"][ATTR_API_EXTENDED_TEXT]
        #return self.collector.daily_forecasts_data[0][ATTR_API_ICON_DESCRIPTOR]

    async def async_update(self):
        await self.coordinator.async_update()


class WeatherDaily(WeatherBase):

    def __init__(self, hass_data, location_name):
        """Initialize the sensor."""
        super().__init__(hass_data, location_name)

    @property
    def name(self):
        """Return the name."""
        return self.location_name + "Daily"

    @property
    def unique_id(self):
        """Return Unique ID string."""
        return self.location_name + "_daily"

    @property
    def forecast(self):
        """Return the forecast."""
        forecasts = []
        if self.collector.daily_forecasts_data is not None:
            days = len(self.collector.daily_forecasts_data)
            for day in range(0, days):
                forecast = {
                    "datetime": self.collector.daily_forecasts_data[day]["date"],
                    "native_temperature": self.collector.daily_forecasts_data[day][ATTR_API_TEMP_MAX],
                    "condition": MAP_CONDITION[self.collector.daily_forecasts_data[day][ATTR_API_ICON_DESCRIPTOR]],
                    "templow": self.collector.daily_forecasts_data[day][ATTR_API_TEMP_MIN],
                    "native_precipitation": self.collector.daily_forecasts_data[day][ATTR_API_RAIN_AMOUNT_MIN],
                    #"precipitation_probability": self.collector.daily_forecasts_data[day][ATTR_API_RAIN_CHANCE],
                }
                forecasts.append(forecast)
        return forecasts
        
    @property
    def condition(self):
        """Return the condition"""
        return MAP_CONDITION[self.collector.daily_forecasts_data[0][ATTR_API_ICON_DESCRIPTOR]]


class WeatherHourly(WeatherBase):

    def __init__(self, hass_data, location_name):
        """Initialize the sensor."""
        super().__init__(hass_data, location_name)

    @property
    def name(self):
        """Return the name."""
        return self.location_name + "Hourly"

    @property
    def unique_id(self):
        """Return Unique ID string."""
        return self.location_name + "_hourly"

    @property
    def forecast(self):
        """Return the forecast."""
        forecasts = []
        if self.collector.hourly_forecasts_data is not None:
            
            hours = len(self.collector.hourly_forecasts_data)
            for hour in range(0, hours):
                forecast = {
                    "datetime": self.collector.hourly_forecasts_data[hour]["time"],
                    "native_temperature": self.collector.hourly_forecasts_data[hour][ATTR_API_TEMP_MAX],
                    "description": self.collector.hourly_forecasts_data[hour][ATTR_API_SHORT_TEXT],

                    "rain_chance": self.collector.hourly_forecasts_data[hour][ATTR_API_RAIN_CHANCE],
                    "rain_level": self.collector.hourly_forecasts_data[hour][ATTR_API_RAIN_AMOUNT_MIN],
                    
                    "wind_description": self.collector.hourly_forecasts_data[hour]["wind_description"],
                    "wind_strenght": self.collector.hourly_forecasts_data[hour]["wind_strenght"],
                    "wind_direction": self.collector.hourly_forecasts_data[hour][ATTR_API_WIND_DIRECTION],
                    
                    "alert": self.collector.hourly_forecasts_data[hour]["alert"],
                   
                }
                forecasts.append(forecast)
        return forecasts

    @property
    def condition(self):
        """Return the condition"""
        return MAP_CONDITION[self.collector.daily_forecasts_data[0][ATTR_API_ICON_DESCRIPTOR]]



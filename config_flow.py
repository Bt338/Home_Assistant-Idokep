import logging

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant import config_entries, exceptions
from homeassistant.core import HomeAssistant, callback

from .const import (
    CONF_CITY,
    CONF_FORCAST_DAYS,
    DOMAIN,
)
from .collector import Collector

_LOGGER = logging.getLogger(__name__)


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):

    VERSION = 1

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> config_entries.OptionsFlow:
        return OptionsFlow(config_entry)

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        data_schema = vol.Schema(
            {
                vol.Required(CONF_CITY, default="Budapest"): str,
                vol.Required(CONF_FORCAST_DAYS, default=10): int,
            }
        )

        errors = {}
        if user_input is not None:
            try:
                self.collector = Collector(
                    user_input[CONF_CITY],
                )

                # Save the user input into self.data so it's retained
                self.data = user_input

                await self.collector.async_update()
                return self.async_create_entry(
                    title="%s" % (self.data["city"]),
                    data=self.data,
                )

            except Exception:
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        # If there is no user input or there were errors, show the form again, including any errors that were found with the input.
        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )



class OptionsFlow(config_entries.OptionsFlow):
    """Handle options."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialise the options flow."""
        self.config_entry = config_entry
        self.data = {}

    async def async_step_init(self, user_input=None):
        """Handle the initial step."""
        data_schema = vol.Schema(
            {
                vol.Required(
                    CONF_CITY,
                    default=self.config_entry.options.get(
                        CONF_CITY,
                        self.config_entry.data.get(
                            CONF_CITY, "Budapest"
                        ),
                    ),
                ): str,
                vol.Required(
                    CONF_FORCAST_DAYS,
                    default=self.config_entry.options.get(
                        CONF_FORCAST_DAYS,
                        self.config_entry.data.get(
                            CONF_FORCAST_DAYS, 10
                        ),
                    ),
                ): int,
            }
        )

        errors = {}
        if user_input is not None:
            try:
                self.collector = Collector(
                    user_input[CONF_CITY],
                )

                # Save the user input into self.data so it's retained
                self.data = user_input

                await self.collector.async_update()
                self.data.update(user_input)
                return self.async_create_entry(
                    title="%s" % (self.data["city"]),
                    data=self.data
                )

            except Exception:
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        # If there is no user input or there were errors, show the form again, including any errors that were found with the input.
        return self.async_show_form(
            step_id="init", data_schema=data_schema, errors=errors
        )

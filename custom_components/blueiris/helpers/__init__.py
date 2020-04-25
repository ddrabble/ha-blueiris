import logging
import sys

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from ..managers.home_assistant import BlueIrisHomeAssistant
from ..managers.password_manager import PasswordManager
from .const import *

_LOGGER = logging.getLogger(__name__)


def clear_ha(hass: HomeAssistant, host):
    if DATA_BLUEIRIS not in hass.data:
        hass.data[DATA_BLUEIRIS] = dict()

    del hass.data[DATA_BLUEIRIS][host]


def get_ha(hass: HomeAssistant, host):
    ha_data = hass.data.get(DATA_BLUEIRIS, dict())
    ha = ha_data.get(host)

    return ha


async def async_set_ha(hass: HomeAssistant, host, entry: ConfigEntry):
    try:
        if DATA_BLUEIRIS not in hass.data:
            hass.data[DATA_BLUEIRIS] = dict()

        if PASSWORD_MANAGER_BLUEIRIS not in hass.data:
            hass.data[PASSWORD_MANAGER_BLUEIRIS] = PasswordManager(hass)

        password_manager = hass.data[PASSWORD_MANAGER_BLUEIRIS]

        instance = BlueIrisHomeAssistant(hass, password_manager)

        await instance.async_init(entry)

        hass.data[DATA_BLUEIRIS][host] = instance
    except Exception as ex:
        exc_type, exc_obj, tb = sys.exc_info()
        line_number = tb.tb_lineno

        _LOGGER.error(f"Failed to async_set_ha, error: {ex}, line: {line_number}")


async def handle_log_level(hass: HomeAssistant, entry: ConfigEntry):
    log_level = entry.options.get(CONF_LOG_LEVEL, LOG_LEVEL_DEFAULT)

    if log_level == LOG_LEVEL_DEFAULT:
        return

    log_level_data = {f"custom_components.{DOMAIN}": log_level.lower()}

    await hass.services.async_call(DOMAIN_LOGGER, SERVICE_SET_LEVEL, log_level_data)

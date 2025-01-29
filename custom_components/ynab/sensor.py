"""Sensor platform for ynab."""

import logging
from homeassistant.helpers.entity import Entity

from .const import ACCOUNT_ERROR, CATEGORY_ERROR, DOMAIN_DATA, ICON

_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up sensor platform."""
    sensors = []

    _LOGGER.info(f"####### {discovery_info}")
    # Fetch YNAB data
    await hass.data[DOMAIN_DATA]["client"].update_data()

    # Create main budget sensors
    main_sensors = [
        "budgeted_this_month",
        "activity_this_month",
        "age_of_money",
        "total_balance",
        "need_approval",
        "uncleared_transactions",
        "overspent_categories",
    ]

    for sensor_name in main_sensors:
        sensors.append(YNABSensor(hass, sensor_name))

    _LOGGER.info(config)
    # Create category sensors separately
    categories = config["categories"]
    if categories is not None:
        for category in categories:
            _LOGGER.info(f"Configured categories: {categories}")
            sensors.append(YNABCategorySensor(hass, category))
            sensors.append(YNABCategorySensor(hass, f"{category}_budgeted"))

    # Create account sensors
    accounts = config["accounts"]
    if accounts is not None:
        for account in accounts:
            sensors.append(YNABAccountSensor(hass, account))

    async_add_entities(sensors, True)


class YNABSensor(Entity):
    """General YNAB Sensor class for main metrics."""

    def __init__(self, hass, name):
        """Initialize the sensor."""
        self.hass = hass
        self._name = f"YNAB {name.replace('_', ' ').title()}"
        self._state = None
        self._data_key = name
        self._measurement = "$"

    async def async_update(self):
        """Update the sensor."""
        await self.hass.data[DOMAIN_DATA]["client"].update_data()
        self._state = self.hass.data[DOMAIN_DATA].get(self._data_key)

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    @property
    def unit_of_measurement(self):
        return self._measurement

    @property
    def icon(self):
        return ICON


class YNABCategorySensor(Entity):
    """Sensor for individual budget categories."""

    def __init__(self, hass, category):
        """Initialize the sensor."""
        self.hass = hass
        self._name = f"YNAB {category.replace('_', ' ').title()}"
        self._state = None
        self._category = category
        self._measurement = "$"

    async def async_update(self):
        """Update the sensor."""
        await self.hass.data[DOMAIN_DATA]["client"].update_data()
        self._state = self.hass.data[DOMAIN_DATA].get(self._category)

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    @property
    def unit_of_measurement(self):
        return self._measurement

    @property
    def icon(self):
        return ICON


class YNABAccountSensor(Entity):
    """Sensor for individual accounts in YNAB."""

    def __init__(self, hass, account):
        """Initialize the sensor."""
        self.hass = hass
        self._name = f"YNAB Account {account.replace('_', ' ').title()}"
        self._state = None
        self._account = account
        self._measurement = "$"

    async def async_update(self):
        """Update the sensor."""
        await self.hass.data[DOMAIN_DATA]["client"].update_data()
        self._state = self.hass.data[DOMAIN_DATA].get(self._account)

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    @property
    def unit_of_measurement(self):
        return self._measurement

    @property
    def icon(self):
        return ICON

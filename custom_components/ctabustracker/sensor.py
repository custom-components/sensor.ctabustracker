"""
Show departure information from ctabustracker (Chicago Transit Authority).

For more details about this component, please refer to the documentation at
https://github.com/smcpeck/sensor.ctabustracker/
"""
import datetime as dt
import logging
import requests

import voluptuous as vol

import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_NAME
from homeassistant.helpers.entity import Entity
from homeassistant.util import Throttle

__version__ = '0.0.4'

_LOGGER = logging.getLogger(__name__)

CONF_API_KEY = 'api_key'
CONF_DEPARTURES = 'departures'
CONF_LINES = 'lines'
CONF_STOP_ID = 'stop_id'
CONF_TYPE = 'type'

BUS_RESOURCE = "http://ctabustracker.com/bustime/api/v2/"
BUS_ENDPOINT = "getpredictions?key={}&stpid={}&format=json"
TRAIN_RESOURCE = "http://lapi.transitchicago.com/api/1.0/"
TRAIN_ENDPOINT = "ttarrivals.aspx?key={}&stpid={}&max={}&outputType=JSON"

TIME_BETWEEN_UPDATES = dt.timedelta(seconds=60)

LINES = vol.Schema({
    vol.Required(CONF_STOP_ID): cv.string,
    vol.Optional(CONF_DEPARTURES, default=1): cv.positive_int,
    vol.Optional(CONF_NAME): cv.string,
})

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_API_KEY): cv.string,
    vol.Required(CONF_TYPE): vol.In(["bus", "train"]),
    vol.Required(CONF_LINES): vol.All(cv.ensure_list, [LINES]),
})


async def async_setup_platform(
        hass, config, async_add_entities, discovery_info=None):   # pylint: disable=W0613
    """Set up the sensor platform."""
    api_key = config[CONF_API_KEY]
    lines = config[CONF_LINES]
    transit_type = config[CONF_TYPE]

    dev = []
    for line in lines:
        api = None
        if transit_type == "bus":
            api = CtaBusData(api_key, line)
        elif transit_type == "train":
            api = CtaTrainData(api_key, line)
 
        for departure in range(0, line['departures']):
            dev.append(CtaSensor(api, transit_type, departure, line))
            
    async_add_entities(dev, True)


class CtaSensor(Entity):
    """Representation of a Home Assistant sensor."""

    def __init__(self, api, transit_type, departure, config):
        """Initialize the sensor."""
        self.api = api
        self.departure = departure
        self.config = config
        self._state = None
        self.transit_type = transit_type
        postfix = '' if departure == 0 else str(departure)
        self._name = "{} {}".format(
            self.config.get('name', 'CTA ' + self.config['stop_id']), postfix)

    def update(self):
        """Get the latest information."""
        try:
            self.api.update()
            data = self.api.data
            _LOGGER.debug(f"[{self.transit_type}] SENSOR.update() data = {data}")

            if data:
                if self.transit_type == "bus":
                    self._state = data[self.departure].get('prdctdn')
                elif self.transit_type == "train":
                    prediction = data[self.departure]
                    pred_time = dt.datetime.strptime(prediction["prdt"], "%Y-%m-%dT%H:%M:%S")
                    arr_time = dt.datetime.strptime(prediction["arrT"], "%Y-%m-%dT%H:%M:%S")
                    minutes_left = int((arr_time-pred_time).total_seconds()/60)
                    if minutes_left <= 1:
                        minutes_left = "DUE"
                    self._state = minutes_left
                else:
                    self._state = "Bad type"
                    _LOGGER.warning("Bad transit_type configured")
            else:
                self._state = "No data"
                _LOGGER.warning("No CTA data")
        except Exception as ex:  # pylint: disable=W0703
            self._state = None
            _LOGGER.error(ex)

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def icon(self):
        """Set sensor icon."""
        return {'bus':'mdi:bus-clock','train':'mdi:train'}[self.transit_type]

class CtaTrainData:
    """Get the latest data and update the states."""

    def __init__(self, api_key, config):
        """Initialize the data object."""
        self.api_key = api_key
        self.config = config
        self.api = "{}{}".format(
            TRAIN_RESOURCE, TRAIN_ENDPOINT.format(
                self.api_key, self.config['stop_id'], self.config['departures']))
        self._data = None

    @Throttle(TIME_BETWEEN_UPDATES)
    def update(self):
        """Get the latest data from ctabustracker."""
        try:
            self._data = requests.get(
                self.api).json().get('ctatt', {}).get('eta', {})
        except Exception as error:  # pylint: disable=W0703
            _LOGGER.error(error)
            self._data = self._data
        return self._data

    @property
    def data(self):
        """Holds data."""
        return self._data
    

class CtaBusData:
    """Get the latest data and update the states."""

    def __init__(self, api_key, config):
        """Initialize the data object."""
        self.api_key = api_key
        self.config = config
        self.api = "{}{}".format(
            BUS_RESOURCE, BUS_ENDPOINT.format(
                self.api_key, self.config['stop_id']))
        self._data = None

    @Throttle(TIME_BETWEEN_UPDATES)
    def update(self):
        """Get the latest data from ctabustracker."""
        try:
            self._data = requests.get(
                self.api).json().get('bustime-response', {}).get('prd', {})
        except Exception as error:  # pylint: disable=W0703
            _LOGGER.error(error)
            self._data = self._data
        

    @property
    def data(self):
        """Holds data."""
        return self._data

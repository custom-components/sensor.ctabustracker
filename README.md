# sensor.ctabustracker

Show departure information from ctabustracker (Chicago Transit Authority).

This plafrom is based of the findings of [@SilvrrGIT](https://github.com/SilvrrGIT)
in this [forum post](https://community.home-assistant.io/t/cta-bus-tracker-sensor/92416)

## Installation
### HACS
Add this as a custom repository and restart your HA instance.

### Manual
To get started put `/custom_components/ctabustracker/sensor.py` here:  
`<config directory>/custom_components/ctabustracker/sensor.py`

## Example configuration.yaml

```yaml
sensor:
  platform: ctabustracker
  api_key: 'dfshkdkf7333ykgdfk73'
  type: 'bus'
  lines:
    - stop_id: 77
      departures: 2
      name: 'Union Station'

sensor:
  platform: ctabustracker
  api_key: 'lk38vjklrj4nj'
  type: 'train'
  lines:
    - stop_id: 3045
      departures: 2
      name: 'Logan Square'
```

### Configuration variables
  
key | type | description  
:--- | :--- | :---  
**platform (Required)** | string | The platform name.
**api_key (Required)** | string | [CTA Bus API Key](https://www.transitchicago.com/developers/bustracker/) *or* [CTA Train API Key](https://www.transitchicago.com/developers/traintracker/)
**type** (Required) | string | Transit type: ["bus", "train"]
**lines (Required)** | list | List of lines you want to track.

> **Note:** Bus times and train times each required a different API key.

### Lines configuration

key | type | description  
:--- | :--- | :---  
**stop_id (Required)** | string | Stop ID (`stpid`)
**departures (Optional)** | int | Number of future departures.
**name (Optional)** | list | Name of the HA sensor

## Change Log
### 0.0.3
[@ludeeus](https://github.com/ludeeus):  Initial release.

### 0.0.3 (on HACS)
[@jonochocki](https://github.com/jonochocki):  Added easy install via HACS support.

### 0.0.4
[@smcpeck](https://github.com/smcpeck): Added support for train lines.
- `route` config variable is no longer supported since the APIs don't need it was a "bus only" API parameter.

***
contributor | support
:--- | :--- 
[@ludeeus](https://github.com/ludeeus) | [![BuyMeCoffee](https://camo.githubusercontent.com/cd005dca0ef55d7725912ec03a936d3a7c8de5b5/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f6275792532306d6525323061253230636f666665652d646f6e6174652d79656c6c6f772e737667)](https://www.buymeacoffee.com/ludeeus)
[@smcpeck](https://github.com/smcpeck) | [![BuyMeCoffee](https://camo.githubusercontent.com/cd005dca0ef55d7725912ec03a936d3a7c8de5b5/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f6275792532306d6525323061253230636f666665652d646f6e6174652d79656c6c6f772e737667)](https://www.buymeacoffee.com/shaunmcpeck)

# Wavespa

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)
[![hacs][hacsbadge]][hacs]

This custom component integrates with the Wavespa cloud API, providing control of devices such as WaveSpa Garda hot tubs.

<p float="left">
  <img src="images/demo-thermostat.png" width="200" />
  <img src="images/demo-controls.png" width="200" />
  <img src="images/demo-diagnostic.png" width="200" />
</p>

## Foreword

Thank you to the bestway integration and various HA forum posts for pointers so I could reverese engineer this to work
Most of the words in this Readem come from the Bestway integration I forked from 

## Required Account

You must have an account with the Wavespa mobile app Lay-Z-Spa app credentials will not work. Both apps appear to have identical feature sets.

Wavespa uses different API endpoints for EU and US. If you get an error stating account could not be found, try using the other endpoint. If this does not help, then create a new account under a supported country.

## Device Support

A Wi-Fi enabled model is required. No custom hardware is required.

See the [supported devices](docs/supported-devices.md) list for more details.

## Installation

This integration is delivered as a HACS custom repository.

1. Download and install [HACS][hacs-download].
2. Add a [custom repository][hacs-custom] in HACS. You will need to enter the URL of this repository when prompted: `https://github.com/GraemeDBlue/ha-wavespa`.

## Configuration

Ensure you can control your device using the Wavespa mobile app. At time of writing, there was also a Lay-Z-Spa branded app, but despite this being the recommended app in the installation manual, the spa could not be added. The Wavespa app worked flawlessly.

- Go to **Configuration** > **Devices & Services** > **Add Integration**, then find **Wavespa** in the list.
- Enter your Wavespa username and password when prompted.

## Update speed

Any changes made to the spa settings via the Wavespa app or physical controls can take a short amount of time to be reflected in Home Assistant. This delay is typically under 30 seconds, but can sometimes extend to a few minutes.

## Improvement ideas

Achieve faster (or even local) updates.

- Capture more traffic from the mobile app to work out how it receives updates so quickly.
- The integration currently has to poll, but the mobile app is able to reflect changes based on physical button presses within a fraction of a second.
- A brief recent attempt suggested that the Android app may have certificate pinning enabled, making this slightly harder than expected. Perhaps decompilation is an easier route.
- We know the spa talks directly to the cloud using MQTT. Traffic captures against the Android app appeared to show only HTTPS traffic.

## Acknowledgements

- https://github.com/cdpuk/ha-bestway
- https://github.com/B-Hartley/bruces_homeassistant_config

## Contributing

If you want to contribute to this please read the [Contribution Guidelines](CONTRIBUTING.md).

[commits-shield]: https://img.shields.io/github/commit-activity/y/GraemeDBlue/ha-wavespa.svg?style=for-the-badge
[commits]: https://github.com/GraemeDBlue/ha-wavespa/commits/main
[hacs]: https://github.com/custom-components/hacs
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[license-shield]: https://img.shields.io/github/license/GraemeDBlue/ha-wavespa.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/GraemeDBlue/ha-wavespa.svg?style=for-the-badge
[releases]: https://github.com/GraemeDBlue/ha-wavespa/releases
[hacs-download]: https://hacs.xyz/docs/setup/download
[hacs-custom]: https://hacs.xyz/docs/faq/custom_repositories

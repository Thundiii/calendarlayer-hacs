# CalendarLayer for Home Assistant

CalendarLayer exposes entities from `calendar.thundiii.de` as Home Assistant sensor entities.

## Features

- HACS-compatible custom integration structure
- UI-based setup via Home Assistant config flow
- API token validation during setup
- Dynamic sensor creation from CalendarLayer entities
- Clean unload/reload support
- German and English setup texts

## Installation via HACS

1. Open HACS in Home Assistant.
2. Add `https://github.com/thundiii/calendarlayer-hacs` as a custom repository.
3. Select repository type `Integration`.
4. Install `CalendarLayer`.
5. Restart Home Assistant.
6. Go to **Settings > Devices & services > Add integration** and search for `CalendarLayer`.
7. Enter your CalendarLayer API token.

## Manual installation

Copy `custom_components/calendarlayer` into your Home Assistant `custom_components` directory and restart Home Assistant.

## Configuration

The integration is configured from the Home Assistant UI. YAML configuration is not required.

## Notes

This repository is a HACS custom integration, not a Home Assistant OS add-on. Add-ons are containerized services; this project installs a Home Assistant integration under `custom_components`.

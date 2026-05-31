# Home Assistant sensors for RecipeBox

RecipeBox exposes a JSON summary at `/api/state` (via the add-on's ingress URL).
Because ingress URLs are dynamic, the simplest reliable way to read it from Home
Assistant is to expose the add-on on a fixed port and point a RESTful sensor at it.

## 1. Give the add-on a fixed port (optional but recommended)
In the add-on **Configuration** tab, set the network port for `8099/tcp` to e.g. `8099`.
Then the API is reachable at `http://homeassistant.local:8099/api/state`
(or `http://<HA-IP>:8099/api/state`).

## 2. Add a REST sensor to configuration.yaml

```yaml
rest:
  - resource: "http://homeassistant.local:8099/api/state"
    scan_interval: 300
    sensor:
      - name: "RecipeBox Recipes"
        unique_id: recipebox_recipes
        value_template: "{{ value_json.recipes }}"
        icon: mdi:book-open-variant
      - name: "RecipeBox Favorites"
        unique_id: recipebox_favorites
        value_template: "{{ value_json.favorites }}"
        icon: mdi:star
        json_attributes_path: "$"
        json_attributes:
          - favorite_titles
      - name: "RecipeBox Shopping"
        unique_id: recipebox_shopping
        value_template: "{{ value_json.shopping_open }}"
        icon: mdi:cart
      - name: "RecipeBox Meals Today"
        unique_id: recipebox_meals_today
        value_template: "{{ value_json.meals_today }}"
        icon: mdi:silverware-fork-knife
```

This creates:
- `sensor.recipebox_recipes` – total number of recipes
- `sensor.recipebox_favorites` – number of favorites (with a `favorite_titles` attribute listing them)
- `sensor.recipebox_shopping` – number of unchecked shopping items
- `sensor.recipebox_meals_today` – number of meals planned for today

Restart Home Assistant (or reload REST entities) after editing the YAML.

## Notes
- The endpoint returns JSON like:
  `{"recipes": 12, "favorites": 3, "favorite_titles": [...], "shopping_open": 5, "meals_today": 2}`
- If you prefer not to open a port, you can also use the ingress URL with a long-lived
  token, but a fixed port + REST sensor is by far the easiest.

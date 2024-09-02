import folium

from .models import Pokemon, PokemonEntity
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.utils import timezone


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def check_image(request, image_field):
    if image_field and hasattr(image_field, 'url'):
        return request.build_absolute_uri(image_field.url)
    return DEFAULT_IMAGE_URL


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    time_now = timezone.localtime()
    for pokemon_entity in PokemonEntity.objects.filter(
            appeared_at__lte=time_now,
            disappeared_at__gte=time_now
    ):
        pokemon_image = check_image(request, pokemon_entity.pokemon.image)
        add_pokemon(
            folium_map,
            pokemon_entity.lat,
            pokemon_entity.lon,
            pokemon_image
        )

    pokemons_on_page = []
    for pokemon in Pokemon.objects.all():
        img_url = check_image(request, pokemon.image)
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': img_url,
            'title_ru': pokemon.title_ru,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    requested_pokemon = get_object_or_404(Pokemon, id=int(pokemon_id))
    image_url = check_image(request, requested_pokemon.image)
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemon_info = {
        "title_ru": requested_pokemon.title_ru,
        "title_en": requested_pokemon.title_en,
        "title_jp": requested_pokemon.title_jp,
        "description": requested_pokemon.description,
        "img_url": image_url,
        "previous_evolution": None,
        "next_evolution": None
    }

    for entity in PokemonEntity.objects.filter(pokemon=requested_pokemon):
        add_pokemon(
            folium_map,
            entity.lat,
            entity.lon,
            image_url
        )

    if requested_pokemon.previous_evolution:
        prev_image_url = check_image(request, requested_pokemon.previous_evolution.image)
        previous_evolution = {
            "title_ru": requested_pokemon.previous_evolution.title_ru,
            "pokemon_id": requested_pokemon.previous_evolution.id,
            "img_url": prev_image_url
        }
        pokemon_info['previous_evolution'] = previous_evolution

    next_evolution = requested_pokemon.next_evolutions.first()
    if next_evolution:
        next_image_url = check_image(request, next_evolution.image)
        next_evolution_info = {
            "title_ru": next_evolution.title_ru,
            "pokemon_id": next_evolution.id,
            "img_url": next_image_url
        }
        pokemon_info['next_evolution'] = next_evolution_info

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(),
        'pokemon': pokemon_info
    })
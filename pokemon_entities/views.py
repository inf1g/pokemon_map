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
    for pokemon_entity in PokemonEntity.objects.filter(
            appeared_at__lte=timezone.localtime(),
            disappeared_at__gte=timezone.localtime()
    ):
        add_pokemon(
            folium_map,
            pokemon_entity.lat,
            pokemon_entity.lon,
            request.build_absolute_uri(pokemon_entity.pokemon.image.url)
        )

    pokemons_on_page = []
    for pokemon in Pokemon.objects.all():
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': request.build_absolute_uri(pokemon.image.url),
            'title_ru': pokemon.title_ru,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    requested_pokemon = get_object_or_404(Pokemon, id=int(pokemon_id))
    image_url = (
        request.build_absolute_uri(requested_pokemon.image.url)
        if requested_pokemon.image else DEFAULT_IMAGE_URL
    )
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemon_dict = {
        "title_ru": requested_pokemon.title_ru,
        "title_en": requested_pokemon.title_en,
        "title_jp": requested_pokemon.title_jp,
        "description": requested_pokemon.description,
        "img_url": image_url,
        "previous_evolution": None
    }

    for entity in PokemonEntity.objects.filter(pokemon=requested_pokemon):
        add_pokemon(
            folium_map,
            entity.lat,
            entity.lon,
            image_url
        )

        if requested_pokemon.evolves:
            previous_evolution = {
                "title_ru": requested_pokemon.evolves.title_ru,
                "pokemon_id": requested_pokemon.evolves.id,
                "img_url": (
                    request.build_absolute_uri(requested_pokemon.evolves.image.url)
                    if requested_pokemon.evolves.image else DEFAULT_IMAGE_URL
                )
            }
            pokemon_dict['previous_evolution'] = previous_evolution

        next_evolution = requested_pokemon.evolution.first()
        if next_evolution:
            next_evolution_dict = {
                "title_ru": next_evolution.title_ru,
                "pokemon_id": next_evolution.id,
                "img_url": (
                    request.build_absolute_uri(next_evolution.image.url)
                    if next_evolution.image else DEFAULT_IMAGE_URL
                )
            }
            pokemon_dict['next_evolution'] = next_evolution_dict

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(),
        'pokemon': pokemon_dict
    })
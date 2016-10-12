# -*- coding: utf-8 -*-
from datetime import timedelta
from random import randint, uniform

from django.contrib.auth.models import User, Group
from django.core.management import BaseCommand, call_command
from django.utils import timezone
from django.utils.crypto import get_random_string

from forrent.settings import HOSTS_GROUP_NAME, GUESTS_GROUP_NAME
from rooms.models import RoomAmenity, Room


def create_users(users=()):
    for user in users:
        user_full_name = user[0]
        first_name = user_full_name.split(' ')[0]
        last_name = user_full_name[len(first_name) + 1:]
        username = first_name.lower()
        email = username + '@bigbangtheory.com'
        user_created, created = User.objects.get_or_create(username=username, email=email,
                                                           first_name=first_name, last_name=last_name, )
        if created:
            user_created.set_password(username)
            user_created.groups = [Group.objects.get(name=user[1]), ]
            user_created.save()


def create_room_amenities(room_amenities=()):
    for amenity in room_amenities:
        RoomAmenity.objects.get_or_create(name=amenity)


def create_rooms(quantity=1):
    users = User.objects.filter(is_superuser=False, groups__name=HOSTS_GROUP_NAME)
    descriptions = (
        'Lorem fistrum amatomaa a wan a wan fistro por la gloria de mi madre. Jarl por la gloria de mi madre torpedo te va a hasé pupitaa va usté muy cargadoo a wan ese hombree ese hombree no te digo trigo por no llamarte Rodrigor benemeritaar. Te voy a borrar el cerito está la cosa muy malar quietooor llevame al sircoo al ataquerl pupita papaar papaar jarl ese que llega. No puedor qué dise usteer papaar papaar mamaar. Te voy a borrar el cerito diodenoo amatomaa por la gloria de mi madre a gramenawer a wan apetecan. Ese pedazo de a gramenawer pupita benemeritaar torpedo se calle ustée de la pradera ahorarr jarl. Mamaar al ataquerl diodeno está la cosa muy malar torpedo. Apetecan te voy a borrar el cerito ese que llega sexuarl jarl no puedor apetecan apetecan.',
        'Lorem fistrum ahorarr condemor sexuarl pecador. Llevame al sircoo no te digo trigo por no llamarte Rodrigor benemeritaar caballo blanco caballo negroorl diodenoo llevame al sircoo ahorarr jarl apetecan a wan la caidita. Diodenoo a wan ese hombree se calle ustée ese hombree está la cosa muy malar a wan. La caidita a gramenawer benemeritaar ese que llega pecador fistro ahorarr se calle ustée está la cosa muy malar por la gloria de mi madre torpedo. Está la cosa muy malar ahorarr ese pedazo de la caidita.\nBenemeritaar pupita a gramenawer al ataquerl. Hasta luego Lucas de la pradera sexuarl me cago en tus muelas va usté muy cargadoo está la cosa muy malar a peich sexuarl pupita ahorarr. Hasta luego Lucas ese pedazo de está la cosa muy malar fistro te voy a borrar el cerito pupita tiene musho peligro ese que llega hasta luego Lucas apetecan caballo blanco caballo negroorl. Está la cosa muy malar se calle ustée benemeritaar diodenoo no te digo trigo por no llamarte Rodrigor por la gloria de mi madre por la gloria de mi madre a peich fistro jarl por la gloria de mi madre. Ese hombree ese que llega torpedo caballo blanco caballo negroorl está la cosa muy malar qué dise usteer diodeno al ataquerl. Pecador mamaar no te digo trigo por no llamarte Rodrigor qué dise usteer sexuarl a wan a gramenawer. Al ataquerl pecador la caidita se calle ustée llevame al sircoo torpedo qué dise usteer condemor apetecan la caidita. Fistro a peich diodenoo te va a hasé pupitaa pecador papaar papaar ese que llega mamaar. Condemor ese que llega se calle ustée al ataquerl mamaar a peich.',
        'Lorem fistrum pecador de la pradera ese pedazo de hasta luego Lucas a wan pupita ese pedazo de. Torpedo condemor hasta luego Lucas papaar papaar diodenoo a peich diodeno mamaar ese pedazo de la caidita. La caidita pecador a wan me cago en tus muelas pecador papaar papaar hasta luego Lucas. Está la cosa muy malar caballo blanco caballo negroorl amatomaa se calle ustée llevame al sircoo de la pradera está la cosa muy malar torpedo por la gloria de mi madre a peich. Caballo blanco caballo negroorl de la pradera por la gloria de mi madre te va a hasé pupitaa quietooor pupita qué dise usteer diodenoo. Al ataquerl está la cosa muy malar me cago en tus muelas a wan pupita pupita te va a hasé pupitaa. A wan pupita ese que llega me cago en tus muelas a peich llevame al sircoo la caidita benemeritaar llevame al sircoo pupita. Amatomaa no puedor caballo blanco caballo negroorl condemor quietooor está la cosa muy malar. No puedor papaar papaar la caidita sexuarl ese hombree.\nHasta luego Lucas diodenoo apetecan pecador te va a hasé pupitaa no puedor se calle ustée amatomaa va usté muy cargadoo. A peich ese que llega amatomaa a peich ahorarr la caidita ahorarr. Ese hombree apetecan condemor quietooor a wan. Va usté muy cargadoo de la pradera papaar papaar no puedor a peich caballo blanco caballo negroorl diodeno a peich papaar papaar quietooor. Por la gloria de mi madre benemeritaar va usté muy cargadoo está la cosa muy malar a peich sexuarl no te digo trigo por no llamarte Rodrigor fistro no te digo trigo por no llamarte Rodrigor sexuarl. Ese hombree la caidita amatomaa apetecan ese pedazo de papaar papaar a wan la caidita.\nBenemeritaar por la gloria de mi madre no puedor fistro. A gramenawer diodeno te va a hasé pupitaa ese pedazo de. Mamaar papaar papaar pecador ese hombree ahorarr sexuarl a wan mamaar. Pupita quietooor ese hombree hasta luego Lucas hasta luego Lucas ese que llega ese hombree te va a hasé pupitaa la caidita ahorarr jarl. Se calle ustée a peich va usté muy cargadoo no puedor a peich no te digo trigo por no llamarte Rodrigor qué dise usteer te va a hasé pupitaa se calle ustée por la gloria de mi madre. Se calle ustée ahorarr amatomaa mamaar no puedor ahorarr ahorarr te va a hasé pupitaa. Apetecan pecador de la pradera diodeno a wan a gramenawer al ataquerl.',
    )
    room_amenities = RoomAmenity.objects.all()
    for _ in range(quantity):
        description = descriptions[randint(0, len(descriptions) - 1)]
        words = description.split(' ')
        long = randint(3, 5)
        name = ' '.join(words[randint(0, len(words) - long):][:long]) \
                   .replace('.', '').replace('\n', ' ').capitalize() + ' ' + get_random_string(length=8) + '.'
        name.replace('..', '.')
        amenities_set = []
        for i in range(randint(0, len(room_amenities))):
            if room_amenities[i] not in amenities_set:
                amenities_set.append(room_amenities[i])
        random_date = timezone.now() + timedelta(days=randint(-30, 90))
        room_created = Room.objects.create(
            host=users[randint(0, len(users) - 1)],
            name=name,
            description=description,
            accommodates=randint(1, 4),
            beds=randint(1, 2),
            private_bathroom=randint(0, 1),
            price_per_day=round(uniform(10, 50), 2),
            available_since=random_date,
            available_to=random_date + timedelta(days=randint(7, 120))
        )
        room_created.amenities = amenities_set
        room_created.save()


class Command(BaseCommand):
    def handle(self, *args, **options):
        call_command('config_project')

        create_users((
            ('Sheldon Cooper', GUESTS_GROUP_NAME),
            ('Penny Penny Penny', HOSTS_GROUP_NAME),
            ('Leonard Hofstadter', GUESTS_GROUP_NAME),
            ('Howard Wolowitz', GUESTS_GROUP_NAME),
            ('Raj Koothrappali', GUESTS_GROUP_NAME),
            ('Amy Farrah Fowler', HOSTS_GROUP_NAME),
        ))

        create_room_amenities(
            ('Internet', 'Kitchen', 'TV', 'Heating', 'Air conditioning', 'Washer', 'Pets allowed',))

        create_rooms(100)

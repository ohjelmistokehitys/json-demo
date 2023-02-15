import sqlite3
import json
from sqlite3 import Connection
from pathlib import Path
from collections import namedtuple

Artist = namedtuple('Artist', 'id, name')
Album = namedtuple('Artist', 'id, title, artist_id')

index_file: Path = Path(__file__).parent / 'api' / 'artists.json'


def get_artists() -> list[Artist]:
    con = sqlite3.connect("Chinook_Sqlite.sqlite")
    cur = con.cursor()

    res = cur.execute("SELECT ArtistId, Name FROM Artist")
    rows = res.fetchall()
    con.close()

    return [Artist(id, name) for id, name in rows]


def get_albums() -> list[Album]:
    con = sqlite3.connect("Chinook_Sqlite.sqlite")
    cur = con.cursor()

    res = cur.execute("SELECT AlbumId, Title, ArtistId FROM Album")
    rows = res.fetchall()
    con.close()

    return [Album(id, title, artist_id) for id, title, artist_id in rows]


def write_index_file(artists: list[Artist]):
    '''
    Writes a single JSON file with an object, where artist ids are keys and names are values.
    '''
    index_json = {'artists': [{'id': id, 'name': name, 'url': f'api/artists/{id}.json'} for id, name in artists],
                  'license': 'https://github.com/lerocha/chinook-database/blob/master/LICENSE.md'}
    index_file.write_text(json.dumps(index_json, indent=4))


def write_artists_files(artists: list[Artist], albums: list[Album]):
    '''
    Writes a JSON file for each artists, containing the albums of that artist.
    '''
    albums_by_artists = {
        id: [album for album in albums if album.artist_id == id] for id, name in artists
    }

    for artist in artists:
        json_file = index_file.parent / 'artists' / f'{artist.id}.json'
        own_albums = albums_by_artists[artist.id]
        data = {
            'id': artist.id,
            'name': artist.name,
            'albums': [{'id': album.id, 'title': album.title} for album in own_albums],
            'license': 'https://github.com/lerocha/chinook-database/blob/master/LICENSE.md'
        }
        json_file.write_text(json.dumps(data, indent=4))


if __name__ == '__main__':
    artists = get_artists()
    albums = get_albums()

    write_index_file(artists)
    write_artists_files(artists, albums)

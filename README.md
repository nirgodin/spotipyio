# Spotipyio
An async Python wrapper to the Spotify API

## Before Starting
In case you don't already own a Spotify API account including a `client_id`, `client_secret` and a `redirect_uri`, please 
go first to the [Spotify developers page]() and create one.

Successfully created the account? Great, let's start cooking

## Installation
### Pip
```bash 
pip install spotipyio
```

### Pipenv
```bash 
pipenv add spotipyio
```

### Poetry
```bash 
poetry add spotipyio
```

## Getting Started
### Sending your first request

```python
import asyncio
from spotipyio import SpotifyClient, SpotifySession
from typing import List


async def fetch_tracks_info(tracks_ids: List[str]) -> List[dict]:
    spotify_session = SpotifySession(
        client_id="<your-spotify-client-session>",
        client_secret="<your-spotify-client-secret>",
        redirect_uri="<your-spotify-redirect-uri>"
    )
    
    async with spotify_session as session:
        client = SpotifyClient.create(session)
        
        return await client.tracks.info.run(tracks_ids)


if __name__ == '__main__':
    tracks_ids = [""]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(fetch_tracks_info(tracks_ids))
```

Let's walk through this example one line by another.

### The SpotifySession
The `SpotifySession` object is used to instantiate the aiohttp ClientSession used to send asynchronous requests to the 
Spotify API. This objects creates and stores the authorization headers required by the Spotify API. This session is 
instantiated using the Spotify API `client_id`, `client_secret` and `redirect_uri` you created in the Before Starting 
section.

**Pay attention:** The `SpotifySession` object is an async context manager. This means that all your code must be 
indented under the `async with spotify_session as session` block. Once the code exists the indentation block, the 
client session will close and you will no longer be able to use it to send requests.

### The SpotifyClient
The `SpotifyClient` object is the single object you need to use to execute your business logic. Once created, you will 
not have to use any other object to send requests. In the above example, we are using it to fetch tracks information. 
The easiest way to create it is by using the `.create` classmethod as is done above.

Pay attention we are providing the `tracks.info.run` method not a single track id but a list of ids. This is 
one of the greatest benefits the package is offering to the user. If you're familiar with the Spotify API you might 
already know it doesn't offer this kind of functionality, but only a single track endpoint or several_tracks endpoint 
limited to maximum 50 tracks ids. The `tracks.info.run` method - as well as other similar methods for other types of 
data - can receive any number of tracks ids. It automatically takes care of optimizing your requests by splitting it 
to 50 ids chunks and parallelizing the requests.

## Deep Dive
### SpotifySession
#### Grant Type
#### Caching

### SpotifyClient
The `SpotifyClient` object is built with two principles in mind. First, it aims to offer an API that is both intuitive 
and matches as far as possible the actual Spotify API structure as presented in the 
[official documentation](https://developer.spotify.com/documentation/web-api/reference). 
To this end, the client doesn't holds any logic by itself, but only hosts a variety of objects, each designed to 
represent a logical subset of the API endpoints. The following sections present each object's methods.
* albums
* artists
* current_user
* playlists
* search
* tracks
* users

## Testing
Testing is a central part of software development, but when it comes to 
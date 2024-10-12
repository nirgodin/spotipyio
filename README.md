from zoneinfo import reset_tzpathfrom aiohttp import ClientResponseErrorfrom tests.conftest import spotify_clientfrom tests.managers.playlists.conftest import playlist_idfrom spotipyio.auth import SpotifyGrantTypefrom spotipyio import SpotifyClient

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
pipenv install spotipyio
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
Testing is central to software development, but when it comes to external APIs like Spotify's it can be tricky 
to test our code without sending any actual request. To this end, spotipy introduces `SpotifyTestClient`. This object 
is designed to help you test components that use the `SpotifyClient` seamlessly, without having to mock or patch 
anything, or familiarize yourself with the internals of `SpotifyClient`. 

### Installation
To avoid adding dev dependencies to our production code, the test client sits under a dedicated `testing` module, which 
requirements' are optional. To install these extra requirements, execute the relevant command.

#### Pip
```bash 
pip install spotipyio[testing]
```

#### Pipenv
```bash 
pipenv install spotipyio[testing]
```

#### Poetry
```bash 
poetry add spotipyio[testing]
```

#### A notice about versions management
As the test client it is designed only for testing, you should include it in only in your dev dependencies. 
On a poetry based project, for example, your `pyproject.toml` file should look somewhat like this:

```toml
[tool.poetry.dependencies]
spotipyio = { version = ">=1,<2" }

[tool.poetry.group.dev.dependencies]
spotipyio = { version = "*", extras = ["testing"] }
```

**Pay attention**: the version is pinned only in the dependencies section. The dev dependencies section should not pin 
a version, to avoid conflicts between two sections.

### Testing your first component
Imagine having a simple function that should fetch a playlist from Spotify and return a list of the 
playlist's tracks names. This function should look something like this:
```python
from typing import List
from spotipyio import SpotifyClient

async def get_playlist_tracks(spotify_client: SpotifyClient, playlist_id: str) -> List[str]:
    playlist = await spotify_client.playlists.info.run_single(playlist_id)
    items = playlist["tracks"]["items"]
    
    return [item["track"]["name"] for item in items]
```

Now, Let's test it:
```python
import pytest

from spotipyio.testing import SpotifyTestClient


@pytest.fixture
async def test_client() -> SpotifyTestClient:
    async with SpotifyTestClient() as client:
        yield client


async def test_get_playlist_tracks(test_client: SpotifyTestClient):
    # Arrange
    spotify_client = test_client.create_client()
    playlist_id = "readme-example"
    test_client.playlists.info.expect_success(playlist_id)

    # Act
    actual = await get_playlist_tracks(spotify_client, playlist_id)

    # Assert
    assert isinstance(actual, list)
```

What do we have here? Let's break it down step by step
1. First, we import `SpotifyTestClient` from the previously mentioned `spotipyio.testing` module. Notice that if you 
didn't install the package including the `testing` extra you will encounter an `ImportError` at this stage.
2. We create a fixture of `SpotifyTestClient`. Notice we use a `yield` statement instead of `return`, to keep 
the fixture context alive until teardown
3. We use the test client to instantiate a `SpotifyClient` instance. This is done using a simple `create_client` 
method, which sets up a client that shares the exact same settings as the test client.
4. Finally, we make sure our playlist request will be successful by calling `test_client.playlists.info.expect_success`.
This makes sure our request to the specific playlist id we're providing will be answered with a 200 status code.

#### Setting the response json
This test, of course, is not very good. Mainly, it only validates the return value is a list, but it doesn't **really** 
check the actual value returned by the `get_platlist_tracks` function. To check this functionality, let's provide it 
an actual response json we expect. Here's a revised version:

```python
async def test_get_playlist_tracks(test_client: SpotifyTestClient):
    # Arrange
    expected = ["Bohemian Raphsody", "The Blacker The Berry", "Take Five", "Jhonny B. Goode"]
    response_items = [{"track": {"name": name}} for name in expected]
    response_json = {"tracks": {"items": response_items}}
    spotify_client = test_client.create_client()
    playlist_id = "readme-example"
    test_client.playlists.info.expect_success(playlist_id, [response_json])

    # Act
    actual = await get_playlist_tracks(spotify_client, playlist_id)
    
    # Assert
    assert actual == expected
```

We've added our arrange block three lines where we define our expected value, than use it to create a mock playlist 
json that will be returned from the API. Than, we provide the test client with this response json, making sure that 
when a request to fetch the `readme-example` playlist will be received, this will be the exact json that will be 
returned. Notice that now our assertion is much stronger - we expect the actual value to be equal to our expectation.

#### Testing exception handling
Up until now we've been focusing only on testing successful scenarios. But what about exception handling? Handling 
exceptions is absolutely a must when it comes to work with external APIs like Spotify's. How should we test it? Let's 
start by wrapping our function with a simple try-except block

```python
from typing import List
from spotipyio import SpotifyClient
from aiohttp.client_exceptions import ClientResponseError

async def get_playlist_tracks(spotify_client: SpotifyClient, playlist_id: str) -> List[str]:
    try:
        playlist = await spotify_client.playlists.info.run_single(playlist_id)
        items = playlist["tracks"]["items"]
        
        return [item["track"]["name"] for item in items]
    
    except ClientResponseError:
        print("Failed to fetch playlist. Retuning empty list instead")
        return []
```
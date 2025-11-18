from pydantic import BaseModel
import requests
from typing import List

class Meme(BaseModel):
    id: str
    name: str
    url: str
    width: int
    height: int
    box_count: int
    captions: int


class Data(BaseModel):
    memes: List[Meme]


class Model(BaseModel):
    success: bool
    data: Data

def get_all_memes() -> List[Meme]:
    """Fetches all memes from the Imgflip API."""
    print("Fetching all memes from Imgflip API...")
    url = "https://api.imgflip.com/get_memes"
    response = requests.get(url)
    model = Model.model_validate_json(response.text)
    print(f"Fetched {len(model.data.memes)} memes from Imgflip API.")
    return model.data.memes

def get_memes_names(all_memes: List[Meme]) -> List[str]:
    """Fetches a list of available memes from the Imgflip API."""
    print("Getting meme names...")
    available_memes = [meme.name for meme in all_memes]
    return available_memes

def get_meme_by_name(name: str, all_memes: List[Meme]) -> Meme:
    """Fetches a meme by its name from the Imgflip API."""
    print(f"Getting meme details for: {name}...")
    meme = next((meme for meme in all_memes if meme.name == name), None)
    if meme is None:
        raise ValueError(f"Meme with name '{name}' not found.")
    return meme
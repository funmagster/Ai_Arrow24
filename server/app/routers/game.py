from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from app.model.game import *
from app.db.db import close_room
from app.func.game import *

routers = APIRouter()


@routers.post("/start_game")
async def get_start_game(game_start: Game_start):
    active_members = await close_room(game_start.room)
    story = await oboz_LLM.get_story(game_start.prompt)
    story_splits = split_story(story)

    prompt_img = await oboz_LLM.get_prompt_img(story_splits[0])
    characters = await oboz_LLM.get_character(active_members, story)
    story_img = await oboz_LLM.get_img(prompt_img)
    if story_img is None:
        story_img = await image_to_base64(image_path='default_img.png', format='png')

    return JSONResponse(status_code=200, content={
        'status_code': 200,
        'success': True,
        'story': story,
        'history': story_splits[0],
        'characters': [split_characters(characters)],
        'img': story_img
    })


@routers.post("/play")
async def get_start_game(game_play: Game_play):
    answer = await oboz_LLM.get_play(
        game_play.count_room_complete,
        game_play.history,
        game_play.story,
        game_play.character,
        game_play.prompt
    )
    print(answer)
    try:
        answer = get_json_format(answer)
    except json.decoder.JSONDecodeError as err:
        answer = {
            'answer': answer.replace('{', '')\
                          .replace('}', '')\
                          .replace("'action': ", '')\
                          .replace("'answer': ", ''),
            'action': 3
        }
    story_img = None
    if answer['action'] != 1 and answer['action'] != 2:
        prompt_img = await oboz_LLM.get_prompt_img(answer['answer'])
        story_img = await oboz_LLM.get_img(prompt_img)

    new_history = await oboz_LLM.summarize(
        game_play.history + answer['answer'],
    )
    return JSONResponse(status_code=200, content={
        'status_code': 200,
        'success': True,
        'answer': answer['answer'],
        'action': answer['action'],
        'history': new_history,
        'img': story_img
    })

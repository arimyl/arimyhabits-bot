import dataclasses
import json


@dataclasses.dataclass
class LINEUser:
    user_id: str
    user_name: str


def get_profile(line_bot_api: object, user_id: str):
    """プロフィールを取得する"""
    profile = line_bot_api.get_profile(user_id)  # json
    profile_dict = json.loads(profile)  # dict
    display_name = profile_dict["displayName"]
    language = profile_dict["language"]
    status_message = profile_dict["statusMessage"]
    user_obj = LINEUser(user_id, display_name)

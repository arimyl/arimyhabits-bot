import dataclasses
import json
from inspect import signature


@dataclasses.dataclass
class LINEUser:
    user_id: str
    user_name: str

    @classmethod
    def from_kwargs(cls, **kwargs):
        # cls.__dataclass_fields__.keys()
        # fetch the constractor's signature
        cls_fields = {fields for fields in signature(cls).parameters}

        # split the keargs into native ones and new ones
        native_args, new_args = {}, {}
        for name, val in kwargs.items():
            if name in cls_fields:
                native_args[name] = val
            else:
                new_args[name] = val
        
        # use the native ones to create the class ...
        ret = cls(**native_args)
        # ... and add the new ones by hand 
        for new_name, new_val in new_args.items():
            setattr(ret, new_name, new_val)
        return ret


def get_profile(line_bot_api:object, user_id:str):
    """プロフィールを取得する
    """
    profile = line_bot_api.get_profile(user_id) # json
    profile_dict = json.loads(profile) # dict
    display_name = profile_dict['displayName']
    language = profile_dict['language']
    status_message = profile_dict['statusMessage']
    user_obj = LINEUser(user_id, display_name)
    # register_message(status_message, 0)

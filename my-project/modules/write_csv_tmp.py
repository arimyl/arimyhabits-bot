from datetime import datetime as dt
import os
import pathlib as path
from typing import List


main_path = os.path.dirname(os.path.dirname(__file__))
tmp_path = os.path.join(main_path, 'tmp')


def read_temporary(user_id: str) -> List[str]:
    """open file and read textlines"""
    file_path = confirm_file(user_id)
    file_lines = []
    if file_path:
        with open(str(file_path), 'r') as f:
            for line in f.readlines:
                file_lines.append(line)
        
    return file_lines


def register_tmporary(message_text: str, user_id: str) -> None:
    """register text to temporary file"""
    file_path = confirm_file(user_id)
    #
    if file_path is None:
        file_path = path.Path(os.path.join(tmp_path, f'tmp_{user_id}.csv'))
    
    write_csv(create_contents(message_text), file_path.name)
        

def write_csv(contents: List[list], file_name: str='tmp.csv') -> None:
    """一時保存ファイル作成・書き込み
    :contents
    """
    file_path = os.path.join(main_path, file_name)
    with open(file=file_path, mode='w+', newline='\n') as f:
        for content in contents:
            f.write(','.join(content))


def create_contents(message_text: str) -> List[list]:
    """"""
    contents = []
    for t in message_text.split(','):
        content = [t, str(dt.now())[:-3]]
        contents.append(content)
    return contents


def confirm_file(user_id: str) -> bool:
    """csvファイルを確認する
    """
    for file in path.Path(tmp_path).glob('*.csv'):
        # fileName confirm ('tmp_<user_id>.csv')
        if file.stem.split('_')[1] == user_id:
            return file
    return None



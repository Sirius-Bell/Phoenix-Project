import threading
from time import sleep

import PySimpleGUI as Sg
import helperclass
import requests

Sg.theme('DarkAmber')

layout = [[Sg.Text('Access token here:'), Sg.Input(key='access_token')],
          [Sg.Text('Target ID here:'), Sg.Input(key='target_id')],
          [Sg.ProgressBar(size=(20, 20), key='-PROG-', max_value=200, visible=False)],
          [Sg.Text('Completed', visible=False, key='-COMPL-')],
          [Sg.Button('Delete videos', key='-OK-')]]

window = Sg.Window('Phoenix', layout)


class Main:
    def __init__(self, access_token: str, target_id: str):
        """
        Main functions for deleting videos in VK
        :param access_token: token from VK
        :param target_id: target(your) ID
        """
        self.access_token = access_token
        self.target_id = target_id

        self.helper = helperclass.Helper()

    def get_videos(self) -> list:
        url = "https://api.vk.com/method/video.get"
        params = {'access_token': self.access_token, 'v': '5.131', 'count': '200'}

        resp = requests.get(url, params=params).json()
        if 'response' not in resp:
            self.helper.logger.critical('Error getting videos')
            window['-COMPL-'].update('Error getting videos', visible=True)
            return []
        if resp['response']['count'] == 0:
            self.helper.logger.critical('No videos found')
            window['-COMPL-'].update('No videos found', visible=True)
            return []

        return resp['response']['items']

    def video_delete(self, owner_id: str, video_id: str) -> bool:
        params = {'access_token': self.access_token, 'v': '5.131', 'target_id': self.target_id,
                  'owner_id': owner_id, 'video_id': video_id}
        resp = requests.get("https://api.vk.com/method/video.delete", params=params).json()

        if resp['response'] == 1:
            self.helper.logger.info(f'Video deleted: {video_id}')
            return True
        else:
            self.helper.logger.critical(f'Error: {resp}')


def event_ok(values_s):
    ll = Main(access_token=values_s['access_token'], target_id=values_s['target_id'])
    videos = ll.get_videos()

    if not videos:
        return False

    window['-PROG-'].update(max=len(videos), current_count=0, visible=True)

    for i in range(len(videos)):
        ll.video_delete(videos[i]['owner_id'], videos[i]['id'])
        window['-PROG-'].update(i + 1)
        sleep(3)
    window['-COMPL-'].update(visible=True)


while True:
    event, values = window.read()

    if values['access_token'] == '' or values['target_id'] == '':
        window['-COMPL-'].update('Access token or target ID is empty', visible=True)
        continue

    if event == '-OK-':
        thread = threading.Thread(target=event_ok, args=(values,)).start()

    if event == Sg.WIN_CLOSED:
        window.close()
        break

_album_id = "243762445"
vk = None
import requests
import json
import time
import logging
logging.basicConfig(filename='photo_cycle.log', level = logging.INFO,
    format = '%(asctime)s : %(levelname)s : %(message)s')

def start(_vk):
    global vk
    vk = _vk
    print("Hello!")
    alb = vk.photos.get(album_id = _album_id)
    for ph in alb['items']:
        _download_photo_to_buffer(ph["photo_604"])
        time.sleep(600)

import urllib.request
buff_name = "temp.jpg"
prev_ph = None
def _download_photo_to_buffer(url):
    
    urllib.request.urlretrieve(url,buff_name)
    _change_main_photo()

def _change_main_photo():
    try:
        server = vk.photos.getOwnerPhotoUploadServer()
        #UPLOAD PHOTO
        
        answ = requests.post(server['upload_url'],files = {"photo" : open(buff_name, "rb")}).json()

        res = vk.photos.saveOwnerPhoto(server = answ['server'], hash = answ['hash'], photo = answ['photo'])
        logging.info(res)
        vk.wall.delete(post_id = res['post_id'])
        smth = vk.photos.getAll()['items'][1]
        vk.photos.delete(photo_id = smth['id'])

    except Exception as e:
        logging.error(e)
        vk.messages.send(message = e, user_id = "80314023")
    
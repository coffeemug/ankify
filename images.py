
import io
import base64
import sys
import math
from robobrowser import RoboBrowser
from concurrent.futures import ThreadPoolExecutor
from PIL import Image as Img
from PIL import ImageDraw, ImageFont
import statistics as stats

IMG_WIDTH = 128
IMG_HEIGHT = 128
HOR_GRID_COUNT = 4
SEARCH_URL = 'https://www.google.com/search?tbm=isch&q='

def search(txt):
    browser = RoboBrowser(parser='html.parser')
    browser.open(SEARCH_URL + txt)
    images = browser.select('img')
    sources = [i.attrs['src'] for i in images]
    return sources

def download(source):
    browser = RoboBrowser(parser='html.parser')
    browser.open(source)
    res = browser.response
    return res.content

def download_all(sources):
    with ThreadPoolExecutor(max_workers=len(sources)) as e:
        images = e.map(download, sources)
    return list(images)

def to_images(images):
    return list(map(lambda img: Img.open(io.BytesIO(img)), images))

def filterify(images):
    heights = list(map(lambda i: i.height, images))
    median = stats.median(heights)
    lbound = median - (median / 5)
    ubound = median + (median / 5)
    return list(filter(lambda i: i.height > lbound and i.height < ubound , images))

def beautify(images):
    for img in images:
        img.thumbnail([IMG_WIDTH, IMG_HEIGHT])
    return images

def gridify(images):
    VERT_GRID_COUNT = math.ceil(len(images) / HOR_GRID_COUNT)
    max_height = max(images, key=lambda i: i.height).height
    max_height += int(max_height / 10)
    grid_width = HOR_GRID_COUNT * IMG_WIDTH
    grid_height = VERT_GRID_COUNT * max_height
    img = Img.new("RGB", (grid_width, grid_height))
    d = ImageDraw.Draw(img)
    for idx, i in enumerate(images):
        y = (idx // HOR_GRID_COUNT) * max_height
        y += int((max_height / 2) - (i.height / 2))
        x = (idx %  HOR_GRID_COUNT) * IMG_WIDTH
        x += int((IMG_WIDTH / 2) - (i.width / 2))
        img.paste(i, (x, y))
        d.rectangle([x, y, x+10, y+10], fill=(0, 0, 0))
        d.text((x+2, y), str(idx+1), fill=(255, 255, 255))
        
    out = io.BytesIO()
    img.save(out, format='png')
    return out.getvalue()

def img_to_term(img):
    IMAGE_CODE = '\033]1337;File=name={name};inline={inline};size={size}:{base64_img}\a'
    data = {
        'name': base64.b64encode('Unnamed'.encode('utf-8')).decode('ascii'),
        'inline': 1,
        'size': len(img),
        'base64_img': base64.b64encode(img).decode('ascii'),
        }
    txt = IMAGE_CODE.format(**data)
    sys.stdout.write(txt)

def query_images(query):
    sources = search(query)
    images = download_all(sources)
    images = to_images(images)
    images = filterify(images)
    images = beautify(images)
    return images[:8]

def grid_print(images):
    out = gridify(images)
    img_to_term(out)
    print()


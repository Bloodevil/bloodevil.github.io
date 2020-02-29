from requests import get
import os
from flask import Flask, escape, request, render_template

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/home/dante/hobby/bloodevil.github.io/ozingermaker/google_application_credentials.json"

app = Flask(__name__)

def pre_define(set_number):
    if set_number == 1:
        result = [
        ("https://newsimg.hankookilbo.com/2018/09/10/201809101668762602_1.jpg",),
        ("https://newsimg.hankookilbo.com/2018/09/10/201809101668762602_1.jpg",),
        ("https://newsimg.hankookilbo.com/2018/09/10/201809101668762602_1.jpg",),
        ("https://newsimg.hankookilbo.com/2018/09/10/201809101668762602_1.jpg",),
        ("https://newsimg.hankookilbo.com/2018/09/10/201809101668762602_1.jpg",),
        ("https://newsimg.hankookilbo.com/2018/09/10/201809101668762602_1.jpg",),
        ("https://newsimg.hankookilbo.com/2018/09/10/201809101668762602_1.jpg",),
        ("https://newsimg.hankookilbo.com/2018/09/10/201809101668762602_1.jpg",),
        ]
    return result

def detect_faces_uri(uri):
    """Detects faces in the file located in Google Cloud Storage or the web."""
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()
    image = vision.types.Image()
    image.source.image_uri = uri
    
    response = client.face_detection(image=image)
    faces = response.face_annotations
    
    # Names of likelihood from google.cloud.vision.enums
    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY')
    print('Faces:')
    
    for face in faces:
    
        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in face.bounding_poly.vertices])
    
        print('face bounds: {}'.format(','.join(vertices)))
        return vertices

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

def search(q):
    key = "AIzaSyBo2tU2JCnlCfdqeGnHw9i3qn3sTouKNBE"
    url = "https://www.googleapis.com/customsearch/v1"
    cx = "008370077433993226117:h_plqmrdou0"
    payload = {"cx": cx,
            "imgType": "photo",
            "searchType": "image",
            "q": q,
            "key": key}
    r = get(url, params=payload)
    if r.status_code == 200:
        link = r.json()["items"][0]["link"]
    vertices = detect_faces_uri(link)
    return (link, vertices) 

@app.route('/')
def hello():
    num = request.args.get('num', 1)
    q = request.args.get('q', 'cat')
    print(request.cookies)
    image_urls = pre_define(num)
    image_urls[5] = search(q)
    return render_template('ozinger.html',
            image_urls=image_urls,
            data = "",
            myimage="")

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)

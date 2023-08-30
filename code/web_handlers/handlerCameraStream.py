import io
import tornado.web
from PIL import Image, ImageDraw


class HandlerCameraStream(tornado.web.RequestHandler):
    def initialize(self, m_video):
        self.m_video = m_video

    def image_init(self):
        img = Image.new('RGB', (640, 480), color=(73, 109, 137))
        i = ImageDraw.Draw(img)
        text = "No recordings right now"
        i.text((10, 10), text, fill=(255, 255, 0))
        return img

    def image_from_videostream(self):
        o = self.m_video['video']
        o.seek(0)
        img = Image.open(o)
        return img

    @tornado.gen.coroutine
    def get(self):
        try:
            o = io.BytesIO()
            s = ''              # cleanup in asynch loop
            # _video = False
            if 'video' in self.m_video:
                img = self.image_from_videostream()
                # _video = True
            else:
                img = self.image_init()

            # get valid s before creating headers as we need the length
            img.save(o, format="JPEG")
            s = o.getvalue()
            self.set_header('Content-type', 'image/jpeg')
            self.set_header('Content-length', len(s))
            self.write(s)
        except Exception as e:
            print("handlerCameraStream:Error:" + str(e))
            pass
        # get end
        return

import cv2
import datetime
import time

from io import BytesIO
from PIL import Image


class Camera():
    def __init__(self, configuration, helper, m_modus, m_video):
        self.configuration = configuration
        self.helper = helper
        self.name = 'camera'
        self.m_modus = m_modus
        self.m_video = m_video

        self.byte_io = BytesIO()
        self.config = configuration.config
        self.config_camera = self.config['camera']
        self.current_modus = self.configuration.default_mode()
        self.config_output = self.configuration.output()
        self.default = self.config['default']
        self.now = self.helper.now_str()
        self.switched = True
        self.run()

    # todo double code in handlerCameraStream
    def capture_config(self, type):
        frame_height = self.config_camera['frame_height']
        frame_rate = self.config_output['frame_rate']
        frame_width = self.config_camera['frame_width']
        
        cap = cv2.VideoCapture(0)
        cap.set(3, frame_width)
        cap.set(4, frame_height)
        if cap.isOpened() == False:
            self.log('Unable to read camera feed')
            return [False, False]

        video_name = self.file_name_video(type)
        out = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), frame_rate, (frame_width, frame_height))
        return [cap, out]

    def file_name_image(self, type):
        fName = self.configuration.output_folder() + '/' + self.default['identify'] + '_' + self.config_output['file_name_' + type] + '_' \
                + self.now + self.config['preview']['file_extension']
        return fName

    def file_name_video(self, type):
        fName = self.configuration.output_folder() + '/' + self.default['identify'] + '_' + self.config_output['file_name_' + type] + '_' \
                + self.now + self.config_output['file_extension']
        return fName

    def log(self, text):
        self.helper.log_add_text(self.name, text)

    def queue_write(self, frame):
        imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        jpg = Image.fromarray(imgRGB)
        self.byte_io.seek(0)
        jpg.save(self.byte_io, 'JPEG')
        self.m_video['video'] = self.byte_io

    def text_detected(self):
        _text = self.config_camera['text']['motion_detected_true']
        _text = _text + ' ' + self.text_now()
        return _text

    def text_detected_false(self):
        _text = self.config_camera['text']['motion_detected_false']
        _text = _text + ' ' + self.text_now()
        return _text

    def text_now(self):
        _text_now = str(datetime.datetime.now().strftime(self.config['camera']['text']['format_time']))
        return _text_now
    
    def record_motion(self, duration=100):
        type_motion = 'motion'
        cap, out = self.capture_config(type_motion)

        if cap is False or out is False:
            self.log('failed to initialse camera')
            return

        detected = False
        firstFrame = None
        min_area = 500
        preview = True

        while duration >= 1:
            (grabbed, frame) = cap.read()
            text = "not detected"

            if not grabbed:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)

            if firstFrame is None:
                firstFrame = gray
                continue

            frameDelta = cv2.absdiff(firstFrame, gray)
            thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

            thresh = cv2.dilate(thresh, None, iterations=2)
            (_, contours, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            for c in contours:
                if cv2.contourArea(c) < min_area:
                    continue
                # detected
                (x, y, w, h) = cv2.boundingRect(c)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                text = self.text_detected()
                detected = True

            cv2.putText(frame, "Status: {}".format(text), (10, 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            '''
            not sure if still needed
            cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                        (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
            '''

            if detected:
                if preview:
                    _image_name = self.file_name_image(type_motion)
                    cv2.imwrite(_image_name, frame)
                    self.log('preview ' + _image_name)
                    preview = False
                out.write(frame)
                text = self.text_detected_false()

            duration -= 1
            # end detection loop

        # end detection
        cap.release()
        out.release()
        self.log('recorded detected motions')
        return

    def record_video(self, duration=100):
        type_record = 'record'
        cap, out = self.capture_config(type_record)

        if cap is False or out is False:
            self.log('failed to initialse camera')
            return

        recording = True

        ret, frame = cap.read()

        _image_name = self.file_name_image(type_record)
        cv2.imwrite(_image_name, frame)
        self.log('preview ' + _image_name)

        while recording:
            ret, frame = cap.read()
            if ret:
                self.queue_write(frame)
                out.write(frame)
            # Break the loop
            else:
                break
            duration -= 1
            if duration <= 1:
                recording = False

        # end recording
        cap.release()
        out.release()
        self.log('recorded video')
        return

    def show_video(self, duration=100):
        type_motion = 'motion'
        cap, out = self.capture_config(type_motion)

        if cap is False or out is False:
            self.log('failed to initialse camera')
            return

        detected = False
        firstFrame = None
        min_area = 500

        while duration >= 1:
            (grabbed, frame) = cap.read()
            text = "not detected"

            if not grabbed:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)

            if firstFrame is None:
                firstFrame = gray
                continue

            frameDelta = cv2.absdiff(firstFrame, gray)
            thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

            thresh = cv2.dilate(thresh, None, iterations=2)
            (_, contours, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            for c in contours:
                if cv2.contourArea(c) < min_area:
                    continue
                # detected
                (x, y, w, h) = cv2.boundingRect(c)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                text = self.text_detected()
                detected = True

            cv2.putText(frame, "Status: {}".format(text), (10, 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

            self.queue_write(frame)
            if detected:
                self.log('showed detected motions')
                text = self.text_detected_false()

            duration -= 1
            # end detection loop

        # end detection
        cap.release()
        out.release()
        self.log('showed video')
        return

    # -- main ----------------------------------------------------------------
    def run(self):
        self.log('camera started')

        new_modus = {}
        running = True

        while running:
            try:
                new_modus = self.helper.copy_modus(self.m_modus, new_modus)
                if type(new_modus) == dict:
                    if self.helper.is_different_modus(self.current_modus, new_modus):
                        self.log('new modus' + str(new_modus))
                        self.current_modus = new_modus
                        self.switched = True
                else:
                    self.log('bad modus' + str(new_modus))
            except Exception as e:
                # sometimes empty errors here
                pass

            # execute camera modes
            cm = self.current_modus['camera']
            if cm == self.config['camera']['mode']['record_interval']:
                now_old = self.helper.now()
                for i in range(self.config['camera']['interval']['repeat']):
                    now = self.helper.now()
                    delta = now - now_old
                    self.log('interval record ' + str(i))
                    while delta.total_seconds() < self.config['camera']['interval']['wait']:
                        now = self.helper.now()
                        delta = now - now_old
                    now_old = self.helper.now()
                    self.now = self.helper.now_str()
                    self.record_video(duration=self.config_output['file_length'])
                self.log('STOP INTERVAL')
                self.m_modus['camera'] = self.config['camera']['mode']['stop']
            if cm == self.config['camera']['mode']['record_video']:
                self.now = self.helper.now_str()
                self.record_video(duration=self.config_output['file_length'])
            if cm == self.config['camera']['mode']['record_motion']:
                self.now = self.helper.now_str()
                self.record_motion(duration=self.config_output['file_length'])
            if cm == self.config['camera']['mode']['show_video']:
                self.now = self.helper.now_str()
                self.show_video(duration=self.config_output['file_length'])
                
            # idle modes
            if cm == self.config['camera']['mode']['pause']:
                if self.switched:
                    self.log('camera paused')
                    self.switched = False
            if cm == self.config['camera']['mode']['stop']:
                if self.switched:
                    self.log('camera stopped')
                    self.switched = False

            # camera loop
            if not cm.startswith('record'):
                time.sleep(0.01)

        self.log('stopped running')

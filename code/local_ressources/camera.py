import cv2
import datetime
import time

from io import BytesIO
from PIL import Image


class Camera:
    def __init__(self, configuration, default_mode, helper, m_modus, m_video):
        self.configuration = configuration
        self.helper = helper
        self.name = 'camera'
        self.m_modus = m_modus
        self.m_video = m_video

        self.byte_io = BytesIO()
        self.config = configuration.config
        self.config_camera = self.config['camera']
        self.current_modus = default_mode
        self.default = self.config['DEFAULT']
        self.min_area = 500
        self.now = self.helper.now_str()
        self.switched = True

        _output = self.default['output']
        self.config_output = self.config[_output]

        self.run()

    def capture_config(self, type):
        frame_height = self.config_camera['frame_height']
        frame_rate = self.config_output['frame_rate']
        frame_width = self.config_camera['frame_width']

        _input = self.config_camera['input']
        if _input not in self.config['input']:
            self.log('input source for camera not in defaults')
            return [False, False]

        _input = self.config['input'][_input]
        self.log('using camera from input ' + str(_input))
        cap = cv2.VideoCapture(_input)
        cap.set(3, frame_width)
        cap.set(4, frame_height)
        if not cap.isOpened():
            self.log('Unable to read camera feed')
            return [False, False]

        if type == 'show_video':
            return [cap, 'none']

        video_name = self.file_name_video(type)
        out = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), frame_rate, (frame_width, frame_height))
        return [cap, out]

    def file_name_image(self, type):
        fName = self.configuration.output_folder() + '/' + self.default['identify'] + '_' + self.config_output['file_name_' + type] + '_' \
                + self.now + self.config['preview']['file_extension']
        return fName

    def file_name_video(self, type):
        f_name = self.configuration.output_folder() + '/' + self.default['identify'] + '_' + self.config_output['file_name_' + type] + '_' \
                + self.now + self.config_output['file_extension']
        return f_name

    def frame_draw_detections(self, frame, first_frame, gray):
        detected = False
        frame_delta = cv2.absdiff(first_frame, gray)
        text = self.text_detected_false()
        thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)

        contours = []
        try:
            (_, contours, _) = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        except Exception as e:
            self.log('frame_draw_detections exception ' + str(e))
            return frame, detected

        for c in contours:
            if cv2.contourArea(c) > self.min_area:
                (x, y, w, h) = cv2.boundingRect(c)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                text = self.text_detected()
                detected = True

        cv2.putText(frame, "Status: {}".format(text), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        return frame, detected

    def frame_grey(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        return gray

    def log(self, text):
        self.helper.log_add_text(self.name, text)

    def queue_video_write(self, frame):
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        jpg = Image.fromarray(img_rgb)
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
            self.log('failed to initialise camera')
            return

        first_frame = None
        preview = True

        while duration >= 1:
            (grabbed, frame) = cap.read()

            if not grabbed:
                self.log('failed to grab camera')
                break

            gray = self.frame_grey(frame)
            if first_frame is None:
                first_frame = gray
                continue
            frame, detected = self.frame_draw_detections(frame, first_frame, gray)

            if detected:
                if preview:
                    _image_name = self.file_name_image(type_motion)
                    cv2.imwrite(_image_name, frame)
                    self.log('preview ' + _image_name)
                    preview = False
                out.write(frame)
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
            self.log('failed to initialise camera')
            return

        recording = True
        ret, frame = cap.read()

        _image_name = self.file_name_image(type_record)
        cv2.imwrite(_image_name, frame)
        self.log('preview ' + _image_name)

        while recording:
            ret, frame = cap.read()
            if ret:
                self.queue_video_write(frame)
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
        cap, _none = self.capture_config('show_video')

        if cap is False:
            self.log('show_video: failed to initialise camera')
            return

        first_frame = None
        try:
            while duration >= 1:
                grabbed, orig_frame = cap.read()
                if not grabbed:
                    self.log('show_video: failed to grab camera')
                    break
                gray = self.frame_grey(orig_frame)
                if first_frame is None:
                    first_frame = gray
                    continue
                frame, detected = self.frame_draw_detections(orig_frame, first_frame, gray)
                if detected:
                    self.queue_video_write(frame)
                else:
                    self.queue_video_write(orig_frame)
                time.sleep(0.1)
                duration -= 1
                # end detection loop
            cap.release()
            self.log('showed video')
        except Exception as e:
            self.log('show_video exception ' + str(e))
        # end show_video
        return

    # -- main ----------------------------------------------------------------
    def run(self):
        self.log('camera started')

        new_modus = {}
        running = True

        while running:
            try:
                new_modus = self.helper.dict_copy(self.m_modus, new_modus)
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

            self.m_modus['actioncam'] = cm
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
            if not cm.startswith('record') or cm.startswith('record'):
                time.sleep(0.01)

        self.log('stopped running')

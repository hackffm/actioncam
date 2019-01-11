import tornado.web


class HandlerPreview(tornado.web.RequestHandler):
    def initialize(self, configuration, helper):
        self.configuration = configuration
        self.helper = helper

        self.config = configuration.config

    def get(self):
        items = self.preview_files()
        self.render("preview.html", title="Previews", items=items)

    def preview_files(self):
        output_folder = self.configuration.output_folder()
        prev_ext = self.config['preview']['file_extension']
        if output_folder != '':
            pattern = self.configuration.previewpattern()
            if pattern != '':
                files = self.helper.folder_files(output_folder, pattern)
                p_files = []
                for file in files:
                    _date = file.split('_')[2].replace(prev_ext,'')
                    pf = {"name": str(file.replace(prev_ext, '')),
                          "date": _date,
                          "filename": file }
                    p_files.append(pf)
                p_files = sorted(p_files, key=lambda k: k['date'])
                return p_files
            else:
                print('failed get search pattern')
        else:
            print('failed creating preview')

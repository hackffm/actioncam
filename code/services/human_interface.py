from utils import Menu


class HumanInterface:

    def __init__(self, utils_path):
        menu_config = utils_path + 'menu.json'
        self.menu = Menu('main')
        self.menu.load_from_file(menu_config)
        self.run()

    def message_to_human(self):
        _names, _selected = self.menu.submenu_selected()
        for text in _names:
            if text == _selected:
                print(text + ' <')
            else:
                print(str(text))

    def run(self):
        while True:
            try:
                _select = input('select direction:')
                if _select != '':
                    self.menu.submenu_select_direction(_select)
                    self.message_to_human()
            except EOFError:
                pass
            except Exception as e:
                print(e)

import json


class Menu:
    def __init__(self, name):
        self.name = name
        self.submenus = {}
        # index can be a vector, not sure how to do that in python
        self.selection = {'name': '', 'index': [0], 'value': ''}

    def submenu(self, name, content='', text='', value=''):
        if not name:
            return
        _submenu = {}
        _text = ''
        _value = ''
        if text:
            _text = text
        if value:
            _value = value
        _content = {}
        if content:
            _content = content
        else:
            _content[_text] = _value
        _submenu[name] = _content
        return _submenu

    def submenu_add(self, name='', content='', submenu=''):
        if submenu:
            for k, v in submenu.items():
                self.submenus[k] = v
        else:
            if not name:
                return
            self.submenus[name] = content

    def submenu_selected(self):
        _index = self.selection['index']
        _selected = ''
        _submenus = self.submenus

        _index_len = len(_index)
        _names = sorted(_submenus.keys())
        _namesT = _names[:]
        for select in _index:
            if _index_len <= 0:
                return
            if select > len(_names):
                return
            _selected = _names[select]
            _namesT = _names[:]
            if type(_submenus[_selected]) == dict:
                _index_len -= 1
                _names = sorted(_submenus[_selected])
                _submenus = _submenus[_selected]
        return [_namesT, _selected]

    def submenu_selection_value_by_index(self, index):
        _submenus = self.submenus
        _names = sorted(_submenus.keys())
        _selected = ''
        _index_len = len(index)
        _value = ''
        for select in index:
            if _index_len <= 0:
                return
            if select > len(_names):
                return
            _selected = _names[select]
            if type(_submenus[_selected]) == dict:
                _index_len -= 1
                _names = sorted(_submenus[_selected])
                _submenus = _submenus[_selected]
            else:
                _value = _submenus[_selected]
        self.selection['name'] = _selected
        self.selection['value'] = _value
        return

    def submenus_len(self, index):
        _submenus = self.submenus
        _names = sorted(_submenus.keys())
        _len = 0
        _index_len = len(index)
        for select in index:
            _len = len(_names)
            if select > (_len - 1):
                select = 0
            _selected = _names[select]
            if type(_submenus[_selected]) == dict:
                _index_len -= 1
                _names = sorted(_submenus[_selected])
                _submenus = _submenus[_selected]
            else:
                if _index_len <= 1:
                    return _len
                else:
                    return -1
        return _len

    def submenu_select_direction(self, direction):
        # this is a pointer !
        _index = self.selection['index']
        _i = len(_index) - 1
        _submenus_size = self.submenus_len(_index)
        # find new index for direction
        if 'down' == direction:
            _index[_i] = _index[_i] + 1
            if _index[_i] > _submenus_size - 1:
                _index[_i] = 0
        if 'up' == direction:
            if _index[_i] <= 0:
                _index[_i] = _submenus_size
            else:
                _index[_i] = _index[_i] - 1
        if 'right' == direction:
            # copy _index to safely investigate _index
            _indexT = _index[:]
            _indexT.append(0)
            _len = self.submenus_len(_indexT)
            if _len >= 1:
                _index.append(0)
        if 'left' == direction:
            if len(_index) > 1:
                _index.pop()
                _len = len(_index) - 1
                _index[_len] = 0
        # find name for new index
        self.submenu_selection_value_by_index(_index)
        return

    # ---helper--------------------------------------------------------
    def file_exists(self, file_name):
        try:
            _file = open(file_name)
            _file.close()
            return True
        except IOError:
            print('There was an error opening the file! ' + file_name)
        return False

    def load_from_file(self, config_name):
        if not self.file_exists(config_name):
            return
        with open(config_name) as json_data:
            config = json.load(json_data)
        if type(config) == dict:
            self.submenus = config
        print('loaded {} to submenus'.format(config_name))

    def save_to_file(self, config_name):
        _j = json.dumps(self.submenus, sort_keys=True, indent=4, ensure_ascii=False)
        with open(config_name, 'w') as outfile:
            outfile.write(_j)

    def selected_text(self):
        textfield = []
        _names, _selected = self.submenu_selected()
        for text in _names:
            if text == _selected:
                if self.selection['value'] != '':
                    textfield.append(text + ' <==')
                else:
                    textfield.append(text + ' ...>')
            else:
                textfield.append(str(text))
        return textfield

    def selected_show(self):
        _textlines = self.selected_text()

        for line in _textlines:
            print(line)

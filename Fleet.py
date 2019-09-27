class Fleet:

    def __init__(self, game_handle=None, item_list=[]):
        self.game_handle = game_handle
        self.items = item_list

    def update(self):
        for item in self.items:
            item.update()

    def append(self, item):
        self.items.append(item)

    def show(self):
        for item in self.items:
            item.show()

    def remove(self, item):
        self.items.remove(item)
        # del item

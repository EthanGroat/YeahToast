
class Fleet:

    def __init__(self, item_list=[]):
        self.items = item_list

    def update(self):
        for item in self.items:
            item.update()

    def add(self, item):
        self.items.append(item)

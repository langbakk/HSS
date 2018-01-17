init -1 python:
    import renpy.store as store
    import renpy.exports as renpy # we need this so Ren'Py properly handles rollback with classes
    from operator import attrgetter # we need this for sorting items

    class Item(store.object):
        def __init__(self, name, weight,amount=1):
            self.name = name
            self.weight = weight
            self.amount = amount

    class InvItem(store.object):
        def __init__(self, item, amount):
            self.item = item
            self.name = item.name
            self.amount = amount

    class Container(store.object):
        def __init__(self, weight_max=100):
            self.inventory = []
            self.weight_max = weight_max

        def __iter__(self):
            return iter(self.inventory)

        def finditem(self, item):
            return(self.inventory[[i.item for i in self.inventory].index(item)])
            
        def add_item(self, item, amount=1): #remember to use the item-assignment, not anything else, to add to inventory
            if item.weight * amount > self.weight_max - sum(i.item.weight * i.amount for i in self.inventory):
                renpy.notify(item.name.capitalize+' exceeds max weight you can carry')
            else:
                if self.has_item(item):
                    self.finditem(item).amount += amount
                else:
                    self.inventory.append(InvItem(item, amount))
                name = item.name.lower().replace('fs','').replace('fm','').replace('_',' ').title()
                renpy.notify(name+' added successfully')

        def has_item(self, item, a=1): #remember to use the Item-assignment, not a string to check for items
            if item in [i.item for i in self.inventory]:
                if self.finditem(item).amount >= a:
                    return(self.finditem(item).amount)
                else:
                    return(False)
            else:
                return(False)

        def remove_item(self,item, amount=1): #remember to use the Item-assignment, not a string, to remove items
            if self.has_item(item):
                self.finditem(item).amount -= amount
                if self.finditem(item).amount <= 0:
                    inventory.pop(inventory.index(self.finditem(item)))
                    renpy.notify(item.name.capitalize()+" has been deleted")
                else:
                    renpy.notify("There are "+str(self.finditem(item).amount)+" "+str(item.name)+" left")
            else:
                renpy.notify("Couldn't find the item you were trying to delete")

init -1 python:
    def updateInventory():
        for file in renpy.list_files():
            if file.startswith('images/inventory/') and file.endswith('.png'):
                if 'hover' in file:
                    name = file.replace('images/inventory/','').replace('_idle','').replace('_hover','').replace('.png','')
                    if not hasattr( store, ""+name+"_item" ):
                        setattr(store,""+name+"_item",Item(name,5))
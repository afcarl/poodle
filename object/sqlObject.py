from poodle.poodle import *

class Database(Object):
    tables = Relation("Table")

class Table(Object):
    columns = Relation("Column")
    hasFKlink = Relation("Table")
    hasJoin = Relation("Table")
    is_selected = Bool()

class Column(Object):
    rows = Relation("Row")
    seenAt = StateFact()

class Request(Object):
    atColumn = Property("Column")

class Select(Object):
    columns_available = Relation("Column")
    completed = Bool()
    
class Condition(Object):
    applied = Bool()
    lhs_column = Property("Column")
    
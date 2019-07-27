from poodle.poodle import *

class Database:
    tables = Relation("Table")

class Table:
    columns = Relation("Column")
    hasFKlink = Relation("Table")
    hasJoin = Relation("Table")

class Column:
    rows = Relation("Row")
    seenAt = StateFact()

class Request
    atColumn = Property("Column")


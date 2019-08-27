from poodle import *
from object.sqlObject import *

class SQLActionModelA:
    
    @planned
    def joinColumns(self,
        table1 : Table,
        table2 : Table):
            
        assert table1.hasFKlink == table2
        
        table1.hasJoin = table2

    @planned
    def StartToCollectCollumns(self,
        request1 : Request,
        column1 : Column):

        assert request1.atColumn == column1
        
        column1.seenAt = True

    @planned
    def MoveToColumnInTheSameTable(self,
        request1 : Request,
        column1 : Column,
        column2 : Column,
        table1 : Table):

        assert request1.atColumn == column1 and \
        column1 in table1.columns and \
        column2 in table1.columns
        
        request1.atColumn = column2

    @planned
    def MarkSeenAtColumn(self,
        request1 : Request,
        column1 : Column):
        
        assert request1.atColumn == column1
        
        column1.seenAt = True

    @planned
    def MoveToNextTable(self,
        request1 : Request,
        column1 : Column,
        table1 : Table,
        column2 : Column,
        table2 : Table):
        
        assert request1.atColumn == column1 and \
        column1 in table1.columns and \
        table1.hasJoin == table2 and \
        column2 in table2.columns
        
        request1.atColumn = column2
        

'''class SQLActionModelB:
    # def __init__(self, *args, **kwargs):
        # super().__init__(*args, **kwargs)
        
    @planned
    def selectFromTable(self,
            target_column: Column,
            table: Table,
            select: Select
        ):
        "Only select from table that has target column"
        
        assert \
            target_column in table.columns
        
        table.is_selected = True    
        
        return f"SELECT {table}.{target_column} FROM {table}"
    
    @planned 
    def joinColumns (self,
            table1: Table,
            table2: Table,
            column_right: Column,
            column_left: Column,
            select: Select
        ):
        "Chain-join matching tables"

        assert \
            column_right in column_left.contains_elements_from and \
            column_left in table1.columns and \
            column_right in table2.columns and \
            table1.is_selected == True
        
        select.columns_available.add(column_right)
        select.columns_available.add(column_left)
        table2.is_selected = True
        
        return f"JOIN {table2}.{column_right} ON ({table1}.{column_left} = {table2}.{column_right})"

    @planned
    def applyLikeConditions(self
            select: Select
        ):
        "Finally, apply the conditions when all columns are selected"
        
        for condition in self.conditions:
            assert condition.lhs_column in select.columns_available
        
        where.started = True
        
        return "WHERE "+' '.join(self.conditions)
   '''
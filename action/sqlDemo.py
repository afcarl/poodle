from poodle.poodle import *

class StrObject(Object):
    def __str__(self):
        return str(self.value)

class Table(StrObject):
    columns = Relation("Column")
    is_selected = Bool(False)

class Column(StrObject):
    contains_elements_from = Relation("Column")

class Select(StrObject):
    columns_available = Relation("Column")
    started = Bool(False)
    completed = Bool(False)
    
class Condition(StrObject):
    applied = Bool(False)
    
class SimpleLikeCondition(Condition):
    lhs_column = Property("Column")

class SQLActionModel(Problem):
        
    @planned # plannedOnce? #chained?
    def selectFromTable(self,
            target_column: Column,
            table: Table,
            select: Select
        ):
        "Only select from table that has target column"
        
        assert \
            target_column in table.columns and \
            select.started == False
        
        table.is_selected = True
        select.started = True
        
        return f"SELECT {table}.{target_column} FROM {table}"
    
    @planned 
    def joinTables(self,
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
        
        table2.is_selected = True
        
        return f"JOIN {table2}.{column_right} ON ({table1}.{column_left} = {table2}.{column_right})"
    
    @planned
    def addAvailableColumnsWhenNeeded(self,
            col: Column,
            tbl: Table
            # select: Select # TODO
        ):
        
        assert tbl.is_selected and col in tbl.columns
        
        # select.columns_available.add(col) # TODO
        self.select.columns_available.add(col)

    @planned
    def applyLikeConditions(self,
            select: Select
        ):
        "Finally, apply the conditions when all columns are selected"
        
        s_cond = ""
        
        for condition in self.conditions:
            assert condition.lhs_column in select.columns_available
            s_cond += str(condition) + " "
        
        select.completed = True
        
        return f"WHERE {s_cond}"

class SQLDemoTest(SQLActionModel):
    
    def problem(self):
        self.table1 = self.addObject(Table("tbl1")) 
        self.table2 = self.addObject(Table("tbl2")) 
        self.table3 = self.addObject(Table("tbl3")) 
        self.table4 = self.addObject(Table("tbl4")) 

        self.column1 = self.addObject(Column("col1"))
        self.column2 = self.addObject(Column("col2"))
        self.column3 = self.addObject(Column("col3"))
        self.column4 = self.addObject(Column("col4"))
        self.column5 = self.addObject(Column("col5"))
        self.column6 = self.addObject(Column("col6"))
        self.column7 = self.addObject(Column("col7"))
        self.column8 = self.addObject(Column("col8"))
        self.column9 = self.addObject(Column("col9"))
        self.column10 = self.addObject(Column("col10"))
        self.column11 = self.addObject(Column("col12"))
        self.column12 = self.addObject(Column("col13"))
        self.column13 = self.addObject(Column("col14"))
        self.column14 = self.addObject(Column("col15"))
        self.column15 = self.addObject(Column("col16"))
        self.column16 = self.addObject(Column("col17"))
        
        self.table1.columns.add(self.column1)
        self.table1.columns.add(self.column2)
        self.table1.columns.add(self.column3)
        self.table1.columns.add(self.column4)
        
        self.table2.columns.add(self.column5)
        self.table2.columns.add(self.column6)
        self.table2.columns.add(self.column7)
        self.table2.columns.add(self.column8)
        
        self.table3.columns.add(self.column9)
        self.table3.columns.add(self.column10)
        self.table3.columns.add(self.column11)
        self.table3.columns.add(self.column12)
        
        self.table4.columns.add(self.column13)
        self.table4.columns.add(self.column14)
        self.table4.columns.add(self.column15)
        self.table4.columns.add(self.column16)
        
        self.column3.contains_elements_from.add(self.column7)
        self.column7.contains_elements_from.add(self.column3)
        
        self.column8.contains_elements_from.add(self.column10)
        self.column10.contains_elements_from.add(self.column8)
        
        self.column9.contains_elements_from.add(self.column16)
        self.column16.contains_elements_from.add(self.column9)
        
        self.select = self.addObject(Select())
        
        self.condition1 = self.addObject(SimpleLikeCondition("column4 LIKE 'Hello'"))
        self.condition1.lhs_column = self.column4
        self.condition2 = self.addObject(SimpleLikeCondition("column11 LIKE 'world'"))
        self.condition2.lhs_column = self.column11
        self.conditions = [self.condition1, self.condition2]
        # self.conditions = [self.condition1]
    
    def goal(self):
        assert self.select.completed == True
    
    def solution(self):
        return [
            self.selectFromTable,
            self.joinTables,
            self.joinTables,
            self.addAvailableColumnsWhenNeeded,
            self.addAvailableColumnsWhenNeeded,
            self.addAvailableColumnsWhenNeeded,
            self.applyLikeConditions
        ]
        
   
p = SQLDemoTest()
# p.check_solution(50)
p.run()
for a in p.plan: print(a)
print(' '.join(getattr(p, x.methodName)(**x.kwargs) for x in p.plan))

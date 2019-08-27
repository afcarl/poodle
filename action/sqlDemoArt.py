from poodle import *



class Database(Object):
    tables = Relation("Table")

class Table(Object):
    columns = Relation("Column")
    hasFKlink = Relation("Table")
    hasJoin = Relation("Table")
    is_selected = StateFact()

class Column(Object):
    seenAt = StateFact()

class Request(Object):
    atColumn = Property("Column")
    


class SQLActionModel(Problem):
        
    @planned
    def JoinTables(self,
        table1 : Table,
        table2 : Table):
            
        assert table1.hasFKlink == table2
        
        table1.hasJoin.add(table2)

    @planned
    def Tech_StartToCollectCollumnsA(self,
        request1 : Request,
        column1 : Column):

        request1.atColumn = column1

    @planned
    def Tech_MoveToColumnInTheSameTable(self,
        request1 : Request,
        column1 : Column,
        column2 : Column,
        table1 : Table):

        assert request1.atColumn == column1 and \
        column1 in table1.columns and \
        column2 in table1.columns
        
        request1.atColumn = column2

    @planned
    def SelectColumn(self,
        request1 : Request,
        column1 : Column):
        
        assert request1.atColumn == column1
        
        column1.seenAt = True

    @planned
    def Tech_MoveToJoinedTable(self,
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

class SQLDemoTest(SQLActionModel):
    
    def problem(self):
        
        self.database1 = self.addObject(Database())
        
        self.table1 = self.addObject(Table()) 
        self.table2 = self.addObject(Table()) 
        self.table3 = self.addObject(Table()) 
        self.table4 = self.addObject(Table()) 

        self.column1 = self.addObject(Column())
        self.column2 = self.addObject(Column())
        self.column3 = self.addObject(Column())
        self.column4 = self.addObject(Column())
        self.column5 = self.addObject(Column())
        self.column6 = self.addObject(Column())
        self.column7 = self.addObject(Column())
        self.column8 = self.addObject(Column())
        self.column9 = self.addObject(Column())
        self.column10 = self.addObject(Column())
        self.column11 = self.addObject(Column())
        self.column12 = self.addObject(Column())
        self.column13 = self.addObject(Column())
        self.column14 = self.addObject(Column())
        self.column15 = self.addObject(Column())
        self.column16 = self.addObject(Column())
        
        self.database1.tables.add(self.table1)
        self.database1.tables.add(self.table2)
        self.database1.tables.add(self.table3)
        self.database1.tables.add(self.table4)
        
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
        
        self.request1 = self.addObject(Request())
        self.request1.atColumn = self.column10
        
        self.table1.hasFKlink.add(self.table2)
        self.table2.hasFKlink.add(self.table3)
        self.table3.hasFKlink.add(self.table4)
        self.table2.hasFKlink.add(self.table1)
        self.table3.hasFKlink.add(self.table2)
        self.table4.hasFKlink.add(self.table3)
    def goal(self):
        # return self.request1.atColumn == self.column10
        return  self.column10.seenAt == True  and \
                self.column2.seenAt == True and \
                self.column5.seenAt == True
                
                
    # def solution(self):
    #     return [
    #         self.selectFromTable,
    #         self.joinTables,
    #         self.joinTables,
    #         self.addAvailableColumnsWhenNeeded,
    #         self.addAvailableColumnsWhenNeeded,
    #         self.applyLikeConditions
    #     ]
        
   
p = SQLDemoTest()
p.run()
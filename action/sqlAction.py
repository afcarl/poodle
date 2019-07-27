class SQLActionModel:
    @planned
    def joinColumns(self,
        table1 : DbTable,
        table2 : DbTable):
            
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
        table2 : Table)
        
        assert request1.atColumn == column1 and \
        column1 in table1.columns and \ 
        table1.hasJoin == table2 and \ 
        column2 in table2.columns
        
        request1.atColumn = column2
        

    
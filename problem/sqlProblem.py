from poodle.poodle import *
from object.sqlObject import *
import action.sqlAction

"""
SELECT DISTINCT ADMISSIONS.subject_id FROM mimiciii.ADMISSIONS JOIN mimiciii.microbiologyevents  ON (microbiologyevents.subject_id = mimiciii.ADMISSIONS.subject_id) JOIN mimiciii.D_ITEMS ON (mimiciii.D_ITEMS.ITEMID = microbiologyevents.AB_ITEMID AND mimiciii.D_ITEMS.LINKSTO = 'microbiologyevents' AND D_ITEMS.dbsource != 'carevue' AND D_ITEMS.category != 'Alarms')  WHERE  D_ITEMS.LABEL ILIKE '%CEFAZOLIN%' AND  microbiologyevents.interpretation ILIKE '%S%' AND '1' ;


SELECT count(DISTINCT ADMISSIONS.hadm_id) FROM ADMISSIONS JOIN DIAGNOSES_ICD c ON (c.HADM_ID = ADMISSIONS.HADM_ID) JOIN D_ICD_DIAGNOSES ON (D_ICD_DIAGNOSES.ICD9_CODE = c.ICD9_CODE) JOIN procedureevents_mv b ON (b.HADM_ID = ADMISSIONS.HADM_ID) JOIN D_ITEMS ON (D_ITEMS.ITEMID = b.ITEMID AND D_ITEMS.LINKSTO = 'procedureevents_mv')  WHERE CAST((julianday('now')-julianday(ADMISSIONS.ADMITTIME)) as Integer) BETWEEN 1 AND 360 AND D_ITEMS.LABEL like '%intubation%' AND 1 ;


SELECT count(DISTINCT ADMISSIONS.hadm_id) FROM ADMISSIONS JOIN DIAGNOSES_ICD c ON (c.HADM_ID = ADMISSIONS.HADM_ID) JOIN D_ICD_DIAGNOSES ON (D_ICD_DIAGNOSES.ICD9_CODE = c.ICD9_CODE) JOIN chartevents b ON (b.HADM_ID = ADMISSIONS.HADM_ID) JOIN D_ITEMS ON (D_ITEMS.ITEMID = b.ITEMID AND D_ITEMS.LINKSTO = 'chartevents')  WHERE CAST((julianday('now')-julianday(ADMISSIONS.ADMITTIME)) as Integer) BETWEEN 1 AND 10 AND b.VALUENUM > 9 AND  D_ITEMS.LABEL like '%hemoglobin%' AND 1 ;
"""

class TestSQLProblem(Problem, action.sqlAction.SQLActionModel):

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
        
    def goal(self):
        return  self.column10.seenAt = True and \
                self.column2.seenAt = True and \
                self.column5.seenAt = True
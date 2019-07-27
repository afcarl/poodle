from poodle import *
from object.commonObject import *

class KubeBase(Problem):
    def prepareNumbers(self):

        self.AddedNumber0_0 = self.addObject(AddedNumber()) 
        self.AddedNumber0_0.operator1 =  self.numberFactory.getNumber(0) 
        self.AddedNumber0_0.operator2 =  self.numberFactory.getNumber(0) 
        self.AddedNumber0_0.result =  self.numberFactory.getNumber(0)

        self.AddedNumber0_1 = self.addObject(AddedNumber()) 
        self.AddedNumber0_1.operator1 =  self.numberFactory.getNumber(0) 
        self.AddedNumber0_1.operator2 =  self.numberFactory.getNumber(1) 
        self.AddedNumber0_1.result =  self.numberFactory.getNumber(1)

        self.AddedNumber0_2 = self.addObject(AddedNumber()) 
        self.AddedNumber0_2.operator1 =  self.numberFactory.getNumber(0) 
        self.AddedNumber0_2.operator2 =  self.numberFactory.getNumber(2) 
        self.AddedNumber0_2.result =  self.numberFactory.getNumber(2)

        self.AddedNumber0_3 = self.addObject(AddedNumber()) 
        self.AddedNumber0_3.operator1 =  self.numberFactory.getNumber(0) 
        self.AddedNumber0_3.operator2 =  self.numberFactory.getNumber(3) 
        self.AddedNumber0_3.result =  self.numberFactory.getNumber(3)

        self.AddedNumber0_4 = self.addObject(AddedNumber()) 
        self.AddedNumber0_4.operator1 =  self.numberFactory.getNumber(0) 
        self.AddedNumber0_4.operator2 =  self.numberFactory.getNumber(4) 
        self.AddedNumber0_4.result =  self.numberFactory.getNumber(4)

        self.AddedNumber0_5 = self.addObject(AddedNumber()) 
        self.AddedNumber0_5.operator1 =  self.numberFactory.getNumber(0) 
        self.AddedNumber0_5.operator2 =  self.numberFactory.getNumber(5) 
        self.AddedNumber0_5.result =  self.numberFactory.getNumber(5)

        self.AddedNumber0_6 = self.addObject(AddedNumber()) 
        self.AddedNumber0_6.operator1 =  self.numberFactory.getNumber(0) 
        self.AddedNumber0_6.operator2 =  self.numberFactory.getNumber(6) 
        self.AddedNumber0_6.result =  self.numberFactory.getNumber(6)

        self.AddedNumber0_7 = self.addObject(AddedNumber()) 
        self.AddedNumber0_7.operator1 =  self.numberFactory.getNumber(0) 
        self.AddedNumber0_7.operator2 =  self.numberFactory.getNumber(7) 
        self.AddedNumber0_7.result =  self.numberFactory.getNumber(7)

        self.AddedNumber0_8 = self.addObject(AddedNumber()) 
        self.AddedNumber0_8.operator1 =  self.numberFactory.getNumber(0) 
        self.AddedNumber0_8.operator2 =  self.numberFactory.getNumber(8) 
        self.AddedNumber0_8.result =  self.numberFactory.getNumber(8)

        self.AddedNumber0_9 = self.addObject(AddedNumber()) 
        self.AddedNumber0_9.operator1 =  self.numberFactory.getNumber(0) 
        self.AddedNumber0_9.operator2 =  self.numberFactory.getNumber(9) 
        self.AddedNumber0_9.result =  self.numberFactory.getNumber(9)

        self.AddedNumber0_10 = self.addObject(AddedNumber()) 
        self.AddedNumber0_10.operator1 =  self.numberFactory.getNumber(0) 
        self.AddedNumber0_10.operator2 =  self.numberFactory.getNumber(10) 
        self.AddedNumber0_10.result =  self.numberFactory.getNumber(10)

        self.AddedNumber1_0 = self.addObject(AddedNumber()) 
        self.AddedNumber1_0.operator1 =  self.numberFactory.getNumber(1) 
        self.AddedNumber1_0.operator2 =  self.numberFactory.getNumber(0) 
        self.AddedNumber1_0.result =  self.numberFactory.getNumber(1)

        self.AddedNumber1_1 = self.addObject(AddedNumber()) 
        self.AddedNumber1_1.operator1 =  self.numberFactory.getNumber(1) 
        self.AddedNumber1_1.operator2 =  self.numberFactory.getNumber(1) 
        self.AddedNumber1_1.result =  self.numberFactory.getNumber(2)

        self.AddedNumber1_2 = self.addObject(AddedNumber()) 
        self.AddedNumber1_2.operator1 =  self.numberFactory.getNumber(1) 
        self.AddedNumber1_2.operator2 =  self.numberFactory.getNumber(2) 
        self.AddedNumber1_2.result =  self.numberFactory.getNumber(3)

        self.AddedNumber1_3 = self.addObject(AddedNumber()) 
        self.AddedNumber1_3.operator1 =  self.numberFactory.getNumber(1) 
        self.AddedNumber1_3.operator2 =  self.numberFactory.getNumber(3) 
        self.AddedNumber1_3.result =  self.numberFactory.getNumber(4)

        self.AddedNumber1_4 = self.addObject(AddedNumber()) 
        self.AddedNumber1_4.operator1 =  self.numberFactory.getNumber(1) 
        self.AddedNumber1_4.operator2 =  self.numberFactory.getNumber(4) 
        self.AddedNumber1_4.result =  self.numberFactory.getNumber(5)

        self.AddedNumber1_5 = self.addObject(AddedNumber()) 
        self.AddedNumber1_5.operator1 =  self.numberFactory.getNumber(1) 
        self.AddedNumber1_5.operator2 =  self.numberFactory.getNumber(5) 
        self.AddedNumber1_5.result =  self.numberFactory.getNumber(6)

        self.AddedNumber1_6 = self.addObject(AddedNumber()) 
        self.AddedNumber1_6.operator1 =  self.numberFactory.getNumber(1) 
        self.AddedNumber1_6.operator2 =  self.numberFactory.getNumber(6) 
        self.AddedNumber1_6.result =  self.numberFactory.getNumber(7)

        self.AddedNumber1_7 = self.addObject(AddedNumber()) 
        self.AddedNumber1_7.operator1 =  self.numberFactory.getNumber(1) 
        self.AddedNumber1_7.operator2 =  self.numberFactory.getNumber(7) 
        self.AddedNumber1_7.result =  self.numberFactory.getNumber(8)

        self.AddedNumber1_8 = self.addObject(AddedNumber()) 
        self.AddedNumber1_8.operator1 =  self.numberFactory.getNumber(1) 
        self.AddedNumber1_8.operator2 =  self.numberFactory.getNumber(8) 
        self.AddedNumber1_8.result =  self.numberFactory.getNumber(9)

        self.AddedNumber1_9 = self.addObject(AddedNumber()) 
        self.AddedNumber1_9.operator1 =  self.numberFactory.getNumber(1) 
        self.AddedNumber1_9.operator2 =  self.numberFactory.getNumber(9) 
        self.AddedNumber1_9.result =  self.numberFactory.getNumber(10)

        self.AddedNumber1_10 = self.addObject(AddedNumber()) 
        self.AddedNumber1_10.operator1 =  self.numberFactory.getNumber(1) 
        self.AddedNumber1_10.operator2 =  self.numberFactory.getNumber(10) 
        self.AddedNumber1_10.result =  self.numberFactory.getNumber(11)

        self.AddedNumber2_0 = self.addObject(AddedNumber()) 
        self.AddedNumber2_0.operator1 =  self.numberFactory.getNumber(2) 
        self.AddedNumber2_0.operator2 =  self.numberFactory.getNumber(0) 
        self.AddedNumber2_0.result =  self.numberFactory.getNumber(2)

        self.AddedNumber2_1 = self.addObject(AddedNumber()) 
        self.AddedNumber2_1.operator1 =  self.numberFactory.getNumber(2) 
        self.AddedNumber2_1.operator2 =  self.numberFactory.getNumber(1) 
        self.AddedNumber2_1.result =  self.numberFactory.getNumber(3)

        self.AddedNumber2_2 = self.addObject(AddedNumber()) 
        self.AddedNumber2_2.operator1 =  self.numberFactory.getNumber(2) 
        self.AddedNumber2_2.operator2 =  self.numberFactory.getNumber(2) 
        self.AddedNumber2_2.result =  self.numberFactory.getNumber(4)

        self.AddedNumber2_3 = self.addObject(AddedNumber()) 
        self.AddedNumber2_3.operator1 =  self.numberFactory.getNumber(2) 
        self.AddedNumber2_3.operator2 =  self.numberFactory.getNumber(3) 
        self.AddedNumber2_3.result =  self.numberFactory.getNumber(5)

        self.AddedNumber2_4 = self.addObject(AddedNumber()) 
        self.AddedNumber2_4.operator1 =  self.numberFactory.getNumber(2) 
        self.AddedNumber2_4.operator2 =  self.numberFactory.getNumber(4) 
        self.AddedNumber2_4.result =  self.numberFactory.getNumber(6)

        self.AddedNumber2_5 = self.addObject(AddedNumber()) 
        self.AddedNumber2_5.operator1 =  self.numberFactory.getNumber(2) 
        self.AddedNumber2_5.operator2 =  self.numberFactory.getNumber(5) 
        self.AddedNumber2_5.result =  self.numberFactory.getNumber(7)

        self.AddedNumber2_6 = self.addObject(AddedNumber()) 
        self.AddedNumber2_6.operator1 =  self.numberFactory.getNumber(2) 
        self.AddedNumber2_6.operator2 =  self.numberFactory.getNumber(6) 
        self.AddedNumber2_6.result =  self.numberFactory.getNumber(8)

        self.AddedNumber2_7 = self.addObject(AddedNumber()) 
        self.AddedNumber2_7.operator1 =  self.numberFactory.getNumber(2) 
        self.AddedNumber2_7.operator2 =  self.numberFactory.getNumber(7) 
        self.AddedNumber2_7.result =  self.numberFactory.getNumber(9)

        self.AddedNumber2_8 = self.addObject(AddedNumber()) 
        self.AddedNumber2_8.operator1 =  self.numberFactory.getNumber(2) 
        self.AddedNumber2_8.operator2 =  self.numberFactory.getNumber(8) 
        self.AddedNumber2_8.result =  self.numberFactory.getNumber(10)

        self.AddedNumber2_9 = self.addObject(AddedNumber()) 
        self.AddedNumber2_9.operator1 =  self.numberFactory.getNumber(2) 
        self.AddedNumber2_9.operator2 =  self.numberFactory.getNumber(9) 
        self.AddedNumber2_9.result =  self.numberFactory.getNumber(11)

        self.AddedNumber2_10 = self.addObject(AddedNumber()) 
        self.AddedNumber2_10.operator1 =  self.numberFactory.getNumber(2) 
        self.AddedNumber2_10.operator2 =  self.numberFactory.getNumber(10) 
        self.AddedNumber2_10.result =  self.numberFactory.getNumber(12)

        self.AddedNumber3_0 = self.addObject(AddedNumber()) 
        self.AddedNumber3_0.operator1 =  self.numberFactory.getNumber(3) 
        self.AddedNumber3_0.operator2 =  self.numberFactory.getNumber(0) 
        self.AddedNumber3_0.result =  self.numberFactory.getNumber(3)

        self.AddedNumber3_1 = self.addObject(AddedNumber()) 
        self.AddedNumber3_1.operator1 =  self.numberFactory.getNumber(3) 
        self.AddedNumber3_1.operator2 =  self.numberFactory.getNumber(1) 
        self.AddedNumber3_1.result =  self.numberFactory.getNumber(4)

        self.AddedNumber3_2 = self.addObject(AddedNumber()) 
        self.AddedNumber3_2.operator1 =  self.numberFactory.getNumber(3) 
        self.AddedNumber3_2.operator2 =  self.numberFactory.getNumber(2) 
        self.AddedNumber3_2.result =  self.numberFactory.getNumber(5)

        self.AddedNumber3_3 = self.addObject(AddedNumber()) 
        self.AddedNumber3_3.operator1 =  self.numberFactory.getNumber(3) 
        self.AddedNumber3_3.operator2 =  self.numberFactory.getNumber(3) 
        self.AddedNumber3_3.result =  self.numberFactory.getNumber(6)

        self.AddedNumber3_4 = self.addObject(AddedNumber()) 
        self.AddedNumber3_4.operator1 =  self.numberFactory.getNumber(3) 
        self.AddedNumber3_4.operator2 =  self.numberFactory.getNumber(4) 
        self.AddedNumber3_4.result =  self.numberFactory.getNumber(7)

        self.AddedNumber3_5 = self.addObject(AddedNumber()) 
        self.AddedNumber3_5.operator1 =  self.numberFactory.getNumber(3) 
        self.AddedNumber3_5.operator2 =  self.numberFactory.getNumber(5) 
        self.AddedNumber3_5.result =  self.numberFactory.getNumber(8)

        self.AddedNumber3_6 = self.addObject(AddedNumber()) 
        self.AddedNumber3_6.operator1 =  self.numberFactory.getNumber(3) 
        self.AddedNumber3_6.operator2 =  self.numberFactory.getNumber(6) 
        self.AddedNumber3_6.result =  self.numberFactory.getNumber(9)

        self.AddedNumber3_7 = self.addObject(AddedNumber()) 
        self.AddedNumber3_7.operator1 =  self.numberFactory.getNumber(3) 
        self.AddedNumber3_7.operator2 =  self.numberFactory.getNumber(7) 
        self.AddedNumber3_7.result =  self.numberFactory.getNumber(10)

        self.AddedNumber3_8 = self.addObject(AddedNumber()) 
        self.AddedNumber3_8.operator1 =  self.numberFactory.getNumber(3) 
        self.AddedNumber3_8.operator2 =  self.numberFactory.getNumber(8) 
        self.AddedNumber3_8.result =  self.numberFactory.getNumber(11)

        self.AddedNumber3_9 = self.addObject(AddedNumber()) 
        self.AddedNumber3_9.operator1 =  self.numberFactory.getNumber(3) 
        self.AddedNumber3_9.operator2 =  self.numberFactory.getNumber(9) 
        self.AddedNumber3_9.result =  self.numberFactory.getNumber(12)

        self.AddedNumber3_10 = self.addObject(AddedNumber()) 
        self.AddedNumber3_10.operator1 =  self.numberFactory.getNumber(3) 
        self.AddedNumber3_10.operator2 =  self.numberFactory.getNumber(10) 
        self.AddedNumber3_10.result =  self.numberFactory.getNumber(13)

        self.AddedNumber4_0 = self.addObject(AddedNumber()) 
        self.AddedNumber4_0.operator1 =  self.numberFactory.getNumber(4) 
        self.AddedNumber4_0.operator2 =  self.numberFactory.getNumber(0) 
        self.AddedNumber4_0.result =  self.numberFactory.getNumber(4)

        self.AddedNumber4_1 = self.addObject(AddedNumber()) 
        self.AddedNumber4_1.operator1 =  self.numberFactory.getNumber(4) 
        self.AddedNumber4_1.operator2 =  self.numberFactory.getNumber(1) 
        self.AddedNumber4_1.result =  self.numberFactory.getNumber(5)

        self.AddedNumber4_2 = self.addObject(AddedNumber()) 
        self.AddedNumber4_2.operator1 =  self.numberFactory.getNumber(4) 
        self.AddedNumber4_2.operator2 =  self.numberFactory.getNumber(2) 
        self.AddedNumber4_2.result =  self.numberFactory.getNumber(6)

        self.AddedNumber4_3 = self.addObject(AddedNumber()) 
        self.AddedNumber4_3.operator1 =  self.numberFactory.getNumber(4) 
        self.AddedNumber4_3.operator2 =  self.numberFactory.getNumber(3) 
        self.AddedNumber4_3.result =  self.numberFactory.getNumber(7)

        self.AddedNumber4_4 = self.addObject(AddedNumber()) 
        self.AddedNumber4_4.operator1 =  self.numberFactory.getNumber(4) 
        self.AddedNumber4_4.operator2 =  self.numberFactory.getNumber(4) 
        self.AddedNumber4_4.result =  self.numberFactory.getNumber(8)

        self.AddedNumber4_5 = self.addObject(AddedNumber()) 
        self.AddedNumber4_5.operator1 =  self.numberFactory.getNumber(4) 
        self.AddedNumber4_5.operator2 =  self.numberFactory.getNumber(5) 
        self.AddedNumber4_5.result =  self.numberFactory.getNumber(9)

        self.AddedNumber4_6 = self.addObject(AddedNumber()) 
        self.AddedNumber4_6.operator1 =  self.numberFactory.getNumber(4) 
        self.AddedNumber4_6.operator2 =  self.numberFactory.getNumber(6) 
        self.AddedNumber4_6.result =  self.numberFactory.getNumber(10)

        self.AddedNumber4_7 = self.addObject(AddedNumber()) 
        self.AddedNumber4_7.operator1 =  self.numberFactory.getNumber(4) 
        self.AddedNumber4_7.operator2 =  self.numberFactory.getNumber(7) 
        self.AddedNumber4_7.result =  self.numberFactory.getNumber(11)

        self.AddedNumber4_8 = self.addObject(AddedNumber()) 
        self.AddedNumber4_8.operator1 =  self.numberFactory.getNumber(4) 
        self.AddedNumber4_8.operator2 =  self.numberFactory.getNumber(8) 
        self.AddedNumber4_8.result =  self.numberFactory.getNumber(12)

        self.AddedNumber4_9 = self.addObject(AddedNumber()) 
        self.AddedNumber4_9.operator1 =  self.numberFactory.getNumber(4) 
        self.AddedNumber4_9.operator2 =  self.numberFactory.getNumber(9) 
        self.AddedNumber4_9.result =  self.numberFactory.getNumber(13)

        self.AddedNumber4_10 = self.addObject(AddedNumber()) 
        self.AddedNumber4_10.operator1 =  self.numberFactory.getNumber(4) 
        self.AddedNumber4_10.operator2 =  self.numberFactory.getNumber(10) 
        self.AddedNumber4_10.result =  self.numberFactory.getNumber(14)

        self.AddedNumber5_0 = self.addObject(AddedNumber()) 
        self.AddedNumber5_0.operator1 =  self.numberFactory.getNumber(5) 
        self.AddedNumber5_0.operator2 =  self.numberFactory.getNumber(0) 
        self.AddedNumber5_0.result =  self.numberFactory.getNumber(5)

        self.AddedNumber5_1 = self.addObject(AddedNumber()) 
        self.AddedNumber5_1.operator1 =  self.numberFactory.getNumber(5) 
        self.AddedNumber5_1.operator2 =  self.numberFactory.getNumber(1) 
        self.AddedNumber5_1.result =  self.numberFactory.getNumber(6)

        self.AddedNumber5_2 = self.addObject(AddedNumber()) 
        self.AddedNumber5_2.operator1 =  self.numberFactory.getNumber(5) 
        self.AddedNumber5_2.operator2 =  self.numberFactory.getNumber(2) 
        self.AddedNumber5_2.result =  self.numberFactory.getNumber(7)

        self.AddedNumber5_3 = self.addObject(AddedNumber()) 
        self.AddedNumber5_3.operator1 =  self.numberFactory.getNumber(5) 
        self.AddedNumber5_3.operator2 =  self.numberFactory.getNumber(3) 
        self.AddedNumber5_3.result =  self.numberFactory.getNumber(8)

        self.AddedNumber5_4 = self.addObject(AddedNumber()) 
        self.AddedNumber5_4.operator1 =  self.numberFactory.getNumber(5) 
        self.AddedNumber5_4.operator2 =  self.numberFactory.getNumber(4) 
        self.AddedNumber5_4.result =  self.numberFactory.getNumber(9)

        self.AddedNumber5_5 = self.addObject(AddedNumber()) 
        self.AddedNumber5_5.operator1 =  self.numberFactory.getNumber(5) 
        self.AddedNumber5_5.operator2 =  self.numberFactory.getNumber(5) 
        self.AddedNumber5_5.result =  self.numberFactory.getNumber(10)

        self.AddedNumber5_6 = self.addObject(AddedNumber()) 
        self.AddedNumber5_6.operator1 =  self.numberFactory.getNumber(5) 
        self.AddedNumber5_6.operator2 =  self.numberFactory.getNumber(6) 
        self.AddedNumber5_6.result =  self.numberFactory.getNumber(11)

        self.AddedNumber5_7 = self.addObject(AddedNumber()) 
        self.AddedNumber5_7.operator1 =  self.numberFactory.getNumber(5) 
        self.AddedNumber5_7.operator2 =  self.numberFactory.getNumber(7) 
        self.AddedNumber5_7.result =  self.numberFactory.getNumber(12)

        self.AddedNumber5_8 = self.addObject(AddedNumber()) 
        self.AddedNumber5_8.operator1 =  self.numberFactory.getNumber(5) 
        self.AddedNumber5_8.operator2 =  self.numberFactory.getNumber(8) 
        self.AddedNumber5_8.result =  self.numberFactory.getNumber(13)

        self.AddedNumber5_9 = self.addObject(AddedNumber()) 
        self.AddedNumber5_9.operator1 =  self.numberFactory.getNumber(5) 
        self.AddedNumber5_9.operator2 =  self.numberFactory.getNumber(9) 
        self.AddedNumber5_9.result =  self.numberFactory.getNumber(14)

        self.AddedNumber5_10 = self.addObject(AddedNumber()) 
        self.AddedNumber5_10.operator1 =  self.numberFactory.getNumber(5) 
        self.AddedNumber5_10.operator2 =  self.numberFactory.getNumber(10) 
        self.AddedNumber5_10.result =  self.numberFactory.getNumber(15)

        self.AddedNumber6_0 = self.addObject(AddedNumber()) 
        self.AddedNumber6_0.operator1 =  self.numberFactory.getNumber(6) 
        self.AddedNumber6_0.operator2 =  self.numberFactory.getNumber(0) 
        self.AddedNumber6_0.result =  self.numberFactory.getNumber(6)

        self.AddedNumber6_1 = self.addObject(AddedNumber()) 
        self.AddedNumber6_1.operator1 =  self.numberFactory.getNumber(6) 
        self.AddedNumber6_1.operator2 =  self.numberFactory.getNumber(1) 
        self.AddedNumber6_1.result =  self.numberFactory.getNumber(7)

        self.AddedNumber6_2 = self.addObject(AddedNumber()) 
        self.AddedNumber6_2.operator1 =  self.numberFactory.getNumber(6) 
        self.AddedNumber6_2.operator2 =  self.numberFactory.getNumber(2) 
        self.AddedNumber6_2.result =  self.numberFactory.getNumber(8)

        self.AddedNumber6_3 = self.addObject(AddedNumber()) 
        self.AddedNumber6_3.operator1 =  self.numberFactory.getNumber(6) 
        self.AddedNumber6_3.operator2 =  self.numberFactory.getNumber(3) 
        self.AddedNumber6_3.result =  self.numberFactory.getNumber(9)

        self.AddedNumber6_4 = self.addObject(AddedNumber()) 
        self.AddedNumber6_4.operator1 =  self.numberFactory.getNumber(6) 
        self.AddedNumber6_4.operator2 =  self.numberFactory.getNumber(4) 
        self.AddedNumber6_4.result =  self.numberFactory.getNumber(10)

        self.AddedNumber6_5 = self.addObject(AddedNumber()) 
        self.AddedNumber6_5.operator1 =  self.numberFactory.getNumber(6) 
        self.AddedNumber6_5.operator2 =  self.numberFactory.getNumber(5) 
        self.AddedNumber6_5.result =  self.numberFactory.getNumber(11)

        self.AddedNumber6_6 = self.addObject(AddedNumber()) 
        self.AddedNumber6_6.operator1 =  self.numberFactory.getNumber(6) 
        self.AddedNumber6_6.operator2 =  self.numberFactory.getNumber(6) 
        self.AddedNumber6_6.result =  self.numberFactory.getNumber(12)

        self.AddedNumber6_7 = self.addObject(AddedNumber()) 
        self.AddedNumber6_7.operator1 =  self.numberFactory.getNumber(6) 
        self.AddedNumber6_7.operator2 =  self.numberFactory.getNumber(7) 
        self.AddedNumber6_7.result =  self.numberFactory.getNumber(13)

        self.AddedNumber6_8 = self.addObject(AddedNumber()) 
        self.AddedNumber6_8.operator1 =  self.numberFactory.getNumber(6) 
        self.AddedNumber6_8.operator2 =  self.numberFactory.getNumber(8) 
        self.AddedNumber6_8.result =  self.numberFactory.getNumber(14)

        self.AddedNumber6_9 = self.addObject(AddedNumber()) 
        self.AddedNumber6_9.operator1 =  self.numberFactory.getNumber(6) 
        self.AddedNumber6_9.operator2 =  self.numberFactory.getNumber(9) 
        self.AddedNumber6_9.result =  self.numberFactory.getNumber(15)

        self.AddedNumber6_10 = self.addObject(AddedNumber()) 
        self.AddedNumber6_10.operator1 =  self.numberFactory.getNumber(6) 
        self.AddedNumber6_10.operator2 =  self.numberFactory.getNumber(10) 
        self.AddedNumber6_10.result =  self.numberFactory.getNumber(16)

        self.AddedNumber7_0 = self.addObject(AddedNumber()) 
        self.AddedNumber7_0.operator1 =  self.numberFactory.getNumber(7) 
        self.AddedNumber7_0.operator2 =  self.numberFactory.getNumber(0) 
        self.AddedNumber7_0.result =  self.numberFactory.getNumber(7)

        self.AddedNumber7_1 = self.addObject(AddedNumber()) 
        self.AddedNumber7_1.operator1 =  self.numberFactory.getNumber(7) 
        self.AddedNumber7_1.operator2 =  self.numberFactory.getNumber(1) 
        self.AddedNumber7_1.result =  self.numberFactory.getNumber(8)

        self.AddedNumber7_2 = self.addObject(AddedNumber()) 
        self.AddedNumber7_2.operator1 =  self.numberFactory.getNumber(7) 
        self.AddedNumber7_2.operator2 =  self.numberFactory.getNumber(2) 
        self.AddedNumber7_2.result =  self.numberFactory.getNumber(9)

        self.AddedNumber7_3 = self.addObject(AddedNumber()) 
        self.AddedNumber7_3.operator1 =  self.numberFactory.getNumber(7) 
        self.AddedNumber7_3.operator2 =  self.numberFactory.getNumber(3) 
        self.AddedNumber7_3.result =  self.numberFactory.getNumber(10)

        self.AddedNumber7_4 = self.addObject(AddedNumber()) 
        self.AddedNumber7_4.operator1 =  self.numberFactory.getNumber(7) 
        self.AddedNumber7_4.operator2 =  self.numberFactory.getNumber(4) 
        self.AddedNumber7_4.result =  self.numberFactory.getNumber(11)

        self.AddedNumber7_5 = self.addObject(AddedNumber()) 
        self.AddedNumber7_5.operator1 =  self.numberFactory.getNumber(7) 
        self.AddedNumber7_5.operator2 =  self.numberFactory.getNumber(5) 
        self.AddedNumber7_5.result =  self.numberFactory.getNumber(12)

        self.AddedNumber7_6 = self.addObject(AddedNumber()) 
        self.AddedNumber7_6.operator1 =  self.numberFactory.getNumber(7) 
        self.AddedNumber7_6.operator2 =  self.numberFactory.getNumber(6) 
        self.AddedNumber7_6.result =  self.numberFactory.getNumber(13)

        self.AddedNumber7_7 = self.addObject(AddedNumber()) 
        self.AddedNumber7_7.operator1 =  self.numberFactory.getNumber(7) 
        self.AddedNumber7_7.operator2 =  self.numberFactory.getNumber(7) 
        self.AddedNumber7_7.result =  self.numberFactory.getNumber(14)

        self.AddedNumber7_8 = self.addObject(AddedNumber()) 
        self.AddedNumber7_8.operator1 =  self.numberFactory.getNumber(7) 
        self.AddedNumber7_8.operator2 =  self.numberFactory.getNumber(8) 
        self.AddedNumber7_8.result =  self.numberFactory.getNumber(15)

        self.AddedNumber7_9 = self.addObject(AddedNumber()) 
        self.AddedNumber7_9.operator1 =  self.numberFactory.getNumber(7) 
        self.AddedNumber7_9.operator2 =  self.numberFactory.getNumber(9) 
        self.AddedNumber7_9.result =  self.numberFactory.getNumber(16)

        self.AddedNumber7_10 = self.addObject(AddedNumber()) 
        self.AddedNumber7_10.operator1 =  self.numberFactory.getNumber(7) 
        self.AddedNumber7_10.operator2 =  self.numberFactory.getNumber(10) 
        self.AddedNumber7_10.result =  self.numberFactory.getNumber(17)

        self.AddedNumber8_0 = self.addObject(AddedNumber()) 
        self.AddedNumber8_0.operator1 =  self.numberFactory.getNumber(8) 
        self.AddedNumber8_0.operator2 =  self.numberFactory.getNumber(0) 
        self.AddedNumber8_0.result =  self.numberFactory.getNumber(8)

        self.AddedNumber8_1 = self.addObject(AddedNumber()) 
        self.AddedNumber8_1.operator1 =  self.numberFactory.getNumber(8) 
        self.AddedNumber8_1.operator2 =  self.numberFactory.getNumber(1) 
        self.AddedNumber8_1.result =  self.numberFactory.getNumber(9)

        self.AddedNumber8_2 = self.addObject(AddedNumber()) 
        self.AddedNumber8_2.operator1 =  self.numberFactory.getNumber(8) 
        self.AddedNumber8_2.operator2 =  self.numberFactory.getNumber(2) 
        self.AddedNumber8_2.result =  self.numberFactory.getNumber(10)

        self.AddedNumber8_3 = self.addObject(AddedNumber()) 
        self.AddedNumber8_3.operator1 =  self.numberFactory.getNumber(8) 
        self.AddedNumber8_3.operator2 =  self.numberFactory.getNumber(3) 
        self.AddedNumber8_3.result =  self.numberFactory.getNumber(11)

        self.AddedNumber8_4 = self.addObject(AddedNumber()) 
        self.AddedNumber8_4.operator1 =  self.numberFactory.getNumber(8) 
        self.AddedNumber8_4.operator2 =  self.numberFactory.getNumber(4) 
        self.AddedNumber8_4.result =  self.numberFactory.getNumber(12)

        self.AddedNumber8_5 = self.addObject(AddedNumber()) 
        self.AddedNumber8_5.operator1 =  self.numberFactory.getNumber(8) 
        self.AddedNumber8_5.operator2 =  self.numberFactory.getNumber(5) 
        self.AddedNumber8_5.result =  self.numberFactory.getNumber(13)

        self.AddedNumber8_6 = self.addObject(AddedNumber()) 
        self.AddedNumber8_6.operator1 =  self.numberFactory.getNumber(8) 
        self.AddedNumber8_6.operator2 =  self.numberFactory.getNumber(6) 
        self.AddedNumber8_6.result =  self.numberFactory.getNumber(14)

        self.AddedNumber8_7 = self.addObject(AddedNumber()) 
        self.AddedNumber8_7.operator1 =  self.numberFactory.getNumber(8) 
        self.AddedNumber8_7.operator2 =  self.numberFactory.getNumber(7) 
        self.AddedNumber8_7.result =  self.numberFactory.getNumber(15)

        self.AddedNumber8_8 = self.addObject(AddedNumber()) 
        self.AddedNumber8_8.operator1 =  self.numberFactory.getNumber(8) 
        self.AddedNumber8_8.operator2 =  self.numberFactory.getNumber(8) 
        self.AddedNumber8_8.result =  self.numberFactory.getNumber(16)

        self.AddedNumber8_9 = self.addObject(AddedNumber()) 
        self.AddedNumber8_9.operator1 =  self.numberFactory.getNumber(8) 
        self.AddedNumber8_9.operator2 =  self.numberFactory.getNumber(9) 
        self.AddedNumber8_9.result =  self.numberFactory.getNumber(17)

        self.AddedNumber8_10 = self.addObject(AddedNumber()) 
        self.AddedNumber8_10.operator1 =  self.numberFactory.getNumber(8) 
        self.AddedNumber8_10.operator2 =  self.numberFactory.getNumber(10) 
        self.AddedNumber8_10.result =  self.numberFactory.getNumber(18)

        self.AddedNumber9_0 = self.addObject(AddedNumber()) 
        self.AddedNumber9_0.operator1 =  self.numberFactory.getNumber(9) 
        self.AddedNumber9_0.operator2 =  self.numberFactory.getNumber(0) 
        self.AddedNumber9_0.result =  self.numberFactory.getNumber(9)

        self.AddedNumber9_1 = self.addObject(AddedNumber()) 
        self.AddedNumber9_1.operator1 =  self.numberFactory.getNumber(9) 
        self.AddedNumber9_1.operator2 =  self.numberFactory.getNumber(1) 
        self.AddedNumber9_1.result =  self.numberFactory.getNumber(10)

        self.AddedNumber9_2 = self.addObject(AddedNumber()) 
        self.AddedNumber9_2.operator1 =  self.numberFactory.getNumber(9) 
        self.AddedNumber9_2.operator2 =  self.numberFactory.getNumber(2) 
        self.AddedNumber9_2.result =  self.numberFactory.getNumber(11)

        self.AddedNumber9_3 = self.addObject(AddedNumber()) 
        self.AddedNumber9_3.operator1 =  self.numberFactory.getNumber(9) 
        self.AddedNumber9_3.operator2 =  self.numberFactory.getNumber(3) 
        self.AddedNumber9_3.result =  self.numberFactory.getNumber(12)

        self.AddedNumber9_4 = self.addObject(AddedNumber()) 
        self.AddedNumber9_4.operator1 =  self.numberFactory.getNumber(9) 
        self.AddedNumber9_4.operator2 =  self.numberFactory.getNumber(4) 
        self.AddedNumber9_4.result =  self.numberFactory.getNumber(13)

        self.AddedNumber9_5 = self.addObject(AddedNumber()) 
        self.AddedNumber9_5.operator1 =  self.numberFactory.getNumber(9) 
        self.AddedNumber9_5.operator2 =  self.numberFactory.getNumber(5) 
        self.AddedNumber9_5.result =  self.numberFactory.getNumber(14)

        self.AddedNumber9_6 = self.addObject(AddedNumber()) 
        self.AddedNumber9_6.operator1 =  self.numberFactory.getNumber(9) 
        self.AddedNumber9_6.operator2 =  self.numberFactory.getNumber(6) 
        self.AddedNumber9_6.result =  self.numberFactory.getNumber(15)

        self.AddedNumber9_7 = self.addObject(AddedNumber()) 
        self.AddedNumber9_7.operator1 =  self.numberFactory.getNumber(9) 
        self.AddedNumber9_7.operator2 =  self.numberFactory.getNumber(7) 
        self.AddedNumber9_7.result =  self.numberFactory.getNumber(16)

        self.AddedNumber9_8 = self.addObject(AddedNumber()) 
        self.AddedNumber9_8.operator1 =  self.numberFactory.getNumber(9) 
        self.AddedNumber9_8.operator2 =  self.numberFactory.getNumber(8) 
        self.AddedNumber9_8.result =  self.numberFactory.getNumber(17)

        self.AddedNumber9_9 = self.addObject(AddedNumber()) 
        self.AddedNumber9_9.operator1 =  self.numberFactory.getNumber(9) 
        self.AddedNumber9_9.operator2 =  self.numberFactory.getNumber(9) 
        self.AddedNumber9_9.result =  self.numberFactory.getNumber(18)

        self.AddedNumber9_10 = self.addObject(AddedNumber()) 
        self.AddedNumber9_10.operator1 =  self.numberFactory.getNumber(9) 
        self.AddedNumber9_10.operator2 =  self.numberFactory.getNumber(10) 
        self.AddedNumber9_10.result =  self.numberFactory.getNumber(19)

        self.AddedNumber10_0 = self.addObject(AddedNumber()) 
        self.AddedNumber10_0.operator1 =  self.numberFactory.getNumber(10) 
        self.AddedNumber10_0.operator2 =  self.numberFactory.getNumber(0) 
        self.AddedNumber10_0.result =  self.numberFactory.getNumber(10)

        self.AddedNumber10_1 = self.addObject(AddedNumber()) 
        self.AddedNumber10_1.operator1 =  self.numberFactory.getNumber(10) 
        self.AddedNumber10_1.operator2 =  self.numberFactory.getNumber(1) 
        self.AddedNumber10_1.result =  self.numberFactory.getNumber(11)

        self.AddedNumber10_2 = self.addObject(AddedNumber()) 
        self.AddedNumber10_2.operator1 =  self.numberFactory.getNumber(10) 
        self.AddedNumber10_2.operator2 =  self.numberFactory.getNumber(2) 
        self.AddedNumber10_2.result =  self.numberFactory.getNumber(12)

        self.AddedNumber10_3 = self.addObject(AddedNumber()) 
        self.AddedNumber10_3.operator1 =  self.numberFactory.getNumber(10) 
        self.AddedNumber10_3.operator2 =  self.numberFactory.getNumber(3) 
        self.AddedNumber10_3.result =  self.numberFactory.getNumber(13)

        self.AddedNumber10_4 = self.addObject(AddedNumber()) 
        self.AddedNumber10_4.operator1 =  self.numberFactory.getNumber(10) 
        self.AddedNumber10_4.operator2 =  self.numberFactory.getNumber(4) 
        self.AddedNumber10_4.result =  self.numberFactory.getNumber(14)

        self.AddedNumber10_5 = self.addObject(AddedNumber()) 
        self.AddedNumber10_5.operator1 =  self.numberFactory.getNumber(10) 
        self.AddedNumber10_5.operator2 =  self.numberFactory.getNumber(5) 
        self.AddedNumber10_5.result =  self.numberFactory.getNumber(15)

        self.AddedNumber10_6 = self.addObject(AddedNumber()) 
        self.AddedNumber10_6.operator1 =  self.numberFactory.getNumber(10) 
        self.AddedNumber10_6.operator2 =  self.numberFactory.getNumber(6) 
        self.AddedNumber10_6.result =  self.numberFactory.getNumber(16)

        self.AddedNumber10_7 = self.addObject(AddedNumber()) 
        self.AddedNumber10_7.operator1 =  self.numberFactory.getNumber(10) 
        self.AddedNumber10_7.operator2 =  self.numberFactory.getNumber(7) 
        self.AddedNumber10_7.result =  self.numberFactory.getNumber(17)

        self.AddedNumber10_8 = self.addObject(AddedNumber()) 
        self.AddedNumber10_8.operator1 =  self.numberFactory.getNumber(10) 
        self.AddedNumber10_8.operator2 =  self.numberFactory.getNumber(8) 
        self.AddedNumber10_8.result =  self.numberFactory.getNumber(18)

        self.AddedNumber10_9 = self.addObject(AddedNumber()) 
        self.AddedNumber10_9.operator1 =  self.numberFactory.getNumber(10) 
        self.AddedNumber10_9.operator2 =  self.numberFactory.getNumber(9) 
        self.AddedNumber10_9.result =  self.numberFactory.getNumber(19)

        self.AddedNumber10_10 = self.addObject(AddedNumber()) 
        self.AddedNumber10_10.operator1 =  self.numberFactory.getNumber(10) 
        self.AddedNumber10_10.operator2 =  self.numberFactory.getNumber(10) 
        self.AddedNumber10_10.result =  self.numberFactory.getNumber(20)
									

																					

        self.greaterThan1_0 = self.addObject(GreaterThan()) 
        self.greaterThan1_0.lower =  self.numberFactory.getNumber(0) 
        self.greaterThan1_0.higher =  self.numberFactory.getNumber(1)
																					

        self.greaterThan2_0 = self.addObject(GreaterThan()) 
        self.greaterThan2_0.lower =  self.numberFactory.getNumber(0) 
        self.greaterThan2_0.higher =  self.numberFactory.getNumber(2)
	
        self.greaterThan2_1 = self.addObject(GreaterThan()) 
        self.greaterThan2_1.lower =  self.numberFactory.getNumber(1) 
        self.greaterThan2_1.higher =  self.numberFactory.getNumber(2)
																				

        self.greaterThan3_0 = self.addObject(GreaterThan()) 
        self.greaterThan3_0.lower =  self.numberFactory.getNumber(0) 
        self.greaterThan3_0.higher =  self.numberFactory.getNumber(3)
	
        self.greaterThan3_1 = self.addObject(GreaterThan()) 
        self.greaterThan3_1.lower =  self.numberFactory.getNumber(1) 
        self.greaterThan3_1.higher =  self.numberFactory.getNumber(3)
	
        self.greaterThan3_2 = self.addObject(GreaterThan()) 
        self.greaterThan3_2.lower =  self.numberFactory.getNumber(2) 
        self.greaterThan3_2.higher =  self.numberFactory.getNumber(3)
																			

        self.greaterThan4_0 = self.addObject(GreaterThan()) 
        self.greaterThan4_0.lower =  self.numberFactory.getNumber(0) 
        self.greaterThan4_0.higher =  self.numberFactory.getNumber(4)
	
        self.greaterThan4_1 = self.addObject(GreaterThan()) 
        self.greaterThan4_1.lower =  self.numberFactory.getNumber(1) 
        self.greaterThan4_1.higher =  self.numberFactory.getNumber(4)
	
        self.greaterThan4_2 = self.addObject(GreaterThan()) 
        self.greaterThan4_2.lower =  self.numberFactory.getNumber(2) 
        self.greaterThan4_2.higher =  self.numberFactory.getNumber(4)
	
        self.greaterThan4_3 = self.addObject(GreaterThan()) 
        self.greaterThan4_3.lower =  self.numberFactory.getNumber(3) 
        self.greaterThan4_3.higher =  self.numberFactory.getNumber(4)
																		

        self.greaterThan5_0 = self.addObject(GreaterThan()) 
        self.greaterThan5_0.lower =  self.numberFactory.getNumber(0) 
        self.greaterThan5_0.higher =  self.numberFactory.getNumber(5)
	
        self.greaterThan5_1 = self.addObject(GreaterThan()) 
        self.greaterThan5_1.lower =  self.numberFactory.getNumber(1) 
        self.greaterThan5_1.higher =  self.numberFactory.getNumber(5)
	
        self.greaterThan5_2 = self.addObject(GreaterThan()) 
        self.greaterThan5_2.lower =  self.numberFactory.getNumber(2) 
        self.greaterThan5_2.higher =  self.numberFactory.getNumber(5)
	
        self.greaterThan5_3 = self.addObject(GreaterThan()) 
        self.greaterThan5_3.lower =  self.numberFactory.getNumber(3) 
        self.greaterThan5_3.higher =  self.numberFactory.getNumber(5)
	
        self.greaterThan5_4 = self.addObject(GreaterThan()) 
        self.greaterThan5_4.lower =  self.numberFactory.getNumber(4) 
        self.greaterThan5_4.higher =  self.numberFactory.getNumber(5)
																	

        self.greaterThan6_0 = self.addObject(GreaterThan()) 
        self.greaterThan6_0.lower =  self.numberFactory.getNumber(0) 
        self.greaterThan6_0.higher =  self.numberFactory.getNumber(6)
	
        self.greaterThan6_1 = self.addObject(GreaterThan()) 
        self.greaterThan6_1.lower =  self.numberFactory.getNumber(1) 
        self.greaterThan6_1.higher =  self.numberFactory.getNumber(6)
	
        self.greaterThan6_2 = self.addObject(GreaterThan()) 
        self.greaterThan6_2.lower =  self.numberFactory.getNumber(2) 
        self.greaterThan6_2.higher =  self.numberFactory.getNumber(6)
	
        self.greaterThan6_3 = self.addObject(GreaterThan()) 
        self.greaterThan6_3.lower =  self.numberFactory.getNumber(3) 
        self.greaterThan6_3.higher =  self.numberFactory.getNumber(6)
	
        self.greaterThan6_4 = self.addObject(GreaterThan()) 
        self.greaterThan6_4.lower =  self.numberFactory.getNumber(4) 
        self.greaterThan6_4.higher =  self.numberFactory.getNumber(6)
	
        self.greaterThan6_5 = self.addObject(GreaterThan()) 
        self.greaterThan6_5.lower =  self.numberFactory.getNumber(5) 
        self.greaterThan6_5.higher =  self.numberFactory.getNumber(6)
																

        self.greaterThan7_0 = self.addObject(GreaterThan()) 
        self.greaterThan7_0.lower =  self.numberFactory.getNumber(0) 
        self.greaterThan7_0.higher =  self.numberFactory.getNumber(7)
	
        self.greaterThan7_1 = self.addObject(GreaterThan()) 
        self.greaterThan7_1.lower =  self.numberFactory.getNumber(1) 
        self.greaterThan7_1.higher =  self.numberFactory.getNumber(7)
	
        self.greaterThan7_2 = self.addObject(GreaterThan()) 
        self.greaterThan7_2.lower =  self.numberFactory.getNumber(2) 
        self.greaterThan7_2.higher =  self.numberFactory.getNumber(7)
	
        self.greaterThan7_3 = self.addObject(GreaterThan()) 
        self.greaterThan7_3.lower =  self.numberFactory.getNumber(3) 
        self.greaterThan7_3.higher =  self.numberFactory.getNumber(7)
	
        self.greaterThan7_4 = self.addObject(GreaterThan()) 
        self.greaterThan7_4.lower =  self.numberFactory.getNumber(4) 
        self.greaterThan7_4.higher =  self.numberFactory.getNumber(7)
	
        self.greaterThan7_5 = self.addObject(GreaterThan()) 
        self.greaterThan7_5.lower =  self.numberFactory.getNumber(5) 
        self.greaterThan7_5.higher =  self.numberFactory.getNumber(7)
	
        self.greaterThan7_6 = self.addObject(GreaterThan()) 
        self.greaterThan7_6.lower =  self.numberFactory.getNumber(6) 
        self.greaterThan7_6.higher =  self.numberFactory.getNumber(7)
															

        self.greaterThan8_0 = self.addObject(GreaterThan()) 
        self.greaterThan8_0.lower =  self.numberFactory.getNumber(0) 
        self.greaterThan8_0.higher =  self.numberFactory.getNumber(8)
	
        self.greaterThan8_1 = self.addObject(GreaterThan()) 
        self.greaterThan8_1.lower =  self.numberFactory.getNumber(1) 
        self.greaterThan8_1.higher =  self.numberFactory.getNumber(8)
	
        self.greaterThan8_2 = self.addObject(GreaterThan()) 
        self.greaterThan8_2.lower =  self.numberFactory.getNumber(2) 
        self.greaterThan8_2.higher =  self.numberFactory.getNumber(8)
	
        self.greaterThan8_3 = self.addObject(GreaterThan()) 
        self.greaterThan8_3.lower =  self.numberFactory.getNumber(3) 
        self.greaterThan8_3.higher =  self.numberFactory.getNumber(8)
	
        self.greaterThan8_4 = self.addObject(GreaterThan()) 
        self.greaterThan8_4.lower =  self.numberFactory.getNumber(4) 
        self.greaterThan8_4.higher =  self.numberFactory.getNumber(8)
	
        self.greaterThan8_5 = self.addObject(GreaterThan()) 
        self.greaterThan8_5.lower =  self.numberFactory.getNumber(5) 
        self.greaterThan8_5.higher =  self.numberFactory.getNumber(8)
	
        self.greaterThan8_6 = self.addObject(GreaterThan()) 
        self.greaterThan8_6.lower =  self.numberFactory.getNumber(6) 
        self.greaterThan8_6.higher =  self.numberFactory.getNumber(8)
	
        self.greaterThan8_7 = self.addObject(GreaterThan()) 
        self.greaterThan8_7.lower =  self.numberFactory.getNumber(7) 
        self.greaterThan8_7.higher =  self.numberFactory.getNumber(8)
														

        self.greaterThan9_0 = self.addObject(GreaterThan()) 
        self.greaterThan9_0.lower =  self.numberFactory.getNumber(0) 
        self.greaterThan9_0.higher =  self.numberFactory.getNumber(9)
	
        self.greaterThan9_1 = self.addObject(GreaterThan()) 
        self.greaterThan9_1.lower =  self.numberFactory.getNumber(1) 
        self.greaterThan9_1.higher =  self.numberFactory.getNumber(9)
	
        self.greaterThan9_2 = self.addObject(GreaterThan()) 
        self.greaterThan9_2.lower =  self.numberFactory.getNumber(2) 
        self.greaterThan9_2.higher =  self.numberFactory.getNumber(9)
	
        self.greaterThan9_3 = self.addObject(GreaterThan()) 
        self.greaterThan9_3.lower =  self.numberFactory.getNumber(3) 
        self.greaterThan9_3.higher =  self.numberFactory.getNumber(9)
	
        self.greaterThan9_4 = self.addObject(GreaterThan()) 
        self.greaterThan9_4.lower =  self.numberFactory.getNumber(4) 
        self.greaterThan9_4.higher =  self.numberFactory.getNumber(9)
	
        self.greaterThan9_5 = self.addObject(GreaterThan()) 
        self.greaterThan9_5.lower =  self.numberFactory.getNumber(5) 
        self.greaterThan9_5.higher =  self.numberFactory.getNumber(9)
	
        self.greaterThan9_6 = self.addObject(GreaterThan()) 
        self.greaterThan9_6.lower =  self.numberFactory.getNumber(6) 
        self.greaterThan9_6.higher =  self.numberFactory.getNumber(9)
	
        self.greaterThan9_7 = self.addObject(GreaterThan()) 
        self.greaterThan9_7.lower =  self.numberFactory.getNumber(7) 
        self.greaterThan9_7.higher =  self.numberFactory.getNumber(9)
	
        self.greaterThan9_8 = self.addObject(GreaterThan()) 
        self.greaterThan9_8.lower =  self.numberFactory.getNumber(8) 
        self.greaterThan9_8.higher =  self.numberFactory.getNumber(9)
													

        self.greaterThan10_0 = self.addObject(GreaterThan()) 
        self.greaterThan10_0.lower =  self.numberFactory.getNumber(0) 
        self.greaterThan10_0.higher =  self.numberFactory.getNumber(10)
	
        self.greaterThan10_1 = self.addObject(GreaterThan()) 
        self.greaterThan10_1.lower =  self.numberFactory.getNumber(1) 
        self.greaterThan10_1.higher =  self.numberFactory.getNumber(10)
	
        self.greaterThan10_2 = self.addObject(GreaterThan()) 
        self.greaterThan10_2.lower =  self.numberFactory.getNumber(2) 
        self.greaterThan10_2.higher =  self.numberFactory.getNumber(10)
	
        self.greaterThan10_3 = self.addObject(GreaterThan()) 
        self.greaterThan10_3.lower =  self.numberFactory.getNumber(3) 
        self.greaterThan10_3.higher =  self.numberFactory.getNumber(10)
	
        self.greaterThan10_4 = self.addObject(GreaterThan()) 
        self.greaterThan10_4.lower =  self.numberFactory.getNumber(4) 
        self.greaterThan10_4.higher =  self.numberFactory.getNumber(10)
	
        self.greaterThan10_5 = self.addObject(GreaterThan()) 
        self.greaterThan10_5.lower =  self.numberFactory.getNumber(5) 
        self.greaterThan10_5.higher =  self.numberFactory.getNumber(10)
	
        self.greaterThan10_6 = self.addObject(GreaterThan()) 
        self.greaterThan10_6.lower =  self.numberFactory.getNumber(6) 
        self.greaterThan10_6.higher =  self.numberFactory.getNumber(10)
	
        self.greaterThan10_7 = self.addObject(GreaterThan()) 
        self.greaterThan10_7.lower =  self.numberFactory.getNumber(7) 
        self.greaterThan10_7.higher =  self.numberFactory.getNumber(10)
	
        self.greaterThan10_8 = self.addObject(GreaterThan()) 
        self.greaterThan10_8.lower =  self.numberFactory.getNumber(8) 
        self.greaterThan10_8.higher =  self.numberFactory.getNumber(10)
	
        self.greaterThan10_9 = self.addObject(GreaterThan()) 
        self.greaterThan10_9.lower =  self.numberFactory.getNumber(9) 
        self.greaterThan10_9.higher =  self.numberFactory.getNumber(10)
												

        self.greaterThan11_0 = self.addObject(GreaterThan()) 
        self.greaterThan11_0.lower =  self.numberFactory.getNumber(0) 
        self.greaterThan11_0.higher =  self.numberFactory.getNumber(11)
	
        self.greaterThan11_1 = self.addObject(GreaterThan()) 
        self.greaterThan11_1.lower =  self.numberFactory.getNumber(1) 
        self.greaterThan11_1.higher =  self.numberFactory.getNumber(11)
	
        self.greaterThan11_2 = self.addObject(GreaterThan()) 
        self.greaterThan11_2.lower =  self.numberFactory.getNumber(2) 
        self.greaterThan11_2.higher =  self.numberFactory.getNumber(11)
	
        self.greaterThan11_3 = self.addObject(GreaterThan()) 
        self.greaterThan11_3.lower =  self.numberFactory.getNumber(3) 
        self.greaterThan11_3.higher =  self.numberFactory.getNumber(11)
	
        self.greaterThan11_4 = self.addObject(GreaterThan()) 
        self.greaterThan11_4.lower =  self.numberFactory.getNumber(4) 
        self.greaterThan11_4.higher =  self.numberFactory.getNumber(11)
	
        self.greaterThan11_5 = self.addObject(GreaterThan()) 
        self.greaterThan11_5.lower =  self.numberFactory.getNumber(5) 
        self.greaterThan11_5.higher =  self.numberFactory.getNumber(11)
	
        self.greaterThan11_6 = self.addObject(GreaterThan()) 
        self.greaterThan11_6.lower =  self.numberFactory.getNumber(6) 
        self.greaterThan11_6.higher =  self.numberFactory.getNumber(11)
	
        self.greaterThan11_7 = self.addObject(GreaterThan()) 
        self.greaterThan11_7.lower =  self.numberFactory.getNumber(7) 
        self.greaterThan11_7.higher =  self.numberFactory.getNumber(11)
	
        self.greaterThan11_8 = self.addObject(GreaterThan()) 
        self.greaterThan11_8.lower =  self.numberFactory.getNumber(8) 
        self.greaterThan11_8.higher =  self.numberFactory.getNumber(11)
	
        self.greaterThan11_9 = self.addObject(GreaterThan()) 
        self.greaterThan11_9.lower =  self.numberFactory.getNumber(9) 
        self.greaterThan11_9.higher =  self.numberFactory.getNumber(11)
	
        self.greaterThan11_10 = self.addObject(GreaterThan()) 
        self.greaterThan11_10.lower =  self.numberFactory.getNumber(10) 
        self.greaterThan11_10.higher =  self.numberFactory.getNumber(11)
											

        self.greaterThan12_0 = self.addObject(GreaterThan()) 
        self.greaterThan12_0.lower =  self.numberFactory.getNumber(0) 
        self.greaterThan12_0.higher =  self.numberFactory.getNumber(12)
	
        self.greaterThan12_1 = self.addObject(GreaterThan()) 
        self.greaterThan12_1.lower =  self.numberFactory.getNumber(1) 
        self.greaterThan12_1.higher =  self.numberFactory.getNumber(12)
	
        self.greaterThan12_2 = self.addObject(GreaterThan()) 
        self.greaterThan12_2.lower =  self.numberFactory.getNumber(2) 
        self.greaterThan12_2.higher =  self.numberFactory.getNumber(12)
	
        self.greaterThan12_3 = self.addObject(GreaterThan()) 
        self.greaterThan12_3.lower =  self.numberFactory.getNumber(3) 
        self.greaterThan12_3.higher =  self.numberFactory.getNumber(12)
	
        self.greaterThan12_4 = self.addObject(GreaterThan()) 
        self.greaterThan12_4.lower =  self.numberFactory.getNumber(4) 
        self.greaterThan12_4.higher =  self.numberFactory.getNumber(12)
	
        self.greaterThan12_5 = self.addObject(GreaterThan()) 
        self.greaterThan12_5.lower =  self.numberFactory.getNumber(5) 
        self.greaterThan12_5.higher =  self.numberFactory.getNumber(12)
	
        self.greaterThan12_6 = self.addObject(GreaterThan()) 
        self.greaterThan12_6.lower =  self.numberFactory.getNumber(6) 
        self.greaterThan12_6.higher =  self.numberFactory.getNumber(12)
	
        self.greaterThan12_7 = self.addObject(GreaterThan()) 
        self.greaterThan12_7.lower =  self.numberFactory.getNumber(7) 
        self.greaterThan12_7.higher =  self.numberFactory.getNumber(12)
	
        self.greaterThan12_8 = self.addObject(GreaterThan()) 
        self.greaterThan12_8.lower =  self.numberFactory.getNumber(8) 
        self.greaterThan12_8.higher =  self.numberFactory.getNumber(12)
	
        self.greaterThan12_9 = self.addObject(GreaterThan()) 
        self.greaterThan12_9.lower =  self.numberFactory.getNumber(9) 
        self.greaterThan12_9.higher =  self.numberFactory.getNumber(12)
	
        self.greaterThan12_10 = self.addObject(GreaterThan()) 
        self.greaterThan12_10.lower =  self.numberFactory.getNumber(10) 
        self.greaterThan12_10.higher =  self.numberFactory.getNumber(12)
	
        self.greaterThan12_11 = self.addObject(GreaterThan()) 
        self.greaterThan12_11.lower =  self.numberFactory.getNumber(11) 
        self.greaterThan12_11.higher =  self.numberFactory.getNumber(12)
										

        self.greaterThan13_0 = self.addObject(GreaterThan()) 
        self.greaterThan13_0.lower =  self.numberFactory.getNumber(0) 
        self.greaterThan13_0.higher =  self.numberFactory.getNumber(13)
	
        self.greaterThan13_1 = self.addObject(GreaterThan()) 
        self.greaterThan13_1.lower =  self.numberFactory.getNumber(1) 
        self.greaterThan13_1.higher =  self.numberFactory.getNumber(13)
	
        self.greaterThan13_2 = self.addObject(GreaterThan()) 
        self.greaterThan13_2.lower =  self.numberFactory.getNumber(2) 
        self.greaterThan13_2.higher =  self.numberFactory.getNumber(13)
	
        self.greaterThan13_3 = self.addObject(GreaterThan()) 
        self.greaterThan13_3.lower =  self.numberFactory.getNumber(3) 
        self.greaterThan13_3.higher =  self.numberFactory.getNumber(13)
	
        self.greaterThan13_4 = self.addObject(GreaterThan()) 
        self.greaterThan13_4.lower =  self.numberFactory.getNumber(4) 
        self.greaterThan13_4.higher =  self.numberFactory.getNumber(13)
	
        self.greaterThan13_5 = self.addObject(GreaterThan()) 
        self.greaterThan13_5.lower =  self.numberFactory.getNumber(5) 
        self.greaterThan13_5.higher =  self.numberFactory.getNumber(13)
	
        self.greaterThan13_6 = self.addObject(GreaterThan()) 
        self.greaterThan13_6.lower =  self.numberFactory.getNumber(6) 
        self.greaterThan13_6.higher =  self.numberFactory.getNumber(13)
	
        self.greaterThan13_7 = self.addObject(GreaterThan()) 
        self.greaterThan13_7.lower =  self.numberFactory.getNumber(7) 
        self.greaterThan13_7.higher =  self.numberFactory.getNumber(13)
	
        self.greaterThan13_8 = self.addObject(GreaterThan()) 
        self.greaterThan13_8.lower =  self.numberFactory.getNumber(8) 
        self.greaterThan13_8.higher =  self.numberFactory.getNumber(13)
	
        self.greaterThan13_9 = self.addObject(GreaterThan()) 
        self.greaterThan13_9.lower =  self.numberFactory.getNumber(9) 
        self.greaterThan13_9.higher =  self.numberFactory.getNumber(13)
	
        self.greaterThan13_10 = self.addObject(GreaterThan()) 
        self.greaterThan13_10.lower =  self.numberFactory.getNumber(10) 
        self.greaterThan13_10.higher =  self.numberFactory.getNumber(13)
	
        self.greaterThan13_11 = self.addObject(GreaterThan()) 
        self.greaterThan13_11.lower =  self.numberFactory.getNumber(11) 
        self.greaterThan13_11.higher =  self.numberFactory.getNumber(13)
	
        self.greaterThan13_12 = self.addObject(GreaterThan()) 
        self.greaterThan13_12.lower =  self.numberFactory.getNumber(12) 
        self.greaterThan13_12.higher =  self.numberFactory.getNumber(13)
									

        self.greaterThan14_0 = self.addObject(GreaterThan()) 
        self.greaterThan14_0.lower =  self.numberFactory.getNumber(0) 
        self.greaterThan14_0.higher =  self.numberFactory.getNumber(14)
	
        self.greaterThan14_1 = self.addObject(GreaterThan()) 
        self.greaterThan14_1.lower =  self.numberFactory.getNumber(1) 
        self.greaterThan14_1.higher =  self.numberFactory.getNumber(14)
	
        self.greaterThan14_2 = self.addObject(GreaterThan()) 
        self.greaterThan14_2.lower =  self.numberFactory.getNumber(2) 
        self.greaterThan14_2.higher =  self.numberFactory.getNumber(14)
	
        self.greaterThan14_3 = self.addObject(GreaterThan()) 
        self.greaterThan14_3.lower =  self.numberFactory.getNumber(3) 
        self.greaterThan14_3.higher =  self.numberFactory.getNumber(14)
	
        self.greaterThan14_4 = self.addObject(GreaterThan()) 
        self.greaterThan14_4.lower =  self.numberFactory.getNumber(4) 
        self.greaterThan14_4.higher =  self.numberFactory.getNumber(14)
	
        self.greaterThan14_5 = self.addObject(GreaterThan()) 
        self.greaterThan14_5.lower =  self.numberFactory.getNumber(5) 
        self.greaterThan14_5.higher =  self.numberFactory.getNumber(14)
	
        self.greaterThan14_6 = self.addObject(GreaterThan()) 
        self.greaterThan14_6.lower =  self.numberFactory.getNumber(6) 
        self.greaterThan14_6.higher =  self.numberFactory.getNumber(14)
	
        self.greaterThan14_7 = self.addObject(GreaterThan()) 
        self.greaterThan14_7.lower =  self.numberFactory.getNumber(7) 
        self.greaterThan14_7.higher =  self.numberFactory.getNumber(14)
	
        self.greaterThan14_8 = self.addObject(GreaterThan()) 
        self.greaterThan14_8.lower =  self.numberFactory.getNumber(8) 
        self.greaterThan14_8.higher =  self.numberFactory.getNumber(14)
	
        self.greaterThan14_9 = self.addObject(GreaterThan()) 
        self.greaterThan14_9.lower =  self.numberFactory.getNumber(9) 
        self.greaterThan14_9.higher =  self.numberFactory.getNumber(14)
	
        self.greaterThan14_10 = self.addObject(GreaterThan()) 
        self.greaterThan14_10.lower =  self.numberFactory.getNumber(10) 
        self.greaterThan14_10.higher =  self.numberFactory.getNumber(14)
	
        self.greaterThan14_11 = self.addObject(GreaterThan()) 
        self.greaterThan14_11.lower =  self.numberFactory.getNumber(11) 
        self.greaterThan14_11.higher =  self.numberFactory.getNumber(14)
	
        self.greaterThan14_12 = self.addObject(GreaterThan()) 
        self.greaterThan14_12.lower =  self.numberFactory.getNumber(12) 
        self.greaterThan14_12.higher =  self.numberFactory.getNumber(14)
	
        self.greaterThan14_13 = self.addObject(GreaterThan()) 
        self.greaterThan14_13.lower =  self.numberFactory.getNumber(13) 
        self.greaterThan14_13.higher =  self.numberFactory.getNumber(14)
								

        self.greaterThan15_0 = self.addObject(GreaterThan()) 
        self.greaterThan15_0.lower =  self.numberFactory.getNumber(0) 
        self.greaterThan15_0.higher =  self.numberFactory.getNumber(15)
	
        self.greaterThan15_1 = self.addObject(GreaterThan()) 
        self.greaterThan15_1.lower =  self.numberFactory.getNumber(1) 
        self.greaterThan15_1.higher =  self.numberFactory.getNumber(15)
	
        self.greaterThan15_2 = self.addObject(GreaterThan()) 
        self.greaterThan15_2.lower =  self.numberFactory.getNumber(2) 
        self.greaterThan15_2.higher =  self.numberFactory.getNumber(15)
	
        self.greaterThan15_3 = self.addObject(GreaterThan()) 
        self.greaterThan15_3.lower =  self.numberFactory.getNumber(3) 
        self.greaterThan15_3.higher =  self.numberFactory.getNumber(15)
	
        self.greaterThan15_4 = self.addObject(GreaterThan()) 
        self.greaterThan15_4.lower =  self.numberFactory.getNumber(4) 
        self.greaterThan15_4.higher =  self.numberFactory.getNumber(15)
	
        self.greaterThan15_5 = self.addObject(GreaterThan()) 
        self.greaterThan15_5.lower =  self.numberFactory.getNumber(5) 
        self.greaterThan15_5.higher =  self.numberFactory.getNumber(15)
	
        self.greaterThan15_6 = self.addObject(GreaterThan()) 
        self.greaterThan15_6.lower =  self.numberFactory.getNumber(6) 
        self.greaterThan15_6.higher =  self.numberFactory.getNumber(15)
	
        self.greaterThan15_7 = self.addObject(GreaterThan()) 
        self.greaterThan15_7.lower =  self.numberFactory.getNumber(7) 
        self.greaterThan15_7.higher =  self.numberFactory.getNumber(15)
	
        self.greaterThan15_8 = self.addObject(GreaterThan()) 
        self.greaterThan15_8.lower =  self.numberFactory.getNumber(8) 
        self.greaterThan15_8.higher =  self.numberFactory.getNumber(15)
	
        self.greaterThan15_9 = self.addObject(GreaterThan()) 
        self.greaterThan15_9.lower =  self.numberFactory.getNumber(9) 
        self.greaterThan15_9.higher =  self.numberFactory.getNumber(15)
	
        self.greaterThan15_10 = self.addObject(GreaterThan()) 
        self.greaterThan15_10.lower =  self.numberFactory.getNumber(10) 
        self.greaterThan15_10.higher =  self.numberFactory.getNumber(15)
	
        self.greaterThan15_11 = self.addObject(GreaterThan()) 
        self.greaterThan15_11.lower =  self.numberFactory.getNumber(11) 
        self.greaterThan15_11.higher =  self.numberFactory.getNumber(15)
	
        self.greaterThan15_12 = self.addObject(GreaterThan()) 
        self.greaterThan15_12.lower =  self.numberFactory.getNumber(12) 
        self.greaterThan15_12.higher =  self.numberFactory.getNumber(15)
	
        self.greaterThan15_13 = self.addObject(GreaterThan()) 
        self.greaterThan15_13.lower =  self.numberFactory.getNumber(13) 
        self.greaterThan15_13.higher =  self.numberFactory.getNumber(15)
	
        self.greaterThan15_14 = self.addObject(GreaterThan()) 
        self.greaterThan15_14.lower =  self.numberFactory.getNumber(14) 
        self.greaterThan15_14.higher =  self.numberFactory.getNumber(15)
							

        self.greaterThan16_0 = self.addObject(GreaterThan()) 
        self.greaterThan16_0.lower =  self.numberFactory.getNumber(0) 
        self.greaterThan16_0.higher =  self.numberFactory.getNumber(16)
	
        self.greaterThan16_1 = self.addObject(GreaterThan()) 
        self.greaterThan16_1.lower =  self.numberFactory.getNumber(1) 
        self.greaterThan16_1.higher =  self.numberFactory.getNumber(16)
	
        self.greaterThan16_2 = self.addObject(GreaterThan()) 
        self.greaterThan16_2.lower =  self.numberFactory.getNumber(2) 
        self.greaterThan16_2.higher =  self.numberFactory.getNumber(16)
	
        self.greaterThan16_3 = self.addObject(GreaterThan()) 
        self.greaterThan16_3.lower =  self.numberFactory.getNumber(3) 
        self.greaterThan16_3.higher =  self.numberFactory.getNumber(16)
	
        self.greaterThan16_4 = self.addObject(GreaterThan()) 
        self.greaterThan16_4.lower =  self.numberFactory.getNumber(4) 
        self.greaterThan16_4.higher =  self.numberFactory.getNumber(16)
	
        self.greaterThan16_5 = self.addObject(GreaterThan()) 
        self.greaterThan16_5.lower =  self.numberFactory.getNumber(5) 
        self.greaterThan16_5.higher =  self.numberFactory.getNumber(16)
	
        self.greaterThan16_6 = self.addObject(GreaterThan()) 
        self.greaterThan16_6.lower =  self.numberFactory.getNumber(6) 
        self.greaterThan16_6.higher =  self.numberFactory.getNumber(16)
	
        self.greaterThan16_7 = self.addObject(GreaterThan()) 
        self.greaterThan16_7.lower =  self.numberFactory.getNumber(7) 
        self.greaterThan16_7.higher =  self.numberFactory.getNumber(16)
	
        self.greaterThan16_8 = self.addObject(GreaterThan()) 
        self.greaterThan16_8.lower =  self.numberFactory.getNumber(8) 
        self.greaterThan16_8.higher =  self.numberFactory.getNumber(16)
	
        self.greaterThan16_9 = self.addObject(GreaterThan()) 
        self.greaterThan16_9.lower =  self.numberFactory.getNumber(9) 
        self.greaterThan16_9.higher =  self.numberFactory.getNumber(16)
	
        self.greaterThan16_10 = self.addObject(GreaterThan()) 
        self.greaterThan16_10.lower =  self.numberFactory.getNumber(10) 
        self.greaterThan16_10.higher =  self.numberFactory.getNumber(16)
	
        self.greaterThan16_11 = self.addObject(GreaterThan()) 
        self.greaterThan16_11.lower =  self.numberFactory.getNumber(11) 
        self.greaterThan16_11.higher =  self.numberFactory.getNumber(16)
	
        self.greaterThan16_12 = self.addObject(GreaterThan()) 
        self.greaterThan16_12.lower =  self.numberFactory.getNumber(12) 
        self.greaterThan16_12.higher =  self.numberFactory.getNumber(16)
	
        self.greaterThan16_13 = self.addObject(GreaterThan()) 
        self.greaterThan16_13.lower =  self.numberFactory.getNumber(13) 
        self.greaterThan16_13.higher =  self.numberFactory.getNumber(16)
	
        self.greaterThan16_14 = self.addObject(GreaterThan()) 
        self.greaterThan16_14.lower =  self.numberFactory.getNumber(14) 
        self.greaterThan16_14.higher =  self.numberFactory.getNumber(16)
	
        self.greaterThan16_15 = self.addObject(GreaterThan()) 
        self.greaterThan16_15.lower =  self.numberFactory.getNumber(15) 
        self.greaterThan16_15.higher =  self.numberFactory.getNumber(16)
						

        self.greaterThan17_0 = self.addObject(GreaterThan()) 
        self.greaterThan17_0.lower =  self.numberFactory.getNumber(0) 
        self.greaterThan17_0.higher =  self.numberFactory.getNumber(17)
	
        self.greaterThan17_1 = self.addObject(GreaterThan()) 
        self.greaterThan17_1.lower =  self.numberFactory.getNumber(1) 
        self.greaterThan17_1.higher =  self.numberFactory.getNumber(17)
	
        self.greaterThan17_2 = self.addObject(GreaterThan()) 
        self.greaterThan17_2.lower =  self.numberFactory.getNumber(2) 
        self.greaterThan17_2.higher =  self.numberFactory.getNumber(17)
	
        self.greaterThan17_3 = self.addObject(GreaterThan()) 
        self.greaterThan17_3.lower =  self.numberFactory.getNumber(3) 
        self.greaterThan17_3.higher =  self.numberFactory.getNumber(17)
	
        self.greaterThan17_4 = self.addObject(GreaterThan()) 
        self.greaterThan17_4.lower =  self.numberFactory.getNumber(4) 
        self.greaterThan17_4.higher =  self.numberFactory.getNumber(17)
	
        self.greaterThan17_5 = self.addObject(GreaterThan()) 
        self.greaterThan17_5.lower =  self.numberFactory.getNumber(5) 
        self.greaterThan17_5.higher =  self.numberFactory.getNumber(17)
	
        self.greaterThan17_6 = self.addObject(GreaterThan()) 
        self.greaterThan17_6.lower =  self.numberFactory.getNumber(6) 
        self.greaterThan17_6.higher =  self.numberFactory.getNumber(17)
	
        self.greaterThan17_7 = self.addObject(GreaterThan()) 
        self.greaterThan17_7.lower =  self.numberFactory.getNumber(7) 
        self.greaterThan17_7.higher =  self.numberFactory.getNumber(17)
	
        self.greaterThan17_8 = self.addObject(GreaterThan()) 
        self.greaterThan17_8.lower =  self.numberFactory.getNumber(8) 
        self.greaterThan17_8.higher =  self.numberFactory.getNumber(17)
	
        self.greaterThan17_9 = self.addObject(GreaterThan()) 
        self.greaterThan17_9.lower =  self.numberFactory.getNumber(9) 
        self.greaterThan17_9.higher =  self.numberFactory.getNumber(17)
	
        self.greaterThan17_10 = self.addObject(GreaterThan()) 
        self.greaterThan17_10.lower =  self.numberFactory.getNumber(10) 
        self.greaterThan17_10.higher =  self.numberFactory.getNumber(17)
	
        self.greaterThan17_11 = self.addObject(GreaterThan()) 
        self.greaterThan17_11.lower =  self.numberFactory.getNumber(11) 
        self.greaterThan17_11.higher =  self.numberFactory.getNumber(17)
	
        self.greaterThan17_12 = self.addObject(GreaterThan()) 
        self.greaterThan17_12.lower =  self.numberFactory.getNumber(12) 
        self.greaterThan17_12.higher =  self.numberFactory.getNumber(17)
	
        self.greaterThan17_13 = self.addObject(GreaterThan()) 
        self.greaterThan17_13.lower =  self.numberFactory.getNumber(13) 
        self.greaterThan17_13.higher =  self.numberFactory.getNumber(17)
	
        self.greaterThan17_14 = self.addObject(GreaterThan()) 
        self.greaterThan17_14.lower =  self.numberFactory.getNumber(14) 
        self.greaterThan17_14.higher =  self.numberFactory.getNumber(17)
	
        self.greaterThan17_15 = self.addObject(GreaterThan()) 
        self.greaterThan17_15.lower =  self.numberFactory.getNumber(15) 
        self.greaterThan17_15.higher =  self.numberFactory.getNumber(17)
	
        self.greaterThan17_16 = self.addObject(GreaterThan()) 
        self.greaterThan17_16.lower =  self.numberFactory.getNumber(16) 
        self.greaterThan17_16.higher =  self.numberFactory.getNumber(17)
					

        self.greaterThan18_0 = self.addObject(GreaterThan()) 
        self.greaterThan18_0.lower =  self.numberFactory.getNumber(0) 
        self.greaterThan18_0.higher =  self.numberFactory.getNumber(18)
	
        self.greaterThan18_1 = self.addObject(GreaterThan()) 
        self.greaterThan18_1.lower =  self.numberFactory.getNumber(1) 
        self.greaterThan18_1.higher =  self.numberFactory.getNumber(18)
	
        self.greaterThan18_2 = self.addObject(GreaterThan()) 
        self.greaterThan18_2.lower =  self.numberFactory.getNumber(2) 
        self.greaterThan18_2.higher =  self.numberFactory.getNumber(18)
	
        self.greaterThan18_3 = self.addObject(GreaterThan()) 
        self.greaterThan18_3.lower =  self.numberFactory.getNumber(3) 
        self.greaterThan18_3.higher =  self.numberFactory.getNumber(18)
	
        self.greaterThan18_4 = self.addObject(GreaterThan()) 
        self.greaterThan18_4.lower =  self.numberFactory.getNumber(4) 
        self.greaterThan18_4.higher =  self.numberFactory.getNumber(18)
	
        self.greaterThan18_5 = self.addObject(GreaterThan()) 
        self.greaterThan18_5.lower =  self.numberFactory.getNumber(5) 
        self.greaterThan18_5.higher =  self.numberFactory.getNumber(18)
	
        self.greaterThan18_6 = self.addObject(GreaterThan()) 
        self.greaterThan18_6.lower =  self.numberFactory.getNumber(6) 
        self.greaterThan18_6.higher =  self.numberFactory.getNumber(18)
	
        self.greaterThan18_7 = self.addObject(GreaterThan()) 
        self.greaterThan18_7.lower =  self.numberFactory.getNumber(7) 
        self.greaterThan18_7.higher =  self.numberFactory.getNumber(18)
	
        self.greaterThan18_8 = self.addObject(GreaterThan()) 
        self.greaterThan18_8.lower =  self.numberFactory.getNumber(8) 
        self.greaterThan18_8.higher =  self.numberFactory.getNumber(18)
	
        self.greaterThan18_9 = self.addObject(GreaterThan()) 
        self.greaterThan18_9.lower =  self.numberFactory.getNumber(9) 
        self.greaterThan18_9.higher =  self.numberFactory.getNumber(18)
	
        self.greaterThan18_10 = self.addObject(GreaterThan()) 
        self.greaterThan18_10.lower =  self.numberFactory.getNumber(10) 
        self.greaterThan18_10.higher =  self.numberFactory.getNumber(18)
	
        self.greaterThan18_11 = self.addObject(GreaterThan()) 
        self.greaterThan18_11.lower =  self.numberFactory.getNumber(11) 
        self.greaterThan18_11.higher =  self.numberFactory.getNumber(18)
	
        self.greaterThan18_12 = self.addObject(GreaterThan()) 
        self.greaterThan18_12.lower =  self.numberFactory.getNumber(12) 
        self.greaterThan18_12.higher =  self.numberFactory.getNumber(18)
	
        self.greaterThan18_13 = self.addObject(GreaterThan()) 
        self.greaterThan18_13.lower =  self.numberFactory.getNumber(13) 
        self.greaterThan18_13.higher =  self.numberFactory.getNumber(18)
	
        self.greaterThan18_14 = self.addObject(GreaterThan()) 
        self.greaterThan18_14.lower =  self.numberFactory.getNumber(14) 
        self.greaterThan18_14.higher =  self.numberFactory.getNumber(18)
	
        self.greaterThan18_15 = self.addObject(GreaterThan()) 
        self.greaterThan18_15.lower =  self.numberFactory.getNumber(15) 
        self.greaterThan18_15.higher =  self.numberFactory.getNumber(18)
	
        self.greaterThan18_16 = self.addObject(GreaterThan()) 
        self.greaterThan18_16.lower =  self.numberFactory.getNumber(16) 
        self.greaterThan18_16.higher =  self.numberFactory.getNumber(18)
	
        self.greaterThan18_17 = self.addObject(GreaterThan()) 
        self.greaterThan18_17.lower =  self.numberFactory.getNumber(17) 
        self.greaterThan18_17.higher =  self.numberFactory.getNumber(18)
				

        self.greaterThan19_0 = self.addObject(GreaterThan()) 
        self.greaterThan19_0.lower =  self.numberFactory.getNumber(0) 
        self.greaterThan19_0.higher =  self.numberFactory.getNumber(19)
	
        self.greaterThan19_1 = self.addObject(GreaterThan()) 
        self.greaterThan19_1.lower =  self.numberFactory.getNumber(1) 
        self.greaterThan19_1.higher =  self.numberFactory.getNumber(19)
	
        self.greaterThan19_2 = self.addObject(GreaterThan()) 
        self.greaterThan19_2.lower =  self.numberFactory.getNumber(2) 
        self.greaterThan19_2.higher =  self.numberFactory.getNumber(19)
	
        self.greaterThan19_3 = self.addObject(GreaterThan()) 
        self.greaterThan19_3.lower =  self.numberFactory.getNumber(3) 
        self.greaterThan19_3.higher =  self.numberFactory.getNumber(19)
	
        self.greaterThan19_4 = self.addObject(GreaterThan()) 
        self.greaterThan19_4.lower =  self.numberFactory.getNumber(4) 
        self.greaterThan19_4.higher =  self.numberFactory.getNumber(19)
	
        self.greaterThan19_5 = self.addObject(GreaterThan()) 
        self.greaterThan19_5.lower =  self.numberFactory.getNumber(5) 
        self.greaterThan19_5.higher =  self.numberFactory.getNumber(19)
	
        self.greaterThan19_6 = self.addObject(GreaterThan()) 
        self.greaterThan19_6.lower =  self.numberFactory.getNumber(6) 
        self.greaterThan19_6.higher =  self.numberFactory.getNumber(19)
	
        self.greaterThan19_7 = self.addObject(GreaterThan()) 
        self.greaterThan19_7.lower =  self.numberFactory.getNumber(7) 
        self.greaterThan19_7.higher =  self.numberFactory.getNumber(19)
	
        self.greaterThan19_8 = self.addObject(GreaterThan()) 
        self.greaterThan19_8.lower =  self.numberFactory.getNumber(8) 
        self.greaterThan19_8.higher =  self.numberFactory.getNumber(19)
	
        self.greaterThan19_9 = self.addObject(GreaterThan()) 
        self.greaterThan19_9.lower =  self.numberFactory.getNumber(9) 
        self.greaterThan19_9.higher =  self.numberFactory.getNumber(19)
	
        self.greaterThan19_10 = self.addObject(GreaterThan()) 
        self.greaterThan19_10.lower =  self.numberFactory.getNumber(10) 
        self.greaterThan19_10.higher =  self.numberFactory.getNumber(19)
	
        self.greaterThan19_11 = self.addObject(GreaterThan()) 
        self.greaterThan19_11.lower =  self.numberFactory.getNumber(11) 
        self.greaterThan19_11.higher =  self.numberFactory.getNumber(19)
	
        self.greaterThan19_12 = self.addObject(GreaterThan()) 
        self.greaterThan19_12.lower =  self.numberFactory.getNumber(12) 
        self.greaterThan19_12.higher =  self.numberFactory.getNumber(19)
	
        self.greaterThan19_13 = self.addObject(GreaterThan()) 
        self.greaterThan19_13.lower =  self.numberFactory.getNumber(13) 
        self.greaterThan19_13.higher =  self.numberFactory.getNumber(19)
	
        self.greaterThan19_14 = self.addObject(GreaterThan()) 
        self.greaterThan19_14.lower =  self.numberFactory.getNumber(14) 
        self.greaterThan19_14.higher =  self.numberFactory.getNumber(19)
	
        self.greaterThan19_15 = self.addObject(GreaterThan()) 
        self.greaterThan19_15.lower =  self.numberFactory.getNumber(15) 
        self.greaterThan19_15.higher =  self.numberFactory.getNumber(19)
	
        self.greaterThan19_16 = self.addObject(GreaterThan()) 
        self.greaterThan19_16.lower =  self.numberFactory.getNumber(16) 
        self.greaterThan19_16.higher =  self.numberFactory.getNumber(19)
	
        self.greaterThan19_17 = self.addObject(GreaterThan()) 
        self.greaterThan19_17.lower =  self.numberFactory.getNumber(17) 
        self.greaterThan19_17.higher =  self.numberFactory.getNumber(19)
	
        self.greaterThan19_18 = self.addObject(GreaterThan()) 
        self.greaterThan19_18.lower =  self.numberFactory.getNumber(18) 
        self.greaterThan19_18.higher =  self.numberFactory.getNumber(19)
			

        self.greaterThan20_0 = self.addObject(GreaterThan()) 
        self.greaterThan20_0.lower =  self.numberFactory.getNumber(0) 
        self.greaterThan20_0.higher =  self.numberFactory.getNumber(20)
	
        self.greaterThan20_1 = self.addObject(GreaterThan()) 
        self.greaterThan20_1.lower =  self.numberFactory.getNumber(1) 
        self.greaterThan20_1.higher =  self.numberFactory.getNumber(20)
	
        self.greaterThan20_2 = self.addObject(GreaterThan()) 
        self.greaterThan20_2.lower =  self.numberFactory.getNumber(2) 
        self.greaterThan20_2.higher =  self.numberFactory.getNumber(20)
	
        self.greaterThan20_3 = self.addObject(GreaterThan()) 
        self.greaterThan20_3.lower =  self.numberFactory.getNumber(3) 
        self.greaterThan20_3.higher =  self.numberFactory.getNumber(20)
	
        self.greaterThan20_4 = self.addObject(GreaterThan()) 
        self.greaterThan20_4.lower =  self.numberFactory.getNumber(4) 
        self.greaterThan20_4.higher =  self.numberFactory.getNumber(20)
	
        self.greaterThan20_5 = self.addObject(GreaterThan()) 
        self.greaterThan20_5.lower =  self.numberFactory.getNumber(5) 
        self.greaterThan20_5.higher =  self.numberFactory.getNumber(20)
	
        self.greaterThan20_6 = self.addObject(GreaterThan()) 
        self.greaterThan20_6.lower =  self.numberFactory.getNumber(6) 
        self.greaterThan20_6.higher =  self.numberFactory.getNumber(20)
	
        self.greaterThan20_7 = self.addObject(GreaterThan()) 
        self.greaterThan20_7.lower =  self.numberFactory.getNumber(7) 
        self.greaterThan20_7.higher =  self.numberFactory.getNumber(20)
	
        self.greaterThan20_8 = self.addObject(GreaterThan()) 
        self.greaterThan20_8.lower =  self.numberFactory.getNumber(8) 
        self.greaterThan20_8.higher =  self.numberFactory.getNumber(20)
	
        self.greaterThan20_9 = self.addObject(GreaterThan()) 
        self.greaterThan20_9.lower =  self.numberFactory.getNumber(9) 
        self.greaterThan20_9.higher =  self.numberFactory.getNumber(20)
	
        self.greaterThan20_10 = self.addObject(GreaterThan()) 
        self.greaterThan20_10.lower =  self.numberFactory.getNumber(10) 
        self.greaterThan20_10.higher =  self.numberFactory.getNumber(20)
	
        self.greaterThan20_11 = self.addObject(GreaterThan()) 
        self.greaterThan20_11.lower =  self.numberFactory.getNumber(11) 
        self.greaterThan20_11.higher =  self.numberFactory.getNumber(20)
	
        self.greaterThan20_12 = self.addObject(GreaterThan()) 
        self.greaterThan20_12.lower =  self.numberFactory.getNumber(12) 
        self.greaterThan20_12.higher =  self.numberFactory.getNumber(20)
	
        self.greaterThan20_13 = self.addObject(GreaterThan()) 
        self.greaterThan20_13.lower =  self.numberFactory.getNumber(13) 
        self.greaterThan20_13.higher =  self.numberFactory.getNumber(20)
	
        self.greaterThan20_14 = self.addObject(GreaterThan()) 
        self.greaterThan20_14.lower =  self.numberFactory.getNumber(14) 
        self.greaterThan20_14.higher =  self.numberFactory.getNumber(20)
	
        self.greaterThan20_15 = self.addObject(GreaterThan()) 
        self.greaterThan20_15.lower =  self.numberFactory.getNumber(15) 
        self.greaterThan20_15.higher =  self.numberFactory.getNumber(20)
	
        self.greaterThan20_16 = self.addObject(GreaterThan()) 
        self.greaterThan20_16.lower =  self.numberFactory.getNumber(16) 
        self.greaterThan20_16.higher =  self.numberFactory.getNumber(20)
	
        self.greaterThan20_17 = self.addObject(GreaterThan()) 
        self.greaterThan20_17.lower =  self.numberFactory.getNumber(17) 
        self.greaterThan20_17.higher =  self.numberFactory.getNumber(20)
	
        self.greaterThan20_18 = self.addObject(GreaterThan()) 
        self.greaterThan20_18.lower =  self.numberFactory.getNumber(18) 
        self.greaterThan20_18.higher =  self.numberFactory.getNumber(20)
	
        self.greaterThan20_19 = self.addObject(GreaterThan()) 
        self.greaterThan20_19.lower =  self.numberFactory.getNumber(19) 
        self.greaterThan20_19.higher =  self.numberFactory.getNumber(20)
		

        self.greaterThan21_0 = self.addObject(GreaterThan()) 
        self.greaterThan21_0.lower =  self.numberFactory.getNumber(0) 
        self.greaterThan21_0.higher =  self.numberFactory.getNumber(21)
	
        self.greaterThan21_1 = self.addObject(GreaterThan()) 
        self.greaterThan21_1.lower =  self.numberFactory.getNumber(1) 
        self.greaterThan21_1.higher =  self.numberFactory.getNumber(21)
	
        self.greaterThan21_2 = self.addObject(GreaterThan()) 
        self.greaterThan21_2.lower =  self.numberFactory.getNumber(2) 
        self.greaterThan21_2.higher =  self.numberFactory.getNumber(21)
	
        self.greaterThan21_3 = self.addObject(GreaterThan()) 
        self.greaterThan21_3.lower =  self.numberFactory.getNumber(3) 
        self.greaterThan21_3.higher =  self.numberFactory.getNumber(21)
	
        self.greaterThan21_4 = self.addObject(GreaterThan()) 
        self.greaterThan21_4.lower =  self.numberFactory.getNumber(4) 
        self.greaterThan21_4.higher =  self.numberFactory.getNumber(21)
	
        self.greaterThan21_5 = self.addObject(GreaterThan()) 
        self.greaterThan21_5.lower =  self.numberFactory.getNumber(5) 
        self.greaterThan21_5.higher =  self.numberFactory.getNumber(21)
	
        self.greaterThan21_6 = self.addObject(GreaterThan()) 
        self.greaterThan21_6.lower =  self.numberFactory.getNumber(6) 
        self.greaterThan21_6.higher =  self.numberFactory.getNumber(21)
	
        self.greaterThan21_7 = self.addObject(GreaterThan()) 
        self.greaterThan21_7.lower =  self.numberFactory.getNumber(7) 
        self.greaterThan21_7.higher =  self.numberFactory.getNumber(21)
	
        self.greaterThan21_8 = self.addObject(GreaterThan()) 
        self.greaterThan21_8.lower =  self.numberFactory.getNumber(8) 
        self.greaterThan21_8.higher =  self.numberFactory.getNumber(21)
	
        self.greaterThan21_9 = self.addObject(GreaterThan()) 
        self.greaterThan21_9.lower =  self.numberFactory.getNumber(9) 
        self.greaterThan21_9.higher =  self.numberFactory.getNumber(21)
	
        self.greaterThan21_10 = self.addObject(GreaterThan()) 
        self.greaterThan21_10.lower =  self.numberFactory.getNumber(10) 
        self.greaterThan21_10.higher =  self.numberFactory.getNumber(21)
	
        self.greaterThan21_11 = self.addObject(GreaterThan()) 
        self.greaterThan21_11.lower =  self.numberFactory.getNumber(11) 
        self.greaterThan21_11.higher =  self.numberFactory.getNumber(21)
	
        self.greaterThan21_12 = self.addObject(GreaterThan()) 
        self.greaterThan21_12.lower =  self.numberFactory.getNumber(12) 
        self.greaterThan21_12.higher =  self.numberFactory.getNumber(21)
	
        self.greaterThan21_13 = self.addObject(GreaterThan()) 
        self.greaterThan21_13.lower =  self.numberFactory.getNumber(13) 
        self.greaterThan21_13.higher =  self.numberFactory.getNumber(21)
	
        self.greaterThan21_14 = self.addObject(GreaterThan()) 
        self.greaterThan21_14.lower =  self.numberFactory.getNumber(14) 
        self.greaterThan21_14.higher =  self.numberFactory.getNumber(21)
	
        self.greaterThan21_15 = self.addObject(GreaterThan()) 
        self.greaterThan21_15.lower =  self.numberFactory.getNumber(15) 
        self.greaterThan21_15.higher =  self.numberFactory.getNumber(21)
	
        self.greaterThan21_16 = self.addObject(GreaterThan()) 
        self.greaterThan21_16.lower =  self.numberFactory.getNumber(16) 
        self.greaterThan21_16.higher =  self.numberFactory.getNumber(21)
	
        self.greaterThan21_17 = self.addObject(GreaterThan()) 
        self.greaterThan21_17.lower =  self.numberFactory.getNumber(17) 
        self.greaterThan21_17.higher =  self.numberFactory.getNumber(21)
	
        self.greaterThan21_18 = self.addObject(GreaterThan()) 
        self.greaterThan21_18.lower =  self.numberFactory.getNumber(18) 
        self.greaterThan21_18.higher =  self.numberFactory.getNumber(21)
	
        self.greaterThan21_19 = self.addObject(GreaterThan()) 
        self.greaterThan21_19.lower =  self.numberFactory.getNumber(19) 
        self.greaterThan21_19.higher =  self.numberFactory.getNumber(21)
	
        self.greaterThan21_20 = self.addObject(GreaterThan()) 
        self.greaterThan21_20.lower =  self.numberFactory.getNumber(20) 
        self.greaterThan21_20.higher =  self.numberFactory.getNumber(21)
	

        self.greaterThan22_0 = self.addObject(GreaterThan()) 
        self.greaterThan22_0.lower =  self.numberFactory.getNumber(0) 
        self.greaterThan22_0.higher =  self.numberFactory.getNumber(22)
	
        self.greaterThan22_1 = self.addObject(GreaterThan()) 
        self.greaterThan22_1.lower =  self.numberFactory.getNumber(1) 
        self.greaterThan22_1.higher =  self.numberFactory.getNumber(22)
	
        self.greaterThan22_2 = self.addObject(GreaterThan()) 
        self.greaterThan22_2.lower =  self.numberFactory.getNumber(2) 
        self.greaterThan22_2.higher =  self.numberFactory.getNumber(22)
	
        self.greaterThan22_3 = self.addObject(GreaterThan()) 
        self.greaterThan22_3.lower =  self.numberFactory.getNumber(3) 
        self.greaterThan22_3.higher =  self.numberFactory.getNumber(22)
	
        self.greaterThan22_4 = self.addObject(GreaterThan()) 
        self.greaterThan22_4.lower =  self.numberFactory.getNumber(4) 
        self.greaterThan22_4.higher =  self.numberFactory.getNumber(22)
	
        self.greaterThan22_5 = self.addObject(GreaterThan()) 
        self.greaterThan22_5.lower =  self.numberFactory.getNumber(5) 
        self.greaterThan22_5.higher =  self.numberFactory.getNumber(22)
	
        self.greaterThan22_6 = self.addObject(GreaterThan()) 
        self.greaterThan22_6.lower =  self.numberFactory.getNumber(6) 
        self.greaterThan22_6.higher =  self.numberFactory.getNumber(22)
	
        self.greaterThan22_7 = self.addObject(GreaterThan()) 
        self.greaterThan22_7.lower =  self.numberFactory.getNumber(7) 
        self.greaterThan22_7.higher =  self.numberFactory.getNumber(22)
	
        self.greaterThan22_8 = self.addObject(GreaterThan()) 
        self.greaterThan22_8.lower =  self.numberFactory.getNumber(8) 
        self.greaterThan22_8.higher =  self.numberFactory.getNumber(22)
	
        self.greaterThan22_9 = self.addObject(GreaterThan()) 
        self.greaterThan22_9.lower =  self.numberFactory.getNumber(9) 
        self.greaterThan22_9.higher =  self.numberFactory.getNumber(22)
	
        self.greaterThan22_10 = self.addObject(GreaterThan()) 
        self.greaterThan22_10.lower =  self.numberFactory.getNumber(10) 
        self.greaterThan22_10.higher =  self.numberFactory.getNumber(22)
	
        self.greaterThan22_11 = self.addObject(GreaterThan()) 
        self.greaterThan22_11.lower =  self.numberFactory.getNumber(11) 
        self.greaterThan22_11.higher =  self.numberFactory.getNumber(22)
	
        self.greaterThan22_12 = self.addObject(GreaterThan()) 
        self.greaterThan22_12.lower =  self.numberFactory.getNumber(12) 
        self.greaterThan22_12.higher =  self.numberFactory.getNumber(22)
	
        self.greaterThan22_13 = self.addObject(GreaterThan()) 
        self.greaterThan22_13.lower =  self.numberFactory.getNumber(13) 
        self.greaterThan22_13.higher =  self.numberFactory.getNumber(22)
	
        self.greaterThan22_14 = self.addObject(GreaterThan()) 
        self.greaterThan22_14.lower =  self.numberFactory.getNumber(14) 
        self.greaterThan22_14.higher =  self.numberFactory.getNumber(22)
	
        self.greaterThan22_15 = self.addObject(GreaterThan()) 
        self.greaterThan22_15.lower =  self.numberFactory.getNumber(15) 
        self.greaterThan22_15.higher =  self.numberFactory.getNumber(22)
	
        self.greaterThan22_16 = self.addObject(GreaterThan()) 
        self.greaterThan22_16.lower =  self.numberFactory.getNumber(16) 
        self.greaterThan22_16.higher =  self.numberFactory.getNumber(22)
	
        self.greaterThan22_17 = self.addObject(GreaterThan()) 
        self.greaterThan22_17.lower =  self.numberFactory.getNumber(17) 
        self.greaterThan22_17.higher =  self.numberFactory.getNumber(22)
	
        self.greaterThan22_18 = self.addObject(GreaterThan()) 
        self.greaterThan22_18.lower =  self.numberFactory.getNumber(18) 
        self.greaterThan22_18.higher =  self.numberFactory.getNumber(22)
	
        self.greaterThan22_19 = self.addObject(GreaterThan()) 
        self.greaterThan22_19.lower =  self.numberFactory.getNumber(19) 
        self.greaterThan22_19.higher =  self.numberFactory.getNumber(22)
	
        self.greaterThan22_20 = self.addObject(GreaterThan()) 
        self.greaterThan22_20.lower =  self.numberFactory.getNumber(20) 
        self.greaterThan22_20.higher =  self.numberFactory.getNumber(22)
	
        self.greaterThan22_21 = self.addObject(GreaterThan()) 
        self.greaterThan22_21.lower =  self.numberFactory.getNumber(21) 
        self.greaterThan22_21.higher =  self.numberFactory.getNumber(22)


        self.greaterThan23_0 = self.addObject(GreaterThan()) 
        self.greaterThan23_0.lower =  self.numberFactory.getNumber(0) 
        self.greaterThan23_0.higher =  self.numberFactory.getNumber(23)
	
        self.greaterThan23_1 = self.addObject(GreaterThan()) 
        self.greaterThan23_1.lower =  self.numberFactory.getNumber(1) 
        self.greaterThan23_1.higher =  self.numberFactory.getNumber(23)
	
        self.greaterThan23_2 = self.addObject(GreaterThan()) 
        self.greaterThan23_2.lower =  self.numberFactory.getNumber(2) 
        self.greaterThan23_2.higher =  self.numberFactory.getNumber(23)
	
        self.greaterThan23_3 = self.addObject(GreaterThan()) 
        self.greaterThan23_3.lower =  self.numberFactory.getNumber(3) 
        self.greaterThan23_3.higher =  self.numberFactory.getNumber(23)
	
        self.greaterThan23_4 = self.addObject(GreaterThan()) 
        self.greaterThan23_4.lower =  self.numberFactory.getNumber(4) 
        self.greaterThan23_4.higher =  self.numberFactory.getNumber(23)
	
        self.greaterThan23_5 = self.addObject(GreaterThan()) 
        self.greaterThan23_5.lower =  self.numberFactory.getNumber(5) 
        self.greaterThan23_5.higher =  self.numberFactory.getNumber(23)
	
        self.greaterThan23_6 = self.addObject(GreaterThan()) 
        self.greaterThan23_6.lower =  self.numberFactory.getNumber(6) 
        self.greaterThan23_6.higher =  self.numberFactory.getNumber(23)
	
        self.greaterThan23_7 = self.addObject(GreaterThan()) 
        self.greaterThan23_7.lower =  self.numberFactory.getNumber(7) 
        self.greaterThan23_7.higher =  self.numberFactory.getNumber(23)
	
        self.greaterThan23_8 = self.addObject(GreaterThan()) 
        self.greaterThan23_8.lower =  self.numberFactory.getNumber(8) 
        self.greaterThan23_8.higher =  self.numberFactory.getNumber(23)
	
        self.greaterThan23_9 = self.addObject(GreaterThan()) 
        self.greaterThan23_9.lower =  self.numberFactory.getNumber(9) 
        self.greaterThan23_9.higher =  self.numberFactory.getNumber(23)
	
        self.greaterThan23_10 = self.addObject(GreaterThan()) 
        self.greaterThan23_10.lower =  self.numberFactory.getNumber(10) 
        self.greaterThan23_10.higher =  self.numberFactory.getNumber(23)
	
        self.greaterThan23_11 = self.addObject(GreaterThan()) 
        self.greaterThan23_11.lower =  self.numberFactory.getNumber(11) 
        self.greaterThan23_11.higher =  self.numberFactory.getNumber(23)
	
        self.greaterThan23_12 = self.addObject(GreaterThan()) 
        self.greaterThan23_12.lower =  self.numberFactory.getNumber(12) 
        self.greaterThan23_12.higher =  self.numberFactory.getNumber(23)
	
        self.greaterThan23_13 = self.addObject(GreaterThan()) 
        self.greaterThan23_13.lower =  self.numberFactory.getNumber(13) 
        self.greaterThan23_13.higher =  self.numberFactory.getNumber(23)
	
        self.greaterThan23_14 = self.addObject(GreaterThan()) 
        self.greaterThan23_14.lower =  self.numberFactory.getNumber(14) 
        self.greaterThan23_14.higher =  self.numberFactory.getNumber(23)
	
        self.greaterThan23_15 = self.addObject(GreaterThan()) 
        self.greaterThan23_15.lower =  self.numberFactory.getNumber(15) 
        self.greaterThan23_15.higher =  self.numberFactory.getNumber(23)
	
        self.greaterThan23_16 = self.addObject(GreaterThan()) 
        self.greaterThan23_16.lower =  self.numberFactory.getNumber(16) 
        self.greaterThan23_16.higher =  self.numberFactory.getNumber(23)
	
        self.greaterThan23_17 = self.addObject(GreaterThan()) 
        self.greaterThan23_17.lower =  self.numberFactory.getNumber(17) 
        self.greaterThan23_17.higher =  self.numberFactory.getNumber(23)
	
        self.greaterThan23_18 = self.addObject(GreaterThan()) 
        self.greaterThan23_18.lower =  self.numberFactory.getNumber(18) 
        self.greaterThan23_18.higher =  self.numberFactory.getNumber(23)
	
        self.greaterThan23_19 = self.addObject(GreaterThan()) 
        self.greaterThan23_19.lower =  self.numberFactory.getNumber(19) 
        self.greaterThan23_19.higher =  self.numberFactory.getNumber(23)
	
        self.greaterThan23_20 = self.addObject(GreaterThan()) 
        self.greaterThan23_20.lower =  self.numberFactory.getNumber(20) 
        self.greaterThan23_20.higher =  self.numberFactory.getNumber(23)
	
        self.greaterThan23_21 = self.addObject(GreaterThan()) 
        self.greaterThan23_21.lower =  self.numberFactory.getNumber(21) 
        self.greaterThan23_21.higher =  self.numberFactory.getNumber(23)




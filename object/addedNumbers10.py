from poodle.poodle import * 
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


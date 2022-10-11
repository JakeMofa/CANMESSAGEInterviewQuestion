class CANMessage:
    """Class representing a CAN message"""
    identifier: int 
    data: int = []
    def __init__(self, identifier: int, data: int = []):
        self.identifier = identifier
        self.data = data
                
    def analogDigitalFeedback(self):
        feedBackMsg = {} #define dictionary variable
        feedBackMsg["Feed_Back_and_Diagnostics_Identifier"]= self.data[0]; # since whole 1 byte value contains FDI, 
        '''# bit 7 & 8 represent DI 4 value. when shift by 6, it contains last 2 bits (7 & 8).
        # **001100>>6 will be **. then this value is the DI 4.'''
        feedBackMsg["Digital_Input_4"] =  self.data[1]>>6; 
        '''# bit 5 & 6 represent DI 3 value. when perform & operation with value 0x30 (48d), 
        # it remains only bit 5 & 6 in original value and make other valaues to zero (0). 
        # shifting by 4 make value with only bit 5 & 6.
        # 11**1100>>4 will be **. then this value is the DI 3.'''       
        feedBackMsg["Digital_Input_3"] =  (self.data[1] & 0x30)>>4;
        '''# bit 3 & 4 represent DI 2 value. when perform & operation with value 0x0C (12d), 
        # it remains only bit 3 & 4 in original value and make other valaues to zero (0). 
        # shifting by 4 make value with only bit 5 & 6.
        # 1111**11>>2 will be **. then this value is the DI 2. ''' 
        feedBackMsg["Digital_Input_2"] =  (self.data[1] & 0x0C)>>2;
        '''# bit 1 & 2 represent DI 1 value. when perform & operation with value 0x03 (3d), 
        # it remains only bit 1 & 2 in original value and make other valaues to zero (0). 
        # 000000** will be **. then this value is the DI 1. '''
        feedBackMsg["Digital_Input_1"] =  (self.data[1] & 0x03);
        
        ###  DI 8 same as DI 4.      
        feedBackMsg["Digital_Input_8"] =  self.data[2]>>6;
        ###  DI 7 same as DI 3.
        feedBackMsg["Digital_Input_7"] =  (self.data[2] & 0x30)>>4;
        ###  DI 6 same as DI 2.
        feedBackMsg["Digital_Input_6"] =  (self.data[2] & 0x0C)>>2;
        ###  DI 5 same as DI 1.
        feedBackMsg["Digital_Input_5"] =  (self.data[2] & 0x03);
        
        ###  DI 12 same as DI 3.
        feedBackMsg["Digital_Input_12"] =  self.data[3]>>6;
        ###  DI 11 same as DI 3.
        feedBackMsg["Digital_Input_11"] =  (self.data[3] & 0x30)>>4;
        ###  DI 10 same as DI 2.
        feedBackMsg["Digital_Input_10"] =  (self.data[3] & 0x0C)>>2;
        ###  DI 9 same as DI 1.
        feedBackMsg["Digital_Input_9"] =  (self.data[3] & 0x03);

        ''' Analog input contains 10 bits (1023d). 2 bits of MSB is in one byte and other 8 bits in another byte.
        # since 2 bits in seperate byte, 1st MSB represent value of 512 and 2nd MSB represent 256. other remaining 8 bits represnt value up to 255
        # to get the value, 1st MSB bit should be multiplied by 512 and add to total value.
        # 2nd MSB should be multiplied by 256 and add to total value. The remaining value of the byte should be added to total to make analog value.
        # total = 1STmsb*512 + 2ndMSB*256 + LSB byte.''' 
        #analog raw value in range 0-1023
        analog1_raw_value = self.data[4] + (self.data[5] & 0x01)*256 + ((self.data[5] & 0x02)>>1)*512; 
        analog2_raw_value = self.data[6]+ (self.data[7] & 0x01)*256 + ((self.data[7] & 0x02)>>1)*512;
        analog1_voltage = analog1_raw_value*5/1023; #get voltage value in range 0-5 V
        analog2_voltage = analog2_raw_value*5/1023;
        feedBackMsg["Analog_Input_1"] = round(analog1_voltage,3); #set the value with 3 decimal place
        feedBackMsg["Analog_Input_2"] = round(analog2_voltage,3); 
        
        #return dictionary
        return feedBackMsg
        
    
incoming_message = CANMessage(identifier=int('18EF171E',16),data=[0,201,90,255,255,160,0,246])
print(incoming_message.identifier)
print(incoming_message.data)
#Write a function which takes a CANMessage as input and returns a dictionary containing the values of the message in 4.5.1 
#print the dictionary related to the input
print(incoming_message.analogDigitalFeedback())

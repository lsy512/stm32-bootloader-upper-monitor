import serial
import binascii
import sys
import time
import decimal  

def crc_js(data_in,length):
    crc_cal=0
    for i in range(0,length):
        #print binascii.b2a_hex(data_in[i])

        temp=ord(data_in[i])
       # print temp
        crc_cal  =  crc_cal + temp
    crc_cal_h=crc_cal>>8
    crc_cal_l=crc_cal&255
    #print crc_cal_h,crc_cal_l
    
    return crc_cal_h|crc_cal_l
    #return crc_cal

    
#get file 
f = open('RTK.bin','rb')
byte = f.read()
#print binascii.b2a_hex(byte)
#print '%x'%4
f.close()
size_file= sys.getsizeof(byte)

byte=list(byte)
print crc_js(byte,32)


for_sum= size_file/32
if size_file%32:
    for_sum=for_sum+1
print for_sum


try:
    t = serial.Serial('com22',9600)
except Exception, e:
    print 'open serial failed.'
    exit(1) 

start_time=time.time()
#send start
byte_start=['#',0x01,0x01,'#','#','#']
byte_end=['#',0x01,0x00,'#','#','#']
crc=[0xff,0xff]
print 'send start'
n = t.write(byte_start)
time.sleep(1)

str_r = t.read(20)
#crc_cal1=str(crc_js(str_r,19))
#print type(str_r[19]),str_r[19]
#print type(crc_cal1),crc_cal1

#if str[19]==crc_cal1:
#    print binascii.b2a_hex(str)

print 'send firm'

print for_sum
j=0
for i in range(1,for_sum):
    i_count=(i-1)*32
    newarr = byte[i_count:i_count+32]
    if len(newarr)!=32:
        len_sub=32-len(newarr)
        list_ff = len_sub * ['\xff']
        newarr=newarr+list_ff
        print newarr
    
    crc_end= crc_js(newarr,32)
    newarr.append(crc_end)
        
    n = t.write(newarr)
    true=1
    while true:
        str = t.read(20)
        t.flushInput()
        true=0
    #print round(float(i)/for_sum,3)
    #time.sleep(0.01)
    #j=j+1
    #print j
  
time.sleep(1)
n = t.write(byte_end)

end_time=time.time()

print end_time-start_time

print 'firmware write succeed!'
#print t.portstr    
#print n    
#str = t.read(n)

#print list(str)




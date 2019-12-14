'''
Created on 2017. 7. 3.

@author: cspri
'''

def srcname(src):
    returnvalue = 0
    if src.find("yonhapnews") > -1 :
        returnvalue = 1
        print (src )          
    elif src.find("joins") > -1:
        returnvalue = 2    
        
        
    return returnvalue   
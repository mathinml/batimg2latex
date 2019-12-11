#!/usr/bin/env python
# coding: utf-8


import os
import json
import glob
import time
import base64
import requests


#
# Common module for calling Mathpix OCR service from Python.
#
# N.B.: Set your credentials in environment variables APP_ID and APP_KEY,
# either once via setenv or on the command line as in
# APP_ID=my-id APP_KEY=my-key python3 simple.py 
#

env = os.environ

default_headers = {
    'app_id': env.get('APP_ID', 'Your_APP_ID'),
    'app_key': env.get('APP_KEY', 'Your_APP_KEY'),
    'Content-type': 'application/json'
}

service = 'https://api.mathpix.com/v3/latex'

#
# Return the base64 encoding of an image with the given filename.
#
def image_uri(filename):
    image_data = open(filename, "rb").read()
    return "data:image/jpg;base64," + base64.b64encode(image_data).decode()

#
# Call the Mathpix service with the given arguments, headers, and timeout.
#
def latex(args, headers=default_headers, timeout=30):
    r = requests.post(service,
        data=json.dumps(args), headers=headers, timeout=timeout)
    return json.loads(r.text)


raw_dict = {
         '\a':r'\a', '\b':r'\b', '\c':r'\c', '\f':r'\f',
         '\n':r'\n', '\r':r'\r', '\t':r'\t', '\v':r'\v',
         '\'':r'\'', '\"':r'\"', '\0':r'\0', '\1':r'\1',
         '\2':r'\2', '\3':r'\3', '\4':r'\4', '\5':r'\5',
         '\6':r'\6', '\7':r'\7', '\8':r'\8', '\9':r'\9'}

"""Return a raw string representation of script"""
def raw(script): 

    new_script = ''
    for char in script:
        try:
            new_script += raw_dict[char]
        except KeyError:
            new_script += char
    return new_script


def mathpix_dir(pngs):
    t = time.strftime('%H_%M_%S_')+time.strftime('%d_%m_%Y')
    filename = 'latex_script_'+t+'.tex'
    sfile = open(filename,'w') 
    
    sfile.write('%%'+t+'\n\n')
    for i,pic in enumerate(pngs):
        r = latex({
            'src': image_uri(pic),
            'formats': ['latex_styled']
        })
        equ = r['latex_styled']
        
        
        latexscript = '%%{}\n$$\n{}\n$$\n\n\n'.format(pic,raw(equ))
        print(latexscript)
        sfile.write(latexscript)
        
    sfile.close()    

if __name__ == '__main__':

    equ_png_dir = 'equ_png'
    pnglist = glob.glob(equ_png_dir+'/*.png')
    
    mathpix_dir(pnglist)


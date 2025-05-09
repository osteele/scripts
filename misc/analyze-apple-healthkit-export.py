import os
import re
import xml
import xml.etree
from xml.etree import ElementTree as ET

tree = ET.parse(os.path.expanduser('~/Desktop/apple_health_export/export.xml'))

tree = ET.iterparse(os.path.expanduser('~/Desktop/apple_health_export/export.xml'))

#%%
for event, elem in tree:
    print(event)
    if event == 'end':
        print(elem)
    break
#%%

len('b10cf6ae-4b4e-46ae-9d11-8d3e281f6bfb')
bool(re.match('kernel-[0-9a-f-]{36}\.json', 'kernel-b10cf6ae-4b4e-46ae-9d11-8d3e281f6bfb.json'))

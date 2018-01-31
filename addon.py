"""An addon for getting Kodi setup and configured

"""


import xbmc
import xbmcaddon
import xbmcgui
import xbmcvfs

import json
import os
import sys

#from resources.lib import classes, sources, utils, xml_parser


def jsonrpc(params, method='Addons.ExecuteAddon', addonid='script.kodi_setter_upper'):
    """Send a JSON-RPC command
    
    """
    # build out the data to be sent
    payload = {'jsonrpc': '2.0', 'method': method, 'id': '1'}
    payload['params'] = {'addonid': addonid, 'params': params}

    # format the data
    data = json.dumps(payload)

    # local JSON-RPC
    response = json.loads(xbmc.executeJSONRPC(data))

    if 'result' in response:
        response = response['result']

    xbmc.sleep(1000)
    return response


if __name__ == '__main__':
    opts = ["Modify 'advancedsettings.xml'",
            "Remove 'advancedsettings.xml'"]

    select = xbmcgui.Dialog().select('Kodi Setter-Upper', opts, 0)
    if select >= 0:
        selection = opts[select]
        
        if selection == "Remove 'advancedsettings.xml'":
            if xbmcvfs.exists(xbmc.translatePath('special://userdata/advancedsettings.xml')):
                xbmcvfs.delete(xbmc.translatePath('special://userdata/advancedsettings.xml'))
        
        elif selection == "Modify 'advancedsettings.xml'":
            host = xbmcaddon.Addon('script.mysql_setter_upper').getSetting('host')
            if host in ['0.0.0.0', '']:
                xbmcaddon.Addon('script.mysql_setter_upper').setSetting('host', '')
                host = 'localhost'
                
            path_from = xbmcaddon.Addon('script.mysql_setter_upper').getSetting('path_from')
            path_to = xbmcaddon.Addon('script.mysql_setter_upper').getSetting('path_to')
            
            response = jsonrpc({'ksu_class': 'AdvancedSetting', 'id': 'musicdatabase.type', 'value': 'mysql'})
            response = jsonrpc({'ksu_class': 'AdvancedSetting', 'id': 'musicdatabase.host', 'value': host})
            response = jsonrpc({'ksu_class': 'AdvancedSetting', 'id': 'musicdatabase.port', 'value': '3306'})
            response = jsonrpc({'ksu_class': 'AdvancedSetting', 'id': 'musicdatabase.user', 'value': 'kodi'})
            response = jsonrpc({'ksu_class': 'AdvancedSetting', 'id': 'musicdatabase.pass', 'value': 'kodi'})
            
            response = jsonrpc({'ksu_class': 'AdvancedSetting', 'id': 'videodatabase.type', 'value': 'mysql'})
            response = jsonrpc({'ksu_class': 'AdvancedSetting', 'id': 'videodatabase.host', 'value': host})
            response = jsonrpc({'ksu_class': 'AdvancedSetting', 'id': 'videodatabase.port', 'value': '3306'})
            response = jsonrpc({'ksu_class': 'AdvancedSetting', 'id': 'videodatabase.user', 'value': 'kodi'})
            response = jsonrpc({'ksu_class': 'AdvancedSetting', 'id': 'videodatabase.pass', 'value': 'kodi'})
            
            response = jsonrpc({'ksu_class': 'AdvancedSetting', 'id': 'videolibrary.importwatchedstate', 'value': 'true'})
            response = jsonrpc({'ksu_class': 'AdvancedSetting', 'id': 'videolibrary.importresumepoint', 'value': 'true'})
            
            if path_from and path_to:
                jsonrpc({'ksu_class': 'AdvancedSetting', 'id': 'pathsubstitution.substitute.from', 'value': path_from})
                jsonrpc({'ksu_class': 'AdvancedSetting', 'id': 'pathsubstitution.substitute.to', 'value': path_to})

            xbmcgui.Dialog().ok('MySQL Setter-Upper', "Successfully modified 'advancedsettings.xml'")


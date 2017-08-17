#!/usr/bin/env python

# GIMP Unified Resource Manager (GURM)
# The idea for GURM is based on the Brush Manager by Sean Bogie

# GURM v0.7 was done by Sagenlicht from Cartographers Guild
# http://cartographersguild.com

# Version 0.8.4
# Update by Mike Bush 2013 bushsteven32@yahoo.com
# Modified by Steve J. Bush 2012 bushsteven32@yahoo.com
     
# v0.9 by damo, August 2017
# Some changes for Linux, instead of Windows; bugfixes; easier user settings.

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

###### USER SETTINGS ###################################################
#
# Place gurm.py and gurm.ini in the plug-ins directory
gurm_file = "/home/damo/.config/GIMP/2.9/plug-ins/gurm.ini" 

winIcon = "/usr/share/gimp/2.0/images/wilber.png"

# The following values are px
tabWidth = 66   # tab width
winHeight = 400 # gui window height
boxHeight = 60  # status box height, OK-CLOSE buttons box height
boxWidth = 240  # status box width (Manager name length is relevant)
padding = 10    # list box padding

###### END USER SETTINGS ###############################################


import pygtk
pygtk.require('2.0')
import gtk
import shutil
import os
import sys

try:
    from gimpfu import *                
    import gimp
except ImportError:   
    def main():
        do_gurm()
        
class Config:
    def  read(self):
        try:
            f = open(os.path.dirname(__file__) + os.sep + "gurm.ini","r")
            configFile = f.readlines()
            f.close()
            return configFile
        except:
            dummy = []
            Error().ini_error(dummy).Error().gtkcall()
            
    def write(self, resourceType, configFile):
        for resource in resourceType.keys():
            newConfigFile = []
            foundResource = False
            newInstalledOptions = ""
            tmpLine = []
            for line in configFile:
                if foundResource:
                    if "installedOptions" in line:
                        for i in resourceType[resource]["activeList"]:
                            newInstalledOptions = newInstalledOptions + ("%s" % i + ",")
                        tmpLine = line.split("=")
                        tmpLine = tmpLine[0].strip() + (" = ") + newInstalledOptions + ("\n")
                        newConfigFile.append(tmpLine)
                        foundResource = False
                    else:
                        newConfigFile.append(line)
                else:
                    newConfigFile.append(line)
                    if resource in line:
                        foundResource = True
            configFile = newConfigFile
        f = open(os.path.dirname(__file__) + os.sep + "gurm.ini","w")
        for line in configFile:
            f.write(line)
        f.close
        
    def verify(self):
        wrongPaths = []
        for resource in self.resourceType.keys():
            if os.path.exists(self.resourceType[resource]["gimpPath"]) == False:
                tmpString ="%s" % resource + " gimpPath\n(" + "%s" % self.resourceType[resource]["gimpPath"] + ")\n"
                wrongPaths.append(tmpString)
            if os.path.exists(self.resourceType[resource]["userPath"]) == False:
                tmpString = "%s" % resource + " userPath\n(" + "%s" % self.resourceType[resource]["userPath"] + ")\n"
                wrongPaths.append(tmpString)
        return wrongPaths
        
    def get_gurm_config(self, configFile):
        self.resourceType = {"Brushes" : {"useManager" : "", "gimpPath" : "", "userPath" : "", "extensions" : "", "installedOptions" : "", "folders" : [], "chkbx" : [], "copyList": [], "activeList": [], "vbox" : gtk.VBox()},\
                "Fonts" : {"useManager" : "", "gimpPath" : "", "userPath" : "", "extensions" : "", "installedOptions" : "", "folders" : [], "chkbx" : [], "copyList": [], "activeList": [], "vbox" : gtk.VBox()},\
                "Gradients" : {"useManager" : "", "gimpPath" : "", "userPath" : "", "extensions" : "", "installedOptions" : "", "folders" : [], "chkbx" : [], "copyList": [], "activeList": [], "vbox" : gtk.VBox()},\
                "Palettes" : {"useManager" : "", "gimpPath" : "", "userPath" : "", "extensions" : "", "installedOptions" : "", "folders" : [], "chkbx" : [], "copyList": [], "activeList": [], "vbox" : gtk.VBox()},\
                "Patterns" : {"useManager" : "", "gimpPath" : "", "userPath" : "", "extensions" : "", "installedOptions" : "", "folders" : [], "chkbx" : [], "copyList": [], "activeList": [], "vbox" : gtk.VBox()},\
                "Plug-ins" : {"useManager" : "", "gimpPath" : "", "userPath" : "", "extensions" : "", "installedOptions" : "", "folders" : [], "chkbx" : [], "copyList": [], "activeList": [], "vbox" : gtk.VBox()},\
                "Dynamics" : {"useManager" : "", "gimpPath" : "", "userPath" : "", "extensions" : "", "installedOptions" : "", "folders" : [], "chkbx" : [], "copyList": [], "activeList": [], "vbox" : gtk.VBox()},\
                "Scripts" : {"useManager" : "", "gimpPath" : "", "userPath" : "", "extensions" : "", "installedOptions" : "", "folders" : [], "chkbx" : [], "copyList": [], "activeList": [], "vbox" : gtk.VBox()}}

        for resource in self.resourceType.keys():
            gotAll = 0
            numTabs = 1
            foundResource = False
            for line in configFile:
                if not gotAll == 5:
                    if foundResource:
                        if "useManager" in line:
                            tmpText = line.split("=")
                            if tmpText[1].strip() in ["yes", "Yes", "True", "true", "TRUE"]:
                                self.resourceType[resource]["useManager"] = True
                            else:
                                self.resourceType[resource]["useManager"] = False
                            gotAll += 1
                        if "gimpPath" in line:
                            tmpText = line.split("=")
                            self.resourceType[resource]["gimpPath"] = tmpText[1].strip()
                            gotAll += 1
                        if "userPath" in line:
                            tmpText = line.split("=")
                            self.resourceType[resource]["userPath"] = tmpText[1].strip()
                            gotAll += 1
                        if "extensions" in line:
                            tmpText = line.split("=")
                            extensionsRaw = tmpText[1].strip()
                            self.resourceType[resource]["extensions"] = extensionsRaw.split(",")[:-1]
                            gotAll += 1
                        if "installedOptions" in line:
                            tmpText = line.split("=")
                            installedRaw = tmpText[1].strip()
                            self.resourceType[resource]["installedOptions"] = installedRaw.split(",")[:-1]
                            gotAll += 1
                    else:
                        if resource in line:
                            foundResource = True

        for resource in self.resourceType.keys():
            if self.resourceType[resource]["useManager"] == False:
                del self.resourceType[resource]
            else:
                numTabs = numTabs + 1
                
        verifyPaths = self.verify()
        if verifyPaths == []:
            for resource in self.resourceType.keys():
                for i in os.listdir(self.resourceType[resource]["userPath"]):
                    if os.path.isdir(os.path.join(self.resourceType[resource]["userPath"],i)):
                        self.resourceType[resource]["folders"].append(i)
            return self.resourceType, numTabs
        else:
            Error().ini_error(verifyPaths).Error().gtkcall()
            
class Error:
    def ini_error(self, errorGiven):
        if errorGiven == []:
            resultLabel = "gurm.ini not found"
            errorMessage = "gurm.ini was not found\nPlease verify the file's existence, and its path is in /plug-ins"
        else:
            resultLabel  = "Wrong Paths"
            tmpString = ""
            for error in errorGiven:
                tmpString = tmpString + "%s" % error + "\n"
            errorMessage = "Following paths in the gurm.ini couldn't be verified:\n\n" + tmpString
        msgWindow = gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK, message_format=errorMessage)
        msgWindow.set_title(resultLabel)
        msgWindow.show()
        msgWindow.run()
        msgWindow.destroy()
        sys.exit()
        
    #def gtk_call(self):
        #gtk.main()
        
class GUI:
    def dialog_delete(self, widget, event, data=None):
        return True
        
    def makedialog( self ):
        self.dialog = gtk.Dialog("Please Wait...", self.window,
            gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT)
        self.dialog.connect("delete_event", self.dialog_delete)
        self.dialog.set_size_request( boxWidth, boxHeight )
        self.statuslabel = gtk.Label("Status:")
        self.dialog.vbox.pack_start(self.statuslabel, False, False, 0)
        self.progressbar = gtk.ProgressBar()
        self.dialog.vbox.pack_start(self.progressbar, False, True, 0)
        
    def showdialog(self):
        self.statuslabel.show()
        self.progressbar.show()
        self.dialog.show()
        
    def fileList(self, path, extensions):
        files=[]
        for i in os.listdir(path):
            if os.path.splitext(i)[1] in extensions:
                if os.path.isfile(os.path.join( path,i)):
                    files.append(i)
        return files
        
    def do_copy(self, removeList):
        count = 0
        totalAdd = 0
        for resource in self.resourceType.keys():
            totalAdd = totalAdd +len((self.resourceType[resource]["copyList"]))
        total = totalAdd + len(removeList)
        self.makedialog()
        self.showdialog()
        self.progressbar.set_fraction(1)
        self.statuslabel.set_text("Status: Removing old files...")
        for file in removeList:
            gtk.main_iteration()
            try:
                os.remove(file)
            except:
                continue
            finally:
                count += 1
                self.progressbar.set_fraction(count/total)
        self.statuslabel.set_text("Status: Copying new files...")
        for resource in self.resourceType.keys():
            for file in self.resourceType[resource]["copyList"]:
                gtk.main_iteration()
                try:
                    shutil.copy(file, self.resourceType[resource]["gimpPath"])
                except:
                    continue
                finally:
                    count += 1
                    self.progressbar.set_fraction(count/total)
        for resource in self.resourceType.keys():
            gtk.main_iteration()
            self.statuslabel.set_text("Status: Refreshing " + "%s" % resource + " list...")
            gtk.main_iteration()
            try:
                if resource == "Brushes":
                    pdb.gimp_brushes_refresh()
                if resource == "Dynamics":
                    pdb.gimp_dynamics_refresh()                    
                if resource == "Fonts":
                    pdb.gimp_fonts_refresh()                    
                if resource == "Gradients":         
                    pdb.gimp_gradients_refresh()                                                                          
                if resource == "Palettes":
                    pdb.gimp_palettes_refresh()                         
                if resource == "Patterns":
                    pdb.gimp_patterns_refresh()                         
                if resource == "Plug-ins":         
                    pdb.script_fu_refresh()                         
                if resource == "Scripts":
                    pdb.script_fu_refresh()                         
            except: 
                pass
                
    def ok_clicked(self, *args):
        removeList = []
        for resource in self.resourceType.keys():
            for dir in self.resourceType[resource]["chkbx"]:
                if dir.get_active():
                    self.resourceType[resource]["activeList"].append( dir.get_label())
        for resource in self.resourceType.keys():
            for i in self.resourceType[resource]["activeList"]:
                if not i in self.resourceType[resource]["installedOptions"]:
                    for j in self.fileList(os.path.join(self.resourceType[resource]["userPath"], i), self.resourceType[resource]["extensions"]):
                        self.resourceType[resource]["copyList"].append(os.path.join(self.resourceType[resource]["userPath"], i, j))
        for resource in self.resourceType.keys():
            for i in self.resourceType[resource]["installedOptions"]:
                if not i in self.resourceType[resource]["activeList"]:
                    for j in self.fileList(os.path.join(self.resourceType[resource]["userPath"], i), self.resourceType[resource]["extensions"]):
                        removeList.append(os.path.join(self.resourceType[resource]["gimpPath"], j))
        self.do_copy(removeList)
        writeConfig = Config().write(self.resourceType, self.configFile)
        gtk.main_quit()
        
    def destroy(self, *args):
        gtk.main_quit()
        
    def __init__(self):
        self.configFile = Config().read()
        self.resourceType, self.numTabs = Config().get_gurm_config(self.configFile)
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("destroy", self.destroy)
        self.window.set_title("GIMP Unified Resource Manager")
        self.window.set_icon_from_file(winIcon)
        self.window.set_border_width(1)
        self.window.set_size_request((tabWidth*(self.numTabs)), winHeight)
        self.window.set_position(gtk.WIN_POS_CENTER)
        self.window.show()
        self.mainBox = gtk.VBox()
        self.mainBox.set_border_width(1)
        self.mainBox.set_size_request((tabWidth*(self.numTabs)), winHeight)
        self.window.add(self.mainBox)
        self.mainBox.show()
        self.resourceBox = gtk.VBox()
        self.resourceBox.set_border_width(1)
        self.resourceBox.set_size_request((tabWidth*(self.numTabs)), winHeight-boxHeight)
        self.mainBox.pack_start( self.resourceBox, True, True, 0 )
        self.resourceBox.show()
        self.resourceBook = gtk.Notebook()
        self.resourceBook.set_tab_pos(gtk.POS_TOP)
        self.resourceBox.pack_start( self.resourceBook, True, True, 0 )
        self.resourceBook.show()
        for resource in sorted(self.resourceType.keys()):
            windowHeight = boxHeight
            self.resourceType[resource]["folders"].sort()
            for dirs in self.resourceType[resource]["folders"]:
                windowHeight = windowHeight + 25
                self.resourceType[resource]["chkbx"].append(gtk.CheckButton(os.path.split(dirs)[1]))
            for dirs in self.resourceType[resource]["chkbx"]:
                self.resourceType[resource]["vbox"].pack_start(dirs, False, False, 1)
                if dirs.get_label() in self.resourceType[resource]["installedOptions"]:
                    dirs.set_active(True)
                dirs.show()
            self.tmpBox = gtk.VBox()
            self.tmpBox.set_border_width(1)
            self.tmpBox.set_size_request(boxWidth, winHeight)
            self.tmpBox.show()
            scroll_box = gtk.ScrolledWindow()
            scroll_box.set_border_width(1)
            scroll_box.set_policy( gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC )
            self.tmpBox.pack_start(scroll_box, True, True, 0)
            scroll_box.show()
            self.pageLabel = gtk.Label("%s" %  resource )
            self.pageLabel.show()
            self.resourceType[resource]["vbox"].set_border_width(padding)
            self.resourceType[resource]["vbox"].set_size_request(boxWidth, windowHeight)
            self.resourceType[resource]["vbox"].show()
            scroll_box.add_with_viewport(self.resourceType[resource]["vbox"])
            self.resourceBook.append_page(self.tmpBox, self.pageLabel)
        self.tmpBox = gtk.VBox()
        self.tmpBox.set_border_width(1)
        self.tmpBox.set_size_request(boxWidth, boxHeight)
        self.tmpBox.show()
        scroll_box = gtk.ScrolledWindow()
        scroll_box.set_border_width(1)
        scroll_box.set_policy( gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC )
        self.tmpBox.pack_start(scroll_box, True, True, 0)
        scroll_box.show()
        self.pageLabel = gtk.Label("About\nGURM")
        self.pageLabel.show()
        aboutBox = gtk.VBox()
        aboutBox.set_border_width(1)
        aboutBox.set_size_request(boxWidth, boxHeight)
        aboutBox.show()
        aboutLabel = gtk.Label("GURM\n<b>GIMP Unified Resource Manager</b>\n"\
                    + ("<b>Version 0.9</b>")
                    + ("\n\nGURM v0.7: original script by Sagenlicht from Cartographers Guild")
                    + ("\nGURM v0.8.4: by R.M. Bush 2013")
                    + ("\n\nGURM v0.9: Further modified for Linux by damo, August 2017\n\n\n\n\n\n"))
        aboutLabel.set_use_markup(True)
        aboutLabel.set_justify(gtk.JUSTIFY_CENTER)
        aboutBox.pack_start(aboutLabel, True, True, 0)
        aboutLabel.show()
        scroll_box.add_with_viewport(aboutBox)
        self.resourceBook.append_page(self.tmpBox, self.pageLabel)
        self.resourceBook.set_current_page(0)
        self.buttonBox = gtk.HButtonBox()
        self.buttonBox.set_layout(gtk.BUTTONBOX_END)
        self.buttonBox.set_spacing(20)
        self.buttonBox.set_border_width(1)
        self.buttonBox.set_size_request((tabWidth*(self.numTabs)), boxHeight)
        self.mainBox.pack_start(self.buttonBox, True, True, 1)
        self.buttonBox.show()
        closeButton = gtk.Button( stock = gtk.STOCK_CLOSE )
        closeButton.connect_object( "clicked", gtk.Widget.destroy, self.window)
        self.buttonBox.add(closeButton)
        closeButton.show()
        okButton = gtk.Button(stock = gtk.STOCK_OK)
        okButton.connect("clicked", self.ok_clicked)
        self.buttonBox.add(okButton)
        okButton.show()
        
    def gtk_call(self):
        gtk.main()
        
def do_gurm():
    gurmCall = GUI()
    gurmCall.gtk_call()

try: 
    register(
        "python_fu_gurm",
        "Gimp Unified Resource Manager",
        "Gimp Unified Resource Manager",
        "Christian Kremer/R.M.Bush/damo",
        "Christian Kremer/R.M.Bush/damo",
        "2017",
        "GURM",
        "",
        [],
        [],
        do_gurm,
        menu="<Image>/GURM")
except:
    pass
    
main()

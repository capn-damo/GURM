# GURM
**GIMP Unified Resource Manager**

A GIMP plug-in script to manage installed resources - just load what is needed:

* Brushes
* Dynamics
* Fonts
* Gradients
* Palettes
* Patterns
* Plug-ins
* Scripts

![GURM](gurm-scrot.png)

The idea for GURM is based on the Brush Manager by Sean Bogie, and developed
as [GURM v0.7](http://registry.gimp.org/node/13473) by Sagenlicht, from [Cartographers Guild](http://cartographersguild.com)

It was further developed as [GURM v0.8](http://gimpscripts.com/2012/10/gurm-gimp-unified-resource-manager/), specifically for
Windows, by Steve Bush. This is the version that I have modified for Linux: 
* bugfixes
* cleaned the code
* made the user settings simpler
* added GIMP window icon
* autosize the window, depending on the number of tabs

## Installation

**Table of Contents**

1. What is GURM?
1. Initial Setup
1. How to use GURM
1. What GURM can't do
1. Error Handling 


1.**What is Gurm?**  

  + Gimp Unified Resource Manager (GURM) is a python script and plug-in for GIMP. GURM allows you to handle the addition and removal of resources in GIMP via a small GTK2 GUI. This can significantly speed up loading times and browsing of panels, if you have a large collection of resources.
  
  + Currently the plug-in can handle Brushes, Dynamics, Fonts, Gradients, Palettes, Patterns, Plug-ins and  
  Script-Fu scripts.

2.**Initial Setup**  

   - Prepare GIMP  
  
     Presumably, at the moment you have a lot of resources already in your GIMP folders, and you
     have to clear them before starting to use GURM. All that should be left in `/plug-ins` are `gurm.py` 
     and `gurm.ini`.
        
     Now before you do anything BACKUP your GIMP resource folders (/brushes, /dynamics, /fonts, /gradients, 
     /palettes, /patterns, /plug-ins and /scripts). Then copy the files to the directories you just created.
        
     For example, move everything in `"$HOME/.config/GIMP/<your gimp version>/brushes"` to 
     `"$HOME/graphics/gimp/gimp-resources/brushes"`
        
      Do the same for all the other directories.
      
  - "Installation"  
      * Copy `gurm.py` into your plug-ins folder, which is *normally* located at:  
          `$HOME/.config/GIMP/<your gimp version>/plug-ins`
            
      * Copy `gurm.ini` wherever you want; it is recommended you copy it to the same folder.
        
  - Prepare the python script  
     *  Open `gurm.py` and edit the line beginning "gurm_file = ". It has to be the path to
        where you placed `gurm.ini`. The line should look something like:
        ```
        gurm_file = "<$HOME>/.config/GIMP/<your gimp version>/plug-ins/gurm.ini"  
        ```

  - Prepare the gurm.ini  
     * Edit `gurm.ini`: for every manager type you have to edit "gimpPath" and "userPath". 
     * The **gimpPath**  
            You have to add the path to your GIMP resource folder of the specific manager. 
            Please be sure to NOT use quotations in this file.
            For example, edit the Brush Manager gimpPath to look like:  
            ```
            gimpPath = <$HOME>/.config/GIMP/<your gimp version>/brushes
            ```
     * The **userPath**  
        The userpath is the path where you store all of your files for that manager; you can create 
        this folder wherever you want to. Then add that path to the userPath in the gurm.ini.
        For example, edit the Brush Manager userPath to look like: 
        ```
        userPath = <$HOME>/graphics/gimp/gimp-resources/brushes
        ```
    
  - Prepare the user folders
  
     For every set of resources you plan to use, create another directory for them. Say you have 4
     sets of brushes: one for grunge brushes, one for cloud brushes, one for leaves and one for all the
     other brushes. Create these in the user directory:
     ```
     <$HOME>/graphics/gimp/gimp-resources/brushes/{grunge,cloud,leaves,other}
     ```
            
     Do the same for the other resources (Dynamics, Fonts, Gradients, Palettes, Patterns, Plug-ins and 
     Scripts).

  - useManager
  
     If you don't want to use one of the managers GURM provides, simply replace the "yes"
     with a "no" in the useManager row of the Manager.
     For example: you don't want to use the Palette Manager:
        
     Edit `gurm.ini` and browse to [Palette Manager], the next line should be: `useManager = yes` 
            
     Simply overwrite yes with no and GURM won't use it anymore. (Of course, you don't have to set any paths for 
     the Palette Manager now.). If you want to use it again, just overwrite the `no` with a `yes` again.
        
     The GURM dialog window will adjust its width depending on the number of Manager tabs which are in use.
    

3. **How to use GURM**  

   + The plug-in menu appears on the main menubar of GIMP. Just click on the set of resources you want to use and click "OK". GURM then copies the needed files and refreshes your resource list in GIMP.
        
     If you want to remove a set, uncheck it and then choose "OK" again. GURM will remove the no longer needed files and refreshes your resource list in GIMP. The dialog closes after refreshing the lists.
        
   + Use it without GIMP opened:  
        The script runs as well without GIMP opened. It works exactly the same way as when started from GIMP, except it 
        won't refresh your resource list (although there is no need for it in this case).  
        
   + Change the GURM menu item:  
        If you want the plug-in to appear directly in the GIMP menubar, and not as a GURM menu item, then edit the `register()` function at the end of `gurm.py`. Change:  `menu="<Image>/GURM"` to `menu="<Image>"`

4. **What GURM can't do**  

   +  GURM does not handle zip-archives;  
      
   +  It does not deal with MyPaint brushes;  
      
   +  It does not yet handle other resources, for example tool options, curves, themes etc.
    
5. **Error Handling**  

      Filepath errors in `gurm.py` or `gurm.ini` will be displayed in an error dialog.  
      
      `gurm.py` must be executable: `chmod +x gurm.py`

      If GURM does not copy anything, but everything else seems to work fine, check if you have the needed
      file permissions. Write permissions are needed for the gimpPaths, and for `gurm.ini`. 



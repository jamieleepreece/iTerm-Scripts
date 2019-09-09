#!/usr/bin/env python3.7

# iTerm2 documentation can be found at https://www.iterm2.com/python-api/

import iterm2
from time import sleep

# This script was created with the "basic" environment which does not support adding dependencies
# with pip.

sessions = {};
project_dir = 'cd ~/Sites/{WebsiteName}/Projects \n'
projects = {
    'api.website.co.uk': '', 
    'admin.website.co.uk': '', 
    'www.website.co.uk': ''
}
base = {
    'website-base-api': '', 
}

async def initProjectSpace(session):
    try:
        # Move into main project directory 
        await session.async_send_text(project_dir)

        # Run vagrant 
        await session.async_send_text('vagrant up \n')      

        await session.async_send_text('vagrant ssh \n')       

        await session.async_send_text('cd /var/www/vhosts/ \n')         

    except Exception:
        print('Fault')

async def openSiteDir(session_cur, path, site, project_dir):
    try:

       await session_cur.async_send_text(project_dir)    

       await session_cur.async_send_text('vagrant ssh \n')       

       await session_cur.async_send_text('cd ' + path + site + '\n')   

       await session_cur.async_send_text('clear \n')    

       sleep(1)

    except Exception:
        print('Fault')

async def main(connection):
    # Your code goes here. Here's a bit of example code that adds a tab to the current window:
    app = await iterm2.async_get_app(connection)
    window = app.current_terminal_window

    if window is not None:

        # Restore session if preferable
        # await window.async_restore_window_arrangement('Triple Panel /w Toolbelt')

        await window.async_create_tab()
        await window.async_activate()

        # Set the new window as the current window
        app = await iterm2.async_get_app(connection)
        window = app.current_terminal_window

        # Get the current active pane within the window
        current_tab = window.current_tab
        await current_tab.async_set_title('Name of my cool new tab!')

        # Manage session
        sessions['vagrant'] = current_tab.current_session
        current_session = sessions['vagrant']

        # Boot Vagrant
        await initProjectSpace(current_session) 

        # open sites
        for site in projects:

            # current_session = await openSiteDir(current_session, app)

            # New pane
            await current_session.async_split_pane(False)

            window = app.current_terminal_window
            current_tab = window.current_tab

            sessions[site] = current_tab.current_session

            await openSiteDir(sessions[site], '/var/www/vhosts/', site, project_dir) 

            current_session = sessions[site]

        # Open opt 
        for opt in base:

            await current_session.async_split_pane(False)

            window = app.current_terminal_window
            current_tab = window.current_tab

            sessions[opt] = current_tab.current_session

            await openSiteDir(sessions[opt], '/opt/', opt, project_dir)

            current_session = sessions[opt]

        await current_session.async_split_pane(False)

        window = app.current_terminal_window
        current_tab = window.current_tab

        sessions['free'] = current_tab.current_session

        await sessions['free'].async_send_text(project_dir)    
        await sessions['free'].async_send_text('quote \n')    


    else:
        # You can view this message in the script console.
        print("No current window")

iterm2.run_until_complete(main)

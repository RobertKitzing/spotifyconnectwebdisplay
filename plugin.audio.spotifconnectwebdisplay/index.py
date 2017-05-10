import os
import xbmc
import xbmcaddon
import xbmcplugin
import pyxbmct
import requests
import shutil

_addonSettings = xbmcaddon.Addon(id='plugin.audio.spotifconnectwebdisplay')
_language = _addonSettings.getLocalizedString
baseUrl = _addonSettings.getSetting("connectWebHost")

apiUrlMetadata = '/api/info/metadata'
apiUrlControlSpotify = '/api/playback/'
apiUrlImageUrl = '/api/info/image_url/'


class MyAddon(pyxbmct.AddonDialogWindow):
    def __init__(self, title=''):
        super(MyAddon, self).__init__(title)
        self.setGeometry(1000, 563, 3, 6)
        self.createInfoLabels()
        self.updateInfoLabels()
        self.createButtons()
        self.loop = True
        # Connect a key action (Backspace) to close the window.
        self.connect(pyxbmct.ACTION_NAV_BACK, self.stopLoop)
    def stopLoop(self):
        self.loop = False
        self.close()
    def createInfoLabels(self):
        #Artist Infos
        self.artistName = pyxbmct.Label('')
        self.placeControl(self.artistName, 0, 2, 1, 4)
        #Track Infos
        self.trackName = pyxbmct.Label('')
        self.placeControl(self.trackName, 1, 2, 1, 4)
        #Album Infos
        self.albumName = pyxbmct.Label('')
        self.placeControl(self.albumName, 2, 2, 1, 4)
        #Error
        self.errorLabel = pyxbmct.Label('')
        self.placeControl(self.errorLabel, 0, 0, 1, 1)
    def updateInfoLabels(self):
        try:
            metadata = requests.get(baseUrl + apiUrlMetadata).json()
            self.errorLabel.setLabel('')
            #Artist
            self.artistName.setLabel(str(metadata['artist_name']))
            #Album
            self.albumName.setLabel(str(metadata['album_name']))
            #Track
            self.trackName.setLabel(str(metadata['track_name']))
            #Cover
            self.image = pyxbmct.Image(baseUrl + apiUrlImageUrl + metadata['cover_uri'])
            self.placeControl(self.image, 0, 0, 2, 2)
        except Exception as e:
            self.errorLabel.setLabel('Spotify Connect Web Server unavalible')
    def createButtons(self):
        #Pause Button
        self.buttonPause = pyxbmct.Button('Pause')
        self.placeControl(self.buttonPause, 0, 5)
        self.connect(self.buttonPause, lambda: self.controlspotify('pause'))
        #Play Button
        self.buttonPlay = pyxbmct.Button('Play')#
        self.placeControl(self.buttonPlay, 1, 5)
        self.connect(self.buttonPlay,  lambda: self.controlspotify('play'))
        #Next Track Button
        self.buttonNext = pyxbmct.Button('Next')
        self.placeControl(self.buttonNext, 2, 5)
        self.connect(self.buttonNext,  lambda: self.controlspotify('next'))
        #Shuffle Switch
        #self.radioShuffle = pyxbmct.RadioButton('Shuffle')
        #self.radioShuffle.isSelected
        #self.placeControl(self.radioShuffle, 4, 3)
        #Shuffle Switch
        #self.radioRepeat = pyxbmct.RadioButton('Repeat')
        #self.radioRepeat.setSelected(True)
        #self.placeControl(self.radioRepeat, 5, 3)
        #refresh Track Button
        #self.buttonRefresh = pyxbmct.Button('Refresh')
        #self.placeControl(self.buttonRefresh, 4, 3)
        # self.connect(self.buttonRefresh, self.update_infos)
        self.setNavigation()
    def setNavigation(self):
        self.setFocus(self.buttonNext)
        self.buttonPause.controlDown(self.buttonPlay)
        self.buttonPlay.controlDown(self.buttonNext)
        self.buttonNext.controlDown(self.buttonPause)
        #self.radioShuffle.controlDown(self.radioRepeat)
        #self.radioRepeat.controlDown(self.buttonPause)
#
        self.buttonPause.controlUp(self.buttonNext)
        self.buttonPlay.controlUp(self.buttonPause)
        self.buttonNext.controlUp(self.buttonPlay)
        #self.radioShuffle.controlUp(self.buttonNext)
        #self.radioRepeat.controlUp(self.radioShuffle)
    def controlspotify(self, action):
        requests.get(baseUrl + apiUrlControlSpotify + action).read()

if __name__ == '__main__':
    window = MyAddon('Spotify Connect Web Display')
    while window.loop:
        window.updateInfoLabels()
        window.show()
        xbmc.sleep(1000)
    # Destroy the instance explicitly because
    # underlying xbmcgui classes are not garbage-collected on exit.
    del window

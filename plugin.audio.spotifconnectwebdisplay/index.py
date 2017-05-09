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
        self.setGeometry(1024, 720, 9, 4)
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
        self.artistLabel = pyxbmct.Label('')
        self.placeControl(self.artistLabel, 1, 0)
        self.artistName = pyxbmct.Label('')
        self.placeControl(self.artistName, 1, 1)
        #Album Infos
        self.albumLabel = pyxbmct.Label('')
        self.placeControl(self.albumLabel, 5, 0)
        self.albumName = pyxbmct.Label('')
        self.placeControl(self.albumName, 5, 1)
        #Track Infos
        self.trackLabel = pyxbmct.Label('')
        self.placeControl(self.trackLabel, 2, 0)
        self.trackName = pyxbmct.Label('')
        self.placeControl(self.trackName, 2, 1)
        #Cover
        self.coverImage = pyxbmct.Image('')
        self.placeControl(self.coverImage, 3, 1, 3, 2)
        #Error
        self.errorLabel = pyxbmct.Label('')
        self.placeControl(self.errorLabel, 0, 0, 3, 0)
    def updateInfoLabels(self):
        try:
            metadata = requests.get(baseUrl + apiUrlMetadata).json()
            self.errorLabel.setLabel('')
            #Artist
            self.artistLabel.setLabel('Artist')
            self.artistName.setLabel(str(metadata['artist_name']))
            #Album
            self.albumLabel.setLabel('Album')
            self.albumName.setLabel(str(metadata['album_name']))
            #Track
            self.trackLabel.setLabel('Track')
            self.trackName.setLabel(str(metadata['track_name']))
            #Cover
            self.image = pyxbmct.Image(baseUrl + apiUrlImageUrl + metadata['cover_uri'])
            self.placeControl(self.image, 3, 1, 2, 1)
        except Exception as e:
            self.errorLabel.setLabel('Spotify Connect Web Server unavalible') #, Reason: \n {}'.format(e))
    def createButtons(self):
        #Pause Button
        self.buttonPause = pyxbmct.Button('Pause')
        self.placeControl(self.buttonPause, 1, 3)
        self.connect(self.buttonPause, lambda: self.controlspotify('pause'))
        #Play Button
        self.buttonPlay = pyxbmct.Button('Play')#
        self.placeControl(self.buttonPlay, 2, 3)
        self.connect(self.buttonPlay,  lambda: self.controlspotify('play'))
        #Next Track Button
        self.buttonNext = pyxbmct.Button('Next')
        self.placeControl(self.buttonNext, 3, 3)
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
#        self.buttonRefresh = pyxbmct.Button('Refresh')
#        self.placeControl(self.buttonRefresh, 4, 3)
#        self.connect(self.buttonRefresh, self.update_infos)
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
    #window.doModal()
    while window.loop:
        window.updateInfoLabels()
        window.show()
        xbmc.sleep(300)
    # Destroy the instance explicitly because
    # underlying xbmcgui classes are not garbage-collected on exit.
    del window

#{status
#  "active": true,
#  "logged_in": true,
#  "playing": false,
#  "repeat": true,
#  "shuffle": true
#}

#{metadata
#  "album_name": "Does You Inspire You",
#  "album_uri": "spotify:album:3JuIBAoHi6gUmS3tgF4CPg",
#  "artist_name": "Chairlift",
#  "artist_uri": "spotify:artist:7hAolICGSgXJuM6DUpK5rp",
#  "context_uri": "spotify:user:spotify:playlist:37i9dQZF1DWYJeWl6ior4d",
#  "cover_uri": "spotify:image:af1e40ba897686401c9b0db0931ac9176f6e03e2",
#  "data0": "Indie Klassiker",
#  "duration": 241466,
#  "track_name": "Bruises",
#  "track_uri": "spotify:track:4mdyVTV7Tr5YDFnD2kvSM4",
#  "volume": 52428
#}
#status = requests.get(baseUrl + '/api/info/status').json()
#metadata = requests.get(baseUrl + '/api/info/metadata').json()
#albumIMG = requests.get(baseUrl + '/api/info/image_url/' + metadata['cover_uri'])
        #try:
        #    mdr = requests.get(baseUrl + apiUrlMetadata)
        #    mdr.raise_for_status()
        #    metadata = mdr.json()
        #Artist

# QR Alchemy
Tool for generating and processing qr codes with custom actions on linux. Designed to work in both desktop and phone based linux envronments.

## What can it do?
It allows the creation and processing of qr codes. Thus allowing programs like megapixels to handle more qr code types. However, it is not a qr code scanning utility (it won't try to use your camera in any way).
Offers the following features:
 * Allows system to handle new types of qr codes with default settings. Currently supports:
   * Wifi
 * Allows the users to generate and display their own qr codes to share with friends such as:
   * Your current wifi network credentials
   * a custom code written by you
 * Supports creating plugins to allow you to handle your own qr code types via input plugins (see the Input Plugins section for instructions)
 * Supports creating plugins to display custom qr codes via output plugins (see the Output Plugins section for instructions)
 * Allows the offering of the custom defined codes to the system to allow for programs to send the requests to qr_alchemy.
 * Allows the saving of qr codes for later, as well as a brief history of the ones used.

## Legal/Warranty
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


## Installation Instructions
 1. Download a copy of this from Releases section: https://github.com/steve5289/qr_alchemy/releases/

 2. Install the needed dependancies:
```
apt-get update
apt-get install zbar qrencode python3 gnome-ssh-askpass xdg-utils
```

 3. run the configure
```
./configure
```

 4. run make
```
make
```

 5. Run sudo make install
```
sudo make install
```

### Uninstallation
 1. Run The following:
```
./configure
make uninstall
```

## Plugin Documentation

### Plugin Format

Any scripting language that permits direct execution of it's scripts (bash, python, perl, etc...).

### Input Plugins
An input plugin is a plugin that takes in a qr code or more specifically the text from the qr code such as http://www.duckduckgo.com.

The code is given as the plugin's first argument, and is expected to perform some action with said code (such as opening up a browser or connecting to the given wifi network)

### Output Plugins

Output plugins are expected to provide a the text for a qr code from it's stdout after during execution. It is launched twice. First with the arguments 'start' to get the code to display. Once it exits, the output of the plugin will be put into a qr image and displayed. Once that display is closed the plugin is launched again with the argument 'stop'. This permits a plugin to perform an action only while a code is being displayed, and then stopping said action when it's been closed.

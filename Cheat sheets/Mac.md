## Shortcuts

|Function                                                           | Shortcut       | Description                                         |
|-------------------------------------------------------------------|:--------------:|:---------------------------------------------------:|
|Spotlight search                                                   | `Cmd+Space`    |                                                     | 
|Display Shutdown Options                                           | `Ctlr+Power`   | Use `Tab` to navigate & `Space` to select an option |
|Close Document without saving                                      | `Cmd+D`        |                                                     |
|Switch between windows of same app                                 | ``Cmd+` ``     |                                                     |
|Delete file                                                        | `Cmd+Backspace`|                                                     |
|Delete text                                                        | `Fn+Backspace` |                                                     |

## Environment variables

PATH environment variable is simply an order list of directories over which (typically) executables are searched for and run. To include a directory to search for executables on a MAC

Edit the `/Users/<username>/.bash_profile` to include the directory where the executable resides. For example to include the Android Platform tools add the following line to `.bash_profile`.

`export PATH=$PATH:/Users/username/Library/Android/sdk/platform-tools`  
`echo export PATH=$PATH:/Users/username/Library/Android/sdk/platform-tools >> ~/.bash_profile`

The `.bash_profile file` is loaded before Terminal loads your shell environment and contains all the startup configuration and preferences for your command line interface. Within it you can change your terminal prompt, change the colors of text, add aliases to functions you use all the time, and so much more.

Similar to **Windows** `echo %VARIABLE_NAME%`, find the value of the ENV variable: `echo $VARIABLE_NAME` 

List all the path variables `env`

## Terminal ##
Use sudo prior to a command on the Terminal to run with admin privileges. You are going to be asked for your password before the running the command.

Find path for xcode developer tools
```
$ xcode-select -p
```

Clear terminal  `Cmd+K`

## Use Magic keyboard and mouse on Windows

Download bootcamp support software https://support.apple.com/kb/dl1720?locale=en_GB

From BootCamp5.1.5621\BootCamp\Drivers\Apple install:

AppleWirelessTrackpad64
AppleWirelessMouse64
AppleMultiTouchTrackPadInstaller64

And install -> https://magicutilities.net/magic-mouse/home


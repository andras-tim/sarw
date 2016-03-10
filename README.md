# SARW - Set a random wallpaper

Download and set random downloaded wallpapers on Xfce4.

This is a toolchain written for set a random, single and dual monitor wallpapers on multiple monitors.

The ``set-a-random-wallpaper.sh`` wraps these for download a random wallpaper with ***tool-1***, crop for multi monitor
config with ***tool-2***, and set properly on all displays with ***tool-3***.


## Usage

* Set a random wallpaper (search query: "wallpaper"):

    ``` bash
    set-a-random-wallpaper.sh
    ```

* Set a random wallpaper (search query: "funny"):

    ``` bash
    set-a-random-wallpaper.sh 'funny'
    ```


## Tools

### [tool-1] download-random-double-wide-wallpaper.py

Download random double-wide wallpaper from Google Image search


#### Usage
**``download-random-double-wide-wallpaper.py <output_image_path> [<custom__query>]``**

* Download a random search result for "wallpaper" query:

    ``` bash
    download-random-double-wide-wallpaper.py /tmp/test.jpg
    ```

* Download a random search result for "funny" query:

    ``` bash
    download-random-double-wide-wallpaper.py /tmp/test.jpg 'funny'
    ```


### [tool-2] crop-wallpaper-for-multi-monitors.py

Crop double-wide wallpaper to left, center, right parts


#### Usage
**``crop-wallpaper-for-multi-monitors.py <source_path> <destination_path_prefix>``**

* **example input**:

    * ``wide_wallpaper.jpg`` 3840x1080 image file

* **example output**:

    * ``test-wallpaper_a-left.jpg`` 1920x1080, left crop of input file
    * ``test-wallpaper_b-right.jpg`` 1920x1080, right crop of input file
    * ``test-wallpaper_c-center.jpg`` 1920x1080, center crop of input file

``` bash
crop-wallpaper-for-multi-monitors.py 'wide_wallpaper.jpg' 'test-wallpaper'
```


### [tool-3] set-multi-xfce4-wallpapers.py

Set **Xfce4** wallpapers on multiple monitors


#### Configuration

Set placement of monitors by output in ``OUTPUT_POSITIONS`` variable. The not specified monitors will use the *common*
wallpaper.


#### Usage
**``set-multi-wallpapers.py <common> [<left> <right>]``**

* Set the *common* wallpaper on all outputs:

    ``` bash
    set-multi-wallpapers.py '/full/path/common_wallpaper.jpg'
    ```

* Set wallpapers on all monitor according to ``OUTPUT_POSITIONS``:

    ``` bash
    set-multi-wallpapers.py '/full/path/common_wallpaper.jpg' '/full/path/left_monitor_wallpaper.jpg' '/full/path/right_monitor_wallpaper.jpg'
    ```

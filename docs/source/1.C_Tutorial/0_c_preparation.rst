C Language Preparation
===================================

Requirements
-----------------------------------

* Windows - Win 10 and newer, 64 bits
* Linux - 64 bits
* Mac OS X - Version 10.14: "Mojave" or newer, 64 bits

1.Download the Arduino IDE 2.x.x
----------------------------------

#. Visit `Download Arduino IDE <https://www.arduino.cc/en/software>`_ page.

#. Download the IDE for your OS version.

   .. image:: /preparation/img/C_preparation/Install_Arduino_IDE_1.png

.. note:: Uploading code to the Arduino UNO R4 requires Arduino IDE version 2.2 
   or higher. If your version is older, please upgrade to the latest version.

Installation
--------------

Windows
^^^^^^^^

#. Double click the ``arduino-ide_xxxx.exe`` file to run the downloaded file.

#. Read the License Agreement and agree it.

   .. image:: /preparation/img/C_preparation/Install_Arduino_IDE_2.png

#. Choose installation options.

   .. image:: /preparation/img/C_preparation/Install_Arduino_IDE_3.png

#. Choose install location. It is recommended that the software be installed on a drive other than the system drive.

   .. image:: /preparation/img/C_preparation/Install_Arduino_IDE_4.png

#. Then Finish. 

   .. image:: /preparation/img/C_preparation/Install_Arduino_IDE_5.png

MacOS
^^^^^^^^

Double click on the downloaded ``arduino_ide_xxxx.dmg`` file and follow the 
instructions to copy the **Arduino IDE.app** to the **Applications** folder, you will see the Arduino IDE installed successfully after a few seconds.

.. image:: /preparation/img/C_preparation/Install_Arduino_IDE_6.png
    :width: 800

Linux
"""""""

For the tutorial on installing the Arduino IDE 2.0 on a Linux system, please 
refer `Linux-Install Arduino IDE <https://docs.arduino.cc/software/ide-v2/tutorials/getting-started/ide-v2-downloading-and-installing#linux>`_

Open the IDE
^^^^^^^^^^^^^

#. When you first open Arduino IDE 2.0, it automatically installs the Arduino AVR Boards, built-in libraries, and other required files.

   .. image:: /preparation/img/C_preparation/Install_Arduino_IDE_7.png

#. In addition, your firewall or security center may pop up a few times asking you if you want to install some device driver. Please install all of them.

   .. image:: /preparation/img/C_preparation/Install_Arduino_IDE_8.png

#. Now your Arduino IDE is ready!

.. note::
   In the event that some installations didn't work due to network issues or other 
   reasons, you can reopen the Arduino IDE and it will finish the rest of the 
   installation. The Output window will not automatically open after all installations 
   are complete unless you click Verify or Upload.


Setting Up Your Raspberry Pi Pico W
-----------------------------------
1.Install UF2 Firmware
^^^^^^^^^^^^^^^^^^^^^^^^
When you initially connect the Raspberry Pi Pico W or hold down the BOOTSEL button while inserting it, you'll see the device showing up as a drive without being assigned a COM port. This makes it impossible to upload code.

To fix this, you need to install UF2 firmware. This firmware supports MicroPython and is also compatible with the Arduino IDE.

* Download the firmware from the link below (or you can also find it in the project folder: **Ultimate-Starter-Kit-for-Pico-W/Arduino/3.firmware**).

* Connect the Pico W to your computer using a Micro-USB cable and copy the firmware to the root directory of the Pico W.

* Drag and drop the downloaded UF2 firmware into the RPI-RP2 drive.

.. image:: /preparation/img/C_preparation/ins_uf2_1.png

* After this, the RPI-RP2 drive will disappear, and you can proceed with the following steps.

2.Installing the Board Package
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
To program the Raspberry Pi Pico W, you'll need to install the corresponding package in the Arduino IDE. Here's a step-by-step guide:

* In the Boards Manager window, search for pico W. Click the Install button to commence the installation. This will install the Arduino Mbed OS RP2040 Boards package, which includes support for the Raspberry Pi Pico W.

.. image:: /preparation/img/C_preparation/board_ins1.png

* During the process, a few pop-up prompts will appear for the installation of specific device drivers. Select "Install".

.. image:: /preparation/img/C_preparation/board_ins2.png

* Afterwards, there will be a notification indicating that the installation is complete.

3.Selecting the Board and Port
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
* To select the appropriate board, navigate to Tools -> Board -> Arduino Mbed OS RP2040 Boards -> Raspberry Pi Pico W.

.. image:: /preparation/img/C_preparation/select_com1.png

* If your Raspberry Pi Pico W is connected to the computer, set the right port by navigating to Tools -> Port.

.. image:: /preparation/img/C_preparation/select_com2.png

* Arduino 2.0 offers a new quick-select feature. For the Raspberry Pi Pico W, which is typically not auto-recognized, click Select other board and port.

* Type Raspberry Pi Pico W into the search bar, select it when it shows up, choose the appropriate port, and click OK.

.. image:: /preparation/img/C_preparation/select_com3.png

* You can easily reselect it later through this quick access window.

.. image:: /preparation/img/C_preparation/select_com4.png

* Either of these methods will enable you to set the correct board and port. You're now all set to upload code to the Raspberry Pi Pico W.

4.Uploading Code
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
* Open any .ino file or use the empty sketch currently displayed. Then, click the Upload button.

.. image:: /preparation/img/C_preparation/upload_code1.png

* Wait for the uploading message to appear, as shown below.

.. image:: /preparation/img/C_preparation/upload_code2.png

* Hold down the BOOTSEL button, quickly unplug your Raspberry Pi Pico W, and plug it back in.

.. image:: /preparation/img/C_preparation/upload_code4.png

.. note:: 
   * This step is crucial, especially for first-time users on the Arduino IDE. Skipping this step will result in a failed upload.

   * Once you successfully upload the code this time, your Pico W will be recognized by the computer. For future uses, simply plug it into the computer.

* A prompt indicating successful upload will appear.

.. image:: /preparation/img/C_preparation/upload_code3.png

Install libraries (Important)
-----------------------------------
Many libraries are available directly through the Arduino Library Manager. You can access the Library Manager by following these steps:

In the Library Manager, you can search for the desired library by name or browse through different categories.

.. note:: 
   In projects where library installation is required, there will be prompts 
   indicating which libraries to install. Follow the instructions provided, such 
   as "The DHT sensor library library is used here, you can install it from the 
   Library Manager." Simply install the recommended libraries as prompted.

.. image:: /preparation/img/C_preparation/import_lib1.png

Once you find the library you want to install, click on it and then click the INSTALL button.

The Arduino IDE will automatically download and install the library for you.

.. note:: 
   The libraries installed can be found in the default library directory of the Arduino IDE, which is usually located at C:\Users\xxx\Documents\Arduino\libraries.

   If your library directory is different, you can check it by going to **File -> Preferences**.

   .. image:: /preparation/img/C_preparation/import_lib2.png



# Pinout docs

### Art
It's a bit more work than one might like to get any DIY project documented properly. 
At least to the level where the maker could come back 20 years on and reproduce the 
same working artefact from said documentation, but it's also fun to try do so in a 
more editable fashion, so we will give ascii art a go. The template I use is a modified 
version from https://github.com/tvierb/raspberry-ascii

                             .___.              
                    +3V3-- 1-|O O|- 2--+5V
          (SDA)  GPIO2---- 3-|O O|- 4--+5V
         (SCL1)  GPIO3---- 5-|O O|- 6---GND
    (GPIO_GLCK)  GPIO4---- 7-|O O|- 8-----GPIO14 (TXD0)
                     GND-- 9-|O.O|-10-----GPIO15 (RXD0)
    (GPIO_GEN0) GPIO17----11-|O O|-12-----GPIO18 (GPIO_GEN1)
    (GPIO_GEN2) GPIO27----13-|O O|-14---GND
    (GPIO_GEN3) GPIO22----15-|O O|-16-----GPIO23 (GPIO_GEN4)
                    +3V3--17-|O O|-18-----GPIO24 (GPIO_GEN5)
     (SPI_MOSI) GPIO10----19-|O.O|-20---GND
     (SPI_MOSO) GPIO9 ----21-|O O|-22-----GPIO25 (GPIO_GEN6)
     (SPI_SCLK) GPIO11----23-|O O|-24-----GPIO8  (SPI_C0_N)
                     GND--25-|O O|-26-----GPIO7  (SPI_C1_N)
       (EEPROM) ID_SD-----27-|O O|-28-----ID_SC Reserved for ID EEPROM
                GPIO5-----29-|O.O|-30---GND
                GPIO6-----31-|O O|-32-----GPIO12
                GPIO13----33-|O O|-34---GND
                GPIO19----35-|O O|-36-----GPIO16
                GPIO26----37-|O O|-38-----GPIO20
                     GND--39-|O O|-40-----GPIO21
                             '---'

## Sensors
DS81B20(1WD) and MAX6675(SPI)


                 -- 1-|O O|- 2--
                 -- 3-|O O|- 4--
                 -- 5-|O O|- 6--
             1WD -- 7-|O O|- 8--
             Gnd -- 9-|O.O|-10--
                 --11-|O O|-12--
                 --13-|O O|-14--
                 --15-|O O|-16--
             3v3 --17-|O O|-18--
                 --19-|O.O|-20--
            MOSI --21-|O O|-22--
            MOSO --23-|O O|-24--
             CLK --25-|O O|-26--
                 --27-|O O|-28--
             _CS --29-|O.O|-30--
                 --31-|O O|-32--
                 --33-|O O|-34--
                 --35-|O O|-36--
                 --37-|O O|-38--
                 --39-|O O|-40--

 - 1WD goes to the DS81B20 one-wire pin on the sensor
 - MOSI,MOSO,CLK are the SPI channel and use GPIO4 as _CHIP-SELECT line

A few issues for now are that I'm running the May2021 32-bit Rasp OS and really want to update to the 
64bit, so that's a rebuild. Also I intend to rebuild into a SSD, so will have some notes on the 
SSD booting setup work, (when I do that bit) which involves some extra steps you would not have 
suspected.



# References 
(todo: move these to a new doc later)
 - https://github.com/tvierb/raspberry-ascii
 - https://www.raspberrypi-spy.co.uk/2018/02/enable-1-wire-interface-raspberry-pi/#:~:text=The%20Raspberry%20Pi%20has%20a,as%20the%20DS18B20%20temperature%20sensor.
 - https://developers.google.com/sheets/api/quickstart/python
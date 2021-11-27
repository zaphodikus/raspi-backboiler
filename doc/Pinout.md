# Pinout docs

### Art
It's a bit more work than one might like to get any DIY project documented properly. 
At least to the level where the maker could come back 20 years on and reproduce the 
same working artefact from said documentation, but it's also fun to try and do so in a 
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
     (SPI_MISO) GPIO9 ----21-|O O|-22-----GPIO25 (GPIO_GEN6)
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

                           .___.
                 GPIO21-40-|O O|-39-GND   
                 GPIO20-38-|O O|-37-GPIO26
                 GPIO16-36-|O O|-35-GPIO19
                    GND-34-|O O|-33-GPIO13
                 GPIO12-32-|O O|-31-GPIO6 
                    GND-30-|O O|-29-GPIO5 
      (Reserved) ID_SC--28-|O O|-27-ID_SD  (EEPROM)
      (SPI_C1_N) GPIO7--26-|O O|-25-GND   
      (SPI_C0_N) GPIO8--24-|O O|-23-GPIO11 (SPI_SCLK)
     (GPIO_GEN6) GPIO25-22-|O O|-21-GPIO9  (SPI_MISO)
                    GND-20-|O O|-19-GPIO10 (SPI_MOSI)
     (GPIO_GEN5) GPIO24-18-|O O|-17-+3V3  
     (GPIO_GEN4) GPIO23-16-|O O|-15-GPIO22 (GPIO_GEN3)
                    GND-14-|O O|-13-GPIO27 (GPIO_GEN2)
     (GPIO_GEN1) GPIO18-12-|O O|-11-GPIO17 (GPIO_GEN0)
          (RXD0) GPIO15-10-|O O|-9--GND   
          (TXD0) GPIO14--8-|O O|-7--GPIO4  (GLCK)
                    GND--6-|O O|-5--GPIO3  (SCL1)
                    +5V--4-|O O|-3--GPIO2  (SDA)
                    +5V--2-|O O|-1--+3V3  
                           '---'

               (   ( (   (                  
               G   G G   G ( ( (            
               P   P P   P S S R            
               I   I I   I P P e            
               O   O O   O I I s            
           ( ( _   _ _   _ _ _ e            
           T R G   G G   G C C r            
           X X E   E E   E 0 1 v            
           D D N   N N   N _ _ e            
           0 0 1   4 5   6 N N d            
           ) ) )   ) )   ) ) ) )            
                                        
           G G G   G G   G G G I   G   G G G
           P P P   P P   P P P D   P   P P P
           I I I   I I   I I I _   I   I I I
     + + G O O O G O O G O O O S G O G O O O
     5 5 N 1 1 1 N 2 2 N 2 8 7 C N 1 N 1 2 2
     V V D 4 5 8 D 3 4 D 5 | | | D 2 D 6 0 1
     | | | | | | | | | | | | | | | | | | | |
     | | | | 1 1 1 1 1 2 2 2 2 2 3 3 3 3 3 4
     2 4 6 8 0 2 4 6 8 0 2 4 6 8 0 2 4 6 8 0
     M M M M M M M M M M M M M M M M M M M M
    +---------------------------------------+
    |O O O O O O O O O O O O O O O O O O O O|
    |                                       |
    |O O O O O O O O O O O O O O O O O O O O|
    +---------------------------------------+
     M M M M M M M M M M M M M M M M M M M M
     1 3 5 7 9 1 1 1 1 1 2 2 2 2 2 3 3 3 3 3
     | | | | | 1 3 5 7 9 1 3 5 7 9 1 3 5 7 9
     | | | | | | | | | | | | | | | | | | | |
     + G G G G G G G + G G G G I G G G G G G
     3 P P P N P P P 3 P P P N D P P P P P N
     V I I I D I I I V I I I D _ I I I I I D
     3 O O O   O O O 3 O O O   S O O O O O  
       2 3 4   1 2 2   1 9 1   D 5 6 1 1 2  
               7 7 2   0   1         3 9 6  
                            
       ( ( (   ( ( (   ( ( (   (
       S S G   G G G   S S S   E
       D C L   P P P   P P P   E
       A L C   I I I   I I I   P
       ) 1 K   O O O   _ _ _   R
         ) )   _ _ _   M M S   O
               G G G   O I C   M
               E E E   S S L   )
               N N N   I O K
               0 2 3   ) ) )
               ) ) )
    
                             ( ( (          
                     ( ( (   G G G          
                     S S S   P P P          
                 (   P P P   I I I          
                 E   I I I   O O O          
                 E   _ _ _   _ _ _   ( (    
                 P   S M M   G G G   G S (  
                 R   C I O   E E E   L C S  
                 O   L S S   N N N   C L D  
                 M   K O I   3 2 0   K 1 A  
                 )   ) ) )   ) ) )   ) ) )  
                                            
       G G G G G I   G G G   G G G   G G G  
       P P P P P D   P P P   P P P   P P P  
       I I I I I _   I I I + I I I   I I I +
     G O O O O O S G O O O 3 O O O G O O O 3
     N 2 1 1 6 5 D N 1 9 1 V 2 2 1 N 4 3 2 V
     D 6 9 3 | | | D 1 | 0 3 2 7 7 D | | | 3
     | | | | | | | | | | | | | | | | | | | |
     3 3 3 3 3 2 2 2 2 2 1 1 1 1 1 | | | | |
     9 7 5 3 1 9 7 5 3 1 9 7 5 3 1 9 7 5 3 1
     M M M M M M M M M M M M M M M M M M M M
    +----------------------------------------+
    |O O O O O O O O O O O O O O O O O O O O |
    |                                        |
    |O O O O O O O O O O O O O O O O O O O O |
    +----------------------------------------+
     M M M M M M M M M M M M M M M M M M M M
     4 3 3 3 3 3 2 2 2 2 2 1 1 1 1 1 8 6 4 2
     0 8 6 4 2 0 8 6 4 2 0 8 6 4 2 0 | | | |
     | | | | | | | | | | | | | | | | | | | |
     G G G G G G I G G G G G G G G G G G + +
     P P P N P N D P P P N P P N P P P N 5 5
     I I I D I D _ I I I D I I D I I I D V V
     O O O   O   S O O O   O O   O O O      
     2 2 1   1   C 7 8 2   2 2   1 1 1      
     1 0 6   2         5   4 3   8 5 4      
                                      
                 ( ( ( (   ( (   ( ( (
                 R S S G   G G   G R T
                 e P P P   P P   P X X
                 s I I I   I I   I D D
                 e _ _ O   O O   O 0 0
                 r C C _   _ _   _ ) )
                 v 1 0 G   G G   G
                 e _ _ E   E E   E
                 d N N N   N N   N
                 ) ) ) 6   5 4   1
                       )   ) )   )


## Sensors
**DS81B20 (1WD) Temp sensors** 


                      .___.              
                 -- 1-|O O|- 2--                Terminal block
                 -- 3-|O O|- 4--                  +------+
                 -- 5-|O O|- 6--        (black) - |Gnd   |
             1WD -- 7-|O O|- 8--        (yellow)- |sense |
             Gnd -- 9-|O.O|-10--        (red)   - |3V3   |
                 --11-|O O|-12--                  +------+
                 --13-|O O|-14--
                 --15-|O O|-16--
             3v3 --17-|O O|-18--
                 --19-|O.O|-20--
                 --21-|O O|-22--
                 --23-|O O|-24--
                 --25-|O O|-26--
                 --27-|O O|-28--
                 --29-|O.O|-30--
                 --31-|O O|-32--
                 --33-|O O|-34--
                 --35-|O O|-36--
                 --37-|O O|-38--
                 --39-|O O|-40--
                      '---'

 - 1WD need 4K7 Ohm pull-up - connect to the DS81B20 one-wire pin on the sensor.

**MAX6675(SPI) Thermocouple**   


                      .___.              
                 -- 1-|O O|- 2--                   Header
                 -- 3-|O O|- 4--                  +------+
                 -- 5-|O O|- 6--        (black) - |Gnd O |
                 -- 7-|O O|- 8--        (red)   - |3v3 O |
             Gnd -- 9-|O.O|-10--        (   )   - |SCK O |
                 --11-|O O|-12--        (   )   - | CS O |
                 --13-|O O|-14--        (   )   - | DO O |
                 --15-|O O|-16--                  +------+
             3v3 --17-|O O|-18--
                 --19-|O.O|-20--
            MISO --21-|O O|-22--
             SCK --23-|O O|-24--
                 --25-|O O|-26--
                 --27-|O O|-28--
    (GPIO5)  _CS --29-|O.O|-30--
                 --31-|O O|-32--
                 --33-|O O|-34--
                 --35-|O O|-36--
                 --37-|O O|-38--
                 --39-|O O|-40--
                      '---'


 - MISO,SCK are the SPI channel and use GPIO5 as _CHIP-SELECT line.

**BME280(SPI) Pressure sensor BMP280**   


                      .___.              
                 -- 1-|O O|- 2--                   Header
                 -- 3-|O O|- 4--                  +-------+
                 -- 5-|O O|- 6--        (blk  ) - |3v3  O |
                 -- 7-|O O|- 8--        (wht)   - |Gnd  O |
             Gnd -- 9-|O.O|-10--        (gry)   - |SCK  O |
                 --11-|O O|-12--        (bio)   - |MOSI O |
                 --13-|O O|-14--        (blu)   - |_CS  O |
                 --15-|O O|-16--        (grn)   - |MISO O |                  
             3v3 --17-|O O|-18--                  +-------+
            MOSI --19-|O.O|-20--
            MISO --21-|O O|-22--
             SCK --23-|O O|-24--
                 --25-|O O|-26--
                 --27-|O O|-28--
                 --29-|O.O|-30--
     (GPIO6) _CS --31-|O O|-32--
                 --33-|O O|-34--
                 --35-|O O|-36--
                 --37-|O O|-38--
                 --39-|O O|-40--
                      '---'


 - MOSI, MISO, SCK are the SPI channel and use GPIO6 as _CHIP-SELECT line.

**ASD1115 (I2c)**

                             .___.              
                    +3V3-- 1-|O O|- 2--+5V                 + Header+
          (SDA)  GPIO2---- 3-|O O|- 4--+5V            3V3  |   ( ) |
         (SCL1)  GPIO3---- 5-|O O|- 6---GND           Gnd  |   ( ) |
                      ---- 7-|O O|- 8-----            SCL  |   ( ) |
                     GND-- 9-|O.O|-10-----            SDA  |   ( ) |
                      ----11-|O O|-12-----            ADDR | (Gnd) |
                      ----13-|O O|-14---GND           ALRT | (N/C) | 
                      ----15-|O O|-16-----            A0   |   ( ) | MQ-5
                    +3V3--17-|O O|-18-----            A1   |   ( ) | 
                      ----19-|O.O|-20---GND           A2   |   ( ) |
                      ----21-|O O|-22-----            A3   |   ( ) |
                      ----23-|O O|-24-----                 +-------+
                     GND--25-|O O|-26-----       
                      ----27-|O O|-28-----       
                      ----29-|O.O|-30---GND
                      ----31-|O O|-32----- 
                      ----33-|O O|-34---GND
                      ----35-|O O|-36----- 
                      ----37-|O O|-38----- 
                     GND--39-|O O|-40----- 
                             '---'



A few issues for now are that I'm running the May2021 32-bit Rasp OS and really want to update to the 
64bit, so that's a rebuild. Also I intend to rebuild into a SSD, so will have some notes on the 
SSD booting setup work, (when I do that bit) which involves some extra steps you would not have 
suspected.



# References 
(todo: move these to a new doc later)
 - https://github.com/tvierb/raspberry-ascii
 - https://www.raspberrypi-spy.co.uk/2018/02/enable-1-wire-interface-raspberry-pi/#:~:text=The%20Raspberry%20Pi%20has%20a,as%20the%20DS18B20%20temperature%20sensor.
 - https://developers.google.com/sheets/api/quickstart/python
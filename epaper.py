##
 #  updateScreen.py - Updates epaper display
 ##

import epd2in7
import Image
import ImageFont
import ImageDraw
import time
from sensorTools import sensorDatabase 

def updateScreen(date, door1, door2, door3, inTemp, outTemp):
    epd = epd2in7.EPD()
    epd.init()

    # Start with a square image - Later rotate and resize
    image = Image.new('1', (epd2in7.EPD_HEIGHT, epd2in7.EPD_HEIGHT), 255)    # 255: clear the image with white
    draw = ImageDraw.Draw(image)
    mfont = ImageFont.truetype('/home/pi/TempStation/Roboto-Medium.ttf', 18)
    bfont = ImageFont.truetype('/home/pi/TempStation/Roboto-Bold.ttf', 20)
    bbfont = ImageFont.truetype('/home/pi/TempStation/Roboto-Bold.ttf', 24)

    # First draw the dividing lines
    draw.rectangle((0, 60, 264, 63), fill = 0)
    draw.rectangle((0, 132, 264, 135), fill = 0)

    draw.rectangle((84, 0, 87, 60), fill = 0)
    draw.rectangle((176, 0, 179, 60), fill = 0)

    # Now the fixed text
    draw.text((15,0), 'Door 1', font = mfont, fill = 0)
    draw.text((105,0), 'Door 2', font = mfont, fill = 0)
    draw.text((195,0), 'Door 3', font = mfont, fill = 0)
    draw.text((100,65), 'Temps', font = bfont, fill = 0)

    # Next the logic for the door sensors
    if not door1:
        draw.rectangle((1, 25, 82, 58), fill = 255)
        draw.text((5,30), 'CLOSED', font = bfont, fill = 0)
    else:
        draw.rectangle((1, 25, 82, 58), fill = 0)
        draw.text((15,30), 'OPEN', font = bfont, fill = 255)

    if not door2:
        draw.rectangle((89, 25, 174, 58), fill = 255)
        draw.text((95,30), 'CLOSED', font = bfont, fill = 0)
    else:
        draw.rectangle((89, 25, 174, 58), fill = 0)
        draw.text((105,30), 'OPEN', font = bfont, fill = 255)

    if not door3:
        draw.rectangle((181, 25, 263, 58), fill = 255)
        draw.text((185,30), 'CLOSED', font = bfont, fill = 0)
    else:
        draw.rectangle((181, 25, 263, 58), fill = 0)
        draw.text((195,30), 'OPEN', font = bfont, fill = 255)

    # Now temps and time
    intempstr = ' Inside: ' + str(inTemp)
    outtempstr = 'Outside: ' + str(outTemp)
    draw.text((15,90), intempstr, font = mfont, fill = 0)
    draw.text((5,110), outtempstr, font = mfont, fill = 0)
    
    draw.text((50,140), date, font = bfont, fill = 0)

    image = image.rotate(90)
    image = image.crop((0, 0, epd2in7.EPD_WIDTH, epd2in7.EPD_HEIGHT))

#    image.show()

    epd.display_frame(epd.get_frame_buffer(image))

if __name__ == '__main__':
    # Open database of readings:
    db = sensorDatabase('readings.db')

    # Loop to get readings and update display
    looptime = 300

    while True:
        door1status = db.dbGetLast(3002)[0][2]
        door2status = db.dbGetLast(3003)[0][2]
        door3status = db.dbGetLast(4001)[0][2]

        date = db.dbGetLast(1001)[0][0]
        intemp = db.dbGetLast(2003)[0][2] * 1.8 + 32. -9.4
        outtemp = db.dbGetLast(1005)[0][2] * 1.8 + 32.0

        updateScreen(date, door1status, door2status, door3status, intemp, outtemp)

        # Now wait
        time.sleep(looptime)

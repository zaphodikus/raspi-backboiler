# Import the necessary libraries
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from PIL import Image, ImageFont, ImageDraw
import io
import matplotlib as mpl
# we need to tell the lib to use an alternative GTK, this is the hacky way to do so,
# non-hacky way to do so is:
#   export MPLBACKEND=TkAgg
mpl.use("TkAgg")


def white_to_transparency(img):
    """
    Converts all white 255.255.255 pixels, to transparent
    :param img:
    :return: PIL.Image
    """
    x = np.asarray(img.convert('RGBA')).copy()
    x[:, :, 3] = (255 * (x[:, :, :3] != 255).any(axis=2)).astype(np.uint8)
    return Image.fromarray(x)


# Initialize Figure and Axes object
fig, axes = plt.subplots()
fig.set_size_inches(12, 6)  # make graph area wider

# Load in data
tips = pd.read_csv("../sensors.csv")
#tips = tips.iloc[50:550]
tips = tips.iloc[1:550]

# clean up our data
temperatures = []
timestamps = pd.to_datetime(tips['time'])
for column_name in list(tips.columns.values)[1:]:
    if tips[column_name].dtype.name == 'object':  # some data failed to convert to numeric, so lets fix it
        print(f"fixing data in {column_name}")
        tips[column_name] = tips[column_name].str.replace('None', '0')
        tips[column_name] = tips[column_name].astype(np.float64)
for column_name in list(tips.columns.values)[1:]:
    if not (column_name.endswith('H') or column_name.endswith('P')):
        temperatures.append(tips.loc[:, column_name])

for temperature in temperatures:
    axes.plot(timestamps, temperature)

# Format xtick labels as HH:MM
# The default formatter shows timestamps as dates, which don't fit into the ticks
# Set time format and the interval of ticks (every 15 minutes)
xformatter = mpl.dates.DateFormatter('%H:%M')
xlocator = mpl.dates.MinuteLocator(interval=15)
xlocator = mpl.dates.MinuteLocator(byminute=[0, 15, 30, 45], interval=1)
axes.xaxis.set_major_locator(xlocator)
plt.gcf().axes[0].xaxis.set_major_formatter(xformatter)
axes.tick_params(axis='y', labelsize=10)
axes.tick_params(axis='x', labelsize=5, )

plt.setp(axes.get_xticklabels(), rotation=90)
yticks= axes.get_yticks()
yticks = list(range(int(np.min(yticks)), int(np.max(yticks))+5, 5))
axes.set_yticks(yticks)

# label it
axes.set_ylabel("°C")
axes.set_xlabel("Time")
axes.set_title('Raspberry Pi')
axes.legend(loc='upper right')
axes.legend(tips.columns.values[1:len(temperatures)+1])

plt.tight_layout()
# Show the plot or export it to disc
if False:
    plt.show()
else:
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    im = Image.open(buf)
    # timestamp
    ts = str(np.max(timestamps))
    draw = ImageDraw.Draw(im)
    fnt = ImageFont.truetype('arial.ttf', 15)
    draw.text((1042, 205), ts, font=fnt, fill="#000")
    im = white_to_transparency(im)
    #im.show()
    buf.close()
    # todo: save using the timestamp as a safe filename.
    im.save("raspberry.png")


def annotate(image, coordinate, text, font):
    """
    :param image:
    :param coordinate:
    :param text:
    :return: PIL.Image
    """
    draw = ImageDraw.Draw(image)
    #print(f"Draw {text} at {coordinate}")
    # paint a text background behind the annotation to give contrast
    draw.text(coordinate, text, font=font, stroke_width=5,
           fill=(250, 250, 250))
    draw.text(coordinate, text, font=font, stroke_width=1,
           fill=(0, 0, 0))
    return image


# load template
fnt = ImageFont.truetype('arial.ttf', 55)
template = Image.open("static/template800x600.png")
annotations = {"temp2": {"coord": (80, 180), "format": "{:>7}°C"},   # hot out1
               "temp1": {"coord": (80, 263), "format": "{:>7}°C"},   # return 1
               "temp4": {"coord": (80, 360), "format": "{:>7}°C"},  # hot out 2
               "temp5": {"coord": (80, 460), "format": "{:>7}°C"},   # return 2
               "time":  {"coord": (80, 82), "format": "{}"},   # date
               }

# loop over the time series
start = 0
end = 200
interval = 1
for sample in range(start, end-interval, interval):
    diagram = template.convert("RGBA")  # copy, or convert to RBGA so we don't run out of palette entries
    segment_df = tips.iloc[sample:sample+interval]
    if segment_df['time'].count():
        time_string = str(np.max(pd.to_datetime(segment_df['time'])))
        #print(time_string)
        for column_name in list(segment_df.columns.values):
            max_value = np.max(segment_df[column_name].values)
            #print(f"{column_name}={max_temp}")
            if column_name in annotations.keys():
                coord = annotations[column_name]['coord']
                formatter = annotations[column_name]['format']
                txt = formatter.format(max_value)
                annotate(diagram, coord, txt, fnt)

        fn = time_string.replace(':', '_')
        diagram = white_to_transparency(diagram)
        diagram.save(f"img/{fn}.png")
        #diagram.show()

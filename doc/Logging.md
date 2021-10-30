# Datalogging
A quick thing to put up front here, is that I'm going to be using deadbanding to 
save logging space. I'll also use circular buffers on the Edge device for the same 
reason. But I need to expand on this simplistic log compression tactic.

So it's possible to compress timestamps in situ, in my case I'm not doing that at present, 
but presenting timestamps in as integers not string, and lower resolution can cause problems
when you want to log multiple samples at lower resolution in a pinch or even by accident.
 - Compression by resolution: For slow moving data, you don't need milliseconds...unless!
 - Compression by offset: Log one timestamp, and then log just the relative offset as an int (beware wrapping.)
 - Compression by deadband: If the value does not change, don't log it.

## Deadbanding
Always log a sample at startup, regardless, save the time and value in a temporary. For each successive sample, 
that does not differ by value more than the deadband (for example 1 degree celcius), ignore it. After a set interval, 
always log a value anyway. this last bit is important, it covers you for the case where the system shuts down, and you 
don't have a sample to interpolate up to nearby. Typically, deadbands take a lot of tweaking, you want to set them 
so that they give a 10x compression factor. 100x compression is taking it perhaps too far, perhaps reducing the time 
deadband in more.
```
Example: value > 0.5 °C
         time  > 600 seconds
```
Now I want to experiment here and create a "sliding" deadband or logarithmic value sensitive deadband that does not 
fit into the `if abs(value-lastvalue) > deadband:` constraint, because that obviously would not work for something 
like a background radiation sensor reading. So at some point, I'm going to plot some graphs and find a good log base 
and index to use for the value deadbanding at high temperatures, because, for some of the sensors I'm using, accuracy 
is less important than "generally" where it is in relation to where it was a few minutes ago. And that gets hard if we 
want to show cold thermocouples at room temperature, but don't really care about them at all until they get to 
interesting levels like 200 to 300 degrees.

## Circular Buffers
I'm going to not only be creating long term history buffers that span a month at a time, and perhaps some way to 
aggregate those to cover entire lifespan, but I built a circular buffer that works OK-ish in sqlite. It needs 
some optimization, but it's use-able for now. Also going to be pushing those longer term logs into a cloud using 
google spreadsheets. Which should make date mining possible.

## Cloud
Since I'm not confident of getting all things working and not breaking often, and the Raspberry pi Sd card not 
breaking on me. and besides that my programmign skills will corrupt the DB many-many times I'm sure. I'll thus be 
pumping data into a google spreadsheet from early on in the project.

## Matplotlib
And of course using matplotlib. I'm new to the entire topic, so expect some weird stuff to go on in this department 
with bad graphs and bad math.

## Process boundaries
To make some things simpler, the system will use separate processes. Sqllite has some atomicity of some clever SQL 
kind so having one app do data acquisition and pretty much only ever write to the DB, and another app read that data, 
should simplify debugging and force some reduction of complexity. I'm expecting remote sensor data to also come in, 
probably over ethernet, so that will be polled and written to the database, possibly all on the one big sensors app 
initially.
The other app will be the web service, how I do graph "bitmaps" in there with matplotlib in a way that does not overwhelm 
the cpu will be interesting.

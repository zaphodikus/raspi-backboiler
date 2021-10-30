# Datalogging
A quick thing to put up front here, is that I'm going to be using deadbanding to 
save logging space. I'll also use circular buffers on the Edge device for the same 
reason. But I need to expand on this simplistic log compression tactic.

So it's possible to compress timestamps in situ, in my case I'm not doing that at present, 
but presenting timestamps in as integers not string, and lower resolution can cause problems
when you want to log multiple samples at lower resolution in a pinch or even by accident.
 - Compression by resolution: For slow moving data, you don't need milliseconds...unless!
 - Compression by offset: Log one timestamp, and then log just the relative offset as an int (beware wrapping.)
 - Compression by deadband: If the valeu does not change, don't log it

## Deadbanding
Always log a sample at startup, regardless, save the time and value in a temporary. For each successive sample, 
that does not differ by value more than the deadband (for example 1 degree celcius), ignore it. After a set interval, 
always log a value anyway. this last bit is important, it covers you for the case where the system shuts down and you 
don't have a sample to interpolate up to nearby. Typically the deadbands take a lot of tweaking, you want to set them 
so that they give a 10x compression factor. 100x compression is taking it perhaps too far, perhaps reducing the time 
deadband in more.


`
Example: value > 0.5 °C
         time  > 600 seconds
`

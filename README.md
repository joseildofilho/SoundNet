# SoundNet
## Introduction
This project is an implementation of the [OSI protocol] (https://en.wikipedia.org/wiki/OSI_protocols), but the main difference
between the common implementation and this, is the ** Physical Layer ** that is implemented using the sound.

Obvious that has no advantages for the usual, but is very didactic, because we will face many complications
to work with a completely different scenario.
## Technologies
- python 3.6
- pyaudio x.x
- numpy

## Layers
### Physical
The physical layer is here the big star and the beginning, in common implementations it is implemented in hardware and the bits
are transmitted by the cable, in this project the transmission medium is air, so we are going to face a lot of noise in
our microphones, this is also true for the cable and antennas, but the other type of noise, there are some ways to
handle this noise, but they are not simple, and can take up a lot of time to run, so we are assuming that the environment
it will be quiet enough.

The first step is about making a sound with the speaker, and to make this we need a wave, and when I think about waves, 
the first one that shows in my head is the sine, using numpy (code below)
we created this wave, where FRAME_RATE is the amount of points in that wave, DURATION, how many seconds it goes
it is possible to set DURATION to a number less than 1, FREQ is the wave frequency, we recommend not
set high frequencies because the sound will upset you.

    FRAME_RATE = 44100
    FREQ = 200
    DURATION = 1.0
    SIGN = (sin (2 * pi * arange (FRAME_RATE * DURATION) * FREQ / FRAME_RATE)). Astype (float32)

Now we have the wave, and we need to use Pyaudio to play, it's actually very easy to do this, just see the code:

    paudio = pyaudio.PyAudio ()
    stream = paudio.open (format = pyaudio.paFloat32,
    channels = 1,
    rate = frame_rate
    exit = True
    frames_per_buffer = 1)
    stream.start_stream ()
    stream.write (SIGNAL)
    stream.close_stream ()
    stream.close ()
    paudio.terminate ()
The project now works using multiplexing in time, to this type of multiplexing works properly it's necessary to use sync
between clocks of each computer, there's a couple of way to do this, but sync mechanism was not implemented yet,
 just because the size of the windows are very large and we did not find errors caused by lack of time.
 
The representation of information is built on noise and silence, where some noise means 1 and silence means 0.

When the signal is discretized we'll need a strategy to figure out if the signal represents a 1 or 0, to do this, we
choose a naive, that's we check the exact middle of the signal to map to 1 or 0. Ocasionally this strategy could 
generate misunderstand whether the system is not synchronized. 


let reading = 0
function turnOnLight()  {
    pins.digitalWritePin(DigitalPin.P2, 1)
}
function turnOffLight()  {
    pins.digitalWritePin(DigitalPin.P2, 0)
}
turnOffLight()
basic.forever(() => {
    if (reading > 37 && reading < 40) {
        music.beginMelody(music.builtInMelody(Melodies.PowerUp), MelodyOptions.Once)
        turnOnLight()
        basic.pause(1000)
    } else {
        music.rest(music.beat(BeatFraction.Whole))
        turnOffLight()
    }
})
basic.forever(() => {
    reading = pins.analogReadPin(AnalogPin.P1) * -14
    reading = reading / 100
    reading = reading + 100
    basic.showNumber(reading)
    basic.pause(1000)
})

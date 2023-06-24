from ev3dev2.motor import LargeMotor, OUTPUT_B, OUTPUT_C, SpeedPercent
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2._platform.ev3 import INPUT_3

mLeft = LargeMotor(OUTPUT_B)
mRight = LargeMotor(OUTPUT_C)
cs = ColorSensor(INPUT_3)
# while the color is not black, move forward
while cs.color != 1:
    mLeft.on(SpeedPercent(70), 5)
    mRight.on(SpeedPercent(70), 5)
# move forward when black, else turn right til black.
while True:
    # move forward
    if cs.color == 1:
        mLeft.on(SpeedPercent(20), 5)
        mRight.on(SpeedPercent(20), 5)
    else:
        # turn right
        mLeft.on(SpeedPercent(10), 5)
        mRight.off()



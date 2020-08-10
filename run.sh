ver="$(python --version | cut -d' ' -f2)"
ver=${ver:0:3}
if [ "$ver" != "3.7" ]; then
    echo "The version of Python isn't 3.7"
    exit 1
fi

SCRIPT='rule_based_lane_model.py'
SCRIPT_FORCE='rule_based_force_model.py'
FPS='240'

#pythonsMLGame.py -r -i ml_play_template.py arkanoid NORMAL 2
#python MLGame.py -r -f 24 -f 240 -m Rrule_based_force_model.pyacingCar 2 COIN
#python MLGame.py -r -m RacingCar 1
#exit 0
python MLGame.py -r -f $FPS\
                    -i $SCRIPT\
                    -i $SCRIPT_FORCE\
                    RacingCar 2 COIN

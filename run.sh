ver="$(python --version | cut -d' ' -f2)"
ver=${ver:0:3}
if [ "$ver" != "3.7" ]; then
    echo "The version of Python isn't 3.7"
    exit 1
fi

SCRIPT='rule_based.py'

#pythonsMLGame.py -r -i ml_play_template.py arkanoid NORMAL 2
#python MLGame.py -r -m RacingCar 2 COIN
#python MLGame.py -r -m RacingCar 1
python MLGame.py -r -i $SCRIPT\
                    -i $SCRIPT\
                    RacingCar 2 COIN

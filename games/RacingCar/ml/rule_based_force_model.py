class MLPlay:
    def __init__(self, player):
        self.player = player
        if self.player == "player1":
            self.player_no = 0
        elif self.player == "player2":
            self.player_no = 1
        elif self.player == "player3":
            self.player_no = 2
        elif self.player == "player4":
            self.player_no = 3
        self.car_vel = 0
        self.car_pos = ()
        self.coin_num = 0
        self.computer_cars = []
        self.coins_pos = []
        self.dist_up_norm = 40
        self.dist_lr_norm = 20

    def update(self, scene_info: dict):
        self.computer_cars = []

        """
        Generate the command according to the received scene information
        """
        for car in scene_info["cars_info"]:
            car["pos"] = (car["pos"][0], -car["pos"][1]) # fix the inverse of y axis
            if car["id"] == self.player_no:
                self.car_pos = car["pos"]
                self.car_vel = car["velocity"]
                self.coin_num = car["coin_num"]
            else:
                self.computer_cars.append(car["pos"])

        for car in scene_info["computer_cars"]:
            self.computer_cars.append((car[0], -car[1]))
        scene_info["computer_cars"] = self.computer_cars

        if scene_info.__contains__("coins"):
            self.coins_pos = scene_info["coins"]

        if scene_info["frame"] == 0:
            return "SPEED"

        if scene_info["status"] != "ALIVE":
            return "RESET"

        car_border = {"left": self.car_pos[0]-40, "right": self.car_pos[0]+40, "up": self.car_pos[1]+80, "down": self.car_pos[1]-80}


        """
        if self.player == "player1":
            print(car_border)
        """

        eva = self.evaluate()
        if eva[0] <= 0:
            return ["MOVE_LEFT", "SPEED"]
        else:
            return ["MOVE_RIGHT", "SPEED"]

        return ["SPEED"]

    def reset(self):
        """
        Reset the status
        """
        print("reset ml script")
        pass
    
    def car_dist(car_src: tuple, car_tar: tuple):
        src_x = car_src[0]; src_y = car_src[1]
        tar_x = car_tar[0]; tar_y = car_tar[1]

        return (tar_x - src_x, tar_y - src_y)

    def evaluate(self):
        sum_x = 0.0
        N = 1000000.0

        for car in self.computer_cars:
            diff_x = self.car_pos[0] - car[0]
            diff_y = abs(self.car_pos[1] - car[1])
            if -40 <= diff_x <= 40:
                if diff_x <= 0:
                    diff_x = -40
                else:
                    diff_x = 40
            if 0 <= diff_y <= 80:
                diff_y = 80
            sum_x = sum_x + N/diff_x * 1/diff_y
        
        sum_x = sum_x + N/(self.car_pos[0] - 30)/80 + N/(self.car_pos[0] - 600)/80

        if self.player_no == 0:
            print(sum_x)
        return (sum_x, 0)

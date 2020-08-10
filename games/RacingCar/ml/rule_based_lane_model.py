import math

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
        self.frame_count = 0

    def update(self, scene_info: dict):
        self.computer_cars = []
        self.coins_pos = []

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
            for coin in scene_info["coins"]:
                self.coins_pos.append((coin[0], -coin[1]))
            scene_info["coins"] = self.coins_pos

        if scene_info["frame"] == 0:
            return "SPEED"

        if scene_info["status"] != "ALIVE":
            return "RESET"

        car_border = {"left": self.car_pos[0]-40, "right": self.car_pos[0]+40, "up": self.car_pos[1]+80, "down": self.car_pos[1]-80}


        """
        if self.player == "player1":
            print(car_border)
        """

        if self.frame_count < 60:
            self.frame_count += 1
        else:
            self.lane_rank()
            self.frame_count = 0

        eva = self.evaluate()
        command = []
        if eva[0] <= 0:
            command.append("MOVE_LEFT")
        else:
            command.append("MOVE_RIGHT")
        if eva[1] >= 0:
            command.append("SPEED")
        else:
            command.append("BRAKE")
            #print("BRAKE")
        return command

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
        sum_y = 0.0
        N = 1000000.0
        lane_candidate_num = 2
        detect_range_x = 46
        detect_range_y = 120
        detect_range_x_front = 35
        detect_range_y_front_max = 120
        detect_range_y_front_min = 100

        lane_score = self.lane_rank()
        chosen_lane = []
        for i in range(lane_candidate_num):
            land_x = lane_score[i][0]*70+35
            chosen_lane.append(land_x)
        chosen_lane.sort(key = lambda s: abs(s - self.car_pos[0]))

        for car in self.computer_cars:
            diff_x = self.car_pos[0] - car[0] + 1
            diff_y = self.car_pos[1] - car[1]
            if abs(diff_y) <= detect_range_y and\
                    abs(diff_x) <= detect_range_x and\
                    diff_x != 0:
                sum_x += 1/(diff_x*abs(diff_x))
            if detect_range_y_front_min <= -diff_y <= detect_range_y_front_max and\
                    abs(diff_x) <= detect_range_x_front and\
                    diff_y !=0:
                #print(f"diff_x:{diff_x}, diff_y:{diff_y}")
                sum_y += 1/(diff_y*abs(diff_y))
        
        if sum_x != 0:
            return (sum_x, sum_y)
        else:
            return (chosen_lane[0] - self.car_pos[0], sum_y)

    def lane_rank(self):
        lane_width = 70
        base_line_car = self.car_pos[1] + 40
        base_line_coin = self.car_pos[1] - 40
        lane_cars = []
        lane_coins = []
        lane_score = []
        my_lane = -1
        score_of_coin = 80
        coin_dist_norm = 140

        for i in range(9):
            l = i*lane_width
            r = (i+1)*lane_width
            if l <= self.car_pos[0] < r:
                my_lane = i

        for i in range(9):
            lane_cars.append([])
        for car in self.computer_cars:
            car_x = car[0]
            car_y = car[1]
            for i in range(9):
                l = i*lane_width
                r = (i+1)*lane_width
                if base_line_car < car_y and l <= car_x < r:
                    lane_cars[i].append((car_x, car_y))
        for lane in lane_cars:
            lane.sort(key = lambda s: s[1])

        for i in range(9):
            lane_coins.append([])
        for coin in self.coins_pos:
            coin_x = coin[0]
            coin_y = coin[1]
            coin_lane = -1
            for i in range(9):
                l = i*lane_width
                r = (i+1)*lane_width
                if base_line_coin < coin_y and l <= coin_x < r:
                    if lane_cars[i] and coin_y < lane_cars[i][0][1]:
                            lane_coins[i].append(coin)
                    else:
                        lane_coins[i].append(coin)

        for i in range(9):
            #coin_score = len(lane_coins[i])*score_of_coin
            coin_score = 0
            for coin in lane_coins[i]:
                diff_x = self.car_pos[0] - coin[0]
                diff_y = self.car_pos[1] - coin[1]
                coin_dist = math.sqrt(diff_x**2 + diff_y**2)
                #print(coin_dist)
                if 0 < coin_dist/coin_dist_norm < 1:
                    coin_dist = coin_dist / coin_dist_norm
                    #coin_score += score_of_coin/(coin_dist**2)
                    coin_score += score_of_coin/coin_dist**2
                    #print((diff_x, diff_y))
                    #print(score_of_coin/(coin_dist**2))
                else:
                    coin_score += score_of_coin

            if lane_cars[i]:
                lane_score.append((i, lane_cars[i][0][1] + coin_score))
            else:
                if i == my_lane:
                    lane_score.append((i, 250+1 + coin_score))
                else:
                    lane_score.append((i, 250 + coin_score))


        lane_score.sort(key = lambda s: s[1], reverse = True)

        """
        if self.player_no == 0:
            for i in range(9):
                print(f"lane {i}", end='')
                print(lane_cars[i])
            print(lane_score)
            print(f"current lane: {my_lane}")
        """
        return lane_score


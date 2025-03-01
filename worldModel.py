class WorldModel:
    def __init__(self, agentType):
        self.agentType = agentType
        self.perceptor_dict = {'hj1': 0.0, 'hj2': 0.0, 'laj1': 0.0, 'laj2': 0.0, 'laj3': 0.0, 'laj4': 0.0, 'llj1': 0.0,
                               'llj2': 0.0, 'llj3': 0.0,
                               'llj4': 0.0,
                               'llj5': 0.0, 'llj6': 0.0, 'rlj1': 0.0, 'rlj2': 0.0, 'rlj3': 0.0, 'rlj4': 0.0,
                               'rlj5': 0.0,
                               'rlj6': 0.0, 'raj1': 0.0,
                               'raj2': 0.0,
                               'raj3': 0.0, 'raj4': 0.0}

        self.effector_dict = {'he1': 0.0, 'he2': 0.0, 'lae1': 0.0, 'lae2': 0.0, 'lae3': 0.0, 'lae4': 0.0, 'lle1': 0.0,
                              'lle2': 0.0, 'lle3': 0.0,
                              'lle4': 0.0, 'lle5': 0.0, 'lle6': 0.0, 'rle1': 0.0, 'rle2': 0.0, 'rle3': 0.0, 'rle4': 0.0,
                              'rle5': 0.0, 'rle6': 0.0,
                              'rae1': 0.0, 'rae2': 0.0, 'rae3': 0.0, 'rae4': 0.0}

        self.worldModel_dict = {'time': 0.0, 'pm': '', 'GYR': [0.0, 0.0, 0.0], 'ACC': [0.0, 0.0, 0.0],
                                'FRP_LC': [0.0, 0.0, 0.0],
                                'FRP_LF': [0.0, 0.0, 0.0],
                                'FRP_RC': [0.0, 0.0, 0.0], 'FRP_RF': [0.0, 0.0, 0.0], 'ball': [0.0, 0.0, 0.0]}

        if self.agentType == 4:
            self.effector_dict['rle7'] = 0.0
            self.effector_dict['lle7'] = 0.0
            self.perceptor_dict['rlj7'] = 0.0
            self.perceptor_dict['llj7'] = 0.0

    def updateWorld(self, serverList, agentList):
        # init
        self.worldModel_dict['FRP_LC'] = [0, 0, 0]
        self.worldModel_dict['FRP_LF'] = [0, 0, 0]
        self.worldModel_dict['FRP_RC'] = [0, 0, 0]
        self.worldModel_dict['FRP_RF'] = [0, 0, 0]

        for block in serverList:
            if 'time' in block:
                self.worldModel_dict['time'] = float(block[1][1])
            if 'GS' in block:
                self.worldModel_dict['pm'] = block[4][1]
            if 'GYR' in block:
                self.worldModel_dict['GYR'] = [float(block[2][1]), float(block[2][2]), float(block[2][3])]
            if 'ACC' in block:
                self.worldModel_dict['ACC'] = [float(block[2][1]), float(block[2][2]), float(block[2][3])]
            if 'See' in block:
                for x in block:
                    if 'B' in x:
                        self.worldModel_dict['ball'] = [float(x[1][1]), float(x[1][2]), float(x[1][3])]
            if 'FRP' in block:
                if block[1][1] == 'rf':
                    self.worldModel_dict['FRP_RC'] = [float(block[2][1]), float(block[2][2]), float(block[2][3])]
                    self.worldModel_dict['FRP_RF'] = [float(block[3][1]), float(block[3][2]), float(block[3][3])]
                if block[1][1] == 'lf':
                    self.worldModel_dict['FRP_LC'] = [float(block[2][1]), float(block[2][2]), float(block[2][3])]
                    self.worldModel_dict['FRP_LF'] = [float(block[3][1]), float(block[3][2]), float(block[3][3])]
            if 'HJ' in block:
                self.perceptor_dict[block[1][1]] = float(block[2][1])

        for block in agentList:
            if block[0] in self.effector_dict.keys():
                self.effector_dict[block[0]] = float(block[1])

        # print(self.effector_dict)
        # print(self.worldModel_dict)
        # print(self.perceptor_dict)

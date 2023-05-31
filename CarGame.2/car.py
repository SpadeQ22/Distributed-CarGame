class Car:
    def __init__(self,id):
        self.display_width = 800
        self.display_height = 600
        self.x_coordinate = None
        self.y_coordinate = None
        self.high_score = 0
        self.pending_message=False
        self.id=id
        self.initialize()

    def initialize(self):
        self.x_coordinate = (self.display_width * 0.45)
        self.y_coordinate = (self.display_height * 0.8)
        self.width = 49
        self.connected=False

    def to_dict(self,message):
        return {'id': self.id, 'x_coordinate': self.x_coordinate, 'y_coordinate': self.y_coordinate,'high_score': self.high_score,
                'message': message}





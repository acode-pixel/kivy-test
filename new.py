import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.clock import Clock
from kivy.vector import Vector
from random import randint

class PongPaddle(Widget):

    score = NumericProperty(0)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            speedup = 1.1
            offset = 0.02 * Vector(0, ball.center_y-self.center_y)
            ball.velocity = speedup * (offset - ball.velocity)

class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)

    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class PongGame(Widget):
    ball = ObjectProperty(None)

    def on_touch_move(self, touch):
        if touch.x < self.width/3:
            self.player1.center_y = touch.y
        if touch.x > self.width - self.width/3:
            self.player2.center_y = touch.y

    def serve_ball(self, vel):
        self.ball.center = self.center
        self.ball.velocity = vel

    def update(self, dt):
        self.ball.move()
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

        if(self.ball.y < 0) or (self.ball.top > self.height):
            self.ball.velocity_y *= -1

        if (self.ball.x < 0) or (self.ball.right > self.width):
            self.ball.velocity_x *= -1

        if self.ball.x < self.x:
            self.player2.score += 1
            self.serve_ball((4, 0))
        if self.ball.right > self.width:
            self.player1.score += 1
            self.serve_ball((-4, 0))

class PongApp(App):
    def build(self):
        game = PongGame()
        game.serve_ball((4, 0))
        Clock.schedule_interval(game.update, 1.0/60.0)
        return game

if __name__ == "__main__":
    PongApp().run()

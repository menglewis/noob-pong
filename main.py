from random import random
from math import sin, cos, pi
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.core.audio import SoundLoader


class PongPaddle(Widget):
    score = NumericProperty(0)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            sound = SoundLoader.load('audio/bounce.wav')
            if sound:
                sound.play()
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.1
            ball.velocity = vel.x, vel.y + offset


class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)
    base_velocity = None

    def serve_ball(self, vel=1):
        if self.base_velocity is None:
            self.base_velocity = self.width / 180
        if vel < 0:
            vel = -1 * self.base_velocity
        else:
            vel = self.base_velocity
        vel = self.get_random_serve_vector(vel)
        self.ball.center = self.center
        self.ball.velocity = vel
        print(self.width)

    def get_random_serve_vector(self, vel=None, max_angle=30):
        if vel is None:
            vel = self.base_velocity
        if max_angle > 75:
            max_angle = 75
        angle = ((random() * max_angle * 2 ) - max_angle ) * pi/180
        return (vel*cos(angle), vel*sin(angle))

    def update(self, dt):
        self.ball.move()

        #bounce of paddles
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

        #bounce ball off bottom or top
        if (self.ball.y < self.y) or (self.ball.top > self.top):
            self.ball.velocity_y *= -1

        #went of to a side to score point?
        if self.ball.x < self.x:
            self.player2.score += 1
            sound = SoundLoader.load('audio/noob.wav')
            if sound:
                sound.play()
            self.serve_ball(vel=4)
        if self.ball.x + self.ball.width > self.width:
            self.player1.score += 1
            sound = SoundLoader.load('audio/noob.wav')
            if sound:
                sound.play()
            self.serve_ball(vel=-4)

        #if self.player1.score >= 10:
        #   l = Label(text='Noob 1 wins!')
        #if self.player2.score >=10:
        #    l = Label(text='Noob 2 wins!')


    def on_touch_move(self, touch):
        if touch.x < self.width / 3:
            self.player1.center_y = touch.y
        if touch.x > self.width - self.width / 3:
            self.player2.center_y = touch.y


class PongApp(App):
    def build(self):
        game = PongGame()
        #game.base_velocity = float(game.width) / 20
        #print(game.base_velocity)
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game

if __name__ == '__main__':
    PongApp().run()
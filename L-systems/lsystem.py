import turtle

class LSystem:
    def __init__(self, screen):
        self.turtle = turtle.RawTurtle(screen)
        self.turtle.speed(0)
        self.turtle.hideturtle()
        self.drawing = True

    def clear(self):
        self.drawing = False
        self.turtle.clear()

    def setup_position(self, x, y, angle):
        self.turtle.penup()
        self.turtle.setposition(x, y)
        self.turtle.setheading(angle)
        self.turtle.pendown()

    def apply_rules(self, axiom, rules, iterations):
        for _ in range(iterations):
            new_axiom = ""
            for char in axiom:
                new_axiom += rules.get(char, char)
            axiom = new_axiom
        return axiom

    def draw(self, commands, angle, length):
        self.drawing = True
        stack = []
        for cmd in commands:
            if not self.drawing:
                break
            if cmd == 'F':
                self.turtle.forward(length)
            elif cmd == 'b':
                self.turtle.penup()
                self.turtle.forward(length)
                self.turtle.pendown()
            elif cmd == '+':
                self.turtle.right(angle)
            elif cmd == '-':
                self.turtle.left(angle)
            elif cmd == '[':
                stack.append((self.turtle.position(), self.turtle.heading()))
            elif cmd == ']':
                pos, heading = stack.pop()
                self.turtle.penup()
                self.turtle.setposition(pos)
                self.turtle.setheading(heading)
                self.turtle.pendown()
        

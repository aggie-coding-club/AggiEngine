from Box2D import b2ContactListener

class ContactListener(b2ContactListener):
    def __init__(self):
        b2ContactListener.__init__(self)
    def BeginContact(self, contact):
        bodyA = contact.fixtureA.body
        bodyB = contact.fixtureB.body
        bodyA.userData.BeginContact(bodyB)
        bodyB.userData.BeginContact(bodyA)

    def EndContact(self, contact):
        bodyA = contact.fixtureA.body
        bodyB = contact.fixtureB.body
        bodyA.userData.EndContact(bodyB)
        bodyB.userData.EndContact(bodyA)

    def PreSolve(self, contact, manifold):
        bodyA = contact.fixtureA.body
        bodyB = contact.fixtureB.body
        bodyA.userData.PreSolve(bodyB, manifold)
        bodyB.userData.PreSolve(bodyA, manifold)
    
    def PostSolve(self, contact, impulse):
        bodyA = contact.fixtureA.body
        bodyB = contact.fixtureB.body
        bodyA.userData.PostSolve(bodyB, impulse)
        bodyB.userData.PostSolve(bodyA, impulse)
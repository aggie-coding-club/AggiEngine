from Box2D import b2ContactListener


class ContactListener(b2ContactListener):

    def __init__(self):
        b2ContactListener.__init__(self)

    def BeginContact(self, contact):
        bodyA = contact.fixtureA.body
        bodyB = contact.fixtureB.body
        bodyA.userData.beginContact(bodyB)
        bodyB.userData.beginContact(bodyA)

    def EndContact(self, contact):
        bodyA = contact.fixtureA.body
        bodyB = contact.fixtureB.body
        bodyA.userData.endContact(bodyB)
        bodyB.userData.endContact(bodyA)

    def PreSolve(self, contact, manifold):
        bodyA = contact.fixtureA.body
        bodyB = contact.fixtureB.body
        bodyA.userData.preSolve(bodyB, manifold)
        bodyB.userData.preSolve(bodyA, manifold)

    def PostSolve(self, contact, impulse):
        bodyA = contact.fixtureA.body
        bodyB = contact.fixtureB.body
        bodyA.userData.postSolve(bodyB, impulse)
        bodyB.userData.postSolve(bodyA, impulse)

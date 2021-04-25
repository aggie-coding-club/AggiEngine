from Box2D import b2ContactListener


class ContactListener(b2ContactListener):

    def __init__(self):
        b2ContactListener.__init__(self)

    def BeginContact(self, contact):
        """
        Called when two Box2D bodies collide and calls their beginContact(otherBody) methods
        ``contact:`` The contact event
        """
        bodyA = contact.fixtureA.body
        bodyB = contact.fixtureB.body
        bodyA.userData.beginContact(bodyB)
        bodyB.userData.beginContact(bodyA)

    def EndContact(self, contact):
        """
        Called when two Box2D bodies collide and calls their endContact(otherBody) methods
        ``contact:`` The contact event
        """
        bodyA = contact.fixtureA.body
        bodyB = contact.fixtureB.body
        bodyA.userData.endContact(bodyB)
        bodyB.userData.endContact(bodyA)

    def PreSolve(self, contact, manifold):
        '''
        Called before Box2D handles a contact while the bodies are still overlapping
        '''
        bodyA = contact.fixtureA.body
        bodyB = contact.fixtureB.body
        bodyA.userData.preSolve(bodyB, manifold)
        bodyB.userData.preSolve(bodyA, manifold)

    def PostSolve(self, contact, impulse):
        '''
        Called after Box2D handles a contact while the bodies are no longer overlapping
        '''
        bodyA = contact.fixtureA.body
        bodyB = contact.fixtureB.body
        bodyA.userData.postSolve(bodyB, impulse)
        bodyB.userData.postSolve(bodyA, impulse)

import pystk


def control(aim_point, current_vel):
    """
    Set the Action for the low-level controller
    :param aim_point: Aim point, in screen coordinate frame [-1..1]
    :param current_vel: Current velocity of the kart
    :return: a pystk.Action (set acceleration, brake, steer, drift)
    """
    action = pystk.Action()

    """
    Your code here 
    Hint: Use action.acceleration (0..1) to change the velocity. Try targeting a target_velocity (e.g. 20).
        action.acceleration the acceleration of the kart normalized to [0, 1 ]
    Hint: Use action.brake to True/False to brake (optionally)
        action.brake boolean indicator for braking
    Hint: Use action.steer to turn the kart towards the aim_point, clip the steer angle to -1..1
        action.steer the steering angle of the kart normalized to [-1, 1]
    Hint: You may want to use action.drift=True for wide turns (it will turn faster)
        action.drift a special action that makes the kart drift, useful for tight turns
    
    action.nitro burns nitro for fast acceleration
    
    - Play around with setting a target velocity, and setting your acceleration to achieve that velocity
    - If the first entry of your aim point is negative, that means you want to turn left, since the target 
        point is to the left of the center of the screen; and if the first entry of your aim point is positive,
        this means that you want to turn right.
    - If your aim point is too far left or far right, this means you are turning hard and should set drift to true
    """

    target_velocity = 0
    action.steer = aim_point[0]
    if action.steer > 0.3:
        action.steer = 1
    if action.steer < -0.3:
        action.steer = -1

    if -0.1 <= action.steer <= 0.1:
        target_velocity = 50
    elif -0.2 <= action.steer <= 0.2:
        target_velocity = 45
    elif -0.35 <= action.steer <= 0.35:
        target_velocity = 35
        action.drift = True
    elif -0.4 <= action.steer <= 0.4:
        target_velocity = 28
        action.drift = True
    else:
        target_velocity = 15
        action.drift = True

    vel_diff = target_velocity - current_vel

    if vel_diff > 30:
        action.acceleration = 1
        action.nitro = True
    elif vel_diff > 20:
        action.acceleration = 0.8
    elif vel_diff > 0:
        action.acceleration = 0.3
    else:
        action.brake = True

    return action


if __name__ == '__main__':
    from utils import PyTux
    from argparse import ArgumentParser


    def test_controller(args):
        import numpy as np
        pytux = PyTux()
        for t in args.track:
            steps, how_far = pytux.rollout(t, control, max_frames=1000, verbose=args.verbose)
            print(steps, how_far)
        pytux.close()


    parser = ArgumentParser()
    parser.add_argument('track', nargs='+')
    parser.add_argument('-v', '--verbose', action='store_true')
    args = parser.parse_args()
    test_controller(args)

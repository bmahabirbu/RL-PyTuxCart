import pystk


def control(aim_point, current_vel, steer_gain=6, skid_thresh=0.2, target_vel=25):
    import numpy as np
    #this seems to initialize an object
    action = pystk.Action()

    #compute acceleration
    target_velocity = 25
    action.brake = False
    action.nitro = True

    X = aim_point[0]
    Y = aim_point[1]*-1
    action.steer = np.arctan(Y/X)
    
    if(current_vel < 8*target_velocity/16):
        action.acceleration = 1
    elif(current_vel < 7*target_velocity/8 and current_vel > 8*target_velocity/16):
        action.acceleration = .7
    elif(current_vel < target_velocity and current_vel > 7*target_velocity/8):
        action.acceleration = .55
    else:
        action.acceleration = -1
        action.brake = True
        
    if(aim_point[0] > .3):
        action.steer = 1
    if(aim_point[0] < -.3):
        action.steer = -1
    if(aim_point[0] > .05):
        action.steer = .9
    if(aim_point[0] < -.05):
        action.steer = -.9

    if (aim_point[0] < 1 and aim_point[0] > .3):
        action.drift = True
    if(aim_point[0] > -1 and aim_point[0] < -.3):
        action.drift = True

    return action

if __name__ == '__main__':
    from utils import PyTux
    from argparse import ArgumentParser

    def test_controller(args):
        import numpy as np
        pytux = PyTux()
        for t in args.track:
            #it seems that steps measures the number of steps until termination (with max_frames=1000 ensuring termination after 1000 steps)
            #how far measures the amount traversed by the cart
            steps, how_far = pytux.rollout(t, control, max_frames=1000, verbose=args.verbose)
            print(steps, how_far)
        pytux.close()


    parser = ArgumentParser()
    parser.add_argument('track', nargs='+')
    parser.add_argument('-v', '--verbose', action='store_true')
    args = parser.parse_args()
    test_controller(args)

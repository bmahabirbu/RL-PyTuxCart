import pystk
import numpy as np

def control(aim_point, current_vel):
    """
    Set the Action for the low-level controller
    :param aim_point: Aim point, in screen coordinate frame [-1..1]
    :param current_vel: Current velocity of the kart
    :return: a pystk.Action (set acceleration, brake, steer, drift)
    """
    #aim_point [-1,1] Top right [1,-1] Bottom left [1,1] Bottom right [-1,-1] Top left.
    
    action = pystk.Action()
    
    target_velocity = 22

    #print("aim point",aim_point)
    #print("Speed",current_vel)
    
    action.nitro = True

    if(current_vel < target_velocity/2):
        action.acceleration = 1
        
    elif(current_vel > target_velocity/2 and current_vel < 7*target_velocity/8):
        action.acceleration = 0.6 # .97377
        
    elif(current_vel > 7*target_velocity/8 and current_vel < target_velocity):
        action.acceleration = -0.25 # -.140493
        
    elif(current_vel >= target_velocity):
        action.acceleration = -0.95 # -0.94901
        action.brake = True
    
    #print("Accel",action.acceleration)


    if(abs(aim_point[0]) <= 0.025): #0.025
        action.steer = 0
        
    elif(abs(aim_point[0]) >= 0.025 and abs(aim_point[0]) <= 0.2): # 0.025
        action.steer = aim_point[0]
        
    elif(abs(aim_point[0]) > 0.2):
        
        if(aim_point[0] > 0):
            action.steer = 1
        elif(aim_point[0] < 0):
            action.steer = -1
            
        if(abs(aim_point[0]) >= 0.3):
            action.drift = True
    
    #print("steer angle",action.steer)

    
    return action
    
    
    """
    Your code here
    Hint: Use action.acceleration (0..1) to change the velocity. Try targeting a target_velocity (e.g. 20).
    Hint: Use action.brake to True/False to brake (optionally)
    Hint: Use action.steer to turn the kart towards the aim_point, clip the steer angle to -1..1
    Hint: You may want to use action.drift=True for wide turns (it will turn faster)
    """
    

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

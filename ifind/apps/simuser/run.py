import sys
from sim_user import SimulatedUser
from progress_indicator import ProgressIndicator
from config_readers.simulation_config_reader import SimulationConfigReader

def main(config_filename):
    """
    The main simulation!
    For every configuration permutation, create a Simulated user object, and run the simulation (the while loop).
    Then save, report, and repeat ad naseum.
    """
    config_reader = SimulationConfigReader(config_filename)
    
    print dir(config_reader)
    
    for configuration in config_reader:
        user = SimulatedUser(configuration)
        user.show_query_list()
        progress = ProgressIndicator(configuration)
        
        configuration.output.display_config()
        
        while not configuration.user.logger.is_finished():
            progress.update()  # Update the progress indicator in the terminal.
            user.decide_action()
        
        configuration.output.display_report()
        configuration.output.save()

def usage(script_name):
    """
    Prints the usage message to the output stream.
    """
    print "Usage: {0} [configuration_filename]".format(script_name)

if __name__ == '__main__':
    if len(sys.argv) < 2 or len(sys.argv) > 2:
        usage(sys.argv[0])
    else:
        main(sys.argv[1])
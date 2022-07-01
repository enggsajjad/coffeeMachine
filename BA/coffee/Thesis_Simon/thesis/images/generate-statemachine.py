from transitions.extensions import GraphMachine as Machine

class CoffeeMachine():
    states = ['water_alert', 'coffee_ground', 'get_uid', 'unlocked',
              'wait_water_finished', 'wait_coffee_finished', 'wait_order_complete', 'maintenance']

    transitions = [
        # trigger, source, destination
        {'trigger': 'water_level_high', 'source': 'get_uid', 'dest': 'water_alert'},
        {'trigger': 'unlock', 'source': 'get_uid', 'dest': 'unlocked'},
        {'trigger': 'water_level_low', 'source': 'water_alert', 'dest': 'get_uid'},
        {'trigger': 'grinder_low', 'source': 'unlocked', 'dest': 'coffee_ground'},
        {'trigger': 'flow_2_started', 'source': 'unlocked',
            'dest': 'wait_water_finished'},
        {'trigger': 'flow_2_stopped', 'source': 'wait_water_finished',
            'dest': 'wait_order_complete'},
        {'trigger': 'flow_1_started', 'source': 'coffee_ground',
            'dest': 'wait_coffee_finished'},
        {'trigger': 'flow_1_stopped', 'source': 'wait_coffee_finished',
            'dest': 'wait_order_complete'},
        {'trigger': 'sleep_detected',
            'source': 'wait_water_finished', 'dest': 'unlocked'},
        {'trigger': 'order_complete',
            'source': 'wait_order_complete', 'dest': 'get_uid'},
        # {'trigger': 'maintenance', 'source': '*', 'dest': 'maintenance'},
        # {'trigger': 'reset', 'source': '*', 'dest': 'get_uid'},
        # cheating detection
        {'trigger': 'grinder_low', 'source': 'get_uid', 'dest': 'coffee_ground', 'before': 'detect_cheating',
            'conditions': 'cheating_condition'},
        # {'trigger': 'grinder_low', 'source': 'water_alert', 'dest': 'coffee_ground'},
    ]

    def __init__(self):

        self.machine = Machine(self, states=self.states,
                               transitions=self.transitions,
                               queued=True,
                               initial='get_uid',
                               use_pygraphviz=False,
                               show_state_attributes=True)

cm = CoffeeMachine()
cm.machine.get_graph().draw('my_state_diagram.png', prog='dot')
import simpy


""" first try """
# def car(env):
#     while True:
#         print('Start parking at %d' % env.now)
#         parking_duration = 5
#         yield env.timeout(parking_duration)
#
#         print('Start driving at %d' % env.now)
#         trip_duration = 2
#         yield env.timeout(trip_duration)

# env = simpy.Environment()
# env.process(car(env))
# env.run(until=15)

""" interrupting """
# (https://simpy.readthedocs.io/en/latest/simpy_intro/process_interaction.html#interrupting-another-process)


# def driver(env, car):
#     yield env.timeout(3)
#     car.action.interrupt()
#
#
# class Car(object):
#     def __init__(self, env):
#         self.env = env
#         print(type(self.run()))
#         print(type(self.run))
#         self.action = env.process(self.run())
#
#     def run(self):
#         while True:
#             print('Start parking and charging at {}'.format(self.env.now))
#             charge_duration = 5
#             try:
#                 yield self.env.process(self.charge(charge_duration))
#             except simpy.Interrupt:
#                 print('Interrupted')
#
#             print("Start driving at {}".format(self.env.now))
#             trip_duration = 2
#             yield self.env.timeout(trip_duration)
#
#     def charge(self, duration):
#         yield self.env.timeout(duration)
#
#
# env = simpy.Environment()
# car = Car(env)
# env.process(driver(env, car))
# env.run(until=15)

""" Shared Resource """


# def car(env, name, bcs, driving_time, charge_duration):
#     # Simulate driving to the BCS
#     yield env.timeout(driving_time)
#
#     # Request one of its charging spots
#     print('%s arriving at %d' % (name, env.now))
#     with bcs.request() as req:
#         yield req
#
#         # Charge the battery
#         print('%s starting to charge at %s' % (name, env.now))
#         yield env.timeout(charge_duration)
#         print('%s leaving the bcs at %s' % (name, env.now))
#
#
# env = simpy.Environment()
# bcs = simpy.Resource(env, capacity=2)
#
# for i in range(4):
#     env.process(car(env, 'Car %d' % i, bcs, i*2, 5))
#
# env.run()

"""Event example"""


class School:
    def __init__(self, env):
        self.env = env
        self.class_ends = env.event()
        self.pupil_procs = [env.process(self.pupil()) for i in range(3)]
        self.bell_proc = env.process(self.bell())

    def bell(self):
        for i in range(2):
            yield self.env.timeout(45)
            # print("in bell", i, self.class_ends.triggered)
            # print("in bell", i, self.class_ends.processed)
            self.class_ends.succeed()
            # print("in bell", i, self.class_ends.triggered)
            # print("in bell", i, self.class_ends.processed)
            print("in bell", i, self.class_ends.callbacks)
            self.class_ends = self.env.event()
            print("Bell rang")

    def pupil(self):
        for i in range(2):
            yield self.class_ends
            print(r' \o/', end='')
            print(self.env.active_process)


env = simpy.Environment()
school = School(env)
# env.run()
while env.peek() != float('inf'):
    print(env.peek())
    env.step()
    # print(school.class_ends, school.class_ends.processed)

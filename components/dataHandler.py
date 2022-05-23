import warnings
import pandas as pd
from datetime import datetime


class dataHandler:
    times = pd.DataFrame(columns=['Duty ID', 'Start Time', 'End Time', 'Start Stop Description', 'End Stop Description'])
    breaks = pd.DataFrame(columns=['Duty ID', 'Break Start Time', 'Break Duration', 'Break Stop Name'])

    def getTime(self, data):
        duty_id = []
        start_time = []
        end_time = []
        start_stop = []
        end_stop = []
        for duty in data.get('duties'):
            duty_id.append(duty.get('duty_id'))
            duty_start = duty.get('duty_events')[0].get('start_time')  # try to get start_time from first value of list
            start_desc = duty.get('duty_events')[0].get('origin_stop_id')
            last_index = len(duty.get('duty_events')) - 1  # index of last value to get end time
            duty_end = duty.get('duty_events')[last_index].get('end_time')
            end_desc = duty.get('duty_events')[last_index].get('destination_stop_id')

            if duty_start is None or duty_end is None:
                if duty_start is None:
                    start_id, start_sequence, start_index, start_desc = \
                        duty.get('duty_events')[0].get('vehicle_id'), \
                        duty.get('duty_events')[0].get('vehicle_event_sequence'), \
                        None, \
                        duty.get('duty_events')[0].get('origin_stop_id')
                if duty_end is None:
                    end_id, end_sequence, end_index, end_desc = \
                        duty.get('duty_events')[last_index].get('vehicle_id'), \
                        duty.get('duty_events')[last_index].get('vehicle_event_sequence'), \
                        None, \
                        duty.get('duty_events')[last_index].get('destination_stop_id')
                for i in range(0, len(data.get('vehicles'))):
                    if data.get('vehicles')[i].get('vehicle_id') == start_id and start_index is None:
                        start_index = i
                    if data.get('vehicles')[i].get('vehicle_id') == end_id and end_index is None:
                        end_index = i
                if duty_start is None:
                    duty_start = data.get('vehicles')[start_index].get('vehicle_events')[start_sequence].get(
                        'start_time')
                    start_desc = data.get('vehicles')[start_index].get('vehicle_events')[start_sequence].get(
                        'origin_stop_id')
                if duty_end is None:
                    duty_end = data.get('vehicles')[end_index].get('vehicle_events')[end_sequence].get('end_time')
                    end_desc = data.get('vehicles')[end_index].get('vehicle_events')[end_sequence].get(
                        'destination_stop_id')
                if duty_start is None or duty_end is None:
                    raise Exception("Start or End time is None")
                if start_desc is None or end_desc is None:
                    raise Exception("Start or End stop description is None")
            start_time.append(duty_start)
            end_time.append(duty_end)
            start_stop.append(start_desc)
            end_stop.append(end_desc)
        dataHandler.times = pd.DataFrame(list(zip(duty_id, start_time,
                              end_time, start_stop, end_stop)),
                     columns=['Duty ID', 'Start Time', 'End Time', 'Start Stop Description', 'End Stop Description'])

    def getBreaks(self, data):
        duty_id = None
        for duty in data.get('duties'):
            duty_id = duty.get('duty_id')
            break_start_time = None
            break_duration = None
            break_stop_name = None
            first_trip_end = 0
            second_trip_start = 0
            last_event_index = len(duty.get('duty_events')) - 1

            for i in range(0,len(duty.get('duty_events'))):
                first_trip_end = None
                second_trip_start = None
                if i != last_event_index:
                    first_trip_end = duty.get('duty_events')[i].get('end_time')  # try to get start time in case it's a taxi or alike service
                    second_trip_start = duty.get('duty_events')[i+1].get('start_time')  # same as above but for next service
                    if first_trip_end is None:
                        first_id = duty.get('duty_events')[i].get('vehicle_id')
                        start_sequence = duty.get('duty_events')[i].get('vehicle_event_sequence')
                        for x in range(0, len(data.get('vehicles'))):
                            if data.get('vehicles')[x].get('vehicle_id') == first_id:
                                first_trip_end,  first_stop_name = dataHandler.isServiceTrip(data.get('vehicles')[x].get('vehicle_events')[start_sequence], 'end', data)
                            if second_trip_start is None:
                                second_id = duty.get('duty_events')[i+1].get('vehicle_id')
                                second_sequence = duty.get('duty_events')[i+1].get('vehicle_event_sequence')
                                if data.get('vehicles')[x].get('vehicle_id') == second_id:
                                    second_trip_start = dataHandler.isServiceTrip(data.get('vehicles')[x].get('vehicle_events')[second_sequence], 'start', data)
                            if second_trip_start is not None and first_trip_end is not None:
                                break
                    else:
                        first_stop_name = duty.get('duty_events')[i].get('destination_stop_id')
                        if second_trip_start is None:
                            second_id = duty.get('duty_events')[i + 1].get('vehicle_id')
                            second_sequence = duty.get('duty_events')[i + 1].get('vehicle_event_sequence')
                            for x in range(0, len(data.get('vehicles'))):
                                if data.get('vehicles')[x].get('vehicle_id') == second_id:
                                    second_trip_start = dataHandler.isServiceTrip(data.get('vehicles')[x].get('vehicle_events')[second_sequence], 'start', data)
                                    break
                    try:
                        first_trip_end = first_trip_end.split('.')
                        second_trip_start = second_trip_start.split('.')
                    except:  # Check if trip times area available
                        raise Exception('First trip end time or second trip start time missing')
                    break_duration = (datetime.strptime(second_trip_start[1], '%H:%M') - datetime.strptime(first_trip_end[1], '%H:%M'))
                    break_duration = int(break_duration.seconds / 60)
                    if break_duration > 0:
                        break_start_time = first_trip_end[1]
                        break_stop_name = first_stop_name
                        try:
                            with warnings.catch_warnings():
                                warnings.simplefilter(action='ignore', category=FutureWarning)
                                dataHandler.breaks = dataHandler.breaks.append({'Duty ID': duty_id, 'Break Start Time': break_start_time, 'Break Duration': break_duration, 'Break Stop Name': break_stop_name}, ignore_index = True)
                        except:
                            raise Exception('Check if dataframe was updated')

    @staticmethod
    def isServiceTrip(vehicle_event, type, data):
        if vehicle_event.get('trip_id') is None:
            if type == 'end':
                return (vehicle_event.get('end_time'), vehicle_event.get('destination_stop_id'))
            elif type == 'start':
                return vehicle_event.get('start_time')
        else:
            trip_id = vehicle_event.get('trip_id')
            for trip in data.get('trips'):
                if trip.get('trip_id') == trip_id:
                    if type == 'end':
                        return (trip.get('arrival_time'), trip.get('destination_stop_id'))
                    elif type == 'start':
                        return trip.get('departure_time')

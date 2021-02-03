"""
combine_runs.py

This function generates the inputs for a run that combines
constraints from multiple runs according to the given inputs.
It then runs StorageVET.

Zhenhua Zhang Jan 16 2021
"""

import pandas as pd
import numpy as np
import copy

# TODO
def combine_runs(SVet_absolute_path, multiple_runID, app_types, app_hours, regulation_scenario):
    """This function takes as input the type of regulatory scenario desired and three
  pieces of information regarding each run used to make the combined run: the run number,
  the resource type {“NSR”,”SR”,”RA1”,”RA0”,”DR1”,”DR0”…} and the hours in which a resource
  is given priority (e.g. [[6,16], [16,23]]), which may not overlap. It uses this information
  to run StorageVET with the desired combination of storage value stacking"""

    # check that multiple_runID, app_types, and app_hours are the same length
    if all(len(lst) == len(multiple_runID) for lst in [app_types, app_hours]):
        pass
    else:
        raise ValueError("wrong input list length for combine_runs")

    # check for overlap in app_hours & that each element has length 2

    # create empty matrix of user constraints

    # create placeholder for value

    # for each resource...
    for i in range(len(multiple_runID)):
        pass
        # ID folder:
        # read in runs log file
        # runsLog = pd.read_csv(SVet_Path + runs_log_file)
        # runsfilter = runsLog['runID'] == runIDs[i]
        # shortname = runsLog.loc[runsLog['runID'] == runIDs[i]]['shortname'].values[0]
        # # id row with runID
        # # id shortname
        #
        # # call appropriate read-in fn for that resource
        # resultsPath = SVet_Path + "Results/output_run" + str(
        #     runIDs[i]) + "_" + shortname + "/"  # "timeseries_results_runID" + str(runIDs[i]) + ".csv"
        #
        # resType_to_fn(resTypes[i], resultsPath, resHours[i], regScenario)

        # add outputs to user constraint matrix
        # select for most binding user constraints
        # add value to value placeholder

    # write new hourly_timseries input file

    # git commit if NOT test

    # run svet via vc_wrap

    return None


class ConstraintObject:
    def __init__(self, SvetObject, app_hours, regulation_scenario):
        previous_params = SvetObject.new_params
        self.previous_runID = SvetObject.runID
        self.previous_svrun_params = SvetObject.params

        self.previous_initial_hourly_timeseries = SvetObject.initial_hourly_timeseries
        self.runID_result_folder_path = SvetObject.runID_result_folder_path

        # Load constraint parameters
        self.app_hours = app_hours
        self.regulation_scenario = regulation_scenario

        # Load general parameters from previous runID results
        self.battery_charging_power_max = float(previous_params.loc[(previous_params['Tag'] == 'Battery') &
                                                                    (previous_params['Key'] == 'ch_max_rated'),
                                                                    'Value'].values[0])
        self.battery_discharging_power_max = float(previous_params.loc[(previous_params['Tag'] == 'Battery') &
                                                                       (previous_params['Key'] == 'dis_max_rated'),
                                                                       'Value'].values[0])
        self.battery_energy_rated = float(previous_params.loc[(previous_params['Tag'] == 'Battery') &
                                                              (previous_params['Key'] == 'ene_max_rated'),
                                                              'Value'].values[0])
        self.max_soc = float(previous_params.loc[(previous_params['Tag'] == 'Battery') &
                                                 (previous_params['Key'] == 'ulsoc'), 'Value'].values[0]) / 100
        self.min_soc = float(previous_params.loc[(previous_params['Tag'] == 'Battery') &
                                                 (previous_params['Key'] == 'llsoc'), 'Value'].values[0]) / 100
        self.round_trip_efficiency = float(previous_params.loc[(previous_params['Tag'] == 'Battery') &
                                                               (previous_params['Key'] == 'rte'),
                                                               'Value'].values[0]) / 100

        # Load FR scenario parameters
        self.FR_combine_markets = bool(previous_params.loc[(previous_params['Tag'] == 'FR') &
                                                           (previous_params['Key'] == 'CombinedMarket'),
                                                           'Value'].values[0])

        # Load RA scenario parameters
        self.RA_length = float(previous_params.loc[(previous_params['Tag'] == 'RA') &
                                                   (previous_params['Key'] == 'length'), 'Value'].values[0])

        # Load previous dispatched results from the runID folder
        previous_outputs = pd.read_csv(SvetObject.runID_dispatch_timeseries_path)
        previous_outputs['datetime'] = pd.to_datetime(previous_outputs.iloc[:, 0])
        previous_outputs_datetime = previous_outputs['datetime']
        previous_outputs.set_index('datetime')
        self.previous_outputs = previous_outputs

        # Initialize a constraint object
        output = pd.DataFrame(index=previous_outputs_datetime,
                              columns=["chgMin_kW", "chgMax_kW", "eMin_kWh", "eMax_kWh"])
        output.loc[:, "eMin_kWh"] = self.battery_energy_rated * self.min_soc
        output.loc[:, "eMax_kWh"] = self.battery_energy_rated * self.max_soc  # TODO: double counted max_soc previously
        output.loc[:, "chgMin_kW"] = - self.battery_charging_power_max  # TODO: why?
        output.loc[:, "chgMax_kW"] = self.battery_charging_power_max  # TODO: why?
        self.output = output

        # Determine indexes
        self.window_start_index = output.index.hour == app_hours[0]
        self.window_index = (output.index.hour >= app_hours[0]) & (output.index.hour <= app_hours[1])
        self.window_end_index = output.index.hour == app_hours[1]

    def set_NSR_user_constraints(self):
        # Create user constraints based on resource hours and regulation scenario
        NSR_contraint_output = self.output.copy(deep=True).reset_index(drop=True)

        if self.regulation_scenario == 1:  # ENERGY reservations based on resource hours & service prices
            # TODO: account for different ch/disch, and CHARGING EFFICIENCY
            NSR_contraint_output.loc[self.window_index, "chgMin_kW"] = - 1
            NSR_contraint_output.loc[self.window_index, "chgMax_kW"] = 1
            NSR_contraint_output.loc[self.window_index, "eMin_kWh"] = \
                self.battery_energy_rated * self.min_soc + self.battery_charging_power_max  # TODO: why not +discharge?
            NSR_contraint_output.loc[self.window_index, "eMax_kWh"] = \
                self.battery_energy_rated * self.max_soc - self.battery_charging_power_max * self.round_trip_efficiency  # TODO: why -?

            # Calculate NSR values
            previous_outputs_values = self.previous_outputs["NSR Price Signal ($/kW)"] * self.battery_charging_power_max
            NSR_values = sum(previous_outputs_values[self.window_index])

        elif self.regulation_scenario == 2:  # ONE-SIDED reservations based on resource hours
            raise ValueError("regulation_scenario 2 doesn't exist yet for NSR")
        elif self.regulation_scenario == 3:  # Reservations based on PREVIOUS DISPATCH
            # Avoid infeasibility TODO: understand this
            prebvious_outputs_copy = self.previous_outputs.copy(deep=True)
            sel = (prebvious_outputs_copy['Non-spinning Reserve (Discharging) (kW)'] +
                   prebvious_outputs_copy[
                       'Non-spinning Reserve (Charging) (kW)']) >= self.battery_charging_power_max * 2
            prebvious_outputs_copy.loc[sel, 'Non-spinning Reserve (Discharging) (kW)'] = \
                prebvious_outputs_copy.loc[sel, 'Non-spinning Reserve (Discharging) (kW)'] - 1

            charging_min = - 1 * (self.battery_discharging_power_max -
                                  prebvious_outputs_copy['Non-spinning Reserve (Discharging) (kW)'])
            charging_max = self.battery_charging_power_max - \
                           prebvious_outputs_copy['Non-spinning Reserve (Charging) (kW)']
            energy_min = self.battery_energy_rated * self.min_soc + \
                         prebvious_outputs_copy['Non-spinning Reserve (Discharging) (kW)']
            energy_max = self.battery_energy_rated * self.max_soc - \
                         prebvious_outputs_copy['Non-spinning Reserve (Charging) (kW)'] * self.round_trip_efficiency

            # Update constraints in the output
            NSR_contraint_output.loc[self.window_index, "chgMin_kW"] = charging_min.loc[self.window_index]
            NSR_contraint_output.loc[self.window_index, "chgMax_kW"] = charging_max.loc[self.window_index]
            NSR_contraint_output.loc[self.window_index, "eMin_kWh"] = energy_min.loc[self.window_index]
            NSR_contraint_output.loc[self.window_index, "eMax_kWh"] = energy_max.loc[self.window_index]

            # Calculate NSR values
            previous_outputs_values = prebvious_outputs_copy["NSR Price Signal ($/kW)"] * \
                                      (prebvious_outputs_copy['Non-spinning Reserve (Discharging) (kW)'] +
                                       prebvious_outputs_copy['Non-spinning Reserve (Charging) (kW)'])
            NSR_values = sum(previous_outputs_values[self.window_index])

        else:
            raise ValueError("regulation_scenario must be 1, 2 or 3")

        # Create a new hourly timeseries dataframe as the Scenario time series file for a new SV run
        new_hourly_timeseries = self.previous_initial_hourly_timeseries.copy(deep=True)
        new_hourly_timeseries['Power Min (kW)'] = np.array(NSR_contraint_output['chgMin_kW'])
        new_hourly_timeseries['Power Max (kW)'] = np.array(NSR_contraint_output['chgMax_kW'])
        new_hourly_timeseries['Energy Max (kWh)'] = np.array(NSR_contraint_output['eMax_kWh'])
        new_hourly_timeseries['Energy Min (kWh)'] = np.array(NSR_contraint_output['eMin_kWh'])

        new_shortname = "runID{}_constraintNSR_rs{}_hr{}-{}".format(self.previous_runID, self.regulation_scenario,
                                                                    self.app_hours[0], self.app_hours[1])
        old_svrun_params = self.previous_svrun_params
        new_svrun_params = copy.deepcopy(old_svrun_params)
        new_svrun_params['NSR_active'] = "no"
        for k in ['Scenario_time_series_filename', 'Results_dir_absolute_path',
                  'Results_label', 'Results_errors_log_path']:
            new_svrun_params.pop(k, None)
        new_hourly_timeseries_path = self.runID_result_folder_path + \
                                     "/_new_hourly_timeseries_{}.csv".format(new_shortname)
        new_hourly_timeseries.to_csv(new_hourly_timeseries_path, index=False)

        return old_svrun_params, new_svrun_params, new_shortname, new_hourly_timeseries_path, NSR_values

    def set_SR_user_constraints(self):
        """create user constraints for spinning reserve within window defined by resHour
      according to the logic of the regScenario """
        # Create user constraints based on resource hours and regulation scenario
        SR_contraint_output = self.output.copy(deep=True).reset_index(drop=True)

        if self.regulation_scenario == 1:  # ENERGY reservations based on resource hours & service prices
            # TODO: account for different ch/disch, and CHARGING EFFICIENCY
            SR_contraint_output.loc[self.window_index, "chgMin_kW"] = - 1
            SR_contraint_output.loc[self.window_index, "chgMax_kW"] = 1
            SR_contraint_output.loc[self.window_index, "eMin_kWh"] = \
                self.battery_energy_rated * self.min_soc + self.battery_charging_power_max  # TODO: why not +discharge?
            SR_contraint_output.loc[self.window_index, "eMax_kWh"] = \
                self.battery_energy_rated * self.max_soc - self.battery_charging_power_max * self.round_trip_efficiency  # TODO: why -?

            # Calculate NSR values
            previous_outputs_values = self.previous_outputs["SR Price Signal ($/kW)"] * self.battery_charging_power_max
            SR_values = sum(previous_outputs_values[self.window_index])

        elif self.regulation_scenario == 2:  # ONE-SIDED reservations based on resource hours
            raise ValueError("regulation_scenario 2 doesn't exist yet for SR")
        elif self.regulation_scenario == 3:  # Reservations based on PREVIOUS DISPATCH
            # Avoid infeasibility TODO: understand this
            prebvious_outputs_copy = self.previous_outputs.copy(deep=True)
            sel = (prebvious_outputs_copy['Spinning Reserve (Discharging) (kW)'] +
                   prebvious_outputs_copy['Spinning Reserve (Charging) (kW)']) >= self.battery_charging_power_max * 2
            prebvious_outputs_copy.loc[sel, 'Spinning Reserve (Discharging) (kW)'] = \
                prebvious_outputs_copy.loc[sel, 'Spinning Reserve (Discharging) (kW)'] - 1

            charging_min = - 1 * (self.battery_discharging_power_max -
                                  prebvious_outputs_copy['Spinning Reserve (Discharging) (kW)'])
            charging_max = self.battery_charging_power_max - \
                           prebvious_outputs_copy['Spinning Reserve (Charging) (kW)']
            energy_min = self.battery_energy_rated * self.min_soc + \
                         prebvious_outputs_copy['Spinning Reserve (Discharging) (kW)']
            energy_max = self.battery_energy_rated * self.max_soc - \
                         prebvious_outputs_copy['Spinning Reserve (Charging) (kW)'] * self.round_trip_efficiency

            # Update constraints in the output
            SR_contraint_output.loc[self.window_index, "chgMin_kW"] = charging_min.loc[self.window_index]
            SR_contraint_output.loc[self.window_index, "chgMax_kW"] = charging_max.loc[self.window_index]
            SR_contraint_output.loc[self.window_index, "eMin_kWh"] = energy_min.loc[self.window_index]
            SR_contraint_output.loc[self.window_index, "eMax_kWh"] = energy_max.loc[self.window_index]

            # Calculate NSR values
            previous_outputs_values = prebvious_outputs_copy["SR Price Signal ($/kW)"] * \
                                      (prebvious_outputs_copy['Spinning Reserve (Discharging) (kW)'] +
                                       prebvious_outputs_copy['Spinning Reserve (Charging) (kW)'])
            SR_values = sum(previous_outputs_values[self.window_index])

        else:
            raise ValueError("regulation_scenario must be 1, 2 or 3")

        # Create a new hourly timeseries dataframe as the Scenario time series file for a new SV run
        new_hourly_timeseries = self.previous_initial_hourly_timeseries.copy(deep=True)
        new_hourly_timeseries['Power Min (kW)'] = np.array(SR_contraint_output['chgMin_kW'])
        new_hourly_timeseries['Power Max (kW)'] = np.array(SR_contraint_output['chgMax_kW'])
        new_hourly_timeseries['Energy Max (kWh)'] = np.array(SR_contraint_output['eMax_kWh'])
        new_hourly_timeseries['Energy Min (kWh)'] = np.array(SR_contraint_output['eMin_kWh'])

        new_shortname = "runID{}_constraintSR_rs{}_hr{}-{}".format(self.previous_runID, self.regulation_scenario,
                                                                   self.app_hours[0], self.app_hours[1])
        old_svrun_params = self.previous_svrun_params
        new_svrun_params = copy.deepcopy(old_svrun_params)
        new_svrun_params['SR_active'] = "no"
        for k in ['Scenario_time_series_filename', 'Results_dir_absolute_path',
                    'Results_label', 'Results_errors_log_path']:
            new_svrun_params.pop(k, None)
        new_hourly_timeseries_path = self.runID_result_folder_path + \
                                     "/_new_hourly_timeseries_{}.csv".format(new_shortname)
        new_hourly_timeseries.to_csv(new_hourly_timeseries_path, index=False)

        return old_svrun_params, new_svrun_params, new_shortname, new_hourly_timeseries_path, SR_values

    def set_FR_user_constraints(self):
        """create user constraints for frequency regulation within window defined by resHour
      according to the logic of the regScenario """
        # Create user constraints based on resource hours and regulation scenario
        FR_contraint_output = self.output.copy(deep=True).reset_index(drop=True)

        # Create user constraints based on resource hours and regulation scenario
        if self.regulation_scenario == 1:  # ENERGY reservations based on resource hours & service prices
            # TODO: account for different ch/disch, and CHARGING EFFICIENCY
            raise ValueError("regulation_scenario 1 doesn't exist yet for FR")
        elif self.regulation_scenario == 2:  # ONE-SIDED reservations based on resource hours
            raise ValueError("regulation_scenario 2 doesn't exist yet for FR")
        elif self.regulation_scenario == 3:  # Reservations based on PREVIOUS DISPATCH
            # RegUP is provided by charging less / discharging more:
            # Power levels must be high enough that they can be reduced for FR call
            charging_min = - 1 * (self.battery_discharging_power_max -
                                  self.previous_outputs[
                                      'Regulation Up (Discharging) (kW)'] -  # save this portion of discharging
                                  self.previous_outputs['Regulation Up (Charging) (kW)'])  # charge less
            # RegDOWN is provided by charging more / discharging less:
            # Power levels must be low enough that they can be reduced for FR call
            charging_max = self.battery_charging_power_max - \
                           self.previous_outputs['Regulation Down (Charging) (kW)'] - \
                           self.previous_outputs['Regulation Down (Discharging) (kW)']
            # Energy throughput is given - must have space for net (less constraint)
            energy_max = self.battery_energy_rated * self.max_soc + \
                         self.previous_outputs['FR Energy Throughput (kWh)'] - \
                         charging_min * self.round_trip_efficiency  # TODO: k values and RTD sanity check
            energy_min = self.battery_energy_rated * self.min_soc + \
                         self.previous_outputs['FR Energy Throughput (kWh)'] - charging_max

            # Update constraints in the output
            FR_contraint_output.loc[self.window_index, "chgMin_kW"] = charging_min.loc[self.window_index]
            FR_contraint_output.loc[self.window_index, "chgMax_kW"] = charging_max.loc[self.window_index]
            FR_contraint_output.loc[self.window_index, "eMin_kWh"] = energy_min.loc[self.window_index]
            FR_contraint_output.loc[self.window_index, "eMax_kWh"] = energy_max.loc[self.window_index]

            # Calculate FR values
            previous_outputs_values = ((self.previous_outputs.loc[:, "FR Energy Settlement Price Signal ($/kWh)"] *
                                        self.previous_outputs['FR Energy Throughput (kWh)']) +
                                       (self.previous_outputs.loc[:, "Regulation Down Price Signal ($/kW)"] *
                                        (self.previous_outputs['Regulation Down (Charging) (kW)'] +
                                         self.previous_outputs['Regulation Down (Discharging) (kW)'])) +
                                       (self.previous_outputs.loc[:, "Regulation Up Price Signal ($/kW)"] *
                                        (self.previous_outputs['Regulation Up (Charging) (kW)'] +
                                         self.previous_outputs['Regulation Up (Discharging) (kW)'])
                                        ))
            FR_values = sum(previous_outputs_values[self.window_index])

        else:
            raise ValueError("regulation_scenario must be 1, 2 or 3")

        # Create a new hourly timeseries dataframe as the Scenario time series file for a new SV run
        new_hourly_timeseries = self.previous_initial_hourly_timeseries.copy(deep=True)
        new_hourly_timeseries['Power Min (kW)'] = np.array(FR_contraint_output['chgMin_kW'])
        new_hourly_timeseries['Power Max (kW)'] = np.array(FR_contraint_output['chgMax_kW'])
        new_hourly_timeseries['Energy Max (kWh)'] = np.array(FR_contraint_output['eMax_kWh'])
        new_hourly_timeseries['Energy Min (kWh)'] = np.array(FR_contraint_output['eMin_kWh'])

        new_shortname = "runID{}_constraintFR_rs{}_hr{}-{}".format(self.previous_runID, self.regulation_scenario,
                                                                   self.app_hours[0], self.app_hours[1])
        old_svrun_params = self.previous_svrun_params
        new_svrun_params = copy.deepcopy(old_svrun_params)
        new_svrun_params['FR_active'] = "no"
        for k in ['Scenario_time_series_filename', 'Results_dir_absolute_path',
                    'Results_label', 'Results_errors_log_path']:
            new_svrun_params.pop(k, None)
        new_hourly_timeseries_path = self.runID_result_folder_path + \
                                     "/_new_hourly_timeseries_{}.csv".format(new_shortname)
        new_hourly_timeseries.to_csv(new_hourly_timeseries_path, index=False)

        return old_svrun_params, new_svrun_params, new_shortname, new_hourly_timeseries_path, FR_values

    def set_RA0_user_constraints(self, RA_monthly_values_per_kW=5):
        """create user constraints for RA dispmode 0 within window defined by resHour
      according to the logic of the regScenario """
        # Create user constraints based on resource hours and regulation scenario
        new_hourly_timeseries = self.previous_initial_hourly_timeseries.copy(deep=True)
        new_hourly_timeseries.set_index(self.output.index)

        new_hourly_timeseries['Power Min (kW)'] = - self.battery_charging_power_max  # TODO: why?
        new_hourly_timeseries['Power Max (kW)'] = self.battery_charging_power_max  # TODO: why?
        new_hourly_timeseries['Energy Max (kWh)'] = self.battery_energy_rated * \
                                                    self.max_soc  # TODO: previous way has double counted max_soc
        new_hourly_timeseries['Energy Min (kWh)'] = self.battery_energy_rated * self.min_soc

        # Create user constraints based on resource hours and regulation scenario
        if self.regulation_scenario == 1:  # ENERGY reservations based on resource hours & service prices
            # SOC must be sufficient at beginning of each RA period
            new_hourly_timeseries.loc[self.window_start_index,
                                      'Energy Min (kWh)'] = self.battery_discharging_power_max * self.RA_length
            # Set prices of other services as 0 during this window
            incompatible_services = ['FR Price ($/kW)', 'Reg Up Price ($/kW)', 'Reg Down Price ($/kW)',
                                     'NSR Price ($/kW)', 'SR Price ($/kW)']
            for service in incompatible_services:
                new_hourly_timeseries.loc[self.window_index, service] = 0
        elif self.regulation_scenario == 2:  # ONE-SIDED reservations based on resource hours
            # SOC must be sufficient at beginning of each RA period
            new_hourly_timeseries.loc[self.window_start_index, 'Energy Min (kWh)'] = \
                self.battery_discharging_power_max * self.RA_length
        elif self.regulation_scenario == 3:  # Reservations based on PREVIOUS DISPATCH
            raise ValueError("regulation_scenario 3 doesn't exist yet for RA")  # TODO
        else:
            raise ValueError("regulation_scenario must be 1, 2 or 3")

        # Calculate RA values
        RA_values = RA_monthly_values_per_kW * 12 * self.battery_discharging_power_max

        # Create a new hourly timeseries dataframe as the Scenario time series file for a new SV run
        new_shortname = "runID{}_constraintRA0_rs{}_hr{}-{}".format(self.previous_runID, self.regulation_scenario,
                                                                    self.app_hours[0], self.app_hours[1])
        old_svrun_params = self.previous_svrun_params
        new_svrun_params = copy.deepcopy(old_svrun_params)
        new_svrun_params['RA_active'] = "no"
        for k in ['Scenario_time_series_filename', 'Results_dir_absolute_path',
                    'Results_label', 'Results_errors_log_path']:
            new_svrun_params.pop(k, None)
        new_hourly_timeseries_path = self.runID_result_folder_path + \
                                     "/_new_hourly_timeseries_{}.csv".format(new_shortname)
        new_hourly_timeseries.to_csv(new_hourly_timeseries_path, index=False)

        return old_svrun_params, new_svrun_params, new_shortname, new_hourly_timeseries_path, RA_values

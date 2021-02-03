"""
combine_runs.py

This function generates the inputs for a run that combines
constraints from multiple runs according to the given inputs.
It then runs StorageVET.

Zhenhua Zhang Jan 27 2021
"""

import pandas as pd
import numpy as np

from vc_wrap import SvetObject


# def combine_runs(SVet_absolute_path, baseline_svetobject, app_types, app_hours, regulation_scenario):
#     """This function takes as input the type of regulatory scenario desired and three
#   pieces of information regarding each run used to make the combined run:
#
#     the resource type: [“NSR”,”SR”,”RA0”,”FR”]
#     the hours in which a resource is given priority [[6,16], [16,23]]
#     the regulation scenario for reach resource type: [1, 3, 3]
#
#     It uses this information to run StorageVET with the desired combination of storage value stacking"""
#
#     # Check that app_types, and app_hours and regulation_scenario are the same length
#     if all(len(lst) == len(regulation_scenario) for lst in [app_types, app_hours]):
#         pass
#     else:
#         raise ValueError("Wrong input list length for combine_runs")
#
#     # Check for overlap in app_hours & that each element has length 2
#     if all(len(lst) == 2 for lst in app_hours) & (sum(app_hours, []) == sorted(sum(app_hours, []))):
#         pass
#     else:
#         raise ValueError("Wrong input resource hours for combine_runs")
#
#     # Check if app_types contain valid options
#     if all(i in ["NSR", "SR", "RA0", "FR"] for i in app_types):
#         pass
#     else:
#         raise ValueError("Wrong input resource types for combine_runs")
#
#     # Iterate through each resource type
#     new_svet_object = baseline_svetobject
#     for i in range(len(app_types)):
#         new_constraint_object = ConstraintObject(SvetObject=new_svet_object, app_hours=app_hours[i],
#                                                  regulation_scenario=regulation_scenario[i])
#         constraint_function = getattr(new_constraint_object, "set_" + app_types[i] + "_user_constraints")
#         old_svrun_params, new_svrun_params, new_shortname, new_hourly_timeseries_path, values = constraint_function()
#         new_svet_object = SvetObject(SVet_absolute_path=SVet_absolute_path,
#                                      shortname=new_shortname,
#                                      description="run #{}".format(i),
#                                      Scenario_time_series_filename=new_hourly_timeseries_path,
#                                      User_active="yes", User_price=values,
#                                      **new_svrun_params)
#         print(i, "values ", values)
#
#     return print("Combine runs has been completed")


class ConstraintObject:
    def __init__(self, SVet_absolute_path, shortname, baseline_runID, app_hours, regulation_scenario):
        # Specify StorageVET related attributes
        self.SVet_absolute_path = SVet_absolute_path
        self.SVet_script = SVet_absolute_path + "run_StorageVET.py"
        self.default_params_file = SVet_absolute_path + "Model_Parameters_2v1-0-2_default.csv"
        self.runs_log_file = SVet_absolute_path + "Results/runsLog.csv"
        self.results_path = SVet_absolute_path + "Results/"

        # Load user constraint parameters
        self.app_hours = app_hours
        self.regulation_scenario = regulation_scenario

        # Specify attributes for the baseline run
        self.previous_runID = baseline_runID
        self.runID_result_folder_path = self.results_path + "output_run" + self.previous_runID + "_" + shortname
        self.runID_param_path = self.runID_result_folder_path + "/params_run" + self.previous_runID + ".csv"
        self.runID_dispatch_timeseries_path = self.runID_result_folder_path + \
                                              "/timeseries_results_runID" + self.previous_runID + ".csv"
        previous_params = pd.read_csv(self.runID_param_path)
        self.previous_params = previous_params

        # Read baseline hourly timeseries file
        previous_initial_hourly_timeseries = pd.read_csv(self.runID_result_folder_path +
                                                         "/_initial_hourly_timeseries_runID{}.csv"
                                                         .format(self.previous_runID))
        previous_initial_hourly_timeseries['datetime'] = pd.to_datetime(previous_initial_hourly_timeseries.iloc[:, 0])
        previous_initial_hourly_timeseries = previous_initial_hourly_timeseries.set_index('datetime')
        self.previous_initial_hourly_timeseries = previous_initial_hourly_timeseries

        # Read baseline dispatch results
        previous_outputs = pd.read_csv(self.runID_dispatch_timeseries_path)
        previous_outputs['datetime'] = pd.to_datetime(previous_outputs.iloc[:, 0])
        previous_outputs_datetime = previous_outputs['datetime']
        previous_outputs.set_index('datetime')
        self.previous_outputs = previous_outputs

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

        # Initialize a constraint object
        # new_hourly_timeseries = pd.DataFrame(index=pd.to_datetime(self.previous_initial_hourly_timeseries.iloc[:, 0]),
        #                                      columns=["chgMin_kW", "chgMax_kW", "eMin_kWh", "eMax_kWh"])
        # new_hourly_timeseries.loc[:, "eMin_kWh"] = self.battery_energy_rated * self.min_soc
        # new_hourly_timeseries.loc[:, "eMax_kWh"] = self.battery_energy_rated * self.max_soc  # TODO: double counted max_soc previously
        # new_hourly_timeseries.loc[:, "chgMin_kW"] = - self.battery_discharging_power_max
        # new_hourly_timeseries.loc[:, "chgMax_kW"] = self.battery_charging_power_max
        # self.new_hourly_timeseries = new_hourly_timeseries

        # Determine indexes
        self.window_start_index = self.previous_initial_hourly_timeseries.index.hour == app_hours[0]
        self.window_index = (self.previous_initial_hourly_timeseries.index.hour >= app_hours[0] + 1) & \
                            (self.previous_initial_hourly_timeseries.index.hour <= app_hours[1] + 1)
        self.window_end_index = self.previous_initial_hourly_timeseries.index.hour == app_hours[1] + 1

        # Initialize user constraint values
        self.new_shortname = str()
        self.new_hourly_timeseries_path = str()
        self.values = 0

    def set_NSR_user_constraints(self):
        # Create user constraints based on resource hours and regulation scenario
        NSR_contraint_output = self.previous_initial_hourly_timeseries.copy(deep=True).reset_index(drop=True)

        if self.regulation_scenario == 1:  # ENERGY reservations based on resource hours & service prices
            # TODO: account for different ch/disch, and CHARGING EFFICIENCY
            NSR_contraint_output.loc[self.window_index, "Power Min (kW)"] = - 1
            NSR_contraint_output.loc[self.window_index, "Power Max (kW)"] = 1
            NSR_contraint_output.loc[self.window_index, "Energy Min (kWh)"] = \
                self.battery_energy_rated * self.min_soc + self.battery_charging_power_max  # TODO: why not +discharge?
            NSR_contraint_output.loc[self.window_index, "Energy Max (kWh)"] = \
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
            NSR_contraint_output.loc[self.window_index, "Power Min (kW)"] = charging_min.loc[self.window_index]
            NSR_contraint_output.loc[self.window_index, "Power Max (kW)"] = charging_max.loc[self.window_index]
            NSR_contraint_output.loc[self.window_index, "Energy Min (kWh)"] = energy_min.loc[self.window_index]
            NSR_contraint_output.loc[self.window_index, "Energy Max (kWh)"] = energy_max.loc[self.window_index]

            # Calculate NSR values
            previous_outputs_values = prebvious_outputs_copy["NSR Price Signal ($/kW)"] * \
                                      (prebvious_outputs_copy['Non-spinning Reserve (Discharging) (kW)'] +
                                       prebvious_outputs_copy['Non-spinning Reserve (Charging) (kW)'])
            NSR_values = sum(previous_outputs_values[self.window_index])

        else:
            raise ValueError("regulation_scenario must be 1, 2 or 3")

        # Create a new hourly timeseries dataframe as the Scenario time series file for a new SV run
        new_hourly_timeseries = self.previous_initial_hourly_timeseries.copy(deep=True)
        new_hourly_timeseries['Power Min (kW)'] = np.array(NSR_contraint_output['Power Min (kW)'])
        new_hourly_timeseries['Power Max (kW)'] = np.array(NSR_contraint_output['Power Max (kW)'])
        new_hourly_timeseries['Energy Max (kWh)'] = np.array(NSR_contraint_output['Energy Max (kWh)'])
        new_hourly_timeseries['Energy Min (kWh)'] = np.array(NSR_contraint_output['Power Min (kW)'])
        new_shortname = "runID{}_constraintNSR_rs{}_hr{}-{}".format(self.previous_runID, self.regulation_scenario,
                                                                    self.app_hours[0], self.app_hours[1])
        new_hourly_timeseries_path = self.runID_result_folder_path + \
                                     "/_new_hourly_timeseries_{}.csv".format(new_shortname)
        new_hourly_timeseries.to_csv(new_hourly_timeseries_path, index=False)

        # Update attributes
        self.new_shortname = new_shortname
        self.new_hourly_timeseries_path = new_hourly_timeseries_path
        self.values = NSR_values

    def set_SR_user_constraints(self):
        """create user constraints for spinning reserve within window defined by resHour
      according to the logic of the regScenario """
        # Create user constraints based on resource hours and regulation scenario
        SR_contraint_output = self.previous_initial_hourly_timeseries.copy(deep=True).reset_index(drop=True)

        if self.regulation_scenario == 1:  # ENERGY reservations based on resource hours & service prices
            # TODO: account for different ch/disch, and CHARGING EFFICIENCY
            SR_contraint_output.loc[self.window_index, "Power Min (kW)"] = - 1
            SR_contraint_output.loc[self.window_index, "Power Max (kW)"] = 1
            SR_contraint_output.loc[self.window_index, "Energy Min (kWh)"] = \
                self.battery_energy_rated * self.min_soc + self.battery_charging_power_max  # TODO: why not +discharge?
            SR_contraint_output.loc[self.window_index, "Energy Max (kWh)"] = \
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
            sel2 = prebvious_outputs_copy['Spinning Reserve (Discharging) (kW)'] > self.battery_discharging_power_max
            prebvious_outputs_copy.loc[sel2, 'Spinning Reserve (Discharging) (kW)'] = self.battery_discharging_power_max

            charging_min = SR_contraint_output["Power Min (kW)"]
            charging_max = self.battery_charging_power_max - \
                           prebvious_outputs_copy['Spinning Reserve (Charging) (kW)'] - \
                           prebvious_outputs_copy['Spinning Reserve (Discharging) (kW)']
            energy_min = self.battery_energy_rated * self.min_soc + \
                         prebvious_outputs_copy['Spinning Reserve (Discharging) (kW)']
            energy_max = self.battery_energy_rated * self.max_soc - \
                         prebvious_outputs_copy['Spinning Reserve (Charging) (kW)'] * self.round_trip_efficiency

            # Update constraints in the output
            SR_contraint_output.loc[self.window_index, "Power Min (kW)"] = charging_min.loc[self.window_index]
            SR_contraint_output.loc[self.window_index, "Power Max (kW)"] = charging_max.loc[self.window_index]
            SR_contraint_output.loc[self.window_index, "Energy Min (kWh)"] = energy_min.loc[self.window_index]
            SR_contraint_output.loc[self.window_index, "Energy Max (kWh)"] = energy_max.loc[self.window_index]

            # Calculate NSR values
            previous_outputs_values = prebvious_outputs_copy["SR Price Signal ($/kW)"] * \
                                      (prebvious_outputs_copy['Spinning Reserve (Discharging) (kW)'] +
                                       prebvious_outputs_copy['Spinning Reserve (Charging) (kW)'])
            SR_values = sum(previous_outputs_values[self.window_index])

        else:
            raise ValueError("regulation_scenario must be 1, 2 or 3")

        # Create a new hourly timeseries dataframe as the Scenario time series file for a new SV run
        new_hourly_timeseries = self.previous_initial_hourly_timeseries.copy(deep=True)
        new_hourly_timeseries['Power Min (kW)'] = np.array(SR_contraint_output['Power Min (kW)'])
        new_hourly_timeseries['Power Max (kW)'] = np.array(SR_contraint_output['Power Max (kW)'])
        new_hourly_timeseries['Energy Max (kWh)'] = np.array(SR_contraint_output['Energy Max (kWh)'])
        new_hourly_timeseries['Energy Min (kWh)'] = np.array(SR_contraint_output['Power Min (kW)'])
        new_shortname = "runID{}_constraintSR_rs{}_hr{}-{}".format(self.previous_runID, self.regulation_scenario,
                                                                   self.app_hours[0], self.app_hours[1])
        new_hourly_timeseries_path = self.runID_result_folder_path + \
                                     "/_new_hourly_timeseries_{}.csv".format(new_shortname)
        new_hourly_timeseries.to_csv(new_hourly_timeseries_path, index=False)

        # Update attributes
        self.new_shortname = new_shortname
        self.new_hourly_timeseries_path = new_hourly_timeseries_path
        self.values = SR_values

    def set_FR_user_constraints(self):
        """create user constraints for frequency regulation within window defined by resHour
      according to the logic of the regScenario """
        # Create user constraints based on resource hours and regulation scenario
        FR_contraint_output = self.previous_initial_hourly_timeseries.copy(deep=True).reset_index(drop=True)

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

            # avoid infeasibility
            sel = (energy_min + energy_max) >= self.battery_charging_power_max * 2  # both at max
            energy_min.loc[sel] = energy_min.loc[sel] - 1
            sel2 = (energy_min + energy_max) <= self.battery_charging_power_max * -2  # both at min
            energy_max.loc[sel2] = energy_max.loc[sel2] + 1
            sel3 = energy_max - energy_min < 1e-4  # somehow they're still equal
            energy_min.loc[sel3] = energy_min.loc[sel3] - 1

            # Update constraints in the output
            FR_contraint_output.loc[self.window_index, "Power Min (kW)"] = charging_min.loc[self.window_index]
            FR_contraint_output.loc[self.window_index, "Power Max (kW)"] = charging_max.loc[self.window_index]
            FR_contraint_output.loc[self.window_index, "Energy Min (kWh)"] = energy_min.loc[self.window_index]
            FR_contraint_output.loc[self.window_index, "Energy Max (kWh)"] = energy_max.loc[self.window_index]

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
        new_hourly_timeseries['Power Min (kW)'] = np.array(FR_contraint_output['Power Min (kW)'])
        new_hourly_timeseries['Power Max (kW)'] = np.array(FR_contraint_output['Power Max (kW)'])
        new_hourly_timeseries['Energy Max (kWh)'] = np.array(FR_contraint_output['Energy Max (kWh)'])
        new_hourly_timeseries['Energy Min (kWh)'] = np.array(FR_contraint_output['Power Min (kW)'])
        new_shortname = "runID{}_constraintFR_rs{}_hr{}-{}".format(self.previous_runID, self.regulation_scenario,
                                                                   self.app_hours[0], self.app_hours[1])
        new_hourly_timeseries_path = self.runID_result_folder_path + \
                                     "/_new_hourly_timeseries_{}.csv".format(new_shortname)
        new_hourly_timeseries.to_csv(new_hourly_timeseries_path, index=False)

        # Update attributes
        self.new_shortname = new_shortname
        self.new_hourly_timeseries_path = new_hourly_timeseries_path
        self.values = FR_values

    def set_RA0_user_constraints(self, RA_monthly_values_per_kW=5):
        """create user constraints for RA dispmode 0 within window defined by resHour
      according to the logic of the regScenario """
        # Create user constraints based on resource hours and regulation scenario
        new_hourly_timeseries = self.previous_initial_hourly_timeseries.copy(deep=True)
        new_hourly_timeseries.set_index(self.previous_initial_hourly_timeseries.index)

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
        new_hourly_timeseries_path = self.runID_result_folder_path + \
                                     "/_new_hourly_timeseries_{}.csv".format(new_shortname)
        new_hourly_timeseries.to_csv(new_hourly_timeseries_path, index=False)

        # Update attributes
        self.new_shortname = new_shortname
        self.new_hourly_timeseries_path = new_hourly_timeseries_path
        self.values = RA_values
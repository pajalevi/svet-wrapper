"""
combine_runs.py

This function generates the inputs for a run that combines
constraints from multiple runs according to the given inputs.
It then runs StorageVET.

Zhenhua Zhang Jan 27 2021, last updated on Feb 19 2021
"""

import pandas as pd
import numpy as np

from vc_wrap import SvetObject


def combine_runs(SVet_absolute_path, description, shortname, app_types, app_hours, regulation_scenario,
                 **argument_list):
    """This function takes as input the type of regulatory scenario desired and three
  pieces of information regarding each run used to make the combined run:

    the resource type: [“NSR”,”SR”,”RA0”,”FR”]
    the hours in which a resource is given priority [[6,16], [16,23]]
    the regulation scenario for reach resource type: [1, 3, 3]

    It uses this information to run StorageVET with the desired combination of storage value stacking"""

    # Check that app_types, and app_hours and regulation_scenario are the same length
    if all(len(lst) == len(regulation_scenario) for lst in [app_types, app_hours]):
        pass
    else:
        raise ValueError("Wrong input list length for combine_runs")

    # Check for overlap in app_hours & that each element has length 2
    if all(len(lst) == 2 for lst in app_hours) & (sum(app_hours, []) == sorted(sum(app_hours, []))):
        pass
    else:
        raise ValueError("Wrong input resource hours for combine_runs")

    # Check if app_types contain valid options
    if all(i in ["NSR", "SR", "RA0", "FR"] for i in app_types):
        pass
    else:
        raise ValueError("Wrong input resource types for combine_runs")

    # Iterate through each resource type
    baseline = SvetObject(SVet_absolute_path=SVet_absolute_path,
                          shortname=shortname,
                          description=description,
                          **argument_list)
    baseline.run_storagevet()
    new_svet_object = baseline
    for i in range(len(app_types)):
        constraint_init = True if i == 0 else False
        new_constraint_object = ConstraintObject(SVet_absolute_path=SVet_absolute_path,
                                                 shortname=new_svet_object.shortname,
                                                 baseline_runID=new_svet_object.runID,
                                                 app_hours=app_hours[i],
                                                 regulation_scenario=regulation_scenario[i],
                                                 constraint_init=constraint_init)
        getattr(new_constraint_object, "set_" + app_types[i] + "_user_constraints")()
        argument_list[app_types[i] + '_active'] = 'no'
        argument_list['Scenario_time_series_filename'] = new_constraint_object.new_hourly_timeseries_path
        print(i, "values ", new_constraint_object.new_shortname,
              new_constraint_object.values, new_constraint_object.new_hourly_timeseries_path)
        new_svet_object = SvetObject(SVet_absolute_path=SVet_absolute_path,
                                     shortname=new_constraint_object.new_shortname,
                                     description="run #{}".format(i),
                                     User_active="yes", User_price=new_constraint_object.values,
                                     **argument_list)
        new_svet_object.run_storagevet()

    return print("Combine runs has been completed")


class ConstraintObject:
    def __init__(self, SVet_absolute_path, shortname, baseline_runID, app_hours, regulation_scenario,
                 constraint_init=True):
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
        self.runID_proforma_path = self.runID_result_folder_path + "/pro_forma_runID" + self.previous_runID + ".csv"
        previous_proforma = pd.read_csv(self.runID_proforma_path)
        self.previous_proforma = previous_proforma
        previous_params = pd.read_csv(self.runID_param_path)
        self.previous_params = previous_params

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

        # Read baseline hourly timeseries file, initialize the constraints if 1st run
        previous_initial_hourly_timeseries = pd.read_csv(self.runID_result_folder_path +
                                                         "/_initial_hourly_timeseries_runID{}.csv"
                                                         .format(self.previous_runID))
        previous_initial_hourly_timeseries['datetime'] = pd.to_datetime(previous_initial_hourly_timeseries.iloc[:, 0])
        previous_initial_hourly_timeseries = previous_initial_hourly_timeseries.set_index('datetime')

        if constraint_init:
            previous_initial_hourly_timeseries.loc[:, "Energy Min (kWh)"] = self.battery_energy_rated * self.min_soc
            previous_initial_hourly_timeseries.loc[:, "Energy Max (kWh)"] = self.battery_energy_rated * self.max_soc
            previous_initial_hourly_timeseries.loc[:, "Power Min (kW)"] = - self.battery_discharging_power_max
            previous_initial_hourly_timeseries.loc[:, "Power Max (kW)"] = self.battery_charging_power_max
        else:
            pass
        self.previous_initial_hourly_timeseries = previous_initial_hourly_timeseries

        # Determine indexes
        self.window_start_index = self.previous_initial_hourly_timeseries.index.hour == app_hours[0]
        self.window_index = (self.previous_initial_hourly_timeseries.index.hour >= app_hours[0] + 1) & \
                            (self.previous_initial_hourly_timeseries.index.hour <= app_hours[1] + 1)
        self.window_end_index = self.previous_initial_hourly_timeseries.index.hour == app_hours[1] + 1
        if app_hours[1] == 23:
            self.window_index = self.window_index + \
                                (self.previous_initial_hourly_timeseries.index.hour == 0)
            self.window_end_index = self.previous_initial_hourly_timeseries.index.hour == 0
        else:
            pass

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
            # Avoid infeasibility
            previous_outputs_copy = self.previous_outputs.copy(deep=True)
            sel = (previous_outputs_copy['Non-spinning Reserve (Discharging) (kW)'] +
                   previous_outputs_copy[
                       'Non-spinning Reserve (Charging) (kW)']) >= self.battery_charging_power_max * 2
            previous_outputs_copy.loc[sel, 'Non-spinning Reserve (Discharging) (kW)'] = \
                previous_outputs_copy.loc[sel, 'Non-spinning Reserve (Discharging) (kW)'] - 1

            power_min = - 1 * (self.battery_discharging_power_max -
                               previous_outputs_copy['Non-spinning Reserve (Discharging) (kW)'])
            power_max = self.battery_charging_power_max - \
                        previous_outputs_copy['Non-spinning Reserve (Charging) (kW)']
            energy_min = self.battery_energy_rated * self.min_soc + \
                         previous_outputs_copy['Non-spinning Reserve (Discharging) (kW)']
            energy_max = self.battery_energy_rated * self.max_soc - \
                         previous_outputs_copy['Non-spinning Reserve (Charging) (kW)'] * self.round_trip_efficiency

            # Update constraints in the output
            NSR_contraint_output.loc[self.window_index, "Power Min (kW)"] = power_min.loc[self.window_index]
            NSR_contraint_output.loc[self.window_index, "Power Max (kW)"] = power_max.loc[self.window_index]
            NSR_contraint_output.loc[self.window_index, "Energy Min (kWh)"] = energy_min.loc[self.window_index]
            NSR_contraint_output.loc[self.window_index, "Energy Max (kWh)"] = energy_max.loc[self.window_index]

            # Calculate NSR values
            previous_outputs_values = previous_outputs_copy["NSR Price Signal ($/kW)"] * \
                                      (previous_outputs_copy['Non-spinning Reserve (Discharging) (kW)'] +
                                       previous_outputs_copy['Non-spinning Reserve (Charging) (kW)'])
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
                self.battery_energy_rated * self.min_soc + self.battery_charging_power_max  # able to discharge
            SR_contraint_output.loc[self.window_index, "Energy Max (kWh)"] = \
                self.battery_energy_rated * self.max_soc - self.battery_charging_power_max * self.round_trip_efficiency  # save room for charge

            # Calculate SR values
            previous_outputs_values = self.previous_outputs["SR Price Signal ($/kW)"] * self.battery_charging_power_max
            SR_values = sum(previous_outputs_values[self.window_index])

        elif self.regulation_scenario == 2:  # ONE-SIDED reservations based on resource hours
            raise ValueError("regulation_scenario 2 doesn't exist yet for SR")
        elif self.regulation_scenario == 3:  # Reservations based on PREVIOUS DISPATCH
            # Avoid infeasibility TODO: understand this
            previous_outputs_copy = self.previous_outputs.copy(deep=True)
            sel2 = previous_outputs_copy['Spinning Reserve (Discharging) (kW)'] > self.battery_discharging_power_max
            previous_outputs_copy.loc[sel2, 'Spinning Reserve (Discharging) (kW)'] = self.battery_discharging_power_max
            sel = (previous_outputs_copy['Spinning Reserve (Discharging) (kW)'] +
                   previous_outputs_copy['Spinning Reserve (Charging) (kW)']) >= self.battery_charging_power_max * 2
            previous_outputs_copy.loc[sel, 'Spinning Reserve (Discharging) (kW)'] = \
                previous_outputs_copy.loc[sel, 'Spinning Reserve (Discharging) (kW)'] - 1

            power_min = SR_contraint_output["Power Min (kW)"]
            power_max = self.battery_charging_power_max - \
                        previous_outputs_copy['Spinning Reserve (Charging) (kW)'] - \
                        previous_outputs_copy['Spinning Reserve (Discharging) (kW)']
            energy_min = self.battery_energy_rated * self.min_soc + \
                         previous_outputs_copy['Spinning Reserve (Discharging) (kW)']
            energy_max = self.battery_energy_rated * self.max_soc - \
                         previous_outputs_copy['Spinning Reserve (Charging) (kW)'] * self.round_trip_efficiency

            # Update constraints in the output
            SR_contraint_output.loc[self.window_index, "Power Min (kW)"] = power_min.loc[self.window_index]
            SR_contraint_output.loc[self.window_index, "Power Max (kW)"] = power_max.loc[self.window_index]
            SR_contraint_output.loc[self.window_index, "Energy Min (kWh)"] = energy_min.loc[self.window_index]
            SR_contraint_output.loc[self.window_index, "Energy Max (kWh)"] = energy_max.loc[self.window_index]

            # Calculate SR values
            previous_outputs_values = previous_outputs_copy["SR Price Signal ($/kW)"] * \
                                      (previous_outputs_copy['Spinning Reserve (Discharging) (kW)'] +
                                       previous_outputs_copy['Spinning Reserve (Charging) (kW)'])
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
            power_min = - 1 * (self.battery_discharging_power_max -
                               self.previous_outputs[
                                   'Regulation Up (Discharging) (kW)'] -  # save this portion of discharging
                               self.previous_outputs['Regulation Up (Charging) (kW)'])  # charge less
            # RegDOWN is provided by charging more / discharging less:
            # Power levels must be low enough that they can be reduced for FR call
            power_max = self.battery_charging_power_max - \
                        self.previous_outputs['Regulation Down (Charging) (kW)'] - \
                        self.previous_outputs['Regulation Down (Discharging) (kW)']
            # Energy throughput is given - must have space for net (less constraint)
            energy_max = self.battery_energy_rated * self.max_soc + \
                         self.previous_outputs['FR Energy Throughput (kWh)'] - \
                         power_min * self.round_trip_efficiency
            energy_min = self.battery_energy_rated * self.min_soc + \
                         self.previous_outputs['FR Energy Throughput (kWh)'] - \
                         power_max

            # avoid infeasibility for power
            sel = (power_min + power_max) >= self.battery_charging_power_max * 2  # both at max
            power_min.loc[sel] = power_min.loc[sel] - 1
            sel2 = (power_min + power_max) <= self.battery_charging_power_max * -2  # both at min
            power_max.loc[sel2] = power_max.loc[sel2] + 1
            sel3 = power_max - power_min < 1e-4  # somehow they're still equal
            power_min.loc[sel3] = power_min.loc[sel3] - 1

            # Update constraints in the output
            FR_contraint_output.loc[self.window_index, "Power Min (kW)"] = power_min.loc[self.window_index]
            FR_contraint_output.loc[self.window_index, "Power Max (kW)"] = power_max.loc[self.window_index]
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
        new_hourly_timeseries['Energy Min (kWh)'] = np.array(FR_contraint_output['Energy Min (kWh)'])
        new_shortname = "runID{}_constraintFR_rs{}_hr{}-{}".format(self.previous_runID, self.regulation_scenario,
                                                                   self.app_hours[0], self.app_hours[1])
        new_hourly_timeseries_path = self.runID_result_folder_path + \
                                     "/_new_hourly_timeseries_{}.csv".format(new_shortname)
        new_hourly_timeseries.to_csv(new_hourly_timeseries_path, index=False)

        # Update attributes
        self.new_shortname = new_shortname
        self.new_hourly_timeseries_path = new_hourly_timeseries_path
        self.values = FR_values

    def set_RA0_user_constraints(self, RA_monthly_values_per_kW=5): # TODO: read RA monthly values from data file
        """create user constraints for RA dispmode 0 within window defined by resHour
      according to the logic of the regScenario """
        # Create user constraints based on resource hours and regulation scenario
        new_hourly_timeseries = self.previous_initial_hourly_timeseries.copy(deep=True)

        # Create user constraints based on resource hours and regulation scenario
        if self.regulation_scenario == 1:  # ENERGY reservations based on resource hours & service prices
            # SOC must be sufficient at beginning of each RA period
            new_hourly_timeseries.loc[self.window_start_index,
                                      'Energy Min (kWh)'] = self.battery_discharging_power_max * self.RA_length
            # Set prices of other services as 0 during this window, except for energy arbitrage
            incompatible_services = ['FR Price ($/kW)', 'Reg Up Price ($/kW)', 'Reg Down Price ($/kW)',
                                     'NSR Price ($/kW)', 'SR Price ($/kW)']
            for service in incompatible_services:
                new_hourly_timeseries.loc[self.window_index, service] = 0
        elif self.regulation_scenario == 2:  # ONE-SIDED reservations based on resource hours
            # SOC must be sufficient at beginning of each RA period
            new_hourly_timeseries.loc[self.window_start_index, 'Energy Min (kWh)'] = \
                self.battery_discharging_power_max * self.RA_length
        elif self.regulation_scenario == 3:  # ENERGY Reservations based on PREVIOUS DISPATCH
            # Identify previous periods of RA
            ra_start_index = self.previous_outputs.loc[:,'RA Energy Min (kWh)'] > 0
            ra_period_index = self.previous_outputs.loc[:, 'RA Event (y/n)']
            new_hourly_timeseries.loc[ra_start_index.values, 'Energy Min (kWh)'] = \
                self.battery_discharging_power_max * self.RA_length

            # Set prices of other services as 0 during this window, except for energy arbitrage
            incompatible_services = ['FR Price ($/kW)', 'Reg Up Price ($/kW)', 'Reg Down Price ($/kW)',
                                     'NSR Price ($/kW)', 'SR Price ($/kW)']
            for service in incompatible_services:
                new_hourly_timeseries.loc[ra_period_index.values, service] = 0
            # raise ValueError("regulation_scenario 3 doesn't exist yet for RA")  # TODO
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

    def set_DCM_user_constraints(self):
        """create user constraints for demand charge management within window defined by resHour
      according to the logic of the regScenario """
        # Create user constraints based on resource hours and regulation scenario
        DCM_contraint_output = self.previous_initial_hourly_timeseries.copy(deep=True).reset_index(drop=True)

        # Create user constraints based on resource hours and regulation scenario
        if self.regulation_scenario == 1:  # ENERGY reservations based on resource hours & service prices
            raise ValueError("regulation_scenario 1 doesn't exist yet for DCM")
        elif self.regulation_scenario == 2:  # ONE-SIDED reservations based on resource hours
            raise ValueError("regulation_scenario 2 doesn't exist yet for DCM")
        elif self.regulation_scenario == 3:  # Reservations based on PREVIOUS DISPATCH
            # Find monthly maximum
            previous_outputs_copy = self.previous_outputs
            previous_outputs_copy['Month'] = pd.to_datetime(previous_outputs_copy.iloc[:, 0]).dt.month
            monthly_max = previous_outputs_copy.groupby(['Month', 'Demand Charge Billing Periods'])[
                'Net Load (kW)'].transform('max')
            # Add 1 to avoid infeasibility
            previous_outputs_copy['monthly_max'] = monthly_max + 1

            # Battery power plus load should not exceed previously dispatched monthly peak
            power_min = self.previous_outputs['Load (kW)'] - previous_outputs_copy['monthly_max']

            # Update constraints in the output
            DCM_contraint_output.loc[self.window_index, "Power Min (kW)"] = power_min.loc[self.window_index]

            # Calculate DCM values
            # DCM_values = self.previous_proforma['Avoided Demand Charge'][1]

            # Change DCM savings to 0 bc it will show up anyway if included in tariff
            DCM_values = 0

        else:
            raise ValueError("regulation_scenario must be 1, 2 or 3")

        # Create a new hourly timeseries dataframe as the Scenario time series file for a new SV run
        new_hourly_timeseries = self.previous_initial_hourly_timeseries.copy(deep=True)
        new_hourly_timeseries['Power Min (kW)'] = np.array(DCM_contraint_output['Power Min (kW)'])
        new_shortname = "runID{}_constraintDCM_rs{}_hr{}-{}".format(self.previous_runID, self.regulation_scenario,
                                                                    self.app_hours[0], self.app_hours[1])
        new_hourly_timeseries_path = self.runID_result_folder_path + \
                                     "/_new_hourly_timeseries_{}.csv".format(new_shortname)
        new_hourly_timeseries.to_csv(new_hourly_timeseries_path, index=False)

        # Update attributes
        self.new_shortname = new_shortname
        self.new_hourly_timeseries_path = new_hourly_timeseries_path
        self.values = DCM_values

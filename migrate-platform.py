from veracode_api_py import Users
from veracode_api_py import Policies
from veracode_api_py import Applications
from veracode_api_py import BusinessUnits
from veracode_api_py import Teams
from veracode_api_py.apihelper import APIHelper
from os import environ
import json
import requests.exceptions
from colorama import Fore


def proceed():
    return input(Fore.WHITE+'Do you want to continue? [y/n]') == 'y'


def print_all(policies, bus_units, teams, app_profiles):
    print(Fore.BLUE+'Policies:')
    print(Fore.CYAN+', '.join(p['name'] for p in policies))
    print(Fore.BLUE+'Business Units:')
    print(Fore.CYAN+', '.join(b['bu_name'] for b in bus_units if b['bu_name'] != 'Not Specified'))
    print(Fore.BLUE+'Teams:')
    print(Fore.CYAN+', '.join(t['team_name'] for t in teams))
    print(Fore.BLUE+'Application Profiles:')
    print(Fore.CYAN+', '.join(app['profile']['name'] for app in app_profiles if 'profile' in app))


def is_new_policy(policy, existing_policies):
    return not any(p['name'] == policy['name'] for p in existing_policies)


def create_policies(new_policies, existing):
    for policy in new_policies:
        if is_new_policy(policy, existing):
            grace_periods = Policies().format_grace_periods(policy['sev5_grace_period'], policy['sev4_grace_period'], 
                                                            policy['sev3_grace_period'], policy['sev2_grace_period'], 
                                                            policy['sev1_grace_period'], policy['sev0_grace_period'], 
                                                            policy['score_grace_period'], policy['sca_blacklist_grace_period'])
            result = Policies().create(policy['name'], policy['description'], policy['vendor_policy'], 
                                        policy['finding_rules'], policy['scan_frequency_rules'], grace_periods)
            print(Fore.GREEN+'Successfully created Policy {} with GUID {}'.format(result['name'], result['guid']))
            existing.append(result)
        else:
            print(Fore.YELLOW+'Not creating Policy {} because either it already exists or is a default Policy'.format(policy['name']))
    return existing


def is_new_bus_unit(bus_unit, existing_bus):
    return bus_unit['bu_name'] != 'Not Specified' and not any(bu['bu_name'] == bus_unit['bu_name'] for bu in existing_bus)


def create_bus_units(bus_unit, existing):
    for bus_unit in bus_unit:
        if is_new_bus_unit(bus_unit, existing):
            result = BusinessUnits().create(bus_unit['bu_name'])
            print(Fore.GREEN+'Successfully created Business Unit {} with id {}'.format(result['bu_name'], result['bu_id']))
            existing.append(result) 
        else:
            print(Fore.YELLOW+'Not creating Business Unit {} because either it already exists or is a default BU'.format(bus_unit['bu_name']))
    return existing


def is_new_team(team, existing_teams):
    return not any(t['team_name'] == team['team_name'] for t in existing_teams)


def create_teams(teams, existing, bus_units):
    for team in teams:
        if is_new_team(team, existing):
            bu_id = next(bu['bu_id'] for bu in bus_units if bu['bu_name'] == team['business_unit']['bu_name']) if 'business_unit' in team else None
            result = Teams().create(team['team_name'], bu_id)
            print(Fore.GREEN+'Successfully created Team {} with id {}'.format(result['team_name'], result['team_id']))
            existing.append(result)
        else:
            print(Fore.YELLOW+'Not creating Team {} because it already exists'.format(team['team_name']))
    return existing


def create_app(app, teams, business_unit, policy_id, is_default):
    uri = 'appsec/v1/applications'
    httpmethod = 'POST'

    # https://docs.veracode.com/r/r_applications_create
    app_def = {
        'name': app['profile']['name'],
        'business_criticality':app['profile']['business_criticality'],
        'description': app['profile']['description'],
        'policies': [
            {
                'guid': policy_id,
                'is_default': is_default
            }
        ],
        "settings": app['profile']['settings'],
        'tags': app['profile']['tags']
    }

    if business_unit != None:
        bu = {'business_unit': {'guid': business_unit}}
        app_def.update(bu)

    if len(teams) > 0:
        # optionally pass a list of teams to add to the application profile
        team_list = []
        for team in teams:
            team_list.append({'guid': team})
        app_def.update({'teams': team_list})

    payload = json.dumps({'profile': app_def})
    return APIHelper()._rest_request(uri,httpmethod,body=payload)


def create_app_profiles(app_profiles, existing_policies, existing_teams, existing_bus_units):
    for app in app_profiles:
        try:
            bu_id = next(bu['bu_id'] for bu in existing_bus_units if bu['bu_name'] == app['profile']['business_unit']['name']) if app['profile']['business_unit']['name'] != 'Not Specified' else None
            team_ids = []
            if len(app['profile']['teams']) > 0:
                for team in app['profile']['teams']:
                    team_ids.append(next(t['team_id'] for t in existing_teams if team['team_name'] == t['team_name']))
            policy_id = next(p['guid'] for p in existing_policies if app['profile']['policies'][0]['name'] == p['name'])
            policy_is_default = app['profile']['policies'][0]['is_default']
            # result = Applications().create(app['profile']['name'], app['profile']['business_criticality'], bu_id, team_ids)
            result = create_app(app, team_ids, bu_id, policy_id, policy_is_default)
            print(Fore.GREEN+'Successfully created Application Profile {} with id {}'.format(result['profile']['name'], result['guid']))
        except requests.exceptions.RequestException as e:
            print(Fore.RED+'Error creating Application profile {}. Exception thrown: {}'.format(app['profile']['name'], e))
                


def main():
    environ['VERACODE_API_PROFILE'] = 'migratefrom'
    me = Users().get_self()
    print('Transferring custom Policies, Business Units, Teams, and Application profiles from organization '+Fore.MAGENTA+'{}'.format(me['organization']['org_name']))
    if proceed():
        policies = Policies().get_all()
        bus_units = BusinessUnits().get_all()
        teams = Teams().get_all()
        app_profiles = Applications().get_all()

        environ['VERACODE_API_PROFILE'] = 'migrateto'
        me = Users().get_self()
        print('\n\nThis will transfer the following to organization '+Fore.MAGENTA+'{}'.format(me['organization']['org_name']))
        print_all(policies, bus_units, teams, app_profiles)
        if proceed():
            existing_policies = Policies().get_all()
            existing_policies = create_policies(policies, existing_policies)

            existing_bus = BusinessUnits().get_all()
            existing_bus = create_bus_units(bus_units, existing_bus)
            
            existing_teams = Teams().get_all()
            existing_teams = create_teams(teams, existing_teams, existing_bus)

            create_app_profiles(app_profiles, existing_policies, existing_teams, existing_bus)


if __name__ == '__main__':
    main()

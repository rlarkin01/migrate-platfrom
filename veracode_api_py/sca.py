#sca.py - API class for SCA API calls

import json
from urllib import parse
from uuid import UUID 

from .apihelper import APIHelper
from .constants import Constants

class Workspaces():
     sca_base_url = "srcclr/v3/workspaces"
     sca_issues_url = "srcclr/v3/issues"   

     def get_all(self):
          #Gets existing workspaces
          request_params = {}
          return APIHelper()._rest_paged_request(self.sca_base_url,"GET",params=request_params,element="workspaces")

     def get_by_name(self,name: str):
          #Does a name filter on the workspaces list. Note that this is a partial match. Only returns the first match
          name = parse.quote(name) #urlencode any spaces or special characters
          request_params = {'filter[workspace]': name}
          return APIHelper()._rest_paged_request(self.sca_base_url,"GET",params=request_params,element="workspaces")

     def create(self,name: str):
          #pass payload with name, return guid to workspace
          payload = json.dumps({"name": name})
          r = APIHelper()._rest_request(self.sca_base_url,"POST",body=payload,fullresponse=True)
          loc = r.headers.get('location','')
          return loc.split("/")[-1]

     def add_team(self,workspace_guid: UUID,team_id: UUID):
          return APIHelper()._rest_request(self.sca_base_url + "/{}/teams/{}".format(workspace_guid,team_id),"PUT")

     def remove_team(self,workspace_guid: UUID,team_id: UUID):
          return APIHelper()._rest_request(self.sca_base_url + "/{}/teams/{}".format(workspace_guid,team_id),"DELETE")

     def delete(self,workspace_guid: UUID):
          return APIHelper()._rest_request(self.sca_base_url + "/{}".format(workspace_guid),"DELETE") 

     def get_teams(self, workspace_guid: UUID=None):
          if workspace_guid:
               return APIHelper()._rest_request(self.sca_base_url + "/{}/teams".format(workspace_guid),"GET")
          else:
               return APIHelper()._rest_paged_request("srcclr/v3/teams","GET","teams",{})

     def get_projects(self,workspace_guid: UUID):
          return APIHelper()._rest_paged_request(self.sca_base_url + '/{}/projects'.format(workspace_guid),"GET","projects",{})

     def get_project(self,workspace_guid: UUID,project_guid:UUID ):
          uri = self.sca_base_url + '/{}/projects/{}'.format(workspace_guid,project_guid)
          return APIHelper()._rest_request(uri,"GET")

     def get_project_issues(self,workspace_guid: UUID,project_guid: UUID, params={}):
          uri = self.sca_base_url + '/{}/projects/{}/issues'.format(workspace_guid,project_guid)
          return APIHelper()._rest_paged_request(uri,"GET","issues", params)

     def get_project_libraries(self,workspace_guid: UUID,project_guid: UUID):
          uri = self.sca_base_url + '/{}/projects/{}/libraries'.format(workspace_guid,project_guid)
          return APIHelper()._rest_paged_request(uri,"GET","libraries",{})

     def get_agents(self,workspace_guid: UUID):
          return APIHelper()._rest_paged_request(self.sca_base_url + '/{}/agents'.format(workspace_guid),"GET","agents",{})

     def get_agent(self,workspace_guid: UUID,agent_guid: UUID):
          uri = self.sca_base_url + '/{}/agents/{}'.format(workspace_guid,agent_guid)
          return APIHelper()._rest_request(uri,"GET")

     def create_agent(self,workspace_guid: UUID,name: str,agent_type='CLI'):
          if agent_type not in Constants().AGENT_TYPE:
               raise ValueError("{} is not in the list of valid agent types ({})".format(agent_type,Constants().AGENT_TYPE))
          uri = self.sca_base_url + '/{}/agents'.format(workspace_guid)
          body = {'agent_type': agent_type, 'name': name}
          return APIHelper()._rest_request(uri,"POST",body=json.dumps(body))

     def delete_agent(self,workspace_guid: UUID,agent_guid: UUID):
          uri = self.sca_base_url + '/{}/agents/{}'.format(workspace_guid,agent_guid)
          return APIHelper()._rest_request(uri,"DELETE")

     def get_agent_tokens(self,workspace_guid: UUID,agent_guid: UUID):
          uri = self.sca_base_url + '/{}/agents/{}/tokens'.format(workspace_guid,agent_guid)
          return APIHelper()._rest_paged_request(uri, "GET", "tokens" )

     def get_agent_token(self,workspace_guid: UUID,agent_guid: UUID,token_id: UUID):
          uri = self.sca_base_url + '/{}/agents/{}/tokens/{}'.format(workspace_guid,agent_guid,token_id)
          return APIHelper()._rest_request(uri, "GET" )

     def regenerate_agent_token(self,workspace_guid: UUID, agent_guid: UUID):
          uri = self.sca_base_url + '/{}/agents/{}/tokens:regenerate'.format(workspace_guid,agent_guid)
          return APIHelper()._rest_request(uri,"POST")

     def revoke_agent_token(self,workspace_guid: UUID, agent_guid: UUID, token_id: UUID):
          uri = self.sca_base_url + '/{}/agents/{}/tokens/{}'.format(workspace_guid,agent_guid,token_id)
          return APIHelper()._rest_request(uri,"DELETE")

     def get_issues(self,workspace_guid: UUID, branch=None, created_after=None,direct=None, ignored=None, vuln_methods=None, project_id=None):
          params = {}
          if branch:
               params["branch"] = branch
          if created_after:
               params["created_after"] = created_after
          if direct:
               params["direct"] = direct
          if ignored:
               params["ignored"] = ignored
          if vuln_methods:
               params["vuln_methods"] = vuln_methods
          if project_id:
               params["project_id"] = project_id
          uri = self.sca_base_url + '/{}/issues'.format(workspace_guid)
          return APIHelper()._rest_paged_request(uri,"GET","issues",params)

     def get_issue(self,issue_id: UUID):
          uri = self.sca_issues_url + '/{}'.format(issue_id)
          return APIHelper()._rest_request(uri,"GET")

     def get_libraries(self,workspace_guid: UUID,unmatched: bool):
          if unmatched:
               uri = self.sca_base_url + '/{}/libraries/unmatched'.format(workspace_guid)
          else:
               uri = self.sca_base_url + '/{}/libraries'.format(workspace_guid)
          return APIHelper()._rest_paged_request(uri,"GET",'libraries',{})

     def get_library(self,library_id: str):
          uri = "srcclr/v3/libraries/{}".format(library_id)
          return APIHelper()._rest_request(uri,"GET")

     def get_vulnerability(self,vulnerability_id: int):
          uri = "srcclr/v3/vulnerabilities/{}".format(vulnerability_id)
          return APIHelper()._rest_request(uri,"GET")

     def get_license(self,license_id: str):
          uri = "srcclr/v3/licenses/{}".format(license_id)
          return APIHelper()._rest_request(uri,"GET")

     def get_scan(self,scan_id: UUID):
          return APIHelper()._rest_request("srcclr/v3/scans/{}".format(scan_id),"GET")

     def get_events(self, date_gte=None, event_group=None, event_type=None):
          baseuri = "srcclr/v3/events"
          params = {}
          if event_group != None:
               if event_group not in Constants().SCA_EVENT_GROUP:
                    raise ValueError("{} is not in the valid list of SCA event groups ({})".format(event_group,Constants().SCA_EVENT_GROUP))
               params["group"]  = event_group

          if event_type != None:
               params["type"] = event_type

          if date_gte != None:
               params["date_gte"] = date_gte

          return APIHelper()._rest_paged_request(baseuri,"GET","events",params)

class ComponentActivity():
     component_base_uri = "srcclr/v3/component-activity"

     def get(self,component_id: str):
          return APIHelper()._rest_request(self.component_base_uri+"/{}".format(component_id),"GET")

class SBOM():
     entity_base_uri = "srcclr/sbom/v1/targets"
     valid_formats = ['cyclonedx','spdx']

     def get(self,app_guid: UUID, format='cyclonedx',linked=False,vulnerability=True,dependency=True):
          return self._get_sbom(guid=app_guid,format=format,sbom_type='application',linked=linked,vulnerability=vulnerability,dependency=dependency)

     def get_for_project(self,project_guid: UUID, format='cyclonedx', vulnerability=True,dependency=True):
          return self._get_sbom(guid=project_guid,format=format,sbom_type='agent',linked=False,vulnerability=vulnerability,dependency=dependency)

     def _get_sbom(self,guid: UUID,format,sbom_type,linked,vulnerability,dependency):
          if format not in self.valid_formats:
               return  
          params={"type":sbom_type,"vulnerability": vulnerability}
          if linked:
               params["linked"] = linked
          if format=='spdx': #currently only supported for SPDX SBOMs
               params["dependency"] = dependency
          return APIHelper()._rest_request(self.entity_base_uri+"/{}/{}".format(guid,format),"GET",params=params)

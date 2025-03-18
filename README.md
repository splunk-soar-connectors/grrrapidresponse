# GRR Rapid Response

Publisher: Splunk \
Connector Version: 2.0.6 \
Product Vendor: Google \
Product Name: GRR Rapid Response \
Minimum Product Version: 5.2.0

This app implements various investigative actions from the GRR API

### Configuration variables

This table lists the configuration variables required to operate GRR Rapid Response. These variables are specified when configuring a GRR Rapid Response asset in Splunk SOAR.

VARIABLE | REQUIRED | TYPE | DESCRIPTION
-------- | -------- | ---- | -----------
**username** | required | string | Username |
**password** | required | password | Password |
**server** | required | string | GRR Server |
**verify_server_cert** | optional | boolean | Verify server certificate |

### Supported Actions

[test connectivity](#action-test-connectivity) - Validate the asset configuration for connectivity using supplied configuration \
[list connections](#action-list-connections) - List all the connections configured on the device \
[list endpoints](#action-list-endpoints) - List all the endpoints/sensors configured on the device \
[get system info](#action-get-system-info) - Get information about an endpoint \
[get file info](#action-get-file-info) - Look for files matching given criteria \
[get browser cache](#action-get-browser-cache) - Retrieve matching regex in a client's browser cache \
[get hunts](#action-get-hunts) - Retrieve available hunts \
[get cron jobs](#action-get-cron-jobs) - Retrieve available cron jobs

## action: 'test connectivity'

Validate the asset configuration for connectivity using supplied configuration

Type: **test** \
Read only: **True**

#### Action Parameters

No parameters are required for this action

#### Action Output

No Output

## action: 'list connections'

List all the connections configured on the device

Type: **investigate** \
Read only: **True**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**client_id** | required | Grr client id | string | `grr client id` |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failed |
action_result.parameter.client_id | string | `grr client id` | C.7459eeb515c40632 |
action_result.data.\*.payload.@type | string | | type.googleapis.com/NetworkConnection |
action_result.data.\*.payload.family | string | | INET |
action_result.data.\*.payload.localAddress.ip | string | `ip` | 0.0.0.0 |
action_result.data.\*.payload.localAddress.port | numeric | | 138 |
action_result.data.\*.payload.pid | numeric | `pid` | 1 |
action_result.data.\*.payload.remoteAddress.ip | string | `ip` | 22.22.22.22 |
action_result.data.\*.payload.remoteAddress.port | numeric | | 5223 |
action_result.data.\*.payload.state | string | | NONE |
action_result.data.\*.payload.type | string | | SOCK_DGRAM |
action_result.data.\*.payloadType | string | | NetworkConnection |
action_result.data.\*.timestamp | string | | 1521067743700341 |
action_result.summary.flow_id | string | | F:4849031C |
action_result.summary.status | string | | Successfully wrote 56 connections. |
action_result.message | string | | Successfully retrieved netstat information |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'list endpoints'

List all the endpoints/sensors configured on the device

Type: **investigate** \
Read only: **True**

#### Action Parameters

No parameters are required for this action

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failed |
action_result.data.\*.age | string | | 1520550974243553 |
action_result.data.\*.agentInfo.buildTime | string | | 2016-06-14 17:57:23 |
action_result.data.\*.agentInfo.clientDescription | string | | grr darwin amd64 |
action_result.data.\*.agentInfo.clientName | string | | grr |
action_result.data.\*.agentInfo.clientVersion | numeric | | 3102 |
action_result.data.\*.clientId | string | `grr client id` | C.7459eeb515c40632 |
action_result.data.\*.firstSeenAt | string | | 1470712631079150 |
action_result.data.\*.hardwareInfo.biosReleaseDate | string | | 07/30/2013 |
action_result.data.\*.hardwareInfo.biosRevision | string | | 4.6 |
action_result.data.\*.hardwareInfo.biosRomSize | string | | 64 kB |
action_result.data.\*.hardwareInfo.biosVendor | string | | Technologies LTD |
action_result.data.\*.hardwareInfo.biosVersion | string | | MM51.007B.B00 |
action_result.data.\*.hardwareInfo.serialNumber | string | | C07G11R8DJY7 |
action_result.data.\*.hardwareInfo.systemFamily | string | | Not Specified |
action_result.data.\*.hardwareInfo.systemManufacturer | string | | Manufacturer |
action_result.data.\*.hardwareInfo.systemProductName | string | | Macmini5,3 |
action_result.data.\*.hardwareInfo.systemSkuNumber | string | | Not Specified |
action_result.data.\*.hardwareInfo.systemUuid | string | | 564D9FC8-45F6-EED0-961A-ECDA131E1366 |
action_result.data.\*.interfaces.\*.addresses.\*.addressType | string | | INET6 |
action_result.data.\*.interfaces.\*.addresses.\*.packedBytes | string | | /oAAAAAAAADKKhT//lSKIA== |
action_result.data.\*.interfaces.\*.ifname | string | | gif0 |
action_result.data.\*.interfaces.\*.macAddress | string | | sgAeAmcB |
action_result.data.\*.knowledgeBase.hostname | string | `host name` | test-mac-mini.local |
action_result.data.\*.knowledgeBase.os | string | | Darwin |
action_result.data.\*.knowledgeBase.osMajorVersion | numeric | | 10 |
action_result.data.\*.knowledgeBase.osMinorVersion | numeric | | 11 |
action_result.data.\*.knowledgeBase.osRelease | string | | Ubuntu |
action_result.data.\*.knowledgeBase.users.\*.fullName | string | | root |
action_result.data.\*.knowledgeBase.users.\*.homedir | string | | /Users/deleteme |
action_result.data.\*.knowledgeBase.users.\*.lastLogon | string | | 1520034035000000 |
action_result.data.\*.knowledgeBase.users.\*.username | string | | deleteme |
action_result.data.\*.lastBootedAt | string | | 1520029440000000 |
action_result.data.\*.lastClock | string | | 1521070306686653 |
action_result.data.\*.lastCrashAt | string | | 1520030649377194 |
action_result.data.\*.lastSeenAt | string | | 1521070306700415 |
action_result.data.\*.memorySize | string | | 4294967296 |
action_result.data.\*.osInfo.fqdn | string | | test-mac-mini.local |
action_result.data.\*.osInfo.installDate | string | | 1470170520000000 |
action_result.data.\*.osInfo.kernel | string | | 15.6.0 |
action_result.data.\*.osInfo.machine | string | | x86_64 |
action_result.data.\*.osInfo.node | string | | Test-Mac-mini.local |
action_result.data.\*.osInfo.release | string | | OSX |
action_result.data.\*.osInfo.system | string | | Darwin |
action_result.data.\*.osInfo.version | string | | 10.11.6 |
action_result.data.\*.urn | string | | aff4:/C.7459eeb515c40632 |
action_result.data.\*.users.\*.fullName | string | | root |
action_result.data.\*.users.\*.homedir | string | | /Users/deleteme |
action_result.data.\*.users.\*.lastLogon | string | | 1520034035000000 |
action_result.data.\*.users.\*.username | string | | deleteme |
action_result.data.\*.volumes.\*.actualAvailableAllocationUnits | string | | 116864728 |
action_result.data.\*.volumes.\*.bytesPerSector | string | | 4096 |
action_result.data.\*.volumes.\*.sectorsPerAllocationUnit | string | | 1 |
action_result.data.\*.volumes.\*.totalAllocationUnits | string | | 121886744 |
action_result.data.\*.volumes.\*.unixvolume.mountPoint | string | | / |
action_result.summary.num_endpoints | numeric | | 2 |
action_result.message | string | | Num endpoints: 2 |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'get system info'

Get information about an endpoint

Type: **investigate** \
Read only: **True**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**client_id** | required | Grr client id | string | `grr client id` |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failed |
action_result.parameter.client_id | string | `grr client id` | C.7459eeb515c40632 |
action_result.data.\*.age | string | | 1523100856318869 |
action_result.data.\*.agentInfo.buildTime | string | | 2016-06-08 20:27:31 |
action_result.data.\*.agentInfo.clientDescription | string | | grr linux amd64 |
action_result.data.\*.agentInfo.clientName | string | | grr |
action_result.data.\*.agentInfo.clientVersion | numeric | | 3102 |
action_result.data.\*.clientId | string | `grr client id` | C.7459eeb515c40632 |
action_result.data.\*.firstSeenAt | string | | 1470712118344458 |
action_result.data.\*.hardwareInfo.biosReleaseDate | string | | 07/30/2013 |
action_result.data.\*.hardwareInfo.biosRevision | string | | 4.6 |
action_result.data.\*.hardwareInfo.biosRomSize | string | | 64 kB |
action_result.data.\*.hardwareInfo.biosVendor | string | | Technologies LTD |
action_result.data.\*.hardwareInfo.biosVersion | string | | 6.00 |
action_result.data.\*.hardwareInfo.serialNumber | string | | 56 4d 9f c8 45 f6 ee d0-96 1a ec da 13 1e 13 66 |
action_result.data.\*.hardwareInfo.systemFamily | string | | Not Specified |
action_result.data.\*.hardwareInfo.systemManufacturer | string | | Manufacturer |
action_result.data.\*.hardwareInfo.systemProductName | string | | Virtual Platform |
action_result.data.\*.hardwareInfo.systemSkuNumber | string | | Not Specified |
action_result.data.\*.hardwareInfo.systemUuid | string | | 564D9FC8-45F6-EED0-961A-ECDA131E1366 |
action_result.data.\*.interfaces.\*.addresses.\*.addressType | string | | INET INET6 |
action_result.data.\*.interfaces.\*.addresses.\*.packedBytes | string | | fwAAAQ== |
action_result.data.\*.interfaces.\*.ifname | string | | lo |
action_result.data.\*.interfaces.\*.macAddress | string | | AAAAAAAA |
action_result.data.\*.knowledgeBase.hostname | string | `host name` | grr |
action_result.data.\*.knowledgeBase.os | string | | Linux |
action_result.data.\*.knowledgeBase.osMajorVersion | numeric | | 16 |
action_result.data.\*.knowledgeBase.osMinorVersion | numeric | | 4 |
action_result.data.\*.knowledgeBase.osRelease | string | | Ubuntu |
action_result.data.\*.knowledgeBase.users.\*.fullName | string | | root |
action_result.data.\*.knowledgeBase.users.\*.homedir | string | | /root |
action_result.data.\*.knowledgeBase.users.\*.lastLogon | string | | 1518816548000000 |
action_result.data.\*.knowledgeBase.users.\*.username | string | `grr user` | root |
action_result.data.\*.osInfo.kernel | string | | 4.4.0-53-generic |
action_result.data.\*.osInfo.system | string | | Linux |
action_result.data.\*.osInfo.machine | string | | x86_64 |
action_result.data.\*.osInfo.version | string | | 16.4 |
action_result.data.\*.osInfo.release | string | | Ubuntu |
action_result.data.\*.osInfo.node | string | | grr |
action_result.data.\*.lastBootedAt | string | | 1519928131000000 |
action_result.data.\*.lastClock | string | | 1520382854151576 |
action_result.data.\*.lastCrashAt | string | | 1520030649377194 |
action_result.data.\*.lastSeenAt | string | | 1520382863513026 |
action_result.data.\*.memorySize | string | | 4143869952 |
action_result.data.\*.osInfo.fqdn | string | | grr |
action_result.data.\*.osInfo.installDate | string | | 1470708645000000 |
action_result.data.\*.urn | string | | aff4:/C.7459eeb515c40632 |
action_result.data.\*.users.\*.fullName | string | | root |
action_result.data.\*.users.\*.homedir | string | | /root |
action_result.data.\*.users.\*.lastLogon | string | | 1518816548000000 |
action_result.data.\*.users.\*.username | string | `grr user` | root |
action_result.data.\*.volumes.\*.actualAvailableAllocationUnits | string | | 44654214 |
action_result.data.\*.volumes.\*.bytesPerSector | string | | 4096 |
action_result.data.\*.volumes.\*.sectorsPerAllocationUnit | string | | 1 |
action_result.data.\*.volumes.\*.totalAllocationUnits | string | | 50409206 |
action_result.data.\*.volumes.\*.unixvolume.mountPoint | string | | / |
action_result.summary.num_users | numeric | | 2 |
action_result.summary.success | boolean | | True |
action_result.message | string | | Num users: 2 |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'get file info'

Look for files matching given criteria

Type: **investigate** \
Read only: **True**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**client_id** | required | Client ID | string | `grr client id` |
**file_path** | required | File Path | string | `grr file path` |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failed |
action_result.parameter.client_id | string | `grr client id` | C.7459eeb515c40632 |
action_result.parameter.file_path | string | `grr file path` | /home |
action_result.data.\*.payload.@type | string | | type.googleapis.com/FileFinderResult |
action_result.data.\*.payload.statEntry.pathspec.path | string | | /home |
action_result.data.\*.payload.statEntry.pathspec.pathOptions | string | | CASE_LITERAL |
action_result.data.\*.payload.statEntry.pathspec.pathtype | string | | OS |
action_result.data.\*.payload.statEntry.stAtime | string | | 1520029482 |
action_result.data.\*.payload.statEntry.stBlksize | numeric | | 1024 |
action_result.data.\*.payload.statEntry.stBlocks | numeric | | 2 |
action_result.data.\*.payload.statEntry.stCtime | string | | 1520029482 |
action_result.data.\*.payload.statEntry.stDev | numeric | | 738197506 |
action_result.data.\*.payload.statEntry.stGid | numeric | | 0 |
action_result.data.\*.payload.statEntry.stIno | numeric | | 5 |
action_result.data.\*.payload.statEntry.stMode | string | | 16749 |
action_result.data.\*.payload.statEntry.stMtime | string | | 1521075375 |
action_result.data.\*.payload.statEntry.stNlink | numeric | | 2 |
action_result.data.\*.payload.statEntry.stDev | numeric | | 0 |
action_result.data.\*.payload.statEntry.stSize | string | | 1 |
action_result.data.\*.payload.statEntry.stUid | numeric | | 0 |
action_result.data.\*.payloadType | string | | FileFinderResult |
action_result.data.\*.timestamp | string | | 1521077728657985 |
action_result.summary.flow_id | string | | F:5EBA859A |
action_result.summary.total_count | string | | 1 |
action_result.message | string | | Successfully retrieved file information |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'get browser cache'

Retrieve matching regex in a client's browser cache

Type: **investigate** \
Read only: **True**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**client_id** | required | Client ID | string | `grr client id` |
**browser_cache_regex** | required | Regex to look for | string | |
**users** | required | Users to query. Use commas to separate | string | `grr user` |
**check_chrome** | optional | Check Chrome | boolean | |
**check_firefox** | optional | Check FireFox | boolean | |
**check_ie** | optional | Check IE | boolean | |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failed |
action_result.parameter.browser_cache_regex | string | | /home/var/\* |
action_result.parameter.check_chrome | boolean | | True False |
action_result.parameter.check_firefox | boolean | | True |
action_result.parameter.check_ie | boolean | | True |
action_result.parameter.client_id | string | `grr client id` | C.7459eeb515c40632 |
action_result.parameter.users | string | `grr user` | test, deleteme |
action_result.data.\*.args.@type | string | | type.googleapis.com/CacheGrepArgs |
action_result.data.\*.args.checkChrome | boolean | | True |
action_result.data.\*.args.checkFirefox | boolean | | True |
action_result.data.\*.args.checkIe | boolean | | True |
action_result.data.\*.args.dataRegex | string | | /home/var/\* |
action_result.data.\*.args.grepUsers | string | | user1 |
action_result.data.\*.context.clientResources.cpuUsage.systemCpuTime | numeric | | 0.0858357697725296 |
action_result.data.\*.context.clientResources.cpuUsage.userCpuTime | numeric | | 1.808138251304626 |
action_result.data.\*.context.createTime | string | | 1520632043714372 |
action_result.data.\*.context.creator | string | `grr user` | admin |
action_result.data.\*.context.currentState | string | | End |
action_result.data.\*.context.networkBytesSent | string | | 153093 |
action_result.data.\*.context.nextOutboundId | string | | 5 |
action_result.data.\*.context.nextProcessedRequest | string | | 5 |
action_result.data.\*.context.outstandingRequests | string | | 0 |
action_result.data.\*.context.sessionId | string | | aff4:/C.7459eeb515c40632/flows/F:2CCAA0A6 |
action_result.data.\*.context.state | string | | TERMINATED |
action_result.data.\*.context.userNotified | boolean | | True False |
action_result.data.\*.creator | string | `grr user` | admin |
action_result.data.\*.flowId | string | | F:EF9BC4AB |
action_result.data.\*.lastActiveAt | string | | 1520632045250433 |
action_result.data.\*.name | string | | CacheGrep |
action_result.data.\*.runnerArgs.clientId | string | | aff4:/C.7459eeb515c40632 |
action_result.data.\*.runnerArgs.flowName | string | | CacheGrep |
action_result.data.\*.startedAt | string | | 1520632043714372 |
action_result.data.\*.state | string | | TERMINATED |
action_result.data.\*.stateData.items.\*.invalid | boolean | | False |
action_result.data.\*.stateData.items.\*.key | string | | all_paths |
action_result.data.\*.urn | string | | aff4:/C.7459eeb515c40632/flows/F:2CCAA0A6 |
action_result.summary.flow_id | string | | F:2CCAA0A6 |
action_result.message | string | | Successfully retrieved browser cache information |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'get hunts'

Retrieve available hunts

Type: **investigate** \
Read only: **True**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**offset** | optional | Starting offset | numeric | |
**count** | optional | Max number of items to fetch | numeric | |
**created_by** | optional | Only return hunts created by a given user. If approved_by or/and description_contains are also supplied, then logical AND is applied to all the criteria. NOTE: This filter can only be used in conjunction with the 'active_within' filter (to prevent queries of death) | string | `grr user` |
**description_contains** | optional | Only return hunts where description contains given substring (matching is case-insensitive). If created_by or/and approved_by are also supplied, then logical AND is applied to all the criteria. NOTE: This filter can only be used in conjunction with the 'active_within' filter (to prevent queries of death) | string | |
**active_within** | optional | Only return hunts that were active within given time duration | string | |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failed |
action_result.parameter.active_within | string | | 10w |
action_result.parameter.count | numeric | | 5 |
action_result.parameter.created_by | string | `grr user` | admin |
action_result.parameter.description_contains | string | | hunt |
action_result.parameter.offset | numeric | | 0 |
action_result.data.\*.clientLimit | string | | 100 |
action_result.data.\*.clientRate | numeric | | 20.5 |
action_result.data.\*.clientsWithResultsCount | string | | 0 |
action_result.data.\*.crashLimit | string | | 100 |
action_result.data.\*.created | string | | 1519928672035551 |
action_result.data.\*.creator | string | `grr user` | admin |
action_result.data.\*.description | string | | Test hunt (copy) |
action_result.data.\*.expires | string | | 1521138272000000 |
action_result.data.\*.isRobot | boolean | | True |
action_result.data.\*.name | string | | GenericHunt |
action_result.data.\*.resultsCount | string | | 0 |
action_result.data.\*.state | string | | PAUSED |
action_result.data.\*.totalCpuUsage | numeric | | 0 |
action_result.data.\*.totalNetUsage | string | | 0 |
action_result.data.\*.urn | string | | aff4:/hunts/H:6FA69D4 |
action_result.summary.total_hunts | numeric | | 1 |
action_result.message | string | | Total hunts: 1 |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'get cron jobs'

Retrieve available cron jobs

Type: **investigate** \
Read only: **True**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**offset** | optional | Starting offset | numeric | |
**count** | optional | Max number of items to fetch | numeric | |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failed |
action_result.parameter.count | numeric | | 3 |
action_result.parameter.offset | numeric | | 0 |
action_result.data.\*.allowOverruns | boolean | | True |
action_result.data.\*.flowArgs.@type | string | | type.googleapis.com/EmptyMessage |
action_result.data.\*.flowName | string | | CleanCronJobs |
action_result.data.\*.isFailing | boolean | | False |
action_result.data.\*.state | string | | ENABLED |
action_result.data.\*.description | string | | |
action_result.data.\*.flowRunnerArgs.flowName | string | | CleanCronJobs |
action_result.data.\*.lastRunTime | string | | 1520972007416756 |
action_result.data.\*.lifetime | string | | 86400 |
action_result.data.\*.periodicity | string | | 86400 |
action_result.data.\*.totalCount | string | | 16 |
action_result.data.\*.urn | string | | aff4:/cron/CleanCronJobs |
action_result.summary | string | | |
action_result.message | string | | |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

______________________________________________________________________

Auto-generated Splunk SOAR Connector documentation.

Copyright 2025 Splunk Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations under the License.

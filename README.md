[comment]: # "Auto-generated SOAR connector documentation"
# GRR Rapid Response

Publisher: Splunk  
Connector Version: 2\.0\.2  
Product Vendor: Google  
Product Name: GRR Rapid Response  
Product Version Supported (regex): "\.\*"  
Minimum Product Version: 4\.9\.39220  

This app implements various investigative actions from the GRR API

### Configuration Variables
The below configuration variables are required for this Connector to operate.  These variables are specified when configuring a GRR Rapid Response asset in SOAR.

VARIABLE | REQUIRED | TYPE | DESCRIPTION
-------- | -------- | ---- | -----------
**username** |  required  | string | Username
**password** |  required  | password | Password
**server** |  required  | string | GRR Server
**verify\_server\_cert** |  optional  | boolean | Verify server certificate

### Supported Actions  
[test connectivity](#action-test-connectivity) - Validate the asset configuration for connectivity using supplied configuration  
[list connections](#action-list-connections) - List all the connections configured on the device  
[list endpoints](#action-list-endpoints) - List all the endpoints/sensors configured on the device  
[get system info](#action-get-system-info) - Get information about an endpoint  
[get file info](#action-get-file-info) - Look for files matching given criteria  
[get browser cache](#action-get-browser-cache) - Retrieve matching regex in a client's browser cache  
[get hunts](#action-get-hunts) - Retrieve available hunts  
[get cron jobs](#action-get-cron-jobs) - Retrieve available cron jobs  

## action: 'test connectivity'
Validate the asset configuration for connectivity using supplied configuration

Type: **test**  
Read only: **True**

#### Action Parameters
No parameters are required for this action

#### Action Output
No Output  

## action: 'list connections'
List all the connections configured on the device

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**client\_id** |  required  | Grr client id | string |  `grr client id` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.client\_id | string |  `grr client id` 
action\_result\.data\.\*\.payload\.\@type | string | 
action\_result\.data\.\*\.payload\.family | string | 
action\_result\.data\.\*\.payload\.localAddress\.ip | string |  `ip` 
action\_result\.data\.\*\.payload\.localAddress\.port | numeric | 
action\_result\.data\.\*\.payload\.pid | numeric |  `pid` 
action\_result\.data\.\*\.payload\.remoteAddress\.ip | string |  `ip` 
action\_result\.data\.\*\.payload\.remoteAddress\.port | numeric | 
action\_result\.data\.\*\.payload\.state | string | 
action\_result\.data\.\*\.payload\.type | string | 
action\_result\.data\.\*\.payloadType | string | 
action\_result\.data\.\*\.timestamp | string | 
action\_result\.summary\.flow\_id | string | 
action\_result\.summary\.status | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'list endpoints'
List all the endpoints/sensors configured on the device

Type: **investigate**  
Read only: **True**

#### Action Parameters
No parameters are required for this action

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.data\.\*\.age | string | 
action\_result\.data\.\*\.agentInfo\.buildTime | string | 
action\_result\.data\.\*\.agentInfo\.clientDescription | string | 
action\_result\.data\.\*\.agentInfo\.clientName | string | 
action\_result\.data\.\*\.agentInfo\.clientVersion | numeric | 
action\_result\.data\.\*\.clientId | string |  `grr client id` 
action\_result\.data\.\*\.firstSeenAt | string | 
action\_result\.data\.\*\.hardwareInfo\.biosReleaseDate | string | 
action\_result\.data\.\*\.hardwareInfo\.biosRevision | string | 
action\_result\.data\.\*\.hardwareInfo\.biosRomSize | string | 
action\_result\.data\.\*\.hardwareInfo\.biosVendor | string | 
action\_result\.data\.\*\.hardwareInfo\.biosVersion | string | 
action\_result\.data\.\*\.hardwareInfo\.serialNumber | string | 
action\_result\.data\.\*\.hardwareInfo\.systemFamily | string | 
action\_result\.data\.\*\.hardwareInfo\.systemManufacturer | string | 
action\_result\.data\.\*\.hardwareInfo\.systemProductName | string | 
action\_result\.data\.\*\.hardwareInfo\.systemSkuNumber | string | 
action\_result\.data\.\*\.hardwareInfo\.systemUuid | string | 
action\_result\.data\.\*\.interfaces\.\*\.addresses\.\*\.addressType | string | 
action\_result\.data\.\*\.interfaces\.\*\.addresses\.\*\.packedBytes | string | 
action\_result\.data\.\*\.interfaces\.\*\.ifname | string | 
action\_result\.data\.\*\.interfaces\.\*\.macAddress | string | 
action\_result\.data\.\*\.knowledgeBase\.hostname | string |  `host name` 
action\_result\.data\.\*\.knowledgeBase\.os | string | 
action\_result\.data\.\*\.knowledgeBase\.osMajorVersion | numeric | 
action\_result\.data\.\*\.knowledgeBase\.osMinorVersion | numeric | 
action\_result\.data\.\*\.knowledgeBase\.osRelease | string | 
action\_result\.data\.\*\.knowledgeBase\.users\.\*\.fullName | string | 
action\_result\.data\.\*\.knowledgeBase\.users\.\*\.homedir | string | 
action\_result\.data\.\*\.knowledgeBase\.users\.\*\.lastLogon | string | 
action\_result\.data\.\*\.knowledgeBase\.users\.\*\.username | string | 
action\_result\.data\.\*\.lastBootedAt | string | 
action\_result\.data\.\*\.lastClock | string | 
action\_result\.data\.\*\.lastCrashAt | string | 
action\_result\.data\.\*\.lastSeenAt | string | 
action\_result\.data\.\*\.memorySize | string | 
action\_result\.data\.\*\.osInfo\.fqdn | string | 
action\_result\.data\.\*\.osInfo\.installDate | string | 
action\_result\.data\.\*\.osInfo\.kernel | string | 
action\_result\.data\.\*\.osInfo\.machine | string | 
action\_result\.data\.\*\.osInfo\.node | string | 
action\_result\.data\.\*\.osInfo\.release | string | 
action\_result\.data\.\*\.osInfo\.system | string | 
action\_result\.data\.\*\.osInfo\.version | string | 
action\_result\.data\.\*\.urn | string | 
action\_result\.data\.\*\.users\.\*\.fullName | string | 
action\_result\.data\.\*\.users\.\*\.homedir | string | 
action\_result\.data\.\*\.users\.\*\.lastLogon | string | 
action\_result\.data\.\*\.users\.\*\.username | string | 
action\_result\.data\.\*\.volumes\.\*\.actualAvailableAllocationUnits | string | 
action\_result\.data\.\*\.volumes\.\*\.bytesPerSector | string | 
action\_result\.data\.\*\.volumes\.\*\.sectorsPerAllocationUnit | string | 
action\_result\.data\.\*\.volumes\.\*\.totalAllocationUnits | string | 
action\_result\.data\.\*\.volumes\.\*\.unixvolume\.mountPoint | string | 
action\_result\.summary\.num\_endpoints | numeric | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'get system info'
Get information about an endpoint

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**client\_id** |  required  | Grr client id | string |  `grr client id` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.client\_id | string |  `grr client id` 
action\_result\.data\.\*\.age | string | 
action\_result\.data\.\*\.agentInfo\.buildTime | string | 
action\_result\.data\.\*\.agentInfo\.clientDescription | string | 
action\_result\.data\.\*\.agentInfo\.clientName | string | 
action\_result\.data\.\*\.agentInfo\.clientVersion | numeric | 
action\_result\.data\.\*\.clientId | string |  `grr client id` 
action\_result\.data\.\*\.firstSeenAt | string | 
action\_result\.data\.\*\.hardwareInfo\.biosReleaseDate | string | 
action\_result\.data\.\*\.hardwareInfo\.biosRevision | string | 
action\_result\.data\.\*\.hardwareInfo\.biosRomSize | string | 
action\_result\.data\.\*\.hardwareInfo\.biosVendor | string | 
action\_result\.data\.\*\.hardwareInfo\.biosVersion | string | 
action\_result\.data\.\*\.hardwareInfo\.serialNumber | string | 
action\_result\.data\.\*\.hardwareInfo\.systemFamily | string | 
action\_result\.data\.\*\.hardwareInfo\.systemManufacturer | string | 
action\_result\.data\.\*\.hardwareInfo\.systemProductName | string | 
action\_result\.data\.\*\.hardwareInfo\.systemSkuNumber | string | 
action\_result\.data\.\*\.hardwareInfo\.systemUuid | string | 
action\_result\.data\.\*\.interfaces\.\*\.addresses\.\*\.addressType | string | 
action\_result\.data\.\*\.interfaces\.\*\.addresses\.\*\.packedBytes | string | 
action\_result\.data\.\*\.interfaces\.\*\.ifname | string | 
action\_result\.data\.\*\.interfaces\.\*\.macAddress | string | 
action\_result\.data\.\*\.knowledgeBase\.hostname | string |  `host name` 
action\_result\.data\.\*\.knowledgeBase\.os | string | 
action\_result\.data\.\*\.knowledgeBase\.osMajorVersion | numeric | 
action\_result\.data\.\*\.knowledgeBase\.osMinorVersion | numeric | 
action\_result\.data\.\*\.knowledgeBase\.osRelease | string | 
action\_result\.data\.\*\.knowledgeBase\.users\.\*\.fullName | string | 
action\_result\.data\.\*\.knowledgeBase\.users\.\*\.homedir | string | 
action\_result\.data\.\*\.knowledgeBase\.users\.\*\.lastLogon | string | 
action\_result\.data\.\*\.knowledgeBase\.users\.\*\.username | string |  `grr user` 
action\_result\.data\.\*\.lastBootedAt | string | 
action\_result\.data\.\*\.lastClock | string | 
action\_result\.data\.\*\.lastCrashAt | string | 
action\_result\.data\.\*\.lastSeenAt | string | 
action\_result\.data\.\*\.memorySize | string | 
action\_result\.data\.\*\.osInfo\.fqdn | string | 
action\_result\.data\.\*\.osInfo\.installDate | string | 
action\_result\.data\.\*\.osInfo\.kernel | string | 
action\_result\.data\.\*\.osInfo\.machine | string | 
action\_result\.data\.\*\.osInfo\.node | string | 
action\_result\.data\.\*\.osInfo\.release | string | 
action\_result\.data\.\*\.osInfo\.system | string | 
action\_result\.data\.\*\.osInfo\.version | string | 
action\_result\.data\.\*\.urn | string | 
action\_result\.data\.\*\.users\.\*\.fullName | string | 
action\_result\.data\.\*\.users\.\*\.homedir | string | 
action\_result\.data\.\*\.users\.\*\.lastLogon | string | 
action\_result\.data\.\*\.users\.\*\.username | string |  `grr user` 
action\_result\.data\.\*\.volumes\.\*\.actualAvailableAllocationUnits | string | 
action\_result\.data\.\*\.volumes\.\*\.bytesPerSector | string | 
action\_result\.data\.\*\.volumes\.\*\.sectorsPerAllocationUnit | string | 
action\_result\.data\.\*\.volumes\.\*\.totalAllocationUnits | string | 
action\_result\.data\.\*\.volumes\.\*\.unixvolume\.mountPoint | string | 
action\_result\.summary\.num\_users | numeric | 
action\_result\.summary\.success | boolean | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'get file info'
Look for files matching given criteria

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**client\_id** |  required  | Client ID | string |  `grr client id` 
**file\_path** |  required  | File Path | string |  `grr file path` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.client\_id | string |  `grr client id` 
action\_result\.parameter\.file\_path | string |  `grr file path` 
action\_result\.data\.\*\.payload\.\@type | string | 
action\_result\.data\.\*\.payload\.statEntry\.pathspec\.path | string | 
action\_result\.data\.\*\.payload\.statEntry\.pathspec\.pathOptions | string | 
action\_result\.data\.\*\.payload\.statEntry\.pathspec\.pathtype | string | 
action\_result\.data\.\*\.payload\.statEntry\.stAtime | string | 
action\_result\.data\.\*\.payload\.statEntry\.stBlksize | numeric | 
action\_result\.data\.\*\.payload\.statEntry\.stBlocks | numeric | 
action\_result\.data\.\*\.payload\.statEntry\.stCtime | string | 
action\_result\.data\.\*\.payload\.statEntry\.stDev | numeric | 
action\_result\.data\.\*\.payload\.statEntry\.stGid | numeric | 
action\_result\.data\.\*\.payload\.statEntry\.stIno | numeric | 
action\_result\.data\.\*\.payload\.statEntry\.stMode | string | 
action\_result\.data\.\*\.payload\.statEntry\.stMtime | string | 
action\_result\.data\.\*\.payload\.statEntry\.stNlink | numeric | 
action\_result\.data\.\*\.payload\.statEntry\.stDev | numeric | 
action\_result\.data\.\*\.payload\.statEntry\.stSize | string | 
action\_result\.data\.\*\.payload\.statEntry\.stUid | numeric | 
action\_result\.data\.\*\.payloadType | string | 
action\_result\.data\.\*\.timestamp | string | 
action\_result\.summary\.flow\_id | string | 
action\_result\.summary\.total\_count | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'get browser cache'
Retrieve matching regex in a client's browser cache

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**client\_id** |  required  | Client ID | string |  `grr client id` 
**browser\_cache\_regex** |  required  | Regex to look for | string | 
**users** |  required  | Users to query\. Use commas to separate | string |  `grr user` 
**check\_chrome** |  optional  | Check Chrome | boolean | 
**check\_firefox** |  optional  | Check FireFox | boolean | 
**check\_ie** |  optional  | Check IE | boolean | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.browser\_cache\_regex | string | 
action\_result\.parameter\.check\_chrome | boolean | 
action\_result\.parameter\.check\_firefox | boolean | 
action\_result\.parameter\.check\_ie | boolean | 
action\_result\.parameter\.client\_id | string |  `grr client id` 
action\_result\.parameter\.users | string |  `grr user` 
action\_result\.data\.\*\.args\.\@type | string | 
action\_result\.data\.\*\.args\.checkChrome | boolean | 
action\_result\.data\.\*\.args\.checkFirefox | boolean | 
action\_result\.data\.\*\.args\.checkIe | boolean | 
action\_result\.data\.\*\.args\.dataRegex | string | 
action\_result\.data\.\*\.args\.grepUsers | string | 
action\_result\.data\.\*\.context\.clientResources\.cpuUsage\.systemCpuTime | numeric | 
action\_result\.data\.\*\.context\.clientResources\.cpuUsage\.userCpuTime | numeric | 
action\_result\.data\.\*\.context\.createTime | string | 
action\_result\.data\.\*\.context\.creator | string |  `grr user` 
action\_result\.data\.\*\.context\.currentState | string | 
action\_result\.data\.\*\.context\.networkBytesSent | string | 
action\_result\.data\.\*\.context\.nextOutboundId | string | 
action\_result\.data\.\*\.context\.nextProcessedRequest | string | 
action\_result\.data\.\*\.context\.outstandingRequests | string | 
action\_result\.data\.\*\.context\.sessionId | string | 
action\_result\.data\.\*\.context\.state | string | 
action\_result\.data\.\*\.context\.userNotified | boolean | 
action\_result\.data\.\*\.creator | string |  `grr user` 
action\_result\.data\.\*\.flowId | string | 
action\_result\.data\.\*\.lastActiveAt | string | 
action\_result\.data\.\*\.name | string | 
action\_result\.data\.\*\.runnerArgs\.clientId | string | 
action\_result\.data\.\*\.runnerArgs\.flowName | string | 
action\_result\.data\.\*\.startedAt | string | 
action\_result\.data\.\*\.state | string | 
action\_result\.data\.\*\.stateData\.items\.\*\.invalid | boolean | 
action\_result\.data\.\*\.stateData\.items\.\*\.key | string | 
action\_result\.data\.\*\.urn | string | 
action\_result\.summary\.flow\_id | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'get hunts'
Retrieve available hunts

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**offset** |  optional  | Starting offset | numeric | 
**count** |  optional  | Max number of items to fetch | numeric | 
**created\_by** |  optional  | Only return hunts created by a given user\. If approved\_by or/and description\_contains are also supplied, then logical AND is applied to all the criteria\. NOTE\: This filter can only be used in conjunction with the 'active\_within' filter \(to prevent queries of death\) | string |  `grr user` 
**description\_contains** |  optional  | Only return hunts where description contains given substring \(matching is case\-insensitive\)\. If created\_by or/and approved\_by are also supplied, then logical AND is applied to all the criteria\. NOTE\: This filter can only be used in conjunction with the 'active\_within' filter \(to prevent queries of death\) | string | 
**active\_within** |  optional  | Only return hunts that were active within given time duration | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.active\_within | string | 
action\_result\.parameter\.count | numeric | 
action\_result\.parameter\.created\_by | string |  `grr user` 
action\_result\.parameter\.description\_contains | string | 
action\_result\.parameter\.offset | numeric | 
action\_result\.data\.\*\.clientLimit | string | 
action\_result\.data\.\*\.clientRate | numeric | 
action\_result\.data\.\*\.clientsWithResultsCount | string | 
action\_result\.data\.\*\.crashLimit | string | 
action\_result\.data\.\*\.created | string | 
action\_result\.data\.\*\.creator | string |  `grr user` 
action\_result\.data\.\*\.description | string | 
action\_result\.data\.\*\.expires | string | 
action\_result\.data\.\*\.isRobot | boolean | 
action\_result\.data\.\*\.name | string | 
action\_result\.data\.\*\.resultsCount | string | 
action\_result\.data\.\*\.state | string | 
action\_result\.data\.\*\.totalCpuUsage | numeric | 
action\_result\.data\.\*\.totalNetUsage | string | 
action\_result\.data\.\*\.urn | string | 
action\_result\.summary\.total\_hunts | numeric | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'get cron jobs'
Retrieve available cron jobs

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**offset** |  optional  | Starting offset | numeric | 
**count** |  optional  | Max number of items to fetch | numeric | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.count | numeric | 
action\_result\.parameter\.offset | numeric | 
action\_result\.data\.\*\.allowOverruns | boolean | 
action\_result\.data\.\*\.description | string | 
action\_result\.data\.\*\.flowArgs\.\@type | string | 
action\_result\.data\.\*\.flowName | string | 
action\_result\.data\.\*\.flowRunnerArgs\.flowName | string | 
action\_result\.data\.\*\.isFailing | boolean | 
action\_result\.data\.\*\.lastRunTime | string | 
action\_result\.data\.\*\.lifetime | string | 
action\_result\.data\.\*\.periodicity | string | 
action\_result\.data\.\*\.state | string | 
action\_result\.data\.\*\.totalCount | string | 
action\_result\.data\.\*\.urn | string | 
action\_result\.summary | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric | 
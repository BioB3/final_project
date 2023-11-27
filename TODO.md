# TO DO

## database.py
**person**
- Attributes
  - ID
  - First
  - Last
  - Type
**login**
- Attributes
  - ID
  - Username
  - Password
  - Role
**project**
- Attributes
  - ProjectID
  - Title
  - Lead
  - Member1
  - Member2
  - Advisor
  - Status
  - Detail
**member_pending_request**
- Attributes
  - ProjectID
  - to_be_member
  - Response
  - Response_date
**advisor_pending_request**
- Attributes
  - ProjectID
  - to_be_advisor
  - Response
  - Response_date

**project_evaluation**
- Attributes
  - ProjectID
  - Respond
## roles
There're currently 6 roles

### student
- can see requests to become member of a project
  - read data from **member_pending_request** table that include the user's info 
- accept or deny the requests
  - update **member_pending_request** table based on the user's decision
- become a leader and create a new project
  - must have no data about the user in **member_pending_request** table
  - update **project** table by creating a new project with the generated project id, the user's name, inputted title and status set to *finding a supervisor*
  - update **login** table by changing the role of user to leader

### leader
- can see their own project information
  - read data from **project** table that include the user's project
- can change their project title and detail
  - update the data in **project** table
- can send request to *student* that is not a member to join and see the status of the request sent
  - the project can only have up to 2 member not including the lead
  - read data from **member_pending_request** table that include the user's project or create new request in the table
- can send request to *faculty* to be the supervisor of the project and see the status of the request sent
  - only 1 request can be sent at a time
  - must have no pending member request
  - read data from **advisor_pending_request** table that include the user's project or create new request in the table
- can submit a project proposal to the supervisor
  - change the project's status from *waiting for proposal* to *waiting for approval*
- can submit the final project report to the supervisor
  - change the project's status from *in progress* to *waiting for evaluation*

### member
- can see and update thier own project title and detail
  - read data from **project** table that include the user's project and update it if needed

### faculty
- can see and send response to the requests to be a supervisor for a project
  - read data from **advisor_pending_request** table that include the user's name and update it if needed
  - update the **login** table and change role to be an anvisor if the user accept the request and the user's not one
  - update the **advisor_pending_request** table based on the user's decision
  - change the project's advisor to the user's name and change the project's status from *finding a supervisor* to *waiting for proposal*
- can see every projects' information
  - read data form **project** table
- can evaluate project reports
  - more details in Proposal.md

### advisor
- can do everything a faculty can do
- can approve a project proposal from projects that they supervised
  - change the project's status form *waiting for approval* to *in progress*
- can approve a final project report from from projects that they supervised
  - change the project's status to *finished*

### admin
- have full access to the database

## The Plan
The plan is to either make a class with role attribute and have various function based on the role or make multiple files that contain a class for each role and import them